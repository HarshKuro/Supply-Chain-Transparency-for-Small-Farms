// js/customer.js
import { db } from './firebase-config.js';
import { 
    collection, getDocs, doc, getDoc, updateDoc, query, where, addDoc, serverTimestamp, writeBatch 
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { showLoader, hideLoader, showAlert, formatCurrency } from './common.js';

let currentUser = null;

// Cart utility
function getCartKey() {
    return currentUser ? `farmerAppCart_${currentUser.id}` : 'farmerAppCart';
}

function getCart() {
    return JSON.parse(localStorage.getItem(getCartKey())) || [];
}

function saveCart(cart) {
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const cart = getCart();
    const el = document.getElementById('cartCount');
    if (el) {
        el.textContent = `${cart.length} items`;
    }
}

// ================= PRODUCT BROWSING =================
export function initCustomerProductsPage(user) {
    currentUser = user;
    updateCartCount();
    loadAvailableProducts();
}

async function loadAvailableProducts() {
    showLoader();
    try {
        const q = query(collection(db, "products"), where("available", "==", true));
        const querySnapshot = await getDocs(q);
        
        const grid = document.getElementById('productGrid');
        grid.innerHTML = '';
        
        if (querySnapshot.empty) {
            grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center;">No products available right now.</div>';
            return;
        }

        querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            
            // Safety check in case quantity is 0 but available is somehow true
            if (data.quantity <= 0) return;

            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <div>
                    <span class="badge delivered">${data.category}</span>
                </div>
                <h3>${data.name}</h3>
                <div class="farmer">By ${data.farmerName}</div>
                <div class="desc">${data.description}</div>
                <div class="price">${formatCurrency(data.price)} / ${data.unit}</div>
                <div style="font-size: 0.9rem; margin-bottom: 1rem;">Available: ${data.quantity} ${data.unit}</div>
                <button class="btn" onclick="addToCart('${docSnap.id}', '${data.name}', ${data.price}, '${data.farmerId}', '${data.farmerName}', ${data.quantity})">Add to Cart</button>
            `;
            grid.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading products:", error);
        showAlert("Failed to load products", "error");
    } finally {
        hideLoader();
    }
}

window.addToCart = (productId, productName, price, farmerId, farmerName, maxQuantity) => {
    const cart = getCart();
    
    // Check if farmer matches existing items (can only order from one farmer, or allow multiple but handle orders per farmer)
    // For simplicity in academic project, we will group by farmer when placing the order, so it's fine.
    
    const existingIndex = cart.findIndex(item => item.productId === productId);
    if (existingIndex > -1) {
        if (cart[existingIndex].quantity + 1 > maxQuantity) {
            showAlert("Requested quantity is not available.", "warning");
            return;
        }
        cart[existingIndex].quantity += 1;
    } else {
        cart.push({
            productId,
            productName,
            price,
            farmerId,
            farmerName,
            quantity: 1,
            maxQuantity
        });
    }
    
    saveCart(cart);
    showAlert(`${productName} added to cart`, "success");
};

// ================= CART & CHECKOUT =================
export function initCartPage(user) {
    currentUser = user;
    renderCart();
    
    document.getElementById('placeOrderBtn').addEventListener('click', placeOrder);
}

function renderCart() {
    const cart = getCart();
    const tbody = document.getElementById('cartTableBody');
    const placeOrderBtn = document.getElementById('placeOrderBtn');
    
    tbody.innerHTML = '';
    
    if (cart.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Your cart is empty.</td></tr>';
        document.getElementById('cartTotal').textContent = '$0.00';
        placeOrderBtn.style.display = 'none';
        return;
    }

    let totalAmount = 0;
    
    cart.forEach((item, index) => {
        const subtotal = item.price * item.quantity;
        totalAmount += subtotal;
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.productName}</td>
            <td>${item.farmerName}</td>
            <td>${formatCurrency(item.price)}</td>
            <td>
                <input type="number" min="1" max="${item.maxQuantity}" value="${item.quantity}" 
                    onchange="updateCartQuantity(${index}, this.value)" 
                    style="width: 70px; padding: 0.25rem;">
            </td>
            <td>${formatCurrency(subtotal)}</td>
            <td>
                <button class="btn btn-sm" style="background-color: var(--error-color); padding: 0.25rem 0.5rem;" onclick="removeFromCart(${index})">Remove</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('cartTotal').textContent = formatCurrency(totalAmount);
    placeOrderBtn.style.display = 'inline-block';
}

window.updateCartQuantity = (index, value) => {
    const cart = getCart();
    const qty = parseInt(value);
    
    if (qty > 0 && qty <= cart[index].maxQuantity) {
        cart[index].quantity = qty;
        saveCart(cart);
        renderCart();
    } else {
        showAlert("Invalid quantity or exceeds stock", "warning");
        renderCart(); // reset value
    }
};

window.removeFromCart = (index) => {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderCart();
};

async function placeOrder() {
    const cart = getCart();
    if (cart.length === 0) return;

    showLoader();
    try {
        // Group items by farmer so each farmer gets a separate order, matching the data model
        const ordersByFarmer = {};
        
        for (const item of cart) {
            if (!ordersByFarmer[item.farmerId]) {
                ordersByFarmer[item.farmerId] = {
                    farmerId: item.farmerId,
                    farmerName: item.farmerName,
                    items: [],
                    totalAmount: 0
                };
            }
            
            ordersByFarmer[item.farmerId].items.push({
                productId: item.productId,
                productName: item.productName,
                quantity: item.quantity,
                price: item.price
            });
            ordersByFarmer[item.farmerId].totalAmount += (item.quantity * item.price);
        }

        const batch = writeBatch(db);

        // First verify all stock is still available
        for (const item of cart) {
            const productRef = doc(db, "products", item.productId);
            const productSnap = await getDoc(productRef);
            
            if (!productSnap.exists()) {
                throw new Error(`${item.productName} is no longer available (deleted by farmer).`);
            }
            if (productSnap.data().quantity < item.quantity) {
                throw new Error(`Insufficient stock for ${item.productName}`);
            }
            
            // Deduct stock
            const newQuantity = productSnap.data().quantity - item.quantity;
            batch.update(productRef, {
                quantity: newQuantity,
                available: newQuantity > 0
            });
        }

        // Create orders
        const ordersRef = collection(db, "orders");
        for (const farmerId in ordersByFarmer) {
            const orderData = ordersByFarmer[farmerId];
            
            // We use standard ref so we can add to batch
            const newOrderRef = doc(ordersRef);
            batch.set(newOrderRef, {
                customerId: currentUser.id,
                customerName: currentUser.name,
                farmerId: orderData.farmerId,
                farmerName: orderData.farmerName,
                items: orderData.items,
                totalAmount: orderData.totalAmount,
                status: "Pending",
                wholesalerId: "",
                driverId: "",
                deliveryAddress: "Customer Default Address", // Can be dynamic if added to user profile
                createdAt: serverTimestamp(),
                updatedAt: serverTimestamp()
            });
        }

        await batch.commit();

        localStorage.removeItem(getCartKey());
        showAlert("Order placed successfully!", "success");
        setTimeout(() => {
            window.location.href = 'orders.html';
        }, 1500);

    } catch (error) {
        console.error("Error placing order:", error);
        showAlert(error.message || "Failed to place order", "error");
    } finally {
        hideLoader();
    }
}

// ================= ORDERS TRACKING =================
export function initCustomerOrdersPage(user) {
    currentUser = user;
    loadCustomerOrders();
}

async function loadCustomerOrders() {
    showLoader();
    try {
        const q = query(collection(db, "orders"), where("customerId", "==", currentUser.id));
        const querySnapshot = await getDocs(q);
        
        const container = document.getElementById('ordersContainer');
        container.innerHTML = '';
        
        if (querySnapshot.empty) {
            container.innerHTML = '<div>You have no orders yet.</div>';
            return;
        }

        const stages = ['Pending', 'Confirmed', 'Verified', 'Assigned', 'Picked Up', 'In Transit', 'Delivered'];

        // Sort descending locally
        const orders = [];
        querySnapshot.forEach(docSnap => orders.push({ id: docSnap.id, ...docSnap.data() }));
        orders.sort((a, b) => b.createdAt - a.createdAt);

        orders.forEach(data => {
            const currentStageIndex = stages.indexOf(data.status);
            
            let trackerHtml = '<div class="tracker">';
            stages.forEach((stage, index) => {
                let statusClass = '';
                if (index < currentStageIndex) statusClass = 'completed';
                else if (index === currentStageIndex) statusClass = 'active';
                
                trackerHtml += `
                    <div class="step ${statusClass}">
                        <div class="circle">${index < currentStageIndex ? '✓' : index + 1}</div>
                        <div>${stage}</div>
                    </div>
                `;
            });
            trackerHtml += '</div>';

            const itemsList = data.items.map(item => `${item.productName} (${item.quantity})`).join(', ');
            
            let feedbackBtn = '';
            if (data.status === 'Delivered') {
                feedbackBtn = `<a href="feedback.html?orderId=${data.id}&farmerName=${encodeURIComponent(data.farmerName)}" class="btn btn-secondary">Give Feedback</a>`;
            }

            const card = document.createElement('div');
            card.className = 'order-card';
            card.innerHTML = `
                <div class="order-header">
                    <div>
                        <strong>Order ID:</strong> ${data.id}<br>
                        <strong>Date:</strong> ${data.createdAt ? data.createdAt.toDate().toLocaleDateString() : 'N/A'}<br>
                        <strong>Farmer:</strong> ${data.farmerName}
                    </div>
                    <div style="text-align: right;">
                        <strong>Total:</strong> ${formatCurrency(data.totalAmount)}<br>
                        ${feedbackBtn}
                    </div>
                </div>
                <div>
                    <strong>Items:</strong> ${itemsList}
                </div>
                ${trackerHtml}
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading orders:", error);
        showAlert("Failed to load orders", "error");
    } finally {
        hideLoader();
    }
}

// ================= FEEDBACK =================
export function initFeedbackPage(user) {
    currentUser = user;
    
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('orderId');
    const farmerName = urlParams.get('farmerName');
    
    if (orderId) {
        document.getElementById('feedbackMessage').style.display = 'none';
        document.getElementById('feedbackForm').style.display = 'block';
        
        document.getElementById('orderId').value = orderId;
        document.getElementById('displayOrderId').textContent = orderId;
        document.getElementById('displayFarmer').textContent = farmerName || 'Unknown';
    } else {
        document.getElementById('feedbackMessage').textContent = 'Please select an order from your Orders page to give feedback.';
        // Optionally, load delivered orders and show a dropdown
    }

    document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const ratingNode = document.querySelector('input[name="rating"]:checked');
        if (!ratingNode) {
            showAlert("Please select a rating.", "warning");
            return;
        }
        
        const rating = parseInt(ratingNode.value);
        const comment = document.getElementById('comment').value;
        const oid = document.getElementById('orderId').value;
        
        showLoader();
        try {
            await addDoc(collection(db, "feedback"), {
                orderId: oid,
                customerId: currentUser.id,
                customerName: currentUser.name,
                rating: rating,
                comment: comment,
                createdAt: serverTimestamp()
            });
            
            showAlert("Thank you for your feedback!", "success");
            setTimeout(() => {
                window.location.href = 'orders.html';
            }, 1500);
        } catch (error) {
            console.error("Error saving feedback:", error);
            showAlert("Failed to save feedback", "error");
        } finally {
            hideLoader();
        }
    });
}

// ================= DASHBOARD =================
export async function initCustomerDashboard(user) {
    currentUser = user;
    try {
        const qProducts = query(collection(db, "products"), where("available", "==", true));
        const snapProducts = await getDocs(qProducts);
        document.getElementById('statProducts').textContent = snapProducts.size;
        
        const qOrders = query(collection(db, "orders"), where("customerId", "==", currentUser.id));
        const snapOrders = await getDocs(qOrders);
        document.getElementById('statOrders').textContent = snapOrders.size;
        
        let pending = 0;
        let delivered = 0;
        snapOrders.forEach(doc => {
            if (doc.data().status === 'Delivered') delivered++;
            else pending++;
        });
        document.getElementById('statPending').textContent = pending;
        document.getElementById('statDelivered').textContent = delivered;
    } catch(e) { console.error(e); }
}
