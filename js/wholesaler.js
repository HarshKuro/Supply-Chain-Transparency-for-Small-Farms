// js/wholesaler.js
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, updateDoc, query, where, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

export function initWholesalerOrdersPage(user) {
    currentUser = user;
    renderApprovalBanner();
    loadOrders();
}

function isWholesalerApproved() {
    if (!currentUser) return false;
    // Default to false if approved is explicitly false or status is pending
    if (currentUser.approved === false || currentUser.approvalStatus === 'pending') {
        return false;
    }
    return true;
}

function renderApprovalBanner() {
    const isApproved = isWholesalerApproved();
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    let banner = document.getElementById('wholesalerApprovalBanner');
    if (!banner) {
        banner = document.createElement('div');
        banner.id = 'wholesalerApprovalBanner';
        mainContent.insertBefore(banner, mainContent.firstChild);
    }

    if (!isApproved) {
        banner.innerHTML = `
            <div style="background: #FFFBEB; border: 1px solid #FCD34D; color: #92400E; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; display: flex; align-items: flex-start; gap: 1rem; box-shadow: var(--shadow-xs);">
                <i data-lucide="alert-triangle" style="width: 28px; height: 28px; color: #D97706; flex-shrink: 0; margin-top: 2px;"></i>
                <div>
                    <h4 style="margin: 0 0 0.25rem 0; font-size: 1.05rem; color: #B45309; font-weight: 700;">Account Pending Administrator Approval</h4>
                    <p style="margin: 0; font-size: 0.9rem; line-height: 1.5; color: #78350F;">
                        Your wholesaler account is registered with AgriTrace but is currently awaiting compliance accreditation from the System Administrator. Until an admin approves your profile, stock verification capabilities are restricted.
                    </p>
                    <div style="margin-top: 0.6rem; font-size: 0.825rem; color: #92400E; display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                        <span><strong>Accreditation Status:</strong> <span class="badge" style="background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D;">Pending Admin Review</span></span>
                        <span>• Contact System Admin: admin@example.com</span>
                    </div>
                </div>
            </div>
        `;
    } else {
        banner.innerHTML = `
            <div style="background: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; padding: 0.85rem 1.25rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; box-shadow: var(--shadow-xs); flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <i data-lucide="shield-check" style="width: 22px; height: 22px; color: #059669;"></i>
                    <span style="font-size: 0.9rem; font-weight: 600;">Accredited Wholesaler • Authorized for Quality Auditing & Stock Verification</span>
                </div>
                <span class="badge delivered" style="font-size: 0.75rem;">Accredited Active</span>
            </div>
        `;
    }
    if (window.lucide) lucide.createIcons();
}

async function loadOrders() {
    if (!currentUser) return;
    
    showLoader();
    try {
        const isApproved = isWholesalerApproved();
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
            
            let actionBtn = '<span style="color: #888; font-size: 0.85rem;">Verified</span>';
            if (data.status === 'Confirmed') {
                if (isApproved) {
                    actionBtn = `<button class="btn btn-sm" onclick="verifyStock('${docSnap.id}')" style="padding: 0.3rem 0.65rem; font-size: 0.825rem; background-color: var(--secondary-color); color: var(--text-color);"><i data-lucide="check-circle" style="width:14px;height:14px;vertical-align:middle;"></i> Verify Stock</button>`;
                } else {
                    actionBtn = `<button class="btn btn-sm" disabled style="padding: 0.3rem 0.65rem; font-size: 0.825rem; opacity: 0.6; cursor: not-allowed; background-color: #E5E7EB; color: #6B7280; border: 1px solid #D1D5DB;" title="Admin approval required to verify stock"><i data-lucide="lock" style="width:14px;height:14px;vertical-align:middle;"></i> Awaiting Approval</button>`;
                }
            }

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.farmerName}</td>
                <td>${data.customerName}</td>
                <td>${itemsList}</td>
                <td>${formatCurrency(data.totalAmount)}</td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>${actionBtn}</td>
            `;
            tbody.appendChild(tr);
        });
        if (window.lucide) lucide.createIcons();
    } catch (error) {
        console.error("Error loading orders:", error);
        showAlert("Failed to load orders", "error");
    } finally {
        hideLoader();
    }
}

window.verifyStock = async (orderId) => {
    if (!isWholesalerApproved()) {
        showAlert("Your account requires Administrator Approval before verifying orders.", "error");
        return;
    }

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
    renderApprovalBanner();
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
