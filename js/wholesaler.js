// js/wholesaler.js
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, updateDoc, query, where, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

export function initWholesalerOrdersPage(user) {
    currentUser = user;
    loadOrders();
}

async function loadOrders() {
    if (!currentUser) return;
    
    showLoader();
    try {
        // Wholesaler sees orders that are either Confirmed (needs verification) 
        // or already Verified/Picked Up etc. (for history).
        // Let's just load all orders that are not Pending for simplicity, or just "Confirmed" and "Verified".
        const q = query(collection(db, "orders"), where("status", "in", ["Confirmed", "Verified"]));
        const querySnapshot = await getDocs(q);
        
        const tbody = document.getElementById('ordersTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No orders need verification.</td></tr>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            const itemsList = data.items.map(item => `${item.productName} (${item.quantity})`).join('<br>');
            const badgeClass = data.status.toLowerCase().replace(' ', '-');
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.farmerName}</td>
                <td>${data.customerName}</td>
                <td>${itemsList}</td>
                <td>${formatCurrency(data.totalAmount)}</td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>
                    ${data.status === 'Confirmed' ? 
                        `<button class="btn btn-sm" onclick="verifyStock('${docSnap.id}')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; background-color: var(--secondary-color); color: var(--text-color);">Verify Stock</button>` : 
                        '<span style="color: #888; font-size: 0.85rem;">Verified</span>'
                    }
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        console.error("Error loading orders:", error);
        showAlert("Failed to load orders", "error");
    } finally {
        hideLoader();
    }
}

window.verifyStock = async (orderId) => {
    if (confirm("Mark this order as Verified?")) {
        showLoader();
        try {
            await updateDoc(doc(db, "orders", orderId), {
                status: "Verified",
                wholesalerId: currentUser.id,
                updatedAt: serverTimestamp()
            });
            showAlert("Order verified!", "success");
            loadOrders();
        } catch (error) {
            console.error("Error verifying order:", error);
            showAlert("Failed to verify order", "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= DASHBOARD =================
export async function initWholesalerDashboard(user) {
    currentUser = user;
    try {
        const q = query(collection(db, "orders"), where("status", "in", ["Confirmed", "Verified", "Assigned", "Picked Up", "In Transit", "Delivered"]));
        const snap = await getDocs(q);
        let toVerify = 0;
        let verified = 0;
        let completed = 0;
        snap.forEach(doc => {
            const status = doc.data().status;
            if (status === 'Confirmed') toVerify++;
            if (status === 'Verified') verified++;
            if (status === 'Delivered') completed++;
        });
        document.getElementById('statVerify').textContent = toVerify;
        document.getElementById('statVerified').textContent = verified;
        document.getElementById('statCompleted').textContent = completed;
    } catch(e) { console.error(e); }
}
