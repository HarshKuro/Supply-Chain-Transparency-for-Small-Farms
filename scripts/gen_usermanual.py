import os
import sys
from docx.shared import Inches, Pt, RGBColor
from doc_utils import (
    init_document, add_title_header, add_heading_1, add_heading_2, add_heading_3,
    add_body_paragraph, add_bullet_point, add_callout,
    add_styled_table, add_screenshot
)

def build_usermanual_doc():
    doc = init_document("AgriTrace Operational User Manual", "System Operations Handbook")
    add_title_header(
        doc,
        title="AgriTrace Operational User Manual",
        subtitle="Complete End-to-End Operating Handbook & Working Lifecycle Flow: From Product Listing and Purchase to Wholesaler Accreditation, QA Verification, Driver Transit, and Admin Audit.",
        category_tag="Operations & User Manual"
    )

    # =========================================================================
    # 1. PLATFORM ARCHITECTURE & SUPPLY CHAIN LIFECYCLE
    # =========================================================================
    add_heading_1(doc, "1. Platform Architecture & Supply Chain Lifecycle")
    add_body_paragraph(
        doc,
        "AgriTrace is a decentralized digital supply chain transparency platform engineered to empower Australian family farms, regional growers, accredited commercial wholesalers, cold-chain logistics fleets, and conscious consumers. In Australia's retail food sector, major supermarket duopolies capture gross margins exceeding 50% to 60%, leaving primary producers vulnerable while obscuring food provenance from shoppers."
    )
    add_body_paragraph(
        doc,
        "By enforcing tamper-evident digital custody transitions at every physical handover, AgriTrace delivers cryptographic proof of origin, transparent farm-gate pricing in Australian Dollars ($ AUD), and end-to-end biosecurity verification."
    )

    # Architectural Diagrams
    add_screenshot(
        doc,
        "01_sitemap_visual_tree.png",
        "Figure 1.1: AgriTrace System Architecture & Hierarchical Visual Sitemap",
        width_inches=6.2
    )
    add_screenshot(
        doc,
        "02_supply_chain_custody_flowchart.png",
        "Figure 1.2: 7-Stage Digital Custody Verification Sequence Flowchart",
        width_inches=6.2
    )

    lifecycle_headers = ["Stage", "Lifecycle Status", "Responsible Stakeholder", "Enforced Verification Action"]
    lifecycle_rows = [
        ["Stage 1", "Order Placed / Pending", "🛒 Consumer", "Shopping cart checkout & atomic inventory deduction in Firestore."],
        ["Stage 2", "Farmer Confirmed", "🌾 Small Farmer", "Physical crop harvesting, packing, batch label generation."],
        ["Stage 3", "Wholesaler Verified", "🏢 Accredited Wholesaler", "Quality audit, biosecurity grade checks, weight validation."],
        ["Stage 4", "Picked Up", "🚚 Logistics Driver", "Loading into refrigerated vehicle; cold-chain custody seal."],
        ["Stage 5", "In Transit", "🚚 Logistics Driver", "Regional highway transit between hub and destination distribution zone."],
        ["Stage 6", "Out for Delivery", "🚚 Logistics Driver", "Local courier route dispatched to residential or commercial address."],
        ["Stage 7", "Delivered", "🚚 Logistics Driver / Consumer", "Contactless or signature handover; unlocks fair-trade feedback form."]
    ]
    add_styled_table(doc, lifecycle_headers, lifecycle_rows, [1.0, 1.4, 1.8, 2.2])

    # =========================================================================
    # 2. COMPLETE END-TO-END WORKING LIFECYCLE IN THE FLOW
    # =========================================================================
    add_heading_1(doc, "2. Complete End-to-End Working Operational Flow")
    add_body_paragraph(
        doc,
        "This section illustrates the full, connected working flow of an authentic transaction through every stage of the AgriTrace platform: from a farmer adding a fresh harvest batch, to a consumer purchasing it, the farmer confirming it, the administrator vetting the wholesaler, the wholesaler auditing the batch, the logistics driver executing physical transport, the customer tracking delivery, and the administrator auditing the final ledger."
    )

    # Step 2.1 Public & Authentication
    add_heading_2(doc, "Step 2.1: Public Entry & 1-Click Authentication")
    add_body_paragraph(
        doc,
        "Users enter via index.html and sign in via login.html using the 1-Click Demo Login toolbar. All accounts are pre-seeded with authentic Australian regional identities and uniform password 'password123'."
    )
    add_screenshot(doc, "flow_01_landing_page.png", "Flow 1: Public Hero Landing Page featuring Australian Regional Produce Mission", width_inches=6.0)
    add_screenshot(doc, "flow_02_login_page.png", "Flow 2: Secure Authentication Portal with Integrated 1-Click Demo Bar", width_inches=6.0)

    # Step 2.2 Farmer Adds Harvest Batch
    add_heading_2(doc, "Step 2.2: Farmer Publishes Fresh Harvest Batch")
    add_body_paragraph(
        doc,
        "Jack Miller (Yarra Valley Harvests VIC) logs into farmer/dashboard.html, opens farmer/products.html, clicks '+ Add Product', and lists a new batch: 'Barossa Valley Organic Shiraz Grapes' ($6.80 AUD/kg, 150 kg stock)."
    )
    add_screenshot(doc, "flow_03_farmer_dashboard.png", "Flow 3: Farmer Operations Command Center & Revenue Telemetry", width_inches=6.0)
    add_screenshot(doc, "flow_04_farmer_add_product_modal.png", "Flow 4: Farmer Add Product Modal with Barossa Valley Grapes Specifications", width_inches=6.0)
    add_screenshot(doc, "flow_05_farmer_product_saved.png", "Flow 5: Newly Added Produce Published Live in Farmer Catalog", width_inches=6.0)

    # Step 2.3 Customer Discovers & Purchases Produce
    add_heading_2(doc, "Step 2.3: Consumer Discovers Produce & Executes Fair-Trade Checkout")
    add_body_paragraph(
        doc,
        "Chloe Taylor (Customer, Melbourne VIC) logs into customer/products.html, spots the newly harvested Barossa Valley grapes with regional origin tag, adds 5 kg to cart, reviews itemized AUD pricing ($34.00 AUD) in customer/cart.html, and executes checkout."
    )
    add_screenshot(doc, "flow_06_customer_marketplace.png", "Flow 6: Fresh Produce Marketplace Displaying Newly Published Barossa Valley Grapes", width_inches=6.0)
    add_screenshot(doc, "flow_07_customer_cart.png", "Flow 7: Shopping Cart with Itemized AUD Pricing and Delivery Destination", width_inches=6.0)
    add_screenshot(doc, "flow_08_customer_order_placed.png", "Flow 8: Fair-Trade Order Checkout Completed with Atomic Stock Reservation", width_inches=6.0)
    add_screenshot(doc, "flow_09_customer_order_tracking_step1.png", "Flow 9: Customer 7-Stage Live Order Tracker (Stage 1: Order Placed)", width_inches=6.0)

    # Step 2.4 Farmer Confirms Inbound Order
    add_heading_2(doc, "Step 2.4: Farmer Confirms Order Preparation")
    add_body_paragraph(
        doc,
        "Jack Miller opens farmer/orders.html, sees Chloe's new inbound order, packs the 5 kg harvest batch, and clicks 'Confirm Order'. The order status advances to 'Farmer Confirmed'."
    )
    add_screenshot(doc, "flow_10_farmer_inbound_order.png", "Flow 10: Inbound Order Queue Displaying Chloe Taylor's New Order", width_inches=6.0)
    add_screenshot(doc, "flow_11_farmer_order_confirmed.png", "Flow 11: Order Confirmed by Farmer and Routed to Wholesaler QA Queue", width_inches=6.0)

    # Step 2.5 Admin Wholesaler Accreditation Governance
    add_heading_2(doc, "Step 2.5: Administrator Wholesaler Accreditation Governance")
    add_body_paragraph(
        doc,
        "Before unvetted wholesalers can certify farm shipments, they must undergo regulatory accreditation. When Matilda Evans (Melbourne Wholesale Hub) registers, her account is locked in 'Pending Review' status."
    )
    add_screenshot(doc, "flow_12_admin_approvals_pending.png", "Flow 12: Admin Approvals Hub Showing Matilda Evans Awaiting Compliance Approval", width_inches=6.0)
    add_screenshot(doc, "flow_13_wholesaler_pending_warning.png", "Flow 13: Unaccredited Wholesaler Dashboard Displaying Regulatory Amber Warning Banner", width_inches=6.0)
    add_screenshot(doc, "flow_14_wholesaler_pending_locked.png", "Flow 14: Wholesaler QA Queue with Stock Verification Controls Locked", width_inches=6.0)
    add_screenshot(doc, "flow_15_admin_wholesaler_approved.png", "Flow 15: Admin Approves Wholesaler — Account Transitioned to Accredited Active Status", width_inches=6.0)
    add_screenshot(doc, "flow_16_admin_wholesaler_revoked.png", "Flow 16: Admin Regulatory Enforcement — One-Click Revocation and Rejection Controls", width_inches=6.0)

    # Step 2.6 Accredited Wholesaler Audits & Verifies Stock
    add_heading_2(doc, "Step 2.6: Accredited Wholesaler Conducts Quality Audit")
    add_body_paragraph(
        doc,
        "Liam Wilson (Sydney Central Produce Markets Pty Ltd), an accredited wholesaler, opens wholesaler/orders.html. He audits crop freshness, temperature logs, and packaging tolerances before clicking 'Verify Stock'. The order transitions to 'Wholesaler Verified'."
    )
    add_screenshot(doc, "flow_17_wholesaler_approved_dashboard.png", "Flow 17: Accredited Wholesaler Dashboard with Certified Regulatory Status", width_inches=6.0)
    add_screenshot(doc, "flow_18_wholesaler_audit_queue.png", "Flow 18: Quality Assurance Queue with Active 'Verify Stock' Controls", width_inches=6.0)
    add_screenshot(doc, "flow_19_wholesaler_stock_verified.png", "Flow 19: Batch Certified & Wholesaler Verified — Dispatched to Logistics Fleet", width_inches=6.0)

    # Step 2.7 Logistics Driver Transit Handover
    add_heading_2(doc, "Step 2.7: Logistics Driver Executes Transit Milestones")
    add_body_paragraph(
        doc,
        "Lucas Brown (Outback Cold Logistics) opens driver/deliveries.html. He accepts the shipment, clicks 'Mark Picked Up' at the cold depot, clicks 'Mark In Transit' along the highway, and clicks 'Mark Delivered' upon physical handover at 42 Elgin Street, Carlton VIC."
    )
    add_screenshot(doc, "flow_20_driver_dashboard.png", "Flow 20: Logistics Driver Fleet Operations & Route Telemetry", width_inches=6.0)
    add_screenshot(doc, "flow_21_driver_deliveries_queue.png", "Flow 21: Verified Shipment Ready for Cold-Chain Transit Pickup", width_inches=6.0)
    add_screenshot(doc, "flow_22_driver_accepted.png", "Flow 22: Shipment Assigned to Refrigerated Vehicle", width_inches=6.0)
    add_screenshot(doc, "flow_23_driver_picked_up.png", "Flow 23: Transit Checkpoint 1 Logged — Picked Up from Hub", width_inches=6.0)
    add_screenshot(doc, "flow_24_driver_in_transit.png", "Flow 24: Transit Checkpoint 2 Logged — In Transit on Regional Highway", width_inches=6.0)
    add_screenshot(doc, "flow_25_driver_delivered.png", "Flow 25: Transit Checkpoint 3 Handover Completed — Order Delivered", width_inches=6.0)

    # Step 2.8 Customer 7-Stage Live Tracking & 5-Star Review
    add_heading_2(doc, "Step 2.8: Customer Live Provenance Tracking & Fair-Trade Rating")
    add_body_paragraph(
        doc,
        "Chloe Taylor opens customer/orders.html. All 7 progress stages are now illuminated green. She navigates to customer/feedback.html and submits a 5-star rating praising Jack Miller's fresh Barossa Valley grapes."
    )
    add_screenshot(doc, "flow_26_customer_delivered_stage7.png", "Flow 26: 7-Stage Custody Tracker Displaying Complete Green Delivered Milestones", width_inches=6.0)
    add_screenshot(doc, "flow_27_customer_feedback_form.png", "Flow 27: Fair-Trade Farmer Quality Rating and Review Submission Workspace", width_inches=6.0)
    add_screenshot(doc, "flow_28_customer_feedback_submitted.png", "Flow 28: 5-Star Farmer Feedback Successfully Committed to Grower Profile", width_inches=6.0)

    # Step 2.9 Admin Master Audit Ledger & Financial Evaluation
    add_heading_2(doc, "Step 2.9: Admin Master Audit Ledger & Financial Telemetry")
    add_body_paragraph(
        doc,
        "The Administrator audits the platform: inspecting the master transaction ledger, stakeholder user directory, global biosecurity catalog, and commercial financial evaluation metrics in AUD."
    )
    add_screenshot(doc, "flow_29_admin_orders_master_ledger.png", "Flow 29: Master Order Transaction Audit Ledger with Delivered Transaction Record", width_inches=6.0)
    add_screenshot(doc, "flow_30_admin_users_stakeholders.png", "Flow 30: Master Stakeholder Registry Across Australian Agricultural Nodes", width_inches=6.0)
    add_screenshot(doc, "flow_31_admin_products_audit.png", "Flow 31: Global Produce Catalog Audit with Barossa Valley Grapes Listed", width_inches=6.0)
    add_screenshot(doc, "flow_32_admin_evaluation_financials.png", "Flow 32: Administrative Commercial Evaluation & Revenue Feasibility Telemetry", width_inches=6.0)

    # =========================================================================
    # 3. DETAILED PORTAL-BY-PORTAL OPERATIONAL GUIDE
    # =========================================================================
    add_heading_1(doc, "3. Detailed Portal Reference & Stakeholder Procedures")
    add_body_paragraph(
        doc,
        "This section details dedicated procedures, account setups, and role-specific permissions across each independent web portal."
    )

    # 3.1 Authentication
    add_heading_2(doc, "3.1 Authentication & 1-Click Demo Bar (login.html)")
    cred_headers = ["Role Domain", "Stakeholder Entity", "Seeded Test Email", "Initial Account Status"]
    cred_rows = [
        ["🛡️ Administrator", "AgriTrace Admin (Canberra ACT)", "admin@example.com", "Full Platform Governance"],
        ["🌾 Small Farmer", "Jack Miller (Yarra Valley Harvests VIC)", "farmer@example.com", "Active Catalog & Orders"],
        ["🏢 Wholesaler (Approved)", "Liam Wilson (Sydney Central Markets NSW)", "wholesaler@example.com", "Accredited for QA Verification"],
        ["⏳ Wholesaler (Pending)", "Matilda Evans (Melbourne Produce Hub VIC)", "wholesaler.pending@example.com", "Pending Admin Approval (Locked)"],
        ["🚚 Transit Driver", "Lucas Brown (Outback Cold Logistics)", "driver@example.com", "Active Route Queue"],
        ["🛒 Direct Consumer", "Chloe Taylor (Melbourne VIC)", "customer@example.com", "Cart & Order Tracking"]
    ]
    add_styled_table(doc, cred_headers, cred_rows, [1.4, 2.0, 1.8, 1.3])

    add_callout(
        doc,
        "Uniform Demo Password: password123\nAll accounts use password123. Clicking any demo button on login.html auto-fills credentials and executes an immediate authenticated session.",
        "Quick Testing Security Key",
        "success"
    )

    # 3.2 Administrator Wholesaler Approvals Focus
    add_heading_2(doc, "3.2 Administrator Wholesaler Approvals Hub (admin/approvals.html)")
    add_body_paragraph(
        doc,
        "The Wholesaler Approvals Hub enforces regulatory compliance. Administrators inspect wholesaler credentials in three distinct operational states:"
    )
    add_bullet_point(doc, "Pending Wholesalers: Unaccredited applications awaiting verification (amber status badge, 'Approve' and 'Reject & Delete' actions).", "State 1: ")
    add_bullet_point(doc, "Accredited Active Wholesalers: Approved distributors with certified authority to audit farm batches (green status badge, 'Revoke' action).", "State 2: ")
    add_bullet_point(doc, "Revocation & Enforcement: Immediate removal of stock verification authority if non-compliant practices are detected.", "State 3: ")

    add_screenshot(doc, "admin_02_approvals_pending.png", "Figure 3.1: Admin Wholesaler Approvals Hub — Pending Wholesaler Review Queue", width_inches=6.0)
    add_screenshot(doc, "admin_02_wholesaler_approved.png", "Figure 3.2: Admin Wholesaler Approvals Hub — Wholesaler Approved & Accredited Active", width_inches=6.0)
    add_screenshot(doc, "admin_02_wholesaler_revoked.png", "Figure 3.3: Admin Wholesaler Approvals Hub — Regulatory Revocation & Governance Controls", width_inches=6.0)

    # Architectural Diagrams for Admin & Revenue
    add_screenshot(doc, "04_admin_governance_architecture.png", "Figure 3.4: Multi-Module Administrative Governance Architecture", width_inches=6.2)
    add_screenshot(doc, "05_commercial_revenue_model.png", "Figure 3.5: Commercial Revenue Flow & Multi-Stream Monetization Model", width_inches=6.2)

    # =========================================================================
    # 4. OPERATIONAL TROUBLESHOOTING MATRIX
    # =========================================================================
    add_heading_1(doc, "4. Operational Troubleshooting & Support Matrix")
    trouble_headers = ["Operational Issue", "Affected Role", "Root Cause Analysis", "Step-by-Step Resolution"]
    trouble_rows = [
        [
            "Stock Verification button is locked/disabled",
            "🏢 Wholesaler",
            "Account status is 'Pending Approval'. Biosecurity vetting has not been finalized.",
            "Contact platform Administrator to review wholesale business license via admin/approvals.html. Once approved, the button unlocks immediately."
        ],
        [
            "Inbound orders not appearing in queue",
            "🌾 Small Farmer",
            "Customer orders have not yet completed checkout or are assigned to another grower.",
            "Verify that produce batch has available quantity > 0 and refresh the 'Incoming Orders' page."
        ],
        [
            "Cannot progress delivery to next checkpoint",
            "🚚 Logistics Driver",
            "Previous checkpoint (e.g., Pickup) was not confirmed, or order has already reached final delivery.",
            "Confirm that the previous milestone was clicked. Orders advance strictly in sequence: Picked Up -> In Transit -> Delivered."
        ],
        [
            "Unable to submit customer feedback",
            "🛒 Consumer",
            "Order is still in transit and has not yet been marked 'Delivered' by the driver.",
            "Wait for courier to execute final delivery handover. Once delivered, the 1-to-5 star rating form activates."
        ],
        [
            "1-Click Demo login does not redirect",
            "All Roles",
            "Browser session cookies or cached token mismatch.",
            "Click 'Logout' in the header or navigate directly to login.html to re-trigger the demo button."
        ]
    ]
    add_styled_table(doc, trouble_headers, trouble_rows, [1.3, 1.1, 1.8, 2.2])

    output_path = os.path.join("docx", "usermanual.docx")
    doc.save(output_path)
    print(f"Successfully generated complete flow User Manual: {output_path}")

if __name__ == "__main__":
    build_usermanual_doc()
