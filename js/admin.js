// js/admin.js - Complete Administration & Wholesaler Accreditation Management
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, deleteDoc, updateDoc, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

// ================= WHOLESALER APPROVALS =================
export function initAdminApprovalsPage(user) {
    currentUser = user;
    loadApprovals();
}

async function loadApprovals() {
    showLoader();
    try {
        const querySnapshot = await getDocs(collection(db, "users"));
        const pendingTbody = document.getElementById('pendingTableBody');
        const approvedTbody = document.getElementById('approvedTableBody');
        
        if (pendingTbody) pendingTbody.innerHTML = '';
        if (approvedTbody) approvedTbody.innerHTML = '';
        
        let pendingCount = 0;
        let approvedCount = 0;

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            if (data.role !== 'wholesaler') return;

            const isApproved = data.approved === true || data.approvalStatus === 'approved';
            const joinedDate = data.createdAt ? data.createdAt.toDate().toLocaleDateString('en-AU') : 'N/A';

            if (!isApproved) {
                pendingCount++;
                if (pendingTbody) {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${data.name}</strong></td>
                        <td>${data.email}</td>
                        <td>${data.phone || 'N/A'}</td>
                        <td><span class="badge in-transit" style="background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D;">Pending Review</span></td>
                        <td>${joinedDate}</td>
                        <td>
                            <button class="btn btn-sm" onclick="toggleWholesalerApproval('${docSnap.id}', true)" style="background-color: #059669; padding: 0.35rem 0.75rem; font-size: 0.825rem; margin-right: 6px;">
                                <i data-lucide="check-circle" style="width:14px;height:14px;vertical-align:middle;"></i> Approve Wholesaler
                            </button>
                            <button class="btn btn-sm" onclick="deleteUserRecord('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.35rem 0.65rem; font-size: 0.825rem;">
                                Reject & Delete
                            </button>
                        </td>
                    `;
                    pendingTbody.appendChild(tr);
                }
            } else {
                approvedCount++;
                if (approvedTbody) {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${data.name}</strong></td>
                        <td>${data.email}</td>
                        <td>${data.phone || 'N/A'}</td>
                        <td><span class="badge delivered">Accredited Active</span></td>
                        <td>${joinedDate}</td>
                        <td>
                            <button class="btn btn-sm" onclick="toggleWholesalerApproval('${docSnap.id}', false)" style="background-color: #DC2626; padding: 0.35rem 0.65rem; font-size: 0.825rem; margin-right: 6px;">
                                <i data-lucide="shield-x" style="width:14px;height:14px;vertical-align:middle;"></i> Revoke
                            </button>
                            <button class="btn btn-sm" onclick="deleteUserRecord('${docSnap.id}')" style="background-color: #6B7280; padding: 0.35rem 0.55rem; font-size: 0.825rem;">
                                Delete
                            </button>
                        </td>
                    `;
                    approvedTbody.appendChild(tr);
                }
            }
        });

        if (pendingTbody && pendingCount === 0) {
            pendingTbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 1.5rem; color: var(--text-muted);">🎉 No wholesaler accounts are currently pending approval. All applications processed!</td></tr>';
        }
        if (approvedTbody && approvedCount === 0) {
            approvedTbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 1.5rem; color: var(--text-muted);">No accredited wholesalers found.</td></tr>';
        }

        const statPendingEl = document.getElementById('statPendingApprovals');
        if (statPendingEl) statPendingEl.textContent = pendingCount;
        const statApprovedEl = document.getElementById('statApprovedWholesalers');
        if (statApprovedEl) statApprovedEl.textContent = approvedCount;

        if (window.lucide) lucide.createIcons();
    } catch (error) {
        console.error("Error loading approvals:", error);
        showAlert("Failed to load wholesaler approvals", "error");
    } finally {
        hideLoader();
    }
}

