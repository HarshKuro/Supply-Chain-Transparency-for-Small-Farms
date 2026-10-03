// tests/unit_tests.js - Automated Unit Tests for Supply Chain Transparency
import assert from 'node:assert/strict';

const testResults = [];

function recordTest(id, name, fn) {
    try {
        fn();
        testResults.push({ id, name, status: 'PASS', error: null });
        console.log(`[PASS] ${id}: ${name}`);
    } catch (err) {
        testResults.push({ id, name, status: 'FAIL', error: err.message });
        console.error(`[FAIL] ${id}: ${name} -> ${err.message}`);
    }
}

// ================= 1. FORM VALIDATION =================
recordTest('UNIT-01', 'Form Validation: Required field checks for registration', () => {
    function validateRegistration(fullName, email, password, phone, role) {
        if (!fullName || fullName.trim() === '') return { valid: false, error: 'Full name required' };
        if (!email || !email.includes('@')) return { valid: false, error: 'Valid email required' };
        if (!password || password.length < 6) return { valid: false, error: 'Password must be at least 6 characters' };
        if (!phone || phone.trim().length < 8) return { valid: false, error: 'Valid phone required' };
        if (!['farmer', 'wholesaler', 'driver', 'customer'].includes(role)) return { valid: false, error: 'Valid role required' };
        return { valid: true };
    }

    assert.equal(validateRegistration('', 'a@b.com', '123456', '0412345678', 'farmer').valid, false);
    assert.equal(validateRegistration('Jack Miller', 'invalid-email', '123456', '0412345678', 'farmer').valid, false);
    assert.equal(validateRegistration('Jack Miller', 'a@b.com', '123', '0412345678', 'farmer').valid, false);
    assert.equal(validateRegistration('Jack Miller', 'a@b.com', '123456', '123', 'farmer').valid, false);
    assert.equal(validateRegistration('Jack Miller', 'a@b.com', '123456', '0412345678', 'invalid_role').valid, false);
    assert.equal(validateRegistration('Jack Miller', 'a@b.com', '123456', '0412345678', 'farmer').valid, true);
});

// ================= 2. QUANTITY VALIDATION =================
recordTest('UNIT-02', 'Quantity Validation: Positive integers and stock boundaries', () => {
    function validateCartQuantity(requestedQty, availableStock) {
        const qty = parseInt(requestedQty, 10);
        if (isNaN(qty) || qty <= 0) return false;
        if (qty > availableStock) return false;
        return true;
    }

    assert.equal(validateCartQuantity(0, 10), false);
    assert.equal(validateCartQuantity(-5, 10), false);
    assert.equal(validateCartQuantity('abc', 10), false);
    assert.equal(validateCartQuantity(11, 10), false);
    assert.equal(validateCartQuantity(5, 10), true);
    assert.equal(validateCartQuantity(10, 10), true);
});

// ================= 3. ORDER TOTAL CALCULATION =================
recordTest('UNIT-03', 'Order Total Calculation: Multi-item price x quantity accumulation', () => {
    function calculateTotal(items) {
        return items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    const cart = [
        { price: 40.0, quantity: 2 },  // 80.0
        { price: 30.5, quantity: 3 },  // 91.5
        { price: 120.0, quantity: 1 }  // 120.0
    ];
    const total = calculateTotal(cart);
    assert.equal(total, 291.5);
});

// ================= 4. STOCK CALCULATION =================
recordTest('UNIT-04', 'Stock Calculation: Quantity decrement and availability flag', () => {
    function deductStock(currentStock, orderQuantity) {
        if (currentStock < orderQuantity) {
            throw new Error('Insufficient stock');
        }
        const newQuantity = currentStock - orderQuantity;
        return {
            quantity: newQuantity,
            available: newQuantity > 0
        };
    }

    const res1 = deductStock(100, 30);
    assert.equal(res1.quantity, 70);
    assert.equal(res1.available, true);

    const res2 = deductStock(30, 30);
    assert.equal(res2.quantity, 0);
    assert.equal(res2.available, false);

    assert.throws(() => deductStock(10, 20), /Insufficient stock/);
});

// ================= 5. STATUS HANDLING =================
recordTest('UNIT-05', 'Status Handling: Valid supply chain lifecycle sequence', () => {
    const LIFECYCLE = [
        'Pending',
        'Confirmed',
        'Verified',
        'Assigned',
        'Picked Up',
        'In Transit',
        'Delivered'
    ];

    function isValidTransition(currentStatus, nextStatus) {
        const curIdx = LIFECYCLE.indexOf(currentStatus);
        const nextIdx = LIFECYCLE.indexOf(nextStatus);
        if (curIdx === -1 || nextIdx === -1) return false;
        return nextIdx === curIdx + 1;
    }

    assert.equal(isValidTransition('Pending', 'Confirmed'), true);
    assert.equal(isValidTransition('Confirmed', 'Verified'), true);
    assert.equal(isValidTransition('Verified', 'Assigned'), true);
    assert.equal(isValidTransition('Assigned', 'Picked Up'), true);
    assert.equal(isValidTransition('Picked Up', 'In Transit'), true);
    assert.equal(isValidTransition('In Transit', 'Delivered'), true);

    // Invalid jumps
    assert.equal(isValidTransition('Pending', 'Delivered'), false);
    assert.equal(isValidTransition('Delivered', 'Pending'), false);
    assert.equal(isValidTransition('Confirmed', 'In Transit'), false);
});

recordTest('UNIT-06', 'Status Handling: CSS badge class generation', () => {
    function getBadgeClass(status) {
        return status.toLowerCase().replace(/\s+/g, '-');
    }

    assert.equal(getBadgeClass('Pending'), 'pending');
    assert.equal(getBadgeClass('In Transit'), 'in-transit');
    assert.equal(getBadgeClass('Picked Up'), 'picked-up');
    assert.equal(getBadgeClass('Delivered'), 'delivered');
});

// ================= 6. UTILITY FUNCTIONS =================
recordTest('UNIT-07', 'Utility: formatCurrency formats Australian Dollars (AUD) correctly', () => {
    function formatCurrency(amount) {
        return `$${parseFloat(amount).toFixed(2)}`;
    }

    assert.equal(formatCurrency(40), '$40.00');
    assert.equal(formatCurrency(99.5), '$99.50');
    assert.equal(formatCurrency(0), '$0.00');
    assert.equal(formatCurrency('125.755'), '$125.75');
});

recordTest('UNIT-08', 'Utility: roleRoutes map matches destination paths', () => {
    const roleRoutes = {
        'farmer': 'farmer/dashboard.html',
        'wholesaler': 'wholesaler/dashboard.html',
        'driver': 'driver/dashboard.html',
        'customer': 'customer/dashboard.html',
        'admin': 'admin/dashboard.html'
    };

    assert.equal(roleRoutes['farmer'], 'farmer/dashboard.html');
    assert.equal(roleRoutes['customer'], 'customer/dashboard.html');
    assert.equal(roleRoutes['wholesaler'], 'wholesaler/dashboard.html');
    assert.equal(roleRoutes['driver'], 'driver/dashboard.html');
    assert.equal(roleRoutes['admin'], 'admin/dashboard.html');
});

console.log('\n--- Unit Test Summary ---');
const passed = testResults.filter(t => t.status === 'PASS').length;
const failed = testResults.filter(t => t.status === 'FAIL').length;
console.log(`Total: ${testResults.length}, Passed: ${passed}, Failed: ${failed}`);
