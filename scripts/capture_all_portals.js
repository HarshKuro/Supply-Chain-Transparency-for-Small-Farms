const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://localhost:8000';
const SCREENSHOT_DIR = path.join(__dirname, '..', 'screenshots');
const DOCX_IMG_DIR = path.join(__dirname, '..', 'docx', 'images');

if (!fs.existsSync(SCREENSHOT_DIR)) fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
if (!fs.existsSync(DOCX_IMG_DIR)) fs.mkdirSync(DOCX_IMG_DIR, { recursive: true });

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function capture(page, filename, desc) {
    const p1 = path.join(SCREENSHOT_DIR, filename);
    const p2 = path.join(DOCX_IMG_DIR, filename);
    await page.screenshot({ path: p1, fullPage: false });
    fs.copyFileSync(p1, p2);
    console.log(`[OK] Captured: ${filename} - ${desc} (Size: ${fs.statSync(p1).size} bytes)`);
}

async function runSession(browser, email, steps) {
    const context = await browser.createBrowserContext();
    const page = await context.newPage();
    await page.setViewport({ width: 1300, height: 850 });

    if (email) {
        console.log(`\n--- Authenticating as: ${email} ---`);
        await page.goto(`${BASE_URL}/login.html`, { waitUntil: 'networkidle2' });
        await page.click(`.demo-btn[data-email="${email}"]`);
        // Wait for redirect to happen
        for (let i = 0; i < 12; i++) {
            await sleep(800);
            if (!page.url().includes('login.html')) break;
        }
        await sleep(1500); // allow data rendering
    }

    for (const step of steps) {
        if (step.url) {
            await page.goto(`${BASE_URL}${step.url}`, { waitUntil: 'networkidle2' });
            await sleep(2200); // allow Firestore queries & table hydration
        }
        await capture(page, step.filename, step.desc);
    }

    await context.close();
}

async function main() {
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new',
        args: ['--no-sandbox', '--disable-gpu']
    });

    // 1. Public Pages
    console.log('=== Capturing Public Pages ===');
    await runSession(browser, null, [
        { url: '/index.html', filename: 'portal_01_landing_page.png', desc: 'Public Hero Landing Page' },
        { url: '/login.html', filename: 'portal_02_login_page.png', desc: 'Authentication Login Portal with 1-Click Demo Bar' },
        { url: '/register.html', filename: 'portal_03_register_page.png', desc: 'User Registration Portal' }
    ]);

    // 2. Farmer Portal
    console.log('=== Capturing Farmer Portal ===');
    await runSession(browser, 'farmer@example.com', [
        { url: '/farmer/dashboard.html', filename: 'farmer_01_dashboard.png', desc: 'Farmer Operations Telemetry' },
        { url: '/farmer/products.html', filename: 'farmer_02_products.png', desc: 'Produce Batch Catalog & AUD Prices' },
        { url: '/farmer/orders.html', filename: 'farmer_03_orders.png', desc: 'Inbound Orders & Fulfillment Confirmation' }
    ]);

    // 3. Wholesaler Pending
    console.log('=== Capturing Pending Wholesaler Portal ===');
    await runSession(browser, 'wholesaler.pending@example.com', [
        { url: '/wholesaler/dashboard.html', filename: 'wholesaler_01_pending_dashboard.png', desc: 'Wholesaler Unaccredited Warning Banner' },
        { url: '/wholesaler/orders.html', filename: 'wholesaler_02_pending_orders.png', desc: 'Wholesaler QA Queue Locked State' }
    ]);

    // 4. Wholesaler Approved
    console.log('=== Capturing Accredited Wholesaler Portal ===');
    await runSession(browser, 'wholesaler@example.com', [
        { url: '/wholesaler/dashboard.html', filename: 'wholesaler_03_approved_dashboard.png', desc: 'Accredited Wholesaler Dashboard' },
        { url: '/wholesaler/orders.html', filename: 'wholesaler_04_approved_orders.png', desc: 'Active Stock Verification QA Queue' }
    ]);

    // 5. Driver Portal
    console.log('=== Capturing Logistics Driver Portal ===');
    await runSession(browser, 'driver@example.com', [
        { url: '/driver/dashboard.html', filename: 'driver_01_dashboard.png', desc: 'Logistics Driver Fleet Dashboard' },
        { url: '/driver/deliveries.html', filename: 'driver_02_deliveries.png', desc: 'Driver Transit Checkpoint Controls' }
    ]);

    // 6. Customer Portal
    console.log('=== Capturing Customer Portal ===');
    await runSession(browser, 'customer@example.com', [
        { url: '/customer/dashboard.html', filename: 'customer_01_dashboard.png', desc: 'Customer Account & Activity Summary' },
        { url: '/customer/products.html', filename: 'customer_02_products.png', desc: 'Fresh Australian Produce Marketplace' },
        { url: '/customer/cart.html', filename: 'customer_03_cart.png', desc: 'Shopping Cart & Transparent Checkout' },
        { url: '/customer/orders.html', filename: 'customer_04_orders.png', desc: '7-Stage Real-Time Custody Tracker' },
        { url: '/customer/feedback.html', filename: 'customer_05_feedback.png', desc: 'Farmer Quality Rating & Review Submission' }
    ]);

    // 7. Admin Portal
    console.log('=== Capturing Admin Governance Portal ===');
    await runSession(browser, 'admin@example.com', [
        { url: '/admin/dashboard.html', filename: 'admin_01_dashboard.png', desc: 'Admin Command Center & Telemetry' },
        { url: '/admin/approvals.html', filename: 'admin_02_approvals.png', desc: 'Wholesaler Accreditation Management' },
        { url: '/admin/users.html', filename: 'admin_03_users.png', desc: 'Global Stakeholder User Registry' },
        { url: '/admin/products.html', filename: 'admin_04_products.png', desc: 'Global Catalog & Biosecurity Audit' },
        { url: '/admin/orders.html', filename: 'admin_05_orders.png', desc: 'Master Transaction Audit Ledger' },
        { url: '/admin/evaluation.html', filename: 'admin_06_evaluation.png', desc: 'Commercial Expense & Revenue Telemetry' }
    ]);

    await browser.close();
    console.log('\n========================================');
    console.log('ALL 23 REAL SCREENSHOTS CAPTURED WITH ISOLATED CONTEXTS!');
    console.log('========================================');
}

main().catch(err => {
    console.error('Fatal capture error:', err);
    process.exit(1);
});