window.toggleWholesalerApproval = async (userId, shouldApprove) => {
    const actionName = shouldApprove ? "approve this wholesaler for quality & stock verification" : "revoke accreditation for this wholesaler";
    if (confirm(`Are you sure you want to ${actionName}?`)) {
        showLoader();
        try {
            await updateDoc(doc(db, "users", userId), {
                approved: shouldApprove,
                approvalStatus: shouldApprove ? 'approved' : 'revoked',
                accreditedAt: shouldApprove ? serverTimestamp() : null
            });
            showAlert(shouldApprove ? "Wholesaler accredited & approved successfully!" : "Wholesaler accreditation revoked.", "success");
            
            // Reload page or tables
            if (document.getElementById('pendingTableBody')) {
                loadApprovals();
            } else if (document.getElementById('usersTableBody')) {
                loadUsers();
            }
        } catch (error) {
            console.error("Error toggling wholesaler approval:", error);
            showAlert("Failed to update wholesaler status: " + error.message, "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= USERS =================
export function initAdminUsersPage(user) {
    currentUser = user;
    loadUsers();
}

async function loadUsers() {
    showLoader();
    try {
        const querySnapshot = await getDocs(collection(db, "users"));
        const tbody = document.getElementById('usersTableBody');
        
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No users found.</td></tr>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            const tr = document.createElement('tr');
            
            let statusPill = '';
            let approvalBtn = '';

            if (data.role === 'wholesaler') {
                const isApproved = data.approved === true || data.approvalStatus === 'approved';
                if (isApproved) {
                    statusPill = ' <span class="badge delivered" style="font-size:0.75rem; padding: 2px 6px;">Approved</span>';
                    approvalBtn = `<button class="btn btn-sm" onclick="toggleWholesalerApproval('${docSnap.id}', false)" style="background-color: #DC2626; padding: 0.25rem 0.5rem; font-size: 0.8rem; margin-right: 4px;" title="Revoke accreditation">Revoke</button>`;
                } else {
                    statusPill = ' <span class="badge in-transit" style="font-size:0.75rem; padding: 2px 6px; background:#FEF3C7; color:#92400E; border:1px solid #FCD34D;">Pending Approval</span>';
                    approvalBtn = `<button class="btn btn-sm" onclick="toggleWholesalerApproval('${docSnap.id}', true)" style="background-color: #059669; padding: 0.25rem 0.5rem; font-size: 0.8rem; margin-right: 4px;" title="Approve wholesaler">Approve</button>`;
                }
            }

            // Prevent admin from deleting themselves easily
            const actionHtml = data.role !== 'admin' ? 
                `${approvalBtn}<button class="btn btn-sm" onclick="deleteUserRecord('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.25rem 0.5rem; font-size: 0.8rem;">Delete</button>` : 
                '<span class="badge" style="background:#e0e7ff; color:#3730a3;">System Admin</span>';

            tr.innerHTML = `
                <td><strong>${data.name}</strong></td>
                <td>${data.email}</td>
                <td>${data.phone || 'N/A'}</td>
                <td style="text-transform: capitalize;">${data.role}${statusPill}</td>
                <td>${data.createdAt ? data.createdAt.toDate().toLocaleDateString('en-AU') : 'N/A'}</td>
                <td>${actionHtml}</td>
            `;
            tbody.appendChild(tr);
        });
        if (window.lucide) lucide.createIcons();
    } catch (error) {
        console.error("Error loading users:", error);
        showAlert("Failed to load users", "error");
    } finally {
        hideLoader();
    }
}

window.deleteUserRecord = async (userId) => {
    if (confirm("Delete this user record from Firestore?")) {
        showLoader();
        try {
            await deleteDoc(doc(db, "users", userId));
            showAlert("User record deleted", "success");
            if (document.getElementById('usersTableBody')) {
                loadUsers();
            } else if (document.getElementById('pendingTableBody')) {
                loadApprovals();
            }
        } catch (error) {
            console.error("Error deleting user:", error);
            showAlert("Failed to delete user", "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= PRODUCTS =================
export function initAdminProductsPage(user) {
    currentUser = user;
    loadProducts();
}

async function loadProducts() {
    showLoader();
    try {
        const querySnapshot = await getDocs(collection(db, "products"));
        const tbody = document.getElementById('productsTableBody');
        
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No products found.</td></tr>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${data.name}</strong><br><small style="color:var(--text-muted);">${data.category || 'Produce'}</small></td>
                <td>${data.farmerName || 'Australian Farm'}</td>
                <td>${formatCurrency(data.price)} AUD / ${data.unit}</td>
                <td>${data.quantity} ${data.unit}</td>
                <td><span class="badge ${data.available ? 'delivered' : 'error'}">${data.available ? 'Available' : 'Unavailable'}</span></td>
                <td><button class="btn btn-sm" onclick="deleteProductAdmin('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.25rem 0.5rem; font-size: 0.8rem;">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });
        if (window.lucide) lucide.createIcons();
    } catch (error) {
        console.error("Error loading products:", error);
        showAlert("Failed to load products", "error");
    } finally {
        hideLoader();
    }
}

window.deleteProductAdmin = async (productId) => {
    if (confirm("Delete this product from catalog?")) {
        showLoader();
        try {
            await deleteDoc(doc(db, "products", productId));
            showAlert("Product deleted", "success");
            loadProducts();
        } catch (error) {
            console.error("Error deleting product:", error);
            showAlert("Failed to delete product", "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= ORDERS =================
export function initAdminOrdersPage(user) {
    currentUser = user;
    loadOrders();
}

async function loadOrders() {
    showLoader();
    try {
        const querySnapshot = await getDocs(collection(db, "orders"));
        const tbody = document.getElementById('ordersTableBody');
        
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No orders found.</td></tr>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            const itemsList = Array.isArray(data.items) ? data.items.map(i => `${i.productName} (${i.quantity})`).join('<br>') : 'N/A';
            const badgeClass = (data.status || '').toLowerCase().replace(' ', '-');
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.customerName || 'N/A'}</td>
                <td>${data.farmerName || 'N/A'}</td>
                <td>${itemsList}</td>
                <td><strong>${formatCurrency(data.totalAmount || 0)} AUD</strong></td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>${data.createdAt ? data.createdAt.toDate().toLocaleDateString('en-AU') : 'N/A'}</td>
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

// ================= DASHBOARD =================
export async function initAdminDashboard(user) {
    currentUser = user;
    try {
        const snapUsers = await getDocs(collection(db, "users"));
        let farmers = 0, customers = 0, drivers = 0, wholesalers = 0;
        let pendingWholesalers = 0, approvedWholesalers = 0;

        snapUsers.forEach(docSnap => {
            const d = docSnap.data();
            const r = d.role;
            if(r === 'farmer') farmers++;
            if(r === 'customer') customers++;
            if(r === 'driver') drivers++;
            if(r === 'wholesaler') {
                wholesalers++;
                if (d.approved === true || d.approvalStatus === 'approved') {
                    approvedWholesalers++;
                } else {
                    pendingWholesalers++;
                }
            }
        });

        if (document.getElementById('statUsers')) document.getElementById('statUsers').textContent = snapUsers.size;
        if (document.getElementById('statFarmers')) document.getElementById('statFarmers').textContent = farmers;
        if (document.getElementById('statCustomers')) document.getElementById('statCustomers').textContent = customers;
        if (document.getElementById('statDrivers')) document.getElementById('statDrivers').textContent = drivers;
        if (document.getElementById('statWholesalers')) document.getElementById('statWholesalers').textContent = wholesalers;
        if (document.getElementById('statPendingWholesalers')) document.getElementById('statPendingWholesalers').textContent = pendingWholesalers;
        if (document.getElementById('statApprovedWholesalers')) document.getElementById('statApprovedWholesalers').textContent = approvedWholesalers;
        
        // Show pending alert banner if any need approval
        const alertContainer = document.getElementById('pendingApprovalAlert');
        if (alertContainer) {
            if (pendingWholesalers > 0) {
                alertContainer.style.display = 'block';
                alertContainer.innerHTML = `
                    <div style="background: #FFFBEB; border: 1px solid #FCD34D; color: #92400E; padding: 1rem 1.25rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <i data-lucide="bell-ring" style="width: 24px; height: 24px; color: #D97706; flex-shrink: 0;"></i>
                            <div>
                                <strong style="font-size: 0.95rem; color: #B45309;">${pendingWholesalers} Wholesaler Account(s) Awaiting Compliance Approval</strong>
                                <p style="margin: 0; font-size: 0.85rem; color: #78350F;">Review and authorize wholesale accreditation so they can verify agricultural stock batches.</p>
                            </div>
                        </div>
                        <a href="approvals.html" class="btn btn-sm" style="background: #D97706; color: white !important;">
                            Review Approvals (${pendingWholesalers}) →
                        </a>
                    </div>
                `;
            } else {
                alertContainer.style.display = 'none';
            }
        }

        const snapProducts = await getDocs(collection(db, "products"));
        if (document.getElementById('statProducts')) document.getElementById('statProducts').textContent = snapProducts.size;
        
        const snapOrders = await getDocs(collection(db, "orders"));
        if (document.getElementById('statOrders')) document.getElementById('statOrders').textContent = snapOrders.size;
        
        let totalRev = 0;
        snapOrders.forEach(o => {
            totalRev += (o.data().totalAmount || 0);
        });
        if (document.getElementById('statRevenue')) {
            document.getElementById('statRevenue').textContent = formatCurrency(totalRev) + ' AUD';
        }

        if (window.lucide) lucide.createIcons();
    } catch(e) { 
        console.error("Dashboard init error:", e); 
    }
}
