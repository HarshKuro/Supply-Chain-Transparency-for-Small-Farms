const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://localhost:8000';
const SCREENSHOT_DIR = path.join(__dirname, '..', 'screenshots');
const DOCX_IMG_DIR = path.join(__dirname, '..', 'docx', 'images');

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

async function run() {
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new',
        args: ['--no-sandbox', '--disable-gpu']
    });

    const context = await browser.createBrowserContext();
    const page = await context.newPage();
    await page.setViewport({ width: 1300, height: 850 });

    // 1. Capture public evaluation-report.html
    console.log('Capturing public evaluation-report.html...');
    await page.goto(`${BASE_URL}/evaluation-report.html`, { waitUntil: 'networkidle2' });
    await sleep(1500);
    await capture(page, '14_browser_evaluation_report.png', 'Public Evaluation Report Page');

    // 2. Authenticate as admin
    console.log('Authenticating as admin...');
    await page.goto(`${BASE_URL}/login.html`, { waitUntil: 'networkidle2' });
    await page.click('.demo-btn[data-email="admin@example.com"]');
    for (let i = 0; i < 12; i++) {
        await sleep(600);
        if (!page.url().includes('login.html')) break;
    }
    await sleep(1500);

    // 3. Capture admin/evaluation.html
    console.log('Capturing admin/evaluation.html...');
    await page.goto(`${BASE_URL}/admin/evaluation.html`, { waitUntil: 'networkidle2' });
    await sleep(2000);
    await capture(page, '17_browser_admin_financial_eval.png', 'Admin Financial Feasibility Dashboard');
    await capture(page, 'admin_06_evaluation.png', 'Admin Evaluation Portal Overview');
    await capture(page, 'flow_32_admin_evaluation_financials.png', 'Admin Evaluation Telemetry Flow');

    await browser.close();
    console.log('Evaluation screenshots refreshed successfully!');
}

run().catch(err => {
    console.error('Capture error:', err);
    process.exit(1);
});
