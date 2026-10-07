const puppeteer = require('puppeteer-core');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function checkPageLoaders() {
    const browser = await puppeteer.launch({ executablePath: CHROME_PATH, headless: 'new' });
    const page = await browser.newPage();

    // Check login page
    await page.goto('http://localhost:8000/login.html');
    await page.click('.demo-btn[data-email="farmer@example.com"]');
    await new Promise(r => setTimeout(r, 1000));
    
    // Check farmer dashboard
    const info = await page.evaluate(() => {
        const loader = document.getElementById('loader');
        const spinner = document.querySelector('.spinner');
        const loadingTexts = Array.from(document.querySelectorAll('*'))
            .filter(el => el.children.length === 0 && el.innerText && el.innerText.toLowerCase().includes('loading'))
            .map(el => `${el.tagName}#${el.id || el.className}: "${el.innerText}"`);
        return {
            url: window.location.href,
            loaderDisplay: loader ? window.getComputedStyle(loader).display : null,
            spinnerFound: !!spinner,
            loadingTexts
        };
    });
    console.log('Farmer dashboard inspection:', JSON.stringify(info, null, 2));

    await browser.close();
}

checkPageLoaders().catch(console.error);
