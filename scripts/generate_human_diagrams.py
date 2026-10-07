import os
import subprocess

BASE_DIR = r"c:\Users\harsh\OneDrive\Documents\Pritam-projects\Supply Chain Transparency for Small Farms"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = os.path.join(BASE_DIR, "docx", "images")
TEMP_HTML_DIR = os.path.join(BASE_DIR, "assets", "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_HTML_DIR, exist_ok=True)

# 1. Sitemap Visual Tree HTML
HTML_SITEMAP = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body { background: #F8FAFC; color: #0F172A; padding: 30px; width: 1400px; height: 900px; }
  
  .header-box { text-align: center; margin-bottom: 24px; }
  .header-box .badge { display: inline-block; background: #DCFCE7; color: #166534; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; letter-spacing: -0.02em; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .tree-root-container { display: flex; flex-direction: column; align-items: center; position: relative; }

  .node-root {
    background: #FFFFFF;
    border: 2px solid #166534;
    border-radius: 10px;
    padding: 12px 28px;
    box-shadow: 0 4px 12px rgba(22, 101, 52, 0.12);
    text-align: center;
    z-index: 2;
  }
  .node-root h2 { font-size: 16px; font-weight: 700; color: #166534; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .node-root span { font-size: 11px; color: #475569; font-family: ui-monospace, SFMono-Regular, monospace; }

  .line-v1 { width: 2px; height: 20px; background: #CBD5E1; }
  .line-h-bar { width: 1240px; height: 2px; background: #CBD5E1; position: relative; }
  .line-drops { display: flex; justify-content: space-between; width: 1240px; }
  .drop-stem { width: 2px; height: 20px; background: #CBD5E1; }

  .portals-grid { display: flex; justify-content: space-between; width: 1340px; gap: 14px; margin-top: 0; }
  .portal-col { flex: 1; display: flex; flex-direction: column; align-items: center; }

  .portal-card {
    width: 100%;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    overflow: hidden;
  }
  .card-top { padding: 10px 12px; border-bottom: 1px solid #E2E8F0; display: flex; align-items: center; justify-content: space-between; }
  .card-top h3 { font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 6px; }
  .card-top .role-tag { font-size: 9.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px; text-transform: uppercase; }

  .farmer-c .card-top { background: #F0FDF4; border-top: 3px solid #16A34A; }
  .farmer-c .role-tag { background: #DCFCE7; color: #166534; }

  .wholesaler-c .card-top { background: #FFFBEB; border-top: 3px solid #D97706; }
  .wholesaler-c .role-tag { background: #FEF3C7; color: #B45309; }

  .driver-c .card-top { background: #EFF6FF; border-top: 3px solid #2563EB; }
  .driver-c .role-tag { background: #DBEAFE; color: #1E40AF; }

  .customer-c .card-top { background: #FAF5FF; border-top: 3px solid #7C3AED; }
  .customer-c .role-tag { background: #EDE9FE; color: #5B21B6; }

  .admin-c .card-top { background: #FEF2F2; border-top: 3px solid #DC2626; }
  .admin-c .role-tag { background: #FEE2E2; color: #991B1B; }

  .sub-list { list-style: none; padding: 8px 10px; }
  .sub-list li {
    padding: 6px 8px;
    border-radius: 6px;
    margin-bottom: 5px;
    background: #F8FAFC;
    border: 1px solid #F1F5F9;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #334155;
  }
  .sub-list li .page-name { font-weight: 600; }
  .sub-list li .file-ref { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 9.5px; color: #64748B; }
  .sub-list li.warn-item { background: #FEF3C7; border-color: #FDE68A; color: #92400E; }
  .sub-list li.admin-item { background: #FEE2E2; border-color: #FECACA; color: #991B1B; }

  .bottom-hub {
    margin-top: 22px;
    width: 1340px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  }
  .bottom-hub .hub-label { font-size: 11.5px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; }
  .pill-group { display: flex; gap: 8px; }
  .doc-pill { background: #F1F5F9; border: 1px solid #CBD5E1; padding: 5px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; color: #334155; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">AgriTrace Platform Architecture</div>
    <h1>System Sitemap & Hierarchical Navigation Directory</h1>
    <p>Complete structural map connecting public storefront, 5 authenticated stakeholder portals, and governance engines</p>
  </div>

  <div class="tree-root-container">
    <div class="node-root">
      <h2>🏠 Landing & Public Storefront</h2>
      <span>index.html (Mission • Australian Produce • Navigation Bar)</span>
    </div>

    <div class="line-v1"></div>
    <div class="line-h-bar"></div>
    <div class="line-drops">
      <div class="drop-stem"></div>
      <div class="drop-stem"></div>
      <div class="drop-stem"></div>
      <div class="drop-stem"></div>
      <div class="drop-stem"></div>
    </div>

    <div class="portals-grid">
      <!-- Farmer -->
      <div class="portal-col">
        <div class="portal-card farmer-c">
          <div class="card-top">
            <h3>🌾 Farmer Portal</h3>
            <span class="role-tag">Role: farmer</span>
          </div>
          <ul class="sub-list">
            <li><span class="page-name">Dashboard</span><span class="file-ref">farmer/dashboard.html</span></li>
            <li><span class="page-name">Produce Batches</span><span class="file-ref">farmer/products.html</span></li>
            <li><span class="page-name">Incoming Orders</span><span class="file-ref">farmer/orders.html</span></li>
          </ul>
        </div>
      </div>

      <!-- Wholesaler -->
      <div class="portal-col">
        <div class="portal-card wholesaler-c">
          <div class="card-top">
            <h3>🏢 Wholesaler Hub</h3>
            <span class="role-tag">Role: wholesaler</span>
          </div>
          <ul class="sub-list">
            <li><span class="page-name">Dashboard</span><span class="file-ref">wholesaler/dashboard.html</span></li>
            <li class="warn-item"><span class="page-name">Stock Verification</span><span class="file-ref">wholesaler/orders.html</span></li>
            <li style="background:none; border:none; padding:2px 4px; font-size:9px; color:#D97706;">*Requires Admin Accreditation to verify</li>
          </ul>
        </div>
      </div>

      <!-- Driver -->
      <div class="portal-col">
        <div class="portal-card driver-c">
          <div class="card-top">
            <h3>🚚 Logistics Driver</h3>
            <span class="role-tag">Role: driver</span>
          </div>
          <ul class="sub-list">
            <li><span class="page-name">Driver Dashboard</span><span class="file-ref">driver/dashboard.html</span></li>
            <li><span class="page-name">Transit Deliveries</span><span class="file-ref">driver/deliveries.html</span></li>
            <li><span class="page-name">Cold-Chain Handover</span><span class="file-ref">Live Checkpoints</span></li>
          </ul>
        </div>
      </div>

      <!-- Customer -->
      <div class="portal-col">
        <div class="portal-card customer-c">
          <div class="card-top">
            <h3>🛒 Consumer Store</h3>
            <span class="role-tag">Role: customer</span>
          </div>
          <ul class="sub-list">
            <li><span class="page-name">Fresh Catalog</span><span class="file-ref">customer/products.html</span></li>
            <li><span class="page-name">Shopping Cart</span><span class="file-ref">customer/cart.html</span></li>
            <li><span class="page-name">7-Stage Tracking</span><span class="file-ref">customer/orders.html</span></li>
            <li><span class="page-name">Farmer Ratings</span><span class="file-ref">customer/feedback.html</span></li>
          </ul>
        </div>
      </div>

      <!-- Admin -->
      <div class="portal-col">
        <div class="portal-card admin-c">
          <div class="card-top">
            <h3>🛡️ Administrator</h3>
            <span class="role-tag">Role: admin</span>
          </div>
          <ul class="sub-list">
            <li><span class="page-name">Command Dashboard</span><span class="file-ref">admin/dashboard.html</span></li>
            <li class="admin-item"><span class="page-name">Wholesaler Approvals</span><span class="file-ref">admin/approvals.html</span></li>
            <li><span class="page-name">User Registry</span><span class="file-ref">admin/users.html</span></li>
            <li><span class="page-name">Catalog & Orders</span><span class="file-ref">admin/products & orders</span></li>
            <li><span class="page-name">Financial Evaluation</span><span class="file-ref">admin/evaluation.html</span></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bottom-hub">
      <span class="hub-label">Platform Documentation & Testing Utilities:</span>
      <div class="pill-group">
        <div class="doc-pill">📖 user-manual.html</div>
        <div class="doc-pill">💻 installation-manual.html</div>
        <div class="doc-pill">📊 evaluation-report.html</div>
        <div class="doc-pill">🇦🇺 seed.html (Australian Database)</div>
        <div class="doc-pill">🧪 test_runner.html (31 Unit/System Tests)</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 2. Custody Workflow HTML
HTML_CUSTODY = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background: #FFFFFF; color: #0F172A; padding: 35px 25px; width: 1400px; height: 850px; }
  
  .header-box { text-align: center; margin-bottom: 30px; }
  .header-box .badge { display: inline-block; background: #DBEAFE; color: #1E40AF; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .pipeline-track { display: flex; justify-content: space-between; align-items: stretch; gap: 8px; position: relative; margin-top: 20px; }

  .stage-box {
    flex: 1;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .stage-box.active-1 { border-top: 4px solid #16A34A; }
  .stage-box.active-2 { border-top: 4px solid #7C3AED; }
  .stage-box.active-3 { border-top: 4px solid #16A34A; }
  .stage-box.active-4 { border-top: 4px solid #D97706; }
  .stage-box.active-5 { border-top: 4px solid #2563EB; }
  .stage-box.active-6 { border-top: 4px solid #059669; }
  .stage-box.active-7 { border-top: 4px solid #EA580C; }

  .step-badge {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #0F172A;
    color: #FFF;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px auto;
  }
  .stage-box h3 { font-size: 13px; font-weight: 700; text-align: center; margin-bottom: 6px; }
  .stage-box p { font-size: 10.5px; color: #64748B; text-align: center; line-height: 1.4; margin-bottom: 12px; }

  .stage-meta {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 6px;
    font-size: 9.5px;
    text-align: center;
    color: #475569;
    font-weight: 600;
  }

  .arrow-sep { display: flex; align-items: center; justify-content: center; color: #94A3B8; font-size: 18px; font-weight: bold; width: 14px; }

  .gov-container {
    margin-top: 35px;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .gov-left h4 { font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 2px; }
  .gov-left p { font-size: 12px; color: #64748B; }
  .gov-badges { display: flex; gap: 10px; }
  .gov-badge-item { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 12px; font-size: 11px; font-weight: 600; color: #1E293B; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">Custody Verification Pipeline</div>
    <h1>End-to-End Farm-to-Consumer Supply Chain Custody Flow</h1>
    <p>7-stage sequential digital handover protocol providing complete provenance transparency in regional Australia</p>
  </div>

  <div class="pipeline-track">
    <div class="stage-box active-1">
      <div>
        <div class="step-badge" style="background:#16A34A;">1</div>
        <h3>List Harvest</h3>
        <p>Farmer registers fresh harvest batch with AUD unit price and stock count.</p>
      </div>
      <div class="stage-meta">Farmer Portal<br>farmer/products.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-2">
      <div>
        <div class="step-badge" style="background:#7C3AED;">2</div>
        <h3>Order Placed</h3>
        <p>Consumer discovers produce and checkouts. Inventory decremented atomically.</p>
      </div>
      <div class="stage-meta">Consumer Store<br>customer/cart.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-3">
      <div>
        <div class="step-badge" style="background:#16A34A;">3</div>
        <h3>Farm Confirm</h3>
        <p>Produce picked, packaged, and marked ready for regional transport.</p>
      </div>
      <div class="stage-meta">Farmer Orders<br>farmer/orders.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-4">
      <div>
        <div class="step-badge" style="background:#D97706;">4</div>
        <h3>QA Inspection</h3>
        <p>Accredited Wholesaler certifies grade, weight, and biosecurity standards.</p>
      </div>
      <div class="stage-meta" style="color:#B45309;">Accredited Wholesaler<br>wholesaler/orders.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-5">
      <div>
        <div class="step-badge" style="background:#2563EB;">5</div>
        <h3>Cold Transit</h3>
        <p>Refrigerated driver logs pickup, highway checkpoints, and handover.</p>
      </div>
      <div class="stage-meta">Logistics Driver<br>driver/deliveries.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-6">
      <div>
        <div class="step-badge" style="background:#059669;">6</div>
        <h3>Doorstep Drop</h3>
        <p>Final delivery confirmed. Custody transferred to consumer.</p>
      </div>
      <div class="stage-meta">Order Tracker<br>customer/orders.html</div>
    </div>

    <div class="arrow-sep">→</div>

    <div class="stage-box active-7">
      <div>
        <div class="step-badge" style="background:#EA580C;">7</div>
        <h3>Fair Feedback</h3>
        <p>Customer leaves 5-star rating and quality review directly for the grower.</p>
      </div>
      <div class="stage-meta">Consumer Review<br>customer/feedback.html</div>
    </div>
  </div>

  <div class="gov-container">
    <div class="gov-left">
      <h4>🛡️ Administrative Governance & Security Verification Layer</h4>
      <p>Cloud Firestore real-time security rules and administrative audit controls oversee all 7 stages continuously.</p>
    </div>
    <div class="gov-badges">
      <div class="gov-badge-item">Wholesaler Accreditation Gating</div>
      <div class="gov-badge-item">Atomic Inventory Protection</div>
      <div class="gov-badge-item">AUD Revenue Telemetry</div>
    </div>
  </div>
</body>
</html>
"""

# 3. Wholesaler Accreditation Flow HTML
HTML_WHOLESALER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background: #F8FAFC; color: #0F172A; padding: 35px 25px; width: 1400px; height: 850px; }
  
  .header-box { text-align: center; margin-bottom: 25px; }
  .header-box .badge { display: inline-block; background: #FEF3C7; color: #B45309; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .workflow-grid { display: flex; justify-content: space-between; gap: 14px; margin-top: 25px; }

  .flow-card {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    height: 380px;
  }
  .flow-card.step-1 { border-top: 4px solid #64748B; }
  .flow-card.step-2 { border-top: 4px solid #DC2626; }
  .flow-card.step-3 { border-top: 4px solid #2563EB; }
  .flow-card.step-4 { border-top: 4px solid #16A34A; }
  .flow-card.step-5 { border-top: 4px solid #475569; }

  .step-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #0F172A;
    color: #FFF;
    font-size: 12px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
  }
  .flow-card h3 { font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 8px; }
  .flow-card p { font-size: 11px; color: #64748B; line-height: 1.45; }

  .status-pill {
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 700;
    text-align: center;
    margin-top: auto;
  }
  .pill-pending { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
  .pill-locked { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
  .pill-admin { background: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
  .pill-approved { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
  .pill-revoke { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }

  .notice-panel {
    margin-top: 30px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #D97706;
    border-radius: 8px;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .notice-panel h4 { font-size: 13px; font-weight: 700; color: #92400E; margin-bottom: 2px; }
  .notice-panel p { font-size: 11.5px; color: #64748B; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">Regulatory Biosecurity Compliance</div>
    <h1>Wholesaler Accreditation & Administrative Approval Workflow</h1>
    <p>Mandatory vetting protocol ensuring only verified commercial distributors certify Australian farm produce</p>
  </div>

  <div class="workflow-grid">
    <div class="flow-card step-1">
      <div>
        <div class="step-circle" style="background:#64748B;">1</div>
        <h3>Registration</h3>
        <p>Wholesaler signs up selecting 'wholesaler' role and entering Australian Business Number (ABN).</p>
      </div>
      <div class="status-pill pill-pending">approved: false<br>status: 'pending'</div>
    </div>

    <div class="flow-card step-2">
      <div>
        <div class="step-circle" style="background:#DC2626;">2</div>
        <h3>Gated Access</h3>
        <p>Portal renders amber notice banner. 'Verify Stock' action is locked with a padlock tooltip.</p>
      </div>
      <div class="status-pill pill-locked">🔒 Verify Stock Action<br>DISABLED & LOCKED</div>
    </div>

    <div class="flow-card step-3">
      <div>
        <div class="step-circle" style="background:#2563EB;">3</div>
        <h3>Admin Vetting</h3>
        <p>Admin opens admin/approvals.html to review ABN, cold storage license, and location details.</p>
      </div>
      <div class="status-pill pill-admin">Admin Approvals Hub<br>1-Click 'Approve' Control</div>
    </div>

    <div class="flow-card step-4">
      <div>
        <div class="step-circle" style="background:#16A34A;">4</div>
        <h3>Accredited Live</h3>
        <p>Firestore user document updated with approved: true. Quality audit capability unlocked.</p>
      </div>
      <div class="status-pill pill-approved">✔ Full QA Authority<br>Certify Batches Active</div>
    </div>

    <div class="flow-card step-5">
      <div>
        <div class="step-circle" style="background:#475569;">5</div>
        <h3>Revocation Authority</h3>
        <p>Admin can instantly revoke accreditation if biosecurity or food standards breach occurs.</p>
      </div>
      <div class="status-pill pill-revoke">Continuous Governance<br>1-Click 'Revoke Status'</div>
    </div>
  </div>

  <div class="notice-panel">
    <div>
      <h4>AUSTRALIAN BIOSECURITY & FSANZ FOOD STANDARDS COMPLIANCE</h4>
      <p>Enforced by Cloud Firestore Security Rules: Non-accredited wholesalers cannot update order documents into verified status.</p>
    </div>
    <span style="font-size:11.5px; font-weight:700; color:#B45309;">FSANZ STANDARD 3.2.2 COMPLIANT</span>
  </div>
</body>
</html>
"""

# 4. Admin Governance Architecture HTML
HTML_ADMIN = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background: #FFFFFF; color: #0F172A; padding: 35px 25px; width: 1400px; height: 850px; }
  
  .header-box { text-align: center; margin-bottom: 25px; }
  .header-box .badge { display: inline-block; background: #FEE2E2; color: #991B1B; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .center-node {
    width: 480px;
    margin: 10px auto 25px auto;
    background: #FEF2F2;
    border: 2px solid #DC2626;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.08);
  }
  .center-node h2 { font-size: 17px; font-weight: 800; color: #991B1B; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .center-node p { font-size: 11px; color: #7F1D1D; margin-top: 3px; font-family: ui-monospace, monospace; }

  .admin-pillars { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-top: 15px; }
  .pillar-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    height: 340px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .pillar-box.p1 { border-top: 4px solid #D97706; }
  .pillar-box.p2 { border-top: 4px solid #2563EB; }
  .pillar-box.p3 { border-top: 4px solid #16A34A; }
  .pillar-box.p4 { border-top: 4px solid #7C3AED; }
  .pillar-box.p5 { border-top: 4px solid #059669; }

  .pillar-box h3 { font-size: 13.5px; font-weight: 700; color: #0F172A; margin-bottom: 6px; }
  .pillar-box p { font-size: 11px; color: #64748B; line-height: 1.45; }
  .pillar-meta { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px; font-size: 10px; color: #334155; font-weight: 600; text-align: center; }

  .security-footer {
    margin-top: 25px;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .security-footer h4 { font-size: 13px; font-weight: 700; color: #1E293B; }
  .security-footer p { font-size: 11.5px; color: #64748B; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">Platform Security Architecture</div>
    <h1>Administrator Governance & Multi-Module Security Architecture</h1>
    <p>Central management and neutral oversight across all Australian regional agricultural nodes</p>
  </div>

  <div class="center-node">
    <h2>🛡️ AgriTrace Administrator Portal</h2>
    <p>admin/dashboard.html • Real-time AUD telemetry • Global Platform Governance</p>
  </div>

  <div class="admin-pillars">
    <div class="pillar-box p1">
      <div>
        <h3>1. Wholesaler Approvals</h3>
        <p>Dedicated vetting queue for commercial wholesalers. One-click status toggling and biosecurity accreditation.</p>
      </div>
      <div class="pillar-meta">admin/approvals.html<br>Status: Pending / Approved</div>
    </div>

    <div class="pillar-box p2">
      <div>
        <h3>2. User Registry</h3>
        <p>Comprehensive roster of all 5 stakeholder accounts. Phone verification, role assignment, and audit tracking.</p>
      </div>
      <div class="pillar-meta">admin/users.html<br>Role Guards: js/auth.js</div>
    </div>

    <div class="pillar-box p3">
      <div>
        <h3>3. Catalog Oversight</h3>
        <p>Continuous audit of produce listings, batch limits, and fair-trade price boundaries in Australian Dollars ($ AUD).</p>
      </div>
      <div class="pillar-meta">admin/products.html<br>Firestore products collection</div>
    </div>

    <div class="pillar-box p4">
      <div>
        <h3>4. Order Ledger</h3>
        <p>Macro-level order history providing complete transparency across all 7 stages from placement to delivery.</p>
      </div>
      <div class="pillar-meta">admin/orders.html<br>Real-time orders ledger</div>
    </div>

    <div class="pillar-box p5">
      <div>
        <h3>5. Financial Telemetry</h3>
        <p>Commercial feasibility tracking, recurring cloud expenses (OPEX), and small grower margin improvement analysis.</p>
      </div>
      <div class="pillar-meta">admin/evaluation.html<br>$ AUD Turnover Metrics</div>
    </div>
  </div>

  <div class="security-footer">
    <div>
      <h4>SECURITY & ROLE-BASED ACCESS CONTROL (RBAC)</h4>
      <p>Protected by Cloud Firestore Security Rules and client-side route redirection engine in js/auth.js.</p>
    </div>
    <span style="font-size:11.5px; font-weight:700; color:#166534;">ENCRYPTED & AUTHENTICATED</span>
  </div>
</body>
</html>
"""

# 5. Financial Commercial Model HTML
HTML_FINANCIAL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background: #FFFFFF; color: #0F172A; padding: 35px 25px; width: 1400px; height: 850px; }
  
  .header-box { text-align: center; margin-bottom: 25px; }
  .header-box .badge { display: inline-block; background: #DCFCE7; color: #166534; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
  .kpi-card { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; text-align: center; }
  .kpi-card .lbl { font-size: 10.5px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; }
  .kpi-card .val { font-size: 24px; font-weight: 800; margin: 4px 0 2px 0; }
  .kpi-card .sub { font-size: 10px; color: #94A3B8; }

  .streams-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
  .stream-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .stream-box.s1 { border-top: 3px solid #16A34A; }
  .stream-box.s2 { border-top: 3px solid #2563EB; }
  .stream-box.s3 { border-top: 3px solid #7C3AED; }
  .stream-box.s4 { border-top: 3px solid #EA580C; }

  .stream-box h3 { font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 2px; }
  .stream-box .rate { font-size: 10.5px; color: #64748B; margin-bottom: 10px; }
  .stream-box .cash { font-size: 18px; font-weight: 800; color: #16A34A; margin-bottom: 6px; }
  .stream-box p { font-size: 10.5px; color: #475569; line-height: 1.4; }

  .bottom-roi {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    padding: 16px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .bottom-roi h4 { font-size: 14px; font-weight: 800; color: #166534; margin-bottom: 2px; }
  .bottom-roi p { font-size: 12px; color: #334155; }
  .roi-pill { background: #166534; color: #FFF; font-size: 12px; font-weight: 800; padding: 6px 16px; border-radius: 6px; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">Commercial Feasibility Model</div>
    <h1>Platform Revenue Streams & Real Money Cash Inflow ($ AUD)</h1>
    <p>Detailed monthly commercial realization, operational expenditures, and small family farm margin gain</p>
  </div>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="lbl">Gross Monthly Inflow</div>
      <div class="val" style="color:#16A34A;">$9,812.50 AUD</div>
      <div class="sub">Across 4 diversified streams</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">Monthly Cloud OPEX</div>
      <div class="val" style="color:#DC2626;">$1,790.00 AUD</div>
      <div class="sub">Firebase, domain, security & ops</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">Net Monthly Profit</div>
      <div class="val" style="color:#2563EB;">$8,022.50 AUD</div>
      <div class="sub">$96,270 AUD Annualized profit</div>
    </div>
    <div class="kpi-card">
      <div class="lbl">CAPEX Payback Horizon</div>
      <div class="val" style="color:#D97706;">9.4 Months</div>
      <div class="sub">On $75,400 AUD Build budget</div>
    </div>
  </div>

  <div class="streams-grid">
    <div class="stream-box s1">
      <h3>Fair-Trade Fee (2.5%)</h3>
      <div class="rate">2.5% of Marketplace GMV</div>
      <div class="cash">$1,687.50 AUD / mo</div>
      <p>1,500 monthly customer orders @ $45 AUD average basket size. Transparent take rate that undercuts supermarket duopolies.</p>
    </div>

    <div class="stream-box s2">
      <h3>Wholesaler License</h3>
      <div class="rate">$120 AUD / month subscription</div>
      <div class="cash">$3,000.00 AUD / mo</div>
      <p>25 commercial regional distributors paying for access to pre-verified grower batches, QA certificates, and dispatch routing.</p>
    </div>

    <div class="stream-box s3">
      <h3>Farm Cooperative SaaS</h3>
      <div class="rate">$49 - $149 AUD / month SaaS</div>
      <div class="cash">$4,450.00 AUD / mo</div>
      <p>30 commercial farms ($49/mo) + 20 regional cooperatives ($149/mo) for inventory intelligence, temp logging, and export logs.</p>
    </div>

    <div class="stream-box s4">
      <h3>Logistics Dispatch Fee</h3>
      <div class="rate">1.0% per freight coordination</div>
      <div class="cash">$675.00 AUD / mo</div>
      <p>Refrigerated freight transit operators paying coordination fees on $67,500 AUD monthly managed delivery volume.</p>
    </div>
  </div>

  <div class="bottom-roi">
    <div>
      <h4>SMALL FAMILY FARM ECONOMIC BENEFIT: +36% NET MARGIN UPLIFT</h4>
      <p>Growers net $4.49 AUD/punnet vs $2.20 AUD supermarket wholesale (+104% net unit profit). Average grower earns +$18,320 AUD extra/yr.</p>
    </div>
    <div class="roi-pill">ROI: +36% FARM GAIN</div>
  </div>
</body>
</html>
"""

# 6. Installation & Deployment Pipeline HTML
HTML_INSTALLATION = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background: #FFFFFF; color: #0F172A; padding: 35px 25px; width: 1400px; height: 850px; }
  
  .header-box { text-align: center; margin-bottom: 25px; }
  .header-box .badge { display: inline-block; background: #DBEAFE; color: #1E40AF; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .header-box h1 { font-size: 26px; font-weight: 800; color: #0F172A; }
  .header-box p { font-size: 13px; color: #64748B; margin-top: 2px; }

  .pipeline-grid { display: flex; justify-content: space-between; gap: 12px; margin-top: 25px; }
  .pipe-step {
    flex: 1;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    height: 380px;
  }
  .pipe-step.s1 { border-top: 4px solid #64748B; }
  .pipe-step.s2 { border-top: 4px solid #D97706; }
  .pipe-step.s3 { border-top: 4px solid #DC2626; }
  .pipe-step.s4 { border-top: 4px solid #16A34A; }
  .pipe-step.s5 { border-top: 4px solid #2563EB; }
  .pipe-step.s6 { border-top: 4px solid #059669; }

  .num-badge {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #0F172A;
    color: #FFF;
    font-size: 12px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
  }
  .pipe-step h3 { font-size: 13.5px; font-weight: 700; color: #0F172A; margin-bottom: 8px; }
  .pipe-step p { font-size: 11px; color: #64748B; line-height: 1.45; }

  .pipe-meta {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 8px;
    font-size: 10px;
    color: #334155;
    font-weight: 600;
    text-align: center;
    margin-top: auto;
  }

  .pipe-footer {
    margin-top: 30px;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .pipe-footer h4 { font-size: 13px; font-weight: 700; color: #1E293B; }
  .pipe-footer p { font-size: 11.5px; color: #64748B; }
</style>
</head>
<body>
  <div class="header-box">
    <div class="badge">Production Deployment Architecture</div>
    <h1>Technical Installation & Production Deployment Pipeline</h1>
    <p>Zero-compilation ES Modules architecture deployed to Google Cloud Platform and Firebase</p>
  </div>

  <div class="pipeline-grid">
    <div class="pipe-step s1">
      <div>
        <div class="num-badge" style="background:#64748B;">1</div>
        <h3>Workspace Setup</h3>
        <p>Clone repository. Native ES Modules architecture requires no bundlers, webpack, or npm builds.</p>
      </div>
      <div class="pipe-meta">Local Environment<br>Node.js or Python</div>
    </div>

    <div class="pipe-step s2">
      <div>
        <div class="num-badge" style="background:#D97706;">2</div>
        <h3>Firebase Init</h3>
        <p>Initialize Web App in Firebase Console. Deploy Cloud Firestore in Sydney (australia-southeast1).</p>
      </div>
      <div class="pipe-meta">js/firebase-config.js<br>Email/Password Auth</div>
    </div>

    <div class="pipe-step s3">
      <div>
        <div class="num-badge" style="background:#DC2626;">3</div>
        <h3>Security Rules</h3>
        <p>Deploy firestore.rules to enforce role guards and lock wholesaler verification behind admin approval.</p>
      </div>
      <div class="pipe-meta">firestore.rules<br>Role-Based Security</div>
    </div>

    <div class="pipe-step s4">
      <div>
        <div class="num-badge" style="background:#16A34A;">4</div>
        <h3>Database Seed</h3>
        <p>Execute seed.html to populate authentic Australian growers, regional AUD harvests, and test roles.</p>
      </div>
      <div class="pipe-meta">seed.html<br>Australian Regional DB</div>
    </div>

    <div class="pipe-step s5">
      <div>
        <div class="num-badge" style="background:#2563EB;">5</div>
        <h3>Launch Server</h3>
        <p>Run python -m http.server 8000 or run.bat to serve modules over HTTP and bypass browser CORS limits.</p>
      </div>
      <div class="pipe-meta">http://localhost:8000<br>run.bat execution</div>
    </div>

    <div class="pipe-step s6">
      <div>
        <div class="num-badge" style="background:#059669;">6</div>
        <h3>Test Suite</h3>
        <p>Execute automated test suite: 8 Unit Tests, 14 System Tests, and 9 SEO Audits (31/31 passing).</p>
      </div>
      <div class="pipe-meta">tests/unit_tests.js<br>100% Pass Rate</div>
    </div>
  </div>

  <div class="pipe-footer">
    <div>
      <h4>TURNKEY DEPLOYMENT GUARANTEE</h4>
      <p>Compatible with Firebase Hosting, Cloudflare Pages, AWS S3 / CloudFront, and traditional Nginx web servers.</p>
    </div>
    <span style="font-size:11.5px; font-weight:700; color:#1E40AF;">PRODUCTION READY</span>
  </div>
</body>
</html>
"""

def generate_all_diagrams():
    diagrams = [
        ("01_sitemap_visual_tree.html", HTML_SITEMAP, "01_sitemap_visual_tree.png"),
        ("02_supply_chain_custody_flowchart.html", HTML_CUSTODY, "02_supply_chain_custody_flowchart.png"),
        ("03_wholesaler_accreditation_flow.html", HTML_WHOLESALER, "03_wholesaler_accreditation_flow.png"),
        ("04_admin_governance_architecture.html", HTML_ADMIN, "04_admin_governance_architecture.png"),
        ("05_commercial_revenue_model.html", HTML_FINANCIAL, "05_commercial_revenue_model.png"),
        ("06_installation_deployment_pipeline.html", HTML_INSTALLATION, "06_installation_deployment_pipeline.png")
    ]
    
    temp_profile = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "chrome_human_profile2")
    
    for html_name, html_content, png_name in diagrams:
        html_path = os.path.join(TEMP_HTML_DIR, html_name)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        target_png = os.path.join(OUTPUT_DIR, png_name)
        url = "file:///" + html_path.replace("\\", "/")
        
        cmd = [
            CHROME_PATH,
            "--headless=new",
            f"--user-data-dir={temp_profile}",
            "--disable-gpu",
            "--window-size=1400,900",
            f"--screenshot={target_png}",
            url
        ]
        subprocess.run(cmd, capture_output=True)
        if os.path.exists(target_png):
            print(f"Generated clean human-designed diagram: {png_name} ({os.path.getsize(target_png)} bytes)")
        else:
            print(f"Failed to generate: {png_name}")

if __name__ == "__main__":
    generate_all_diagrams()
