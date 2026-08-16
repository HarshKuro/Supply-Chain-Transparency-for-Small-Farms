// js/driver.js
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, updateDoc, query, where, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert } from './common.js';

let currentUser = null;

export function initDriverDeliveriesPage(user) {
    currentUser = user;
    loadDeliveries();
}

async function loadDeliveries() {
    if (!currentUser) return;
    
    showLoader();
    try {
        // Driver sees orders that are Verified (ready for pickup) or Assigned/Picked Up/In Transit to them.
        const q = query(collection(db, "orders"), where("status", "in", ["Verified", "Assigned", "Picked Up", "In Transit"]));
        const querySnapshot = await getDocs(q);
        
        const tbody = document.getElementById('deliveriesTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        let hasDeliveries = false;

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            
            // If it's not verified, and the driverId doesn't match currentUser, don't show it.
            // Meaning, they can only see Verified (unassigned) OR their own assigned orders.
            if (data.status !== 'Verified' && data.driverId !== currentUser.id) return;
            
            hasDeliveries = true;
            
            const itemsList = data.items.map(item => `${item.productName} (${item.quantity})`).join('<br>');
            const badgeClass = data.status.toLowerCase().replace(' ', '-');
            
            let actionHtml = '';
            if (data.status === 'Verified') {
                actionHtml = `<button class="btn btn-sm" onclick="updateDeliveryStatus('${docSnap.id}', 'Assigned')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Accept Delivery</button>`;
            } else if (data.status === 'Assigned') {
                actionHtml = `<button class="btn btn-sm" onclick="updateDeliveryStatus('${docSnap.id}', 'Picked Up')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; background-color: #6A1B9A;">Mark Picked Up</button>`;
            } else if (data.status === 'Picked Up') {
                actionHtml = `<button class="btn btn-sm" onclick="updateDeliveryStatus('${docSnap.id}', 'In Transit')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; background-color: #F57F17;">Mark In Transit</button>`;
            } else if (data.status === 'In Transit') {
                actionHtml = `<button class="btn btn-sm" onclick="updateDeliveryStatus('${docSnap.id}', 'Delivered')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; background-color: var(--success-color);">Mark Delivered</button>`;
            }
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.customerName}</td>
                <td>${data.deliveryAddress || 'N/A'}</td>
                <td>${itemsList}</td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>${actionHtml}</td>
            `;
            tbody.appendChild(tr);
        });

        if (!hasDeliveries) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No deliveries available.</td></tr>';
        }

    } catch (error) {
        console.error("Error loading deliveries:", error);
        showAlert("Failed to load deliveries", "error");
    } finally {
        hideLoader();
    }
}

window.updateDeliveryStatus = async (orderId, newStatus) => {
    if (confirm(`Update status to ${newStatus}?`)) {
        showLoader();
        try {
            const updateData = {
                status: newStatus,
                updatedAt: serverTimestamp()
            };
            if (newStatus === 'Assigned') {
                updateData.driverId = currentUser.id;
            }
            
            await updateDoc(doc(db, "orders", orderId), updateData);
            showAlert(`Status updated to ${newStatus}`, "success");
            loadDeliveries();
        } catch (error) {
            console.error("Error updating status:", error);
            showAlert("Failed to update status", "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= DASHBOARD =================
export async function initDriverDashboard(user) {
    currentUser = user;
    try {
        const q = query(collection(db, "orders"), where("status", "in", ["Verified", "Assigned", "Picked Up", "In Transit", "Delivered"]));
        const snap = await getDocs(q);
        let assigned = 0;
        let transit = 0;
        let delivered = 0;
        snap.forEach(doc => {
            const data = doc.data();
            const status = data.status;
            if (status === 'Verified' || data.driverId === currentUser.id) {
                if (status === 'Verified' || status === 'Assigned') assigned++;
                if (status === 'Picked Up' || status === 'In Transit') transit++;
                if (status === 'Delivered') delivered++;
            }
        });
        document.getElementById('statAssigned').textContent = assigned;
        document.getElementById('statTransit').textContent = transit;
        document.getElementById('statDelivered').textContent = delivered;
    } catch(e) { console.error(e); }
}
