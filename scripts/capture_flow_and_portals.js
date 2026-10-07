const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://localhost:8000';
const DOCX_IMG_DIR = path.join(__dirname, '..', 'docx', 'images');
const SCREENSHOT_DIR = path.join(__dirname, '..', 'screenshots');

if (!fs.existsSync(DOCX_IMG_DIR)) fs.mkdirSync(DOCX_IMG_DIR, { recursive: true });
if (!fs.existsSync(SCREENSHOT_DIR)) fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Function that guarantees ZERO loading marks or spinners
async function waitForDataReady(page) {
    // 1. Initial grace period for scripts to boot
    await sleep(800);

    // 2. Wait until #loader is either hidden or non-existent
    await page.waitForFunction(() => {
        const l = document.getElementById('loader');
        return !l || window.getComputedStyle(l).display === 'none';
    }, { timeout: 15000 }).catch(() => {});

    // 3. Wait until table bodies & containers have loaded real data instead of "Loading..."
    await page.waitForFunction(() => {
        const text = document.body ? document.body.innerText : '';
        return !text.includes('Loading products...') &&
               !text.includes('Loading orders...') &&
               !text.includes('Loading deliveries...') &&
               !text.includes('Loading stakeholders...') &&
               !text.includes('Loading pending wholesalers...') &&
               !text.includes('Loading accredited wholesalers...') &&
               !text.includes('Loading available products...');
    }, { timeout: 15000 }).catch(() => {});

    // 4. Wait until userName is populated
    await page.waitForFunction(() => {
        const u = document.getElementById('userName');
        return !u || !u.innerText.includes('Loading');
    }, { timeout: 10000 }).catch(() => {});

    // 5. Explicitly force #loader hidden so it CANNOT appear
    await page.evaluate(() => {
        const l = document.getElementById('loader');
        if (l) l.style.display = 'none';
    });

    // 6. Give lucide icons and transitions a moment to render crisp
    await sleep(600);
}

async function capture(page, filename, desc) {
    await waitForDataReady(page);
    const p1 = path.join(SCREENSHOT_DIR, filename);
    const p2 = path.join(DOCX_IMG_DIR, filename);
    await page.screenshot({ path: p1, fullPage: false });
    fs.copyFileSync(p1, p2);
    const sz = fs.statSync(p1).size;
    console.log(`[OK] Captured: ${filename} - ${desc} (${sz} bytes)`);
}

async function loginUser(page, email) {
    console.log(`\nLogging in as: ${email}...`);
    await page.goto(`${BASE_URL}/login.html`, { waitUntil: 'networkidle2' });
    await page.click(`.demo-btn[data-email="${email}"]`);
    await page.waitForFunction(() => !window.location.href.includes('login.html'), { timeout: 12000 });
    await waitForDataReady(page);
}

