# Supply Chain Transparency for Small Farms | AgriTrace
**Enhancing Fair Trade Through Digital Traceability & Transparent Custody**

## Project Overview
AgriTrace is a modern, responsive web application connecting Australian small family farms, accredited wholesalers, cold-chain transport drivers, and consumers through a transparent, auditable digital workflow. The platform eliminates predatory supermarket duopoly markups (+36% farmer margin gain) while enforcing strict regulatory accreditation and quality auditing.

## Key Stakeholder Portals & Features
- **🌾 Farmer Portal (`farmer/`):** List fresh Australian harvests with AUD pricing, manage inventory, and confirm incoming orders.
- **🏢 Wholesaler Portal (`wholesaler/`):** Quality audit and stock verification. *Requires Administrator accreditation approval before auditing farm batches.*
- **🚚 Logistics Driver Portal (`driver/`):** Cold-chain distribution, pickup confirmation, transit checkpoint updates, and proof-of-delivery handover.
- **🛒 Customer Marketplace (`customer/`):** Browse fresh regional Australian produce, fair trade checkout in AUD, 7-stage live order transparency tracking, and direct farmer reviews.
- **🛡️ Administrator Governance (`admin/`):** Macro-oversight of platform transactions in AUD, user management, and dedicated **Wholesaler Approvals Hub (`admin/approvals.html`)**.

## Integrated Documentation & Manuals
- **🗺️ Site Map (`sitemap.html`):** Complete navigable directory of all public pages, stakeholder portals, and tools.
- **📖 User Manual (`user-manual.html`):** Comprehensive role-by-role guide for all 5 stakeholders with step-by-step instructions.
- **💻 Installation Manual (`installation-manual.html`):** Technical guide for Firebase project creation, Firestore security rules deployment, and local hosting.
- **📊 Evaluation Report (`evaluation-report.html` & `admin/evaluation.html`):** In-depth financial evaluation detailing development CAPEX ($18,900 AUD), recurring cloud OPEX ($280 AUD/mo), gross revenue ($1,027 AUD/mo), and small farm ROI (+95.5% net margin gain, +$10,320 AUD/yr).

## Quick Demo Credentials (Password: `password123`)
- **Admin:** `admin@example.com` (AgriTrace Administrator, Canberra ACT)
- **Farmer:** `farmer@example.com` (Jack Miller, Yarra Valley Harvests VIC)
- **Wholesaler (Approved):** `wholesaler@example.com` (Liam Wilson, Sydney Central Markets NSW)
- **Wholesaler (Pending Approval):** `wholesaler.pending@example.com` (Matilda Evans, Melbourne Produce Hub VIC)
- **Driver:** `driver@example.com` (Lucas Brown, Outback Cold Logistics)
- **Customer:** `customer@example.com` (Chloe Taylor, Melbourne VIC)

## Running Locally
1. Run `run.bat` (automatically detects Python or Node.js HTTP server), or:
2. Run `python -m http.server 8000`, or `npx http-server -p 8000`, or VS Code Live Server.
3. Open `http://localhost:8000/` in your browser.
4. To initialize or refresh Australian demo data, visit `http://localhost:8000/seed.html`.
5. To execute the automated 22-test integration suite, visit `http://localhost:8000/test_runner.html`.
