// js/admin.js
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, deleteDoc 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

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
            
            // Prevent admin from deleting themselves easily
            const actionHtml = data.role !== 'admin' ? 
                `<button class="btn btn-sm" onclick="deleteUserRecord('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.25rem 0.5rem;">Delete</button>` : 
                'Admin';

            tr.innerHTML = `
                <td>${data.name}</td>
                <td>${data.email}</td>
                <td>${data.phone}</td>
                <td style="text-transform: capitalize;">${data.role}</td>
                <td>${data.createdAt ? data.createdAt.toDate().toLocaleDateString() : 'N/A'}</td>
                <td>${actionHtml}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading users:", error);
        showAlert("Failed to load users", "error");
    } finally {
        hideLoader();
    }
}

window.deleteUserRecord = async (userId) => {
    if (confirm("Delete this user record from Firestore? (Authentication account must be deleted manually from Firebase console)")) {
        showLoader();
        try {
            await deleteDoc(doc(db, "users", userId));
            showAlert("User record deleted", "success");
            loadUsers();
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
                <td>${data.name}</td>
                <td>${data.farmerName}</td>
                <td>${formatCurrency(data.price)} / ${data.unit}</td>
                <td>${data.quantity} ${data.unit}</td>
                <td><span class="badge ${data.available ? 'delivered' : 'error'}">${data.available ? 'Available' : 'Unavailable'}</span></td>
                <td><button class="btn btn-sm" onclick="deleteProductAdmin('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.25rem 0.5rem;">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading products:", error);
        showAlert("Failed to load products", "error");
    } finally {
        hideLoader();
    }
}

window.deleteProductAdmin = async (productId) => {
    if (confirm("Delete this product?")) {
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
            const itemsList = data.items.map(i => `${i.productName} (${i.quantity})`).join('<br>');
            const badgeClass = data.status.toLowerCase().replace(' ', '-');
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.customerName}</td>
                <td>${data.farmerName}</td>
                <td>${itemsList}</td>
                <td>${formatCurrency(data.totalAmount)}</td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>${data.createdAt ? data.createdAt.toDate().toLocaleDateString() : 'N/A'}</td>
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

// ================= DASHBOARD =================
export async function initAdminDashboard(user) {
    currentUser = user;
    try {
        const snapUsers = await getDocs(collection(db, "users"));
        let farmers = 0, customers = 0, drivers = 0, wholesalers = 0;
        snapUsers.forEach(doc => {
            const r = doc.data().role;
            if(r === 'farmer') farmers++;
            if(r === 'customer') customers++;
            if(r === 'driver') drivers++;
            if(r === 'wholesaler') wholesalers++;
        });
        document.getElementById('statUsers').textContent = snapUsers.size;
        document.getElementById('statFarmers').textContent = farmers;
        document.getElementById('statCustomers').textContent = customers;
        document.getElementById('statDrivers').textContent = drivers;
        document.getElementById('statWholesalers').textContent = wholesalers;
        
        const snapProducts = await getDocs(collection(db, "products"));
        document.getElementById('statProducts').textContent = snapProducts.size;
        
        const snapOrders = await getDocs(collection(db, "orders"));
        document.getElementById('statOrders').textContent = snapOrders.size;
    } catch(e) { console.error(e); }
}