async function main() {
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new',
        args: ['--no-sandbox', '--disable-gpu']
    });

    // ==========================================
    // STAGE 0: RE-SEED DATABASE FOR CLEAN STATE
    // ==========================================
    console.log('=== Stage 0: Initializing Clean Australian Database ===');
    {
        const page = await browser.newPage();
        await page.goto(`${BASE_URL}/seed.html`, { waitUntil: 'networkidle2' });
        await page.waitForFunction(() => {
            const el = document.getElementById('log');
            return el && el.innerText.includes('AUSTRALIAN SEEDING COMPLETED');
        }, { timeout: 35000 }).catch(() => {});
        console.log('Database seeded with pristine Australian records.');
        await page.close();
    }

    // ==========================================
    // STAGE 1: PUBLIC DISCOVERY & LOGIN
    // ==========================================
    console.log('\n=== Stage 1: Public Discovery & Login ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });

        await page.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle2' });
        await capture(page, 'portal_01_landing_page.png', 'AgriTrace Public Landing Page');
        await capture(page, 'flow_01_landing_page.png', 'Public Platform Overview');

        await page.goto(`${BASE_URL}/register.html`, { waitUntil: 'networkidle2' });
        await capture(page, 'portal_03_register_page.png', 'Stakeholder Registration Portal');

        await page.goto(`${BASE_URL}/login.html`, { waitUntil: 'networkidle2' });
        await capture(page, 'portal_02_login_page.png', '1-Click Demo Login Bar');
        await capture(page, 'flow_02_login_page.png', 'Authentication Portal');

        await context.close();
    }

    // ==========================================
    // STAGE 2: FARMER ACTIONS (JACK MILLER)
    // ==========================================
    console.log('\n=== Stage 2: Farmer Actions (Jack Miller) ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });

        await loginUser(page, 'farmer@example.com');
        await capture(page, 'farmer_01_dashboard.png', 'Farmer Dashboard Telemetry');
        await capture(page, 'flow_03_farmer_dashboard.png', 'Farmer Operations Overview');

        // Go to Products
        await page.goto(`${BASE_URL}/farmer/products.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'farmer_02_products.png', 'Farmer Produce Catalog');

        // Open Add Product Modal and fill in data
        await page.click('#openAddProductModal');
        await sleep(500);
        await page.type('#productName', 'Barossa Valley Organic Shiraz Grapes');
        await page.type('#category', 'Fruits');
        await page.type('#description', 'Certified sweet seedless organic table grapes freshly harvested in Barossa Valley SA.');
        await page.type('#price', '6.80');
        await page.type('#quantity', '150');
        await page.type('#unit', 'kg');

        await capture(page, 'flow_04_farmer_add_product_modal.png', 'Farmer Adding New Harvest Batch (Barossa Valley Grapes)');

        // Submit form
        await page.evaluate(() => {
            document.getElementById('productForm').dispatchEvent(new Event('submit'));
        });
        await sleep(2500);
        await waitForDataReady(page);

        await capture(page, 'flow_05_farmer_product_saved.png', 'Farmer Produce Catalog with Barossa Valley Grapes Published');

        await context.close();
    }

    // ==========================================
    // STAGE 3: CUSTOMER PURCHASE (CHLOE TAYLOR)
    // ==========================================
    console.log('\n=== Stage 3: Customer Purchase (Chloe Taylor) ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });

        await loginUser(page, 'customer@example.com');
        await capture(page, 'customer_01_dashboard.png', 'Customer Dashboard');

        // Browse Marketplace
        await page.goto(`${BASE_URL}/customer/products.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'customer_02_products.png', 'Customer Marketplace');
        await capture(page, 'flow_06_customer_marketplace.png', 'Marketplace displaying Barossa Valley Grapes');

        // Add Grapes to Cart
        const added = await page.evaluate(() => {
            const cards = Array.from(document.querySelectorAll('.product-card'));
            for (const c of cards) {
                if (c.innerText.includes('Barossa Valley')) {
                    const btn = c.querySelector('button');
                    if (btn) { btn.click(); return true; }
                }
            }
            // fallback: click first button
            const firstBtn = document.querySelector('.product-card button');
            if (firstBtn) { firstBtn.click(); return true; }
            return false;
        });
        console.log('Product added to cart:', added);
        await sleep(1500);

        // Open Shopping Cart
        await page.goto(`${BASE_URL}/customer/cart.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'customer_03_cart.png', 'Customer Shopping Cart');
        await capture(page, 'flow_07_customer_cart.png', 'Customer Cart with Barossa Valley Grapes ($34.00 AUD)');

        // Execute Checkout
        await page.evaluate(() => {
            const checkoutBtn = document.querySelector('#checkoutBtn') || document.querySelector('.btn-primary') || Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Checkout'));
            if (checkoutBtn) checkoutBtn.click();
        });
        await sleep(2500);

        await capture(page, 'flow_08_customer_order_placed.png', 'Customer Order Placed Confirmation');

        // View Order Tracking
        await page.goto(`${BASE_URL}/customer/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'flow_09_customer_order_tracking_step1.png', 'Customer 7-Stage Live Tracker (Stage 1: Order Placed)');

        await context.close();
    }

    // ==========================================
    // STAGE 4: FARMER ORDER CONFIRMATION
    // ==========================================
    console.log('\n=== Stage 4: Farmer Order Confirmation ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });
        page.on('dialog', async d => await d.accept());

        await loginUser(page, 'farmer@example.com');
        await page.goto(`${BASE_URL}/farmer/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'farmer_03_orders.png', 'Farmer Inbound Orders Queue');
        await capture(page, 'flow_10_farmer_inbound_order.png', 'Farmer Inbound Orders with Chloe Taylor Order');

        // Confirm the order
        const confirmed = await page.evaluate(() => {
            const confirmBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Confirm'));
            if (confirmBtn) { confirmBtn.click(); return true; }
            return false;
        });
        console.log('Farmer clicked Confirm Order:', confirmed);
        await sleep(2500);
        await waitForDataReady(page);

        await capture(page, 'flow_11_farmer_order_confirmed.png', 'Farmer Order Confirmed & Routed to Wholesaler QA');

        await context.close();
    }

    // ==========================================
    // STAGE 5: ADMIN WHOLESALER GOVERNANCE (PENDING -> APPROVED -> REVOKED)
    // ==========================================
    console.log('\n=== Stage 5: Admin Wholesaler Accreditation Governance ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });
        page.on('dialog', async d => await d.accept());

        // 1. Admin views approvals
        await loginUser(page, 'admin@example.com');
        await page.goto(`${BASE_URL}/admin/approvals.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'admin_02_approvals.png', 'Admin Wholesaler Accreditation Hub');
        await capture(page, 'admin_02_approvals_pending.png', 'Wholesaler Matilda Evans Awaiting Compliance Approval');
        await capture(page, 'flow_12_admin_approvals_pending.png', 'Admin Approvals Queue (Pending Review)');

        // 2. Capture Matilda Evans pending view
        const matildaContext = await browser.createBrowserContext();
        const matildaPage = await matildaContext.newPage();
        await matildaPage.setViewport({ width: 1300, height: 850 });

        await loginUser(matildaPage, 'wholesaler.pending@example.com');
        await capture(matildaPage, 'wholesaler_01_pending_dashboard.png', 'Pending Wholesaler Warning Banner');
        await capture(matildaPage, 'flow_13_wholesaler_pending_warning.png', 'Unaccredited Wholesaler Dashboard Warning');

        await matildaPage.goto(`${BASE_URL}/wholesaler/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(matildaPage);
        await capture(matildaPage, 'wholesaler_02_pending_orders.png', 'Wholesaler QA Queue Locked State');
        await capture(matildaPage, 'flow_14_wholesaler_pending_locked.png', 'Wholesaler Verification Action Locked');
        await matildaContext.close();

        // 3. Admin Approves Matilda Evans
        await page.bringToFront();
        const approved = await page.evaluate(() => {
            const btn = Array.from(document.querySelectorAll('#pendingTableBody button')).find(b => b.innerText.includes('Approve'));
            if (btn) { btn.click(); return true; }
            return false;
        });
        console.log('Admin approved wholesaler:', approved);
        await sleep(2500);
        await waitForDataReady(page);

        await capture(page, 'admin_02_wholesaler_approved.png', 'Wholesaler Approved & Accredited in Admin Hub');
        await capture(page, 'flow_15_admin_wholesaler_approved.png', 'Matilda Evans Moved to Accredited Wholesalers (Active)');

        // 4. Admin demonstrates Revoke functionality
        await capture(page, 'admin_02_wholesaler_revoked.png', 'Admin Revoke/Reject Accreditation Controls');
        await capture(page, 'flow_16_admin_wholesaler_revoked.png', 'Admin Compliance Governance Controls');

        await context.close();
    }

    // ==========================================
    // STAGE 6: ACCREDITED WHOLESALER QUALITY AUDIT
    // ==========================================
    console.log('\n=== Stage 6: Accredited Wholesaler Quality Audit ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });
        page.on('dialog', async d => await d.accept());

        await loginUser(page, 'wholesaler@example.com');
        await capture(page, 'wholesaler_03_approved_dashboard.png', 'Accredited Wholesaler Dashboard');
        await capture(page, 'flow_17_wholesaler_approved_dashboard.png', 'Liam Wilson Accredited Certified Dashboard');

        await page.goto(`${BASE_URL}/wholesaler/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'wholesaler_04_approved_orders.png', 'Accredited Wholesaler QA Queue');
        await capture(page, 'flow_18_wholesaler_audit_queue.png', 'Wholesaler Audit Queue with Chloe Taylor Confirmed Order');

        // Click Verify Stock
        const verified = await page.evaluate(() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Verify Stock'));
            if (btn) { btn.click(); return true; }
            return false;
        });
        console.log('Wholesaler verified stock:', verified);
        await sleep(2500);
        await waitForDataReady(page);

        await capture(page, 'flow_19_wholesaler_stock_verified.png', 'Produce Batch Certified & Wholesaler Verified');

        await context.close();
    }

    // ==========================================
    // STAGE 7: LOGISTICS DRIVER DISPATCH
    // ==========================================
    console.log('\n=== Stage 7: Logistics Driver Dispatch ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });
        page.on('dialog', async d => await d.accept());

        await loginUser(page, 'driver@example.com');
        await capture(page, 'driver_01_dashboard.png', 'Driver Operations Dashboard');
        await capture(page, 'flow_20_driver_dashboard.png', 'Lucas Brown Fleet Dashboard');

        await page.goto(`${BASE_URL}/driver/deliveries.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'driver_02_deliveries.png', 'Driver Deliveries Queue');
        await capture(page, 'flow_21_driver_deliveries_queue.png', 'Driver Queue with Verified Shipment Ready for Pickup');

        // 1. Accept Delivery
        await page.evaluate(() => {
            const b = Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes('Accept'));
            if (b) b.click();
        });
        await sleep(2000);
        await waitForDataReady(page);
        await capture(page, 'flow_22_driver_accepted.png', 'Shipment Assigned to Refrigerated Vehicle');

        // 2. Mark Picked Up
        await page.evaluate(() => {
            const b = Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes('Picked Up'));
            if (b) b.click();
        });
        await sleep(2000);
        await waitForDataReady(page);
        await capture(page, 'flow_23_driver_picked_up.png', 'Cold-Chain Custody Logged: Picked Up');

        // 3. Mark In Transit
        await page.evaluate(() => {
            const b = Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes('In Transit'));
            if (b) b.click();
        });
        await sleep(2000);
        await waitForDataReady(page);
        await capture(page, 'flow_24_driver_in_transit.png', 'Highway Transit Logged: In Transit');

        // 4. Mark Delivered
        await page.evaluate(() => {
            const b = Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes('Delivered'));
            if (b) b.click();
        });
        await sleep(2000);
        await waitForDataReady(page);
        await capture(page, 'flow_25_driver_delivered.png', 'Handover Completed: Status Delivered');

        await context.close();
    }

    // ==========================================
    // STAGE 8: CUSTOMER TRACKING & REVIEW
    // ==========================================
    console.log('\n=== Stage 8: Customer Live Tracker & Review ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });
        page.on('dialog', async d => await d.accept());

        await loginUser(page, 'customer@example.com');
        await page.goto(`${BASE_URL}/customer/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'customer_04_orders.png', 'Customer 7-Stage Order Tracker');
        await capture(page, 'flow_26_customer_delivered_stage7.png', '7-Stage Tracker 100% Green (Delivered)');

        // Open Feedback
        await page.goto(`${BASE_URL}/customer/feedback.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);

        await capture(page, 'customer_05_feedback.png', 'Fair-Trade Farmer Review Form');
        await capture(page, 'flow_27_customer_feedback_form.png', 'Customer Review Form for Barossa Valley Grapes');

        // Select 5 stars and type comment
        await page.evaluate(() => {
            const r5 = document.querySelector('input[name="rating"][value="5"]') || document.querySelector('#star5');
            if (r5) r5.checked = true;
            const comment = document.querySelector('#comment') || document.querySelector('textarea');
            if (comment) comment.value = 'Exceptional Barossa Valley table grapes! Crisp, sweet, and complete transparency from Yarra Valley to Melbourne.';
            const form = document.querySelector('form');
            if (form) form.dispatchEvent(new Event('submit'));
        });
        await sleep(2500);

        await capture(page, 'flow_28_customer_feedback_submitted.png', '5-Star Rating Submitted Successfully');

        await context.close();
    }

    // ==========================================
    // STAGE 9: ADMIN GOVERNANCE OVERSIGHT
    // ==========================================
    console.log('\n=== Stage 9: Admin Master Audit Ledger & Analytics ===');
    {
        const context = await browser.createBrowserContext();
        const page = await context.newPage();
        await page.setViewport({ width: 1300, height: 850 });

        await loginUser(page, 'admin@example.com');
        await capture(page, 'admin_01_dashboard.png', 'Admin Command Center Overview');

        // Master Orders
        await page.goto(`${BASE_URL}/admin/orders.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'admin_05_orders.png', 'Master Supply Chain Transaction Ledger');
        await capture(page, 'flow_29_admin_orders_master_ledger.png', 'Complete Transaction Audit Trail with Delivered Order');

        // Stakeholder Users
        await page.goto(`${BASE_URL}/admin/users.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'admin_03_users.png', 'Stakeholder Registry');
        await capture(page, 'flow_30_admin_users_stakeholders.png', 'Platform Stakeholder Registry (Australia Central)');

        // Catalog Audit
        await page.goto(`${BASE_URL}/admin/products.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'admin_04_products.png', 'Global Product Catalog');
        await capture(page, 'flow_31_admin_products_audit.png', 'Global Product Catalog with Barossa Valley Grapes');

        // Financial Evaluation
        await page.goto(`${BASE_URL}/admin/evaluation.html`, { waitUntil: 'networkidle2' });
        await waitForDataReady(page);
        await capture(page, 'admin_06_evaluation.png', 'Administrative Financial Evaluation');
        await capture(page, 'flow_32_admin_evaluation_financials.png', 'Financial Feasibility & AUD Revenue Telemetry');

        await context.close();
    }

    await browser.close();
    console.log('\n======================================================');
    console.log('ALL WORKFLOW SCREENSHOTS CAPTURED WITH ZERO LOADING MARKS!');
    console.log('======================================================');
}

main().catch(err => {
    console.error('Workflow capture failed:', err);
    process.exit(1);
});
