const puppeteer = require('puppeteer-core');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function runSeed() {
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new'
    });
    const page = await browser.newPage();
    page.on('console', msg => console.log('LOG:', msg.text()));

    console.log('Navigating to seed.html...');
    await page.goto('http://localhost:8000/seed.html', { waitUntil: 'networkidle2' });
    
    // Wait for the seed completion message
    console.log('Waiting for seed process...');
    try {
        await page.waitForFunction(() => {
            const el = document.getElementById('log');
            return el && el.innerText.includes('AUSTRALIAN SEEDING COMPLETED');
        }, { timeout: 30000 });
        console.log('SEED COMPLETED SUCCESSFULLY!');
    } catch (e) {
        console.log('Wait timeout or error:', e.message);
        const logContent = await page.$eval('#log', el => el.innerText).catch(() => 'no log');
        console.log('Current log contents:\n', logContent);
    }

    await browser.close();
}

runSeed().catch(console.error);
