const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://localhost:8000';
const DOCX_IMG_DIR = path.join(__dirname, '..', 'docx', 'images');
const SCREENSHOT_DIR = path.join(__dirname, '..', 'screenshots');

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function capture(page, filename, desc) {
    const p1 = path.join(SCREENSHOT_DIR, filename);
    const p2 = path.join(DOCX_IMG_DIR, filename);
    await page.screenshot({ path: p1, fullPage: false });
    fs.copyFileSync(p1, p2);
    console.log(`[OK] Captured: ${filename} - ${desc} (Size: ${fs.statSync(p1).size} bytes, URL: ${page.url()})`);
}

async function captureRole(browser, email, steps) {
    console.log(`\n=== Capturing role: ${email} ===`);
    const context = await browser.createBrowserContext();
    const page = await context.newPage();
    await page.setViewport({ width: 1300, height: 850 });

    await page.goto(`${BASE_URL}/login.html`, { waitUntil: 'networkidle2' });
    await page.click(`.demo-btn[data-email="${email}"]`);
    
    // Wait for the URL to change from login.html
    await page.waitForFunction(() => !window.location.href.includes('login.html'), { timeout: 10000 });
    console.log('Navigated successfully to:', page.url());
    await sleep(2500); // allow data hydration

    for (const step of steps) {
        if (page.url() !== `${BASE_URL}${step.url}`) {
            await page.goto(`${BASE_URL}${step.url}`, { waitUntil: 'networkidle2' });
            await sleep(2500);
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

    // Driver
    await captureRole(browser, 'driver@example.com', [
        { url: '/driver/dashboard.html', filename: 'driver_01_dashboard.png', desc: 'Driver Dashboard' },
        { url: '/driver/deliveries.html', filename: 'driver_02_deliveries.png', desc: 'Driver Transit Deliveries' }
    ]);

    // Customer
    await captureRole(browser, 'customer@example.com', [
        { url: '/customer/dashboard.html', filename: 'customer_01_dashboard.png', desc: 'Customer Account Dashboard' },
        { url: '/customer/products.html', filename: 'customer_02_products.png', desc: 'Fresh Australian Produce Marketplace' },
        { url: '/customer/cart.html', filename: 'customer_03_cart.png', desc: 'Shopping Cart & Transparent Checkout' },
        { url: '/customer/orders.html', filename: 'customer_04_orders.png', desc: '7-Stage Real-Time Custody Tracker' },
        { url: '/customer/feedback.html', filename: 'customer_05_feedback.png', desc: 'Farmer Quality Rating & Review Submission' }
    ]);

    await browser.close();
    console.log('Done capturing driver and customer!');
}

main().catch(console.error);
