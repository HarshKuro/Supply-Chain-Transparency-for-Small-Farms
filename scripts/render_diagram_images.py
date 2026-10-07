import os
import subprocess

BASE_DIR = r"c:\Users\harsh\OneDrive\Documents\Pritam-projects\Supply Chain Transparency for Small Farms"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DIAGRAMS_HTML_DIR = os.path.join(BASE_DIR, "assets", "diagrams")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(DIAGRAMS_HTML_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# 1. Sitemap Hierarchy Diagram HTML
HTML_SITEMAP = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0B132B; color: #FFFFFF; padding: 35px; width: 1350px; height: 850px; overflow: hidden; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h1 { font-size: 26px; font-weight: 800; color: #48E5C2; letter-spacing: -0.5px; margin-bottom: 5px; }
  .title-bar p { font-size: 14px; color: #94A3B8; }
  
  .root-node {
    background: linear-gradient(135deg, #1B4D20, #2E7D32);
    border: 2px solid #4ADE80;
    border-radius: 14px;
    padding: 14px 28px;
    width: 440px;
    margin: 0 auto 20px auto;
    text-align: center;
    box-shadow: 0 10px 25px rgba(46, 125, 50, 0.4);
  }
  .root-node h2 { font-size: 18px; font-weight: 700; color: #FFF; }
  .root-node span { font-size: 12px; color: #D1FAE5; }

  .connector-v { width: 3px; height: 18px; background: #64748B; margin: 0 auto; }
  .connector-h-bar { width: 1120px; height: 3px; background: #64748B; margin: 0 auto 18px auto; position: relative; }
  
  .portal-row {
    display: flex;
    justify-content: space-between;
    width: 1280px;
    margin: 0 auto;
    gap: 16px;
  }
  .portal-card {
    flex: 1;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    position: relative;
  }
  .portal-card.farmer { border-top: 4px solid #10B981; }
  .portal-card.wholesaler { border-top: 4px solid #F59E0B; }
  .portal-card.driver { border-top: 4px solid #3B82F6; }
  .portal-card.customer { border-top: 4px solid #8B5CF6; }
  .portal-card.admin { border-top: 4px solid #EF4444; }

  .portal-card h3 { font-size: 15px; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
  .portal-card .role-badge { display: inline-block; font-size: 10px; font-weight: 700; text-transform: uppercase; padding: 2px 7px; border-radius: 6px; margin-bottom: 12px; }
  .farmer .role-badge { background: rgba(16, 185, 129, 0.2); color: #34D399; }
  .wholesaler .role-badge { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
  .driver .role-badge { background: rgba(59, 130, 246, 0.2); color: #60A5FA; }
  .customer .role-badge { background: rgba(139, 92, 246, 0.2); color: #A78BFA; }
  .admin .role-badge { background: rgba(239, 68, 68, 0.2); color: #F87171; }

  .sub-pages { list-style: none; }
  .sub-pages li {
    background: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 6px;
    font-size: 11px;
    color: #E2E8F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .sub-pages li .url { font-family: monospace; color: #94A3B8; font-size: 10px; }
  .sub-pages li.warn { border-color: #F59E0B; color: #FDE68A; }

  .bottom-docs-bar {
    margin-top: 22px;
    background: #111827;
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 12px 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  .doc-pill {
    background: #1F2937;
    border: 1px solid #4B5563;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    color: #6EE7B7;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="title-bar">
    <h1>AGRITRACE AUSTRALIA — INTERACTIVE SYSTEM SITEMAP</h1>
    <p>Complete Hierarchical Navigation Taxonomy & Stakeholder Domain Routing Structure</p>
  </div>

  <div class="root-node">
    <h2>🏠 index.html (Storefront & Discovery Hub)</h2>
    <span>Public Landing • Australian Fair Trade Overview • Direct Portals Access</span>
  </div>

  <div class="connector-v"></div>
  <div class="connector-h-bar"></div>

  <div class="portal-row">
    <!-- Farmer -->
    <div class="portal-card farmer">
      <h3>🌾 Farmer Portal</h3>
      <div class="role-badge">Role: farmer</div>
      <ul class="sub-pages">
        <li><span>Dashboard</span><span class="url">dashboard.html</span></li>
        <li><span>Produce Batches</span><span class="url">products.html</span></li>
        <li><span>Incoming Orders</span><span class="url">orders.html</span></li>
      </ul>
    </div>

    <!-- Wholesaler -->
    <div class="portal-card wholesaler">
      <h3>🏢 Wholesaler Hub</h3>
      <div class="role-badge">Role: wholesaler</div>
      <ul class="sub-pages">
        <li><span>Dashboard</span><span class="url">dashboard.html</span></li>
        <li class="warn"><span>Stock Verification*</span><span class="url">orders.html</span></li>
        <li style="border:none; background:none; font-size:9.5px; color:#F59E0B; padding:2px;">*Locked until Accredited by Admin</li>
      </ul>
    </div>

    <!-- Driver -->
    <div class="portal-card driver">
      <h3>🚚 Logistics Driver</h3>
      <div class="role-badge">Role: driver</div>
      <ul class="sub-pages">
        <li><span>Driver Dashboard</span><span class="url">dashboard.html</span></li>
        <li><span>Transit Deliveries</span><span class="url">deliveries.html</span></li>
        <li><span>Cold-Chain Handover</span><span class="url">Live GPS</span></li>
      </ul>
    </div>

    <!-- Customer -->
    <div class="portal-card customer">
      <h3>🛒 Consumer Store</h3>
      <div class="role-badge">Role: customer</div>
      <ul class="sub-pages">
        <li><span>Fresh Catalog</span><span class="url">products.html</span></li>
        <li><span>Shopping Cart</span><span class="url">cart.html</span></li>
        <li><span>7-Stage Tracking</span><span class="url">orders.html</span></li>
        <li><span>Farmer Reviews</span><span class="url">feedback.html</span></li>
      </ul>
    </div>

    <!-- Admin -->
    <div class="portal-card admin">
      <h3>🛡️ Administrator</h3>
      <div class="role-badge">Role: admin</div>
      <ul class="sub-pages">
        <li><span>Operations Hub</span><span class="url">dashboard.html</span></li>
        <li style="border-color:#EF4444; color:#FCA5A5;"><span>Wholesaler Approvals</span><span class="url">approvals.html</span></li>
        <li><span>User Registry</span><span class="url">users.html</span></li>
        <li><span>Catalog & Orders</span><span class="url">products/orders</span></li>
        <li><span>Financial Eval</span><span class="url">evaluation.html</span></li>
      </ul>
    </div>
  </div>

  <div class="bottom-docs-bar">
    <span style="font-size:12px; font-weight:700; color:#9CA3AF;">SHARED PLATFORM DOCUMENTATION & UTILITIES:</span>
    <div class="doc-pill">📖 user-manual.html</div>
    <div class="doc-pill">💻 installation-manual.html</div>
    <div class="doc-pill">📊 evaluation-report.html</div>
    <div class="doc-pill">🇦🇺 seed.html (Australian DB)</div>
    <div class="doc-pill">🧪 test_runner.html (31 Tests)</div>
  </div>
</body>
</html>
"""

# 2. Custody Workflow Diagram HTML
HTML_CUSTODY = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0F172A; color: #FFFFFF; padding: 35px 25px; width: 1350px; height: 800px; overflow: hidden; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h1 { font-size: 26px; font-weight: 800; color: #38BDF8; letter-spacing: -0.5px; margin-bottom: 5px; }
  .title-bar p { font-size: 14px; color: #94A3B8; }

  .flow-track {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 30px;
    gap: 12px;
  }
  .step-node {
    flex: 1;
    background: #1E293B;
    border: 2px solid #334155;
    border-radius: 12px;
    padding: 16px 12px;
    text-align: center;
    position: relative;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
  }
  .step-node .step-num {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: #0284C7;
    color: #FFF;
    font-size: 11px;
    font-weight: 800;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #0F172A;
  }
  .step-node .icon { font-size: 26px; margin: 6px 0 4px 0; }
  .step-node h4 { font-size: 13px; font-weight: 700; color: #F1F5F9; margin-bottom: 4px; }
  .step-node p { font-size: 10px; color: #94A3B8; line-height: 1.35; }
  .step-node .role-tag {
    display: inline-block;
    margin-top: 8px;
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    background: #334155;
    color: #CBD5E1;
  }

  .arrow-node {
    font-size: 18px;
    color: #38BDF8;
    font-weight: bold;
  }

  .gov-panel {
    margin-top: 40px;
    background: linear-gradient(135deg, #1E1B4B, #0F172A);
    border: 2px dashed #6366F1;
    border-radius: 12px;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .gov-panel h3 { font-size: 16px; color: #A5B4FC; margin-bottom: 4px; }
  .gov-panel p { font-size: 12px; color: #CBD5E1; }
  .gov-pills { display: flex; gap: 10px; }
  .gov-pill { background: #312E81; border: 1px solid #4F46E5; color: #E0E7FF; font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 6px; }
</style>
</head>
<body>
  <div class="title-bar">
    <h1>END-TO-END SUPPLY CHAIN TRANSPARENCY & CUSTODY FLOW</h1>
    <p>7-Stage Digital Custody Verification Sequence Connecting Australian Growers to Consumers</p>
  </div>

  <div class="flow-track">
    <!-- Step 1 -->
    <div class="step-node" style="border-color: #10B981;">
      <div class="step-num" style="background:#10B981;">1</div>
      <div class="icon">🌾</div>
      <h4>List Harvest</h4>
      <p>Farmer registers batch with AUD unit price & inventory.</p>
      <span class="role-tag">Farmer Portal</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 2 -->
    <div class="step-node" style="border-color: #8B5CF6;">
      <div class="step-num" style="background:#8B5CF6;">2</div>
      <div class="icon">🛒</div>
      <h4>Order Placed</h4>
      <p>Customer checkouts; stock decremented atomically.</p>
      <span class="role-tag">Consumer Store</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 3 -->
    <div class="step-node" style="border-color: #10B981;">
      <div class="step-num" style="background:#10B981;">3</div>
      <div class="icon">📦</div>
      <h4>Farm Confirm</h4>
      <p>Produce picked, packaged & staged for dispatch.</p>
      <span class="role-tag">Farmer Orders</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 4 -->
    <div class="step-node" style="border-color: #F59E0B;">
      <div class="step-num" style="background:#F59E0B;">4</div>
      <div class="icon">🏢</div>
      <h4>QA Audit</h4>
      <p>Accredited Wholesaler certifies grade & biosecurity.</p>
      <span class="role-tag" style="color:#FBBF24;">Accredited Wholesaler</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 5 -->
    <div class="step-node" style="border-color: #3B82F6;">
      <div class="step-num" style="background:#3B82F6;">5</div>
      <div class="icon">🚚</div>
      <h4>Cold-Chain Handover</h4>
      <p>Driver logs pickup, transit checkpoints & temperature.</p>
      <span class="role-tag">Logistics Driver</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 6 -->
    <div class="step-node" style="border-color: #EC4899;">
      <div class="step-num" style="background:#EC4899;">6</div>
      <div class="icon">🏡</div>
      <h4>Delivered</h4>
      <p>Customer receives fresh produce on doorstep.</p>
      <span class="role-tag">7-Stage Tracker</span>
    </div>

    <div class="arrow-node">➔</div>

    <!-- Step 7 -->
    <div class="step-node" style="border-color: #F59E0B;">
      <div class="step-num" style="background:#F59E0B;">7</div>
      <div class="icon">⭐</div>
      <h4>Fair Trade Review</h4>
      <p>Customer leaves 5-star rating & grower feedback.</p>
      <span class="role-tag">Feedback Collection</span>
    </div>
  </div>

  <div class="gov-panel">
    <div>
      <h3>🛡️ Platform Governance Layer (Admin Portal)</h3>
      <p>Cloud Firestore real-time security rules and administrative audit controls oversee all 7 stages continuously.</p>
    </div>
    <div class="gov-pills">
      <div class="gov-pill">Wholesaler Accreditation Gating</div>
      <div class="gov-pill">Atomic Stock Protection</div>
      <div class="gov-pill">AUD Revenue Telemetry</div>
    </div>
  </div>
</body>
</html>
"""

# 3. Wholesaler Accreditation Flow HTML
HTML_WHOLESALER = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0B132B; color: #FFFFFF; padding: 35px 30px; width: 1350px; height: 800px; overflow: hidden; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h1 { font-size: 26px; font-weight: 800; color: #F59E0B; letter-spacing: -0.5px; margin-bottom: 5px; }
  .title-bar p { font-size: 14px; color: #94A3B8; }

  .workflow-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-top: 25px;
  }
  .flow-card {
    background: #1E293B;
    border: 2px solid #334155;
    border-radius: 12px;
    padding: 20px 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 380px;
  }
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }
  .step-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #F59E0B;
    color: #000;
    font-weight: 800;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .flow-card h3 { font-size: 15px; color: #F8FAFC; font-weight: 700; }
  .flow-card p { font-size: 11.5px; color: #94A3B8; line-height: 1.45; margin-bottom: 14px; }

  .state-badge {
    border-radius: 8px;
    padding: 10px;
    font-size: 11px;
    font-weight: 600;
    text-align: center;
    margin-top: auto;
  }
  .badge-pending {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid #F59E0B;
    color: #FCD34D;
  }
  .badge-locked {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid #EF4444;
    color: #FCA5A5;
  }
  .badge-admin {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid #6366F1;
    color: #C7D2FE;
  }
  .badge-active {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid #10B981;
    color: #6EE7B7;
  }
  .badge-revoke {
    background: rgba(156, 163, 175, 0.15);
    border: 1px solid #9CA3AF;
    color: #E5E7EB;
  }

  .biosecurity-banner {
    margin-top: 25px;
    background: #1C1917;
    border: 2px solid #78350F;
    border-radius: 10px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .biosecurity-banner h4 { color: #F59E0B; font-size: 14px; margin-bottom: 3px; }
  .biosecurity-banner p { color: #D6D3D1; font-size: 11.5px; }
</style>
</head>
<body>
  <div class="title-bar">
    <h1>WHOLESALER ACCREDITATION & APPROVAL GOVERNANCE LIFECYCLE</h1>
    <p>Mandatory Biosecurity Compliance Protocol for Australian Food Quality Auditors</p>
  </div>

  <div class="workflow-grid">
    <!-- Step 1 -->
    <div class="flow-card">
      <div>
        <div class="card-header">
          <div class="step-circle">1</div>
          <h3>Registration</h3>
        </div>
        <p>Wholesaler signs up on register.html selecting 'wholesaler' role and providing Australian Business Number (ABN).</p>
      </div>
      <div class="state-badge badge-pending">
        approved: false<br>
        status: 'pending'
      </div>
    </div>

    <!-- Step 2 -->
    <div class="flow-card">
      <div>
        <div class="card-header">
          <div class="step-circle" style="background:#EF4444; color:#FFF;">2</div>
          <h3>Restricted State</h3>
        </div>
        <p>Wholesaler dashboard renders amber accreditation warning. Stock verification action is locked with a padlock icon.</p>
      </div>
      <div class="state-badge badge-locked">
        🔒 Verify Stock Button<br>
        DISABLED & LOCKED
      </div>
    </div>

    <!-- Step 3 -->
    <div class="flow-card">
      <div>
        <div class="card-header">
          <div class="step-circle" style="background:#6366F1; color:#FFF;">3</div>
          <h3>Admin Review</h3>
        </div>
        <p>Administrator opens admin/approvals.html. Reviews wholesaler credentials, warehouse location, and cold-chain license.</p>
      </div>
      <div class="state-badge badge-admin">
        Admin Approvals Hub<br>
        1-Click 'Approve' Control
      </div>
    </div>

    <!-- Step 4 -->
    <div class="flow-card">
      <div>
        <div class="card-header">
          <div class="step-circle" style="background:#10B981; color:#FFF;">4</div>
          <h3>Accreditation Live</h3>
        </div>
        <p>Firestore user document updated with approved: true. Alert banner clears and stock verification is unlocked.</p>
      </div>
      <div class="state-badge badge-active">
        ✔ Full QA Authority<br>
        Certify Batches Active
      </div>
    </div>

    <!-- Step 5 -->
    <div class="flow-card">
      <div>
        <div class="card-header">
          <div class="step-circle" style="background:#6B7280; color:#FFF;">5</div>
          <h3>Revocation Safe</h3>
        </div>
        <p>If food safety breach or grading dispute arises, Admin can instantly revoke accreditation, locking auditing immediately.</p>
      </div>
      <div class="state-badge badge-revoke">
        Continuous Governance<br>
        Instant Status Revocation
      </div>
    </div>
  </div>

  <div class="biosecurity-banner">
    <div>
      <h4>AUSTRALIAN BIOSECURITY & FSANZ FOOD STANDARDS COMPLIANCE</h4>
      <p>Enforced by Cloud Firestore Security Rules: Non-accredited wholesalers cannot update order documents into verified status.</p>
    </div>
    <span style="font-size:12px; font-weight:700; color:#F59E0B;">STANDARD 3.2.2 COMPLIANT</span>
  </div>
</body>
</html>
"""

# 4. Financial Cash Flow Infographic HTML
HTML_FINANCIAL = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0B132B; color: #FFFFFF; padding: 35px 25px; width: 1350px; height: 800px; overflow: hidden; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h1 { font-size: 26px; font-weight: 800; color: #10B981; letter-spacing: -0.5px; margin-bottom: 5px; }
  .title-bar p { font-size: 14px; color: #94A3B8; }

  .hero-numbers {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 25px;
  }
  .metric-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  }
  .metric-card .val { font-size: 26px; font-weight: 800; margin: 4px 0; }
  .metric-card .lbl { font-size: 11px; text-transform: uppercase; font-weight: 700; color: #94A3B8; }

  .streams-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 25px;
  }
  .stream-card {
    background: #111827;
    border: 2px solid #1F2937;
    border-radius: 12px;
    padding: 18px 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
  }
  .stream-card.s1 { border-top: 4px solid #10B981; }
  .stream-card.s2 { border-top: 4px solid #3B82F6; }
  .stream-card.s3 { border-top: 4px solid #8B5CF6; }
  .stream-card.s4 { border-top: 4px solid #EC4899; }

  .stream-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 4px; color: #F8FAFC; }
  .stream-card .sub-fee { font-size: 11px; color: #94A3B8; margin-bottom: 12px; }
  .stream-card .monthly-inflow {
    font-size: 20px;
    font-weight: 800;
    color: #4ADE80;
    margin-bottom: 8px;
  }
  .stream-card p { font-size: 10.5px; color: #CBD5E1; line-height: 1.4; }

  .bottom-summary-box {
    background: linear-gradient(135deg, #064E3B, #022C22);
    border: 2px solid #059669;
    border-radius: 12px;
    padding: 18px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .bottom-summary-box h3 { font-size: 18px; color: #A7F3D0; font-weight: 800; }
  .bottom-summary-box p { font-size: 12px; color: #D1FAE5; }
  .bottom-summary-box .kpi-badge {
    background: #047857;
    border: 1px solid #10B981;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 800;
    color: #FFF;
  }
</style>
</head>
<body>
  <div class="title-bar">
    <h1>AGRITRACE COMMERCIAL MONETIZATION & REAL MONEY INFLOW ($ AUD)</h1>
    <p>Consolidated Monthly Revenue Breakdown, Operational Overheads, and Net Operating Profit</p>
  </div>

  <div class="hero-numbers">
    <div class="metric-card">
      <div class="lbl">Gross Inflow (Monthly)</div>
      <div class="val" style="color:#10B981;">$9,812.50 AUD</div>
      <div style="font-size:10px; color:#94A3B8;">Across 4 diversified streams</div>
    </div>
    <div class="metric-card">
      <div class="lbl">Monthly OPEX Overhead</div>
      <div class="val" style="color:#F87171;">$1,790.00 AUD</div>
      <div style="font-size:10px; color:#94A3B8;">Firebase, Security & Ops</div>
    </div>
    <div class="metric-card">
      <div class="lbl">Net Cash Profit (Monthly)</div>
      <div class="val" style="color:#38BDF8;">$8,022.50 AUD</div>
      <div style="font-size:10px; color:#94A3B8;">$96,270 AUD Annualized</div>
    </div>
    <div class="metric-card">
      <div class="lbl">CAPEX Payback Horizon</div>
      <div class="val" style="color:#FBBF24;">9.4 Months</div>
      <div style="font-size:10px; color:#94A3B8;">On $75,400 AUD Build Budget</div>
    </div>
  </div>

  <div class="streams-container">
    <div class="stream-card s1">
      <h3>Fair-Trade Fee (2.5%)</h3>
      <div class="sub-fee">2.5% of Gross Marketplace GMV</div>
      <div class="monthly-inflow">$1,687.50 AUD</div>
      <p>1,500 monthly consumer orders @ $45 AUD average basket size. Transparent take rate that undercuts supermarket duopolies.</p>
    </div>

    <div class="stream-card s2">
      <h3>Wholesaler License</h3>
      <div class="sub-fee">$120 AUD / month subscription</div>
      <div class="monthly-inflow">$3,000.00 AUD</div>
      <p>25 commercial regional distributors paying for access to pre-verified grower batches, QA certificates, and dispatch routing.</p>
    </div>

    <div class="stream-card s3">
      <h3>Farm SaaS Tiers</h3>
      <div class="sub-fee">$49 - $149 AUD / month SaaS</div>
      <div class="monthly-inflow">$4,450.00 AUD</div>
      <p>30 commercial farms ($49/mo) + 20 regional cooperatives ($149/mo) for inventory intelligence, temp logging, and export logs.</p>
    </div>

    <div class="stream-card s4">
      <h3>Logistics Dispatch Fee</h3>
      <div class="sub-fee">1.0% per freight coordination</div>
      <div class="monthly-inflow">$675.00 AUD</div>
      <p>Refrigerated freight transit operators paying coordination fees on $67,500 AUD monthly managed delivery volume.</p>
    </div>
  </div>

  <div class="bottom-summary-box">
    <div>
      <h3>SMALL FAMILY FARM ECONOMIC UPLIFT: +36% NET MARGIN</h3>
      <p>Growers net $4.49 AUD/punnet vs $2.20 AUD supermarket wholesale (+104% net unit profit). Average grower earns +$18,320 AUD extra/yr.</p>
    </div>
    <div class="kpi-badge">ROI: +36% FARMER PROFIT</div>
  </div>
</body>
</html>
"""

def render_pages():
    pages = [
        ("flow_sitemap_hierarchy.html", HTML_SITEMAP, "flow_sitemap_hierarchy.png", 1350, 850),
        ("flow_supply_chain_custody.html", HTML_CUSTODY, "flow_supply_chain_custody.png", 1350, 800),
        ("flow_wholesaler_accreditation.html", HTML_WHOLESALER, "flow_wholesaler_accreditation.png", 1350, 800),
        ("flow_commercial_financial_model.html", HTML_FINANCIAL, "flow_commercial_financial_model.png", 1350, 800)
    ]
    
    temp_profile = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "chrome_diag_profile")
    
    for html_name, html_content, out_png_name, w, h in pages:
        html_file = os.path.join(DIAGRAMS_HTML_DIR, html_name)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        target_png1 = os.path.join(SCREENSHOTS_DIR, out_png_name)
        target_png2 = os.path.join(DIAGRAMS_HTML_DIR, out_png_name)
        
        url = "file:///" + html_file.replace("\\", "/")
        cmd = [
            CHROME_PATH,
            "--headless=new",
            f"--user-data-dir={temp_profile}",
            "--disable-gpu",
            f"--window-size={w},{h}",
            f"--screenshot={target_png1}",
            url
        ]
        res = subprocess.run(cmd, capture_output=True)
        # Also copy to assets/diagrams
        if os.path.exists(target_png1):
            with open(target_png1, "rb") as rf, open(target_png2, "wb") as wf:
                wf.write(rf.read())
            print(f"Rendered: {out_png_name} -> {os.path.getsize(target_png1)} bytes")
        else:
            print(f"Failed to render: {out_png_name}")

if __name__ == "__main__":
    render_pages()
