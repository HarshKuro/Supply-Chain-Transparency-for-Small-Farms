// js/farmer.js
import { db } from './firebase-config.js';
import { 
    collection, addDoc, getDocs, doc, updateDoc, deleteDoc, 
    query, where, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

// Initialize Products Page
export function initProductsPage(user) {
    currentUser = user;
    loadProducts();
    setupProductModal();
}

// Setup Modal Events
function setupProductModal() {
    const modal = document.getElementById('productModal');
    const openBtn = document.getElementById('openAddProductModal');
    const closeBtn = document.getElementById('closeProductModal');
    const form = document.getElementById('productForm');

    if(!modal) return;

    openBtn.onclick = () => {
        form.reset();
        document.getElementById('productId').value = '';
        document.getElementById('modalTitle').textContent = 'Add Product';
        document.getElementById('available').checked = true; // default
        modal.style.display = 'flex';
    };

    closeBtn.onclick = () => {
        modal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    form.onsubmit = async (e) => {
        e.preventDefault();
        const id = document.getElementById('productId').value;
        const productData = {
            name: document.getElementById('productName').value,
            category: document.getElementById('category').value,
            description: document.getElementById('description').value,
            price: parseFloat(document.getElementById('price').value),
            quantity: parseInt(document.getElementById('quantity').value),
            unit: document.getElementById('unit').value,
            available: document.getElementById('available').checked && parseInt(document.getElementById('quantity').value) > 0,
            farmerId: currentUser.id,
            farmerName: currentUser.name
        };

        showLoader();
        try {
            if (id) {
                // Update
                await updateDoc(doc(db, "products", id), productData);
                showAlert("Product updated successfully", "success");
            } else {
                // Create
                productData.createdAt = serverTimestamp();
                await addDoc(collection(db, "products"), productData);
                showAlert("Product added successfully", "success");
            }
            modal.style.display = 'none';
            loadProducts();
        } catch (error) {
            console.error("Error saving product:", error);
            showAlert("Failed to save product", "error");
        } finally {
            hideLoader();
        }
    };
}

// Load Products
async function loadProducts() {
    if (!currentUser) return;
    
    showLoader();
    try {
        const q = query(collection(db, "products"), where("farmerId", "==", currentUser.id));
        const querySnapshot = await getDocs(q);
        
        const tbody = document.getElementById('productsTableBody');
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No products found. Add a product to get started.</td></tr>';
            return;
        }

        let totalProducts = 0;
        let availableStock = 0;

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            totalProducts++;
            availableStock += data.quantity;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${data.name}</td>
                <td>${data.category}</td>
                <td>${formatCurrency(data.price)} / ${data.unit}</td>
                <td>${data.quantity} ${data.unit}</td>
                <td>
                    <span class="badge ${data.available ? 'delivered' : 'error'}">
                        ${data.available ? 'Available' : 'Unavailable'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="editProduct('${docSnap.id}')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Edit</button>
                    <button class="btn btn-sm" onclick="deleteProduct('${docSnap.id}')" style="background-color: var(--error-color); padding: 0.25rem 0.5rem; font-size: 0.8rem;">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);

            // Store data globally for editing
            window._productData = window._productData || {};
            window._productData[docSnap.id] = data;
        });

        // Update dashboard stats if they exist
        const statProducts = document.getElementById('statProducts');
        const statStock = document.getElementById('statStock');
        if (statProducts) statProducts.textContent = totalProducts;
        if (statStock) statStock.textContent = availableStock;

    } catch (error) {
        console.error("Error loading products:", error);
        showAlert("Failed to load products", "error");
    } finally {
        hideLoader();
    }
}

// Global functions for inline event handlers
window.editProduct = (id) => {
    const data = window._productData[id];
    if (!data) return;

    document.getElementById('productId').value = id;
    document.getElementById('productName').value = data.name;
    document.getElementById('category').value = data.category;
    document.getElementById('description').value = data.description;
    document.getElementById('price').value = data.price;
    document.getElementById('quantity').value = data.quantity;
    document.getElementById('unit').value = data.unit;
    document.getElementById('available').checked = data.available;
    
    document.getElementById('modalTitle').textContent = 'Edit Product';
    document.getElementById('productModal').style.display = 'flex';
};

window.deleteProduct = async (id) => {
    if (confirm("Are you sure you want to delete this product?")) {
        showLoader();
        try {
            await deleteDoc(doc(db, "products", id));
            showAlert("Product deleted successfully", "success");
            loadProducts();
        } catch (error) {
            console.error("Error deleting product:", error);
            showAlert("Failed to delete product", "error");
        } finally {
            hideLoader();
        }
    }
};

// Expose loadProducts so dashboard can use it if needed
export { loadProducts };

// ================= ORDERS MANAGEMENT =================

export function initFarmerOrdersPage(user) {
    currentUser = user;
    loadFarmerOrders();
}

async function loadFarmerOrders() {
    if (!currentUser) return;
    
    showLoader();
    try {
        const q = query(collection(db, "orders"), where("farmerId", "==", currentUser.id));
        const querySnapshot = await getDocs(q);
        
        const tbody = document.getElementById('ordersTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (querySnapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No orders found.</td></tr>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            const itemsList = data.items.map(item => `${item.productName} (${item.quantity})`).join('<br>');
            const date = data.createdAt ? data.createdAt.toDate().toLocaleDateString() : 'N/A';
            const badgeClass = data.status.toLowerCase().replace(' ', '-');
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><small>${docSnap.id.substring(0,8)}...</small></td>
                <td>${data.customerName}</td>
                <td>${itemsList}</td>
                <td>${formatCurrency(data.totalAmount)}</td>
                <td><span class="badge ${badgeClass}">${data.status}</span></td>
                <td>${date}</td>
                <td>
                    ${data.status === 'Pending' ? 
                        `<button class="btn btn-sm" onclick="confirmOrder('${docSnap.id}')" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Confirm</button>` : 
                        '<span style="color: #888; font-size: 0.85rem;">No action needed</span>'
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

window.confirmOrder = async (orderId) => {
    if (confirm("Confirm this order?")) {
        showLoader();
        try {
            await updateDoc(doc(db, "orders", orderId), {
                status: "Confirmed",
                updatedAt: serverTimestamp()
            });
            showAlert("Order confirmed!", "success");
            loadFarmerOrders();
        } catch (error) {
            console.error("Error confirming order:", error);
            showAlert("Failed to confirm order", "error");
        } finally {
            hideLoader();
        }
    }
};

// ================= DASHBOARD =================
export async function initFarmerDashboard(user) {
    currentUser = user;
    try {
        const qProducts = query(collection(db, "products"), where("farmerId", "==", currentUser.id));
        const snapProducts = await getDocs(qProducts);
        document.getElementById('statProducts').textContent = snapProducts.size;
        let stock = 0;
        snapProducts.forEach(doc => stock += doc.data().quantity);
        document.getElementById('statStock').textContent = stock;
        
        const qOrders = query(collection(db, "orders"), where("farmerId", "==", currentUser.id));
        const snapOrders = await getDocs(qOrders);
        let pending = 0;
        let completed = 0;
        snapOrders.forEach(doc => {
            const status = doc.data().status;
            if (status === 'Pending') pending++;
            else if (status === 'Delivered') completed++;
        });
        document.getElementById('statPending').textContent = pending;
        document.getElementById('statCompleted').textContent = completed;
    } catch(e) {
        console.error(e);
    }
}

