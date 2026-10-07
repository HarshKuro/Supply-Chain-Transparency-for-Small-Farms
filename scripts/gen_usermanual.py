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
        subtitle="Complete Step-by-Step Operating Handbook & Visual Interface Guide for Farmers, Wholesalers, Logistics Drivers, Direct Consumers, and System Administrators.",
        category_tag="Operations & User Manual"
    )

    # =========================================================================
    # 1. PLATFORM ARCHITECTURE & SUPPLY CHAIN LIFECYCLE
    # =========================================================================
    add_heading_1(doc, "1. Platform Architecture & Supply Chain Lifecycle")
    add_body_paragraph(
        doc,
        "AgriTrace is a decentralized digital supply chain transparency platform engineered to empower Australian family farms, independent regional growers, accredited commercial wholesalers, cold-chain logistics providers, and conscious consumers. In Australia's retail food sector, major supermarket duopolies capture gross margins exceeding 50% to 60%, leaving primary producers vulnerable while obscuring food provenance from shoppers."
    )
    add_body_paragraph(
        doc,
        "By enforcing tamper-evident digital custody transitions at every physical handover, AgriTrace delivers cryptographic proof of origin, transparent farm-gate pricing in Australian Dollars ($ AUD), and end-to-end biosecurity verification."
    )

    # Embedded High-Res Clean Diagrams
    add_screenshot(
        doc,
        "01_sitemap_visual_tree.png",
        "Figure 1.1: AgriTrace System Architecture & Hierarchical Visual Sitemap",
        width_inches=6.2
    )
    add_body_paragraph(
        doc,
        "The supply chain enforces a strict 7-stage sequential state machine. An order cannot bypass stages or be altered retroactively once committed to the Cloud Firestore database."
    )
    add_screenshot(
        doc,
        "02_supply_chain_custody_flowchart.png",
        "Figure 1.2: 7-Stage Digital Custody Verification Sequence Flowchart",
        width_inches=6.2
    )

    lifecycle_headers = ["Stage", "Lifecycle Status", "Responsible Stakeholder", "Enforced Verification Action"]
    lifecycle_rows = [
        ["Stage 1", "Order Placed", "🛒 Consumer", "Shopping cart checkout & atomic inventory deduction in Firestore."],
        ["Stage 2", "Farmer Confirmed", "🌾 Small Farmer", "Physical crop harvesting, packing, batch label generation."],
        ["Stage 3", "Wholesaler Verified", "🏢 Accredited Wholesaler", "Quality audit, biosecurity grade checks, weight validation."],
        ["Stage 4", "Picked Up", "🚚 Logistics Driver", "Loading into refrigerated vehicle; cold-chain custody seal."],
        ["Stage 5", "In Transit", "🚚 Logistics Driver", "Regional highway transit between hub and destination distribution zone."],
        ["Stage 6", "Out for Delivery", "🚚 Logistics Driver", "Local courier route dispatched to residential or commercial address."],
        ["Stage 7", "Delivered", "🚚 Logistics Driver / Consumer", "Contactless or signature handover; unlocks fair-trade feedback form."]
    ]
    add_styled_table(doc, lifecycle_headers, lifecycle_rows, [1.0, 1.4, 1.8, 2.2])

    # =========================================================================
    # 2. PUBLIC PORTAL & AUTHENTICATION MANUAL
    # =========================================================================
    add_heading_1(doc, "2. Public Portal, Registration & Authentication (login.html)")
    add_body_paragraph(
        doc,
        "The public web application provides open access to the platform overview, educational transparency metrics, stakeholder registration, and secure authentication with automated role-based routing."
    )

    add_heading_2(doc, "2.1 Public Landing Page (index.html)")
    add_body_paragraph(
        doc,
        "Visitors can explore AgriTrace's core mission, interactive transparency widgets, Australian regional harvest stories, and direct navigation links to all platform documentation."
    )
    add_screenshot(
        doc,
        "portal_01_landing_page.png",
        "Figure 2.1: Public Landing Page featuring Australian Fair-Trade Mission & Direct Portal Entry",
        width_inches=6.0
    )

    add_heading_2(doc, "2.2 Stakeholder Account Registration (register.html)")
    add_body_paragraph(
        doc,
        "New stakeholders register via register.html. Depending on the selected role, the interface dynamically displays pertinent metadata fields required for verification:"
    )
    add_bullet_point(doc, "Full Name & Legal Business Entity Name", "• ")
    add_bullet_point(doc, "Registered Email Address & Australian Mobile Phone (e.g., 0412 345 678)", "• ")
    add_bullet_point(doc, "Secure Account Password (minimum 6 alphanumeric characters)", "• ")
    add_bullet_point(doc, "Role Selection: Farmer, Wholesaler, Logistics Driver, or Consumer", "• ")
    add_bullet_point(doc, "Role-Specific Geographic Metadata (Farm Location for growers; Commercial Warehouse Location for wholesalers; Delivery Address for consumers)", "• ")
    add_screenshot(
        doc,
        "portal_03_register_page.png",
        "Figure 2.2: Stakeholder Registration Portal with Dynamic Role-Based Metadata Fields",
        width_inches=6.0
    )

    add_heading_2(doc, "2.3 Authentication & 1-Click Demo Testing Toolbar (login.html)")
    add_body_paragraph(
        doc,
        "To facilitate rapid User Acceptance Testing (UAT) and operational evaluation without manual credential setup, AgriTrace features an integrated 1-Click Demo Login bar directly on login.html. Clicking any demo button automatically injects seeded credentials and executes secure authentication."
    )
    add_callout(
        doc,
        "Uniform Demo Password: password123\nAll pre-seeded Australian stakeholder accounts utilize the uniform password 'password123'. Clicking any demo toolbar button instantly logs into the selected role environment.",
        "Quick Access Security Key",
        "success"
    )

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

    add_screenshot(
        doc,
        "portal_02_login_page.png",
        "Figure 2.3: Authentication Login Portal with Integrated 1-Click Demo Toolbar and Form Validation",
        width_inches=6.0
    )

    # =========================================================================
    # 3. FARMER OPERATIONS MANUAL
    # =========================================================================
    add_heading_1(doc, "3. Small Farmer Operations Manual (farmer/)")
    add_body_paragraph(
        doc,
        "The Farmer Portal provides small producers, family-run orchards, and regional agricultural cooperatives with direct market access, eliminating middlemen broker commissions. Growers control their own produce catalog, publish seasonal harvest batches in AUD, and track inbound purchase orders in real time."
    )

    add_heading_2(doc, "3.1 Farmer Operations Dashboard (farmer/dashboard.html)")
    add_body_paragraph(
        doc,
        "Upon successful login, the farmer lands on their central telemetry dashboard displaying real-time metrics:"
    )
    add_bullet_point(doc, "Active Produce Listings: Total harvest batches currently live on the public marketplace.", "• ")
    add_bullet_point(doc, "Pending Inbound Orders: Orders placed by consumers awaiting harvest and packaging confirmation.", "• ")
    add_bullet_point(doc, "Gross Farm Revenue ($ AUD): Total cumulative funds earned from fulfilled orders.", "• ")
    add_bullet_point(doc, "Operational Quick Links: Direct navigation to batch creation and fulfillment queues.", "• ")

    add_screenshot(
        doc,
        "farmer_01_dashboard.png",
        "Figure 3.1: Farmer Operations Command Center & Inventory Telemetry (Jack Miller, Yarra Valley VIC)",
        width_inches=6.0
    )

    add_heading_2(doc, "3.2 Listing Fresh Harvest Batches (farmer/products.html)")
    add_body_paragraph(
        doc,
        "To publish a new harvest batch to the marketplace, the farmer follows these sequential steps:"
    )
    add_bullet_point(doc, "Navigate to 'Produce Catalog' (farmer/products.html) from the sidebar.", "Step 1: ")
    add_bullet_point(doc, "Click the '+ Add Produce' action button to trigger the modal dialog.", "Step 2: ")
    add_bullet_point(doc, "Input Produce Name (e.g. 'Yarra Valley Organic Strawberries') and select Category (Fruits, Vegetables, Grains).", "Step 3: ")
    add_bullet_point(doc, "Specify Farm-Gate Price ($ AUD) and Unit of Measure (kg, punnet, bunch, box).", "Step 4: ")
    add_bullet_point(doc, "Enter Total Batch Quantity available (e.g. 120 punnets) and Farm Origin (e.g. 'Coldstream, Yarra Valley VIC').", "Step 5: ")
    add_bullet_point(doc, "Click 'Save Produce'. The batch is immediately broadcast to the consumer marketplace with full origin transparency.", "Step 6: ")

    add_screenshot(
        doc,
        "farmer_02_products.png",
        "Figure 3.2: Farmer Produce Catalog Management with AUD Unit Pricing and Origin Tracking",
        width_inches=6.0
    )

    add_heading_2(doc, "3.3 Fulfilling & Confirming Inbound Orders (farmer/orders.html)")
    add_body_paragraph(
        doc,
        "When a consumer places an order, it appears in the farmer's inbound order queue with status 'Order Placed'. The farmer must verify produce availability and pack the items for wholesale collection."
    )
    add_bullet_point(doc, "Review the customer's delivery destination, items requested, and order timestamp.", "Step 1: ")
    add_bullet_point(doc, "Physically pick and package the harvest batch adhering to Australian food safety standards.", "Step 2: ")
    add_bullet_point(doc, "Click 'Confirm Order'. The status transitions atomically to 'Farmer Confirmed'.", "Step 3: ")
    add_bullet_point(doc, "The order automatically transfers to the Wholesaler Quality Assurance queue for biosecurity certification.", "Step 4: ")

    add_screenshot(
        doc,
        "farmer_03_orders.png",
        "Figure 3.3: Inbound Orders Queue and Batch Confirmation Workspace",
        width_inches=6.0
    )

    # =========================================================================
    # 4. WHOLESALER ACCREDITATION & AUDIT MANUAL
    # =========================================================================
    add_heading_1(doc, "4. Wholesaler Accreditation & Audit Manual (wholesaler/)")
    add_body_paragraph(
        doc,
        "Commercial wholesalers and distribution hubs act as critical quality checkpoints in the Australian agricultural supply chain. In accordance with Australian biosecurity frameworks, unvetted commercial distributors cannot certify food shipments without prior administrative accreditation."
    )

    add_screenshot(
        doc,
        "03_wholesaler_accreditation_flow.png",
        "Figure 4.1: Wholesaler Accreditation & Biosecurity Lifecycle Flowchart",
        width_inches=6.2
    )

    add_heading_2(doc, "4.1 The Unaccredited Wholesaler Experience (wholesaler.pending@example.com)")
    add_body_paragraph(
        doc,
        "Upon registration, a wholesale distributor's status is defaulted to 'Pending Approval'. When logging in with pending credentials (e.g. Matilda Evans, Melbourne Wholesale Hub), the portal enforces strict regulatory lockouts:"
    )
    add_bullet_point(doc, "Prominent amber warning banner displayed across all header views informing the user that their commercial license is under review.", "• ")
    add_bullet_point(doc, "Stock Verification controls on incoming farm orders are completely locked and disabled.", "• ")
    add_bullet_point(doc, "The wholesaler cannot verify batches, dispatch drivers, or modify order states until an Administrator grants formal approval.", "• ")

    add_callout(
        doc,
        "WARNING: Account Pending Administrator Approval\nYour wholesale business credentials must be validated by an Administrator before you can audit stock and certify farm produce shipments. The 'Verify Stock' control remains locked until approval is granted.",
        "Regulatory Biosecurity Restriction",
        "warning"
    )

    add_screenshot(
        doc,
        "wholesaler_01_pending_dashboard.png",
        "Figure 4.2: Pending Wholesaler Dashboard Displaying Regulatory Warning Banner (Matilda Evans)",
        width_inches=6.0
    )

    add_screenshot(
        doc,
        "wholesaler_02_pending_orders.png",
        "Figure 4.3: Wholesaler Quality Assurance Queue with Verification Actions Locked",
        width_inches=6.0
    )

    add_heading_2(doc, "4.2 Accredited Wholesaler Operations (wholesaler@example.com)")
    add_body_paragraph(
        doc,
        "Once verified and approved by an Administrator (e.g. Liam Wilson, Sydney Central Produce Markets), the wholesaler receives full operational privileges:"
    )
    add_bullet_point(doc, "The warning banner is replaced by an accredited badge confirming certified biosecurity status.", "• ")
    add_bullet_point(doc, "Orders in 'Farmer Confirmed' status display active 'Verify Stock' action buttons.", "• ")
    add_bullet_point(doc, "The auditor conducts physical and documentary checks: harvest date, cold storage temperature, weight tolerances, and packaging integrity.", "• ")
    add_bullet_point(doc, "Clicking 'Verify Stock' advances the order to 'Wholesaler Verified', assigning it to the Logistics Driver queue for dispatch.", "• ")

    add_screenshot(
        doc,
        "wholesaler_03_approved_dashboard.png",
        "Figure 4.4: Accredited Wholesaler Certified Command Dashboard (Liam Wilson, Sydney NSW)",
        width_inches=6.0
    )

    add_screenshot(
        doc,
        "wholesaler_04_approved_orders.png",
        "Figure 4.5: Active Produce QA Verification & Batch Certification Workspace",
        width_inches=6.0
    )

    # =========================================================================
    # 5. LOGISTICS & COLD-CHAIN DRIVER MANUAL
    # =========================================================================
    add_heading_1(doc, "5. Logistics & Cold-Chain Driver Manual (driver/)")
    add_body_paragraph(
        doc,
        "Logistics drivers maintain physical custody and cold-chain integrity across regional highways and metropolitan delivery routes (e.g. Lucas Brown, Outback Cold Logistics). The Driver Portal operates seamlessly on mobile and desktop browsers to record transit checkpoints."
    )

    add_heading_2(doc, "5.1 Driver Fleet Dashboard (driver/dashboard.html)")
    add_body_paragraph(
        doc,
        "The driver dashboard summarizes active route assignments, shipments currently in transit, and total delivered packages for the shift."
    )
    add_screenshot(
        doc,
        "driver_01_dashboard.png",
        "Figure 5.1: Logistics Driver Fleet Operations & Milestone Telemetry (Lucas Brown)",
        width_inches=6.0
    )

    add_heading_2(doc, "5.2 Executing Transit Milestone Checkpoints (driver/deliveries.html)")
    add_body_paragraph(
        doc,
        "The driver moves each verified shipment through three mandatory physical transit checkpoints:"
    )
    add_bullet_point(doc, "Checkpoint 1 - 'Mark as Picked Up': Clicked when the refrigerated vehicle collects certified produce from the regional farm or distribution hub. Sets status to 'Picked Up'.", "1. ")
    add_bullet_point(doc, "Checkpoint 2 - 'Mark as In Transit': Clicked upon departure from the central depot onto transit corridors. Sets status to 'In Transit'.", "2. ")
    add_bullet_point(doc, "Checkpoint 3 - 'Confirm Delivery': Clicked upon physical handover at the consumer's delivery address. Sets status to 'Delivered' and concludes custody tracking.", "3. ")

    add_screenshot(
        doc,
        "driver_02_deliveries.png",
        "Figure 5.2: Real-Time Transit Delivery Queue and Checkpoint Execution Controls",
        width_inches=6.0
    )

    # =========================================================================
    # 6. DIRECT CONSUMER MARKETPLACE MANUAL
    # =========================================================================
    add_heading_1(doc, "6. Direct Consumer Marketplace & Transparency Manual (customer/)")
    add_body_paragraph(
        doc,
        "AgriTrace enables Australian consumers to discover genuine regional harvests, purchase directly from family growers, inspect farm provenance, and track orders across 7 transparent milestones."
    )

    add_heading_2(doc, "6.1 Consumer Account Dashboard (customer/dashboard.html)")
    add_body_paragraph(
        doc,
        "The consumer dashboard provides quick access to recent orders, shopping cart status, and submitted farm feedback ratings."
    )
    add_screenshot(
        doc,
        "customer_01_dashboard.png",
        "Figure 6.1: Consumer Account Dashboard & Recent Order Summary (Chloe Taylor, Melbourne VIC)",
        width_inches=6.0
    )

    add_heading_2(doc, "6.2 Discovering Regional Australian Produce (customer/products.html)")
    add_body_paragraph(
        doc,
        "Shoppers browse active listings filtered by category and origin. Every item clearly displays its regional Australian origin badge (e.g. 'Goulburn Valley VIC', 'Bowen QLD', 'Barossa Valley SA') alongside transparent AUD unit pricing."
    )
    add_screenshot(
        doc,
        "customer_02_products.png",
        "Figure 6.2: Fresh Australian Produce Marketplace with Origin Provenance & Category Filters",
        width_inches=6.0
    )

    add_heading_2(doc, "6.3 Shopping Cart & Fair-Trade Checkout (customer/cart.html)")
    add_body_paragraph(
        doc,
        "Shoppers can review cart items, adjust quantities, verify farm sources, and execute fair-trade checkout. The system atomically reserves stock in Firestore and creates an order in 'Order Placed' status."
    )
    add_screenshot(
        doc,
        "customer_03_cart.png",
        "Figure 6.3: Shopping Cart & Fair-Trade Checkout Workspace with Itemized AUD Pricing",
        width_inches=6.0
    )

    add_heading_2(doc, "6.4 7-Stage Live Order Provenance Tracking (customer/orders.html)")
    add_body_paragraph(
        doc,
        "On 'My Orders', the customer can observe real-time progress indicators highlighting each completed stage in the custody pipeline: Order Placed -> Farmer Confirmed -> Wholesaler Verified -> Picked Up -> In Transit -> Out for Delivery -> Delivered."
    )
    add_screenshot(
        doc,
        "customer_04_orders.png",
        "Figure 6.4: 7-Stage Live Order Provenance and Real-Time Custody Tracker",
        width_inches=6.0
    )

    add_heading_2(doc, "6.5 Submitting Farmer Quality Feedback (customer/feedback.html)")
    add_body_paragraph(
        doc,
        "Once an order is marked 'Delivered', the customer can submit an authentic 1-to-5 star quality rating and review comment. Ratings link directly to the grower's profile, fostering long-term consumer trust."
    )
    add_screenshot(
        doc,
        "customer_05_feedback.png",
        "Figure 6.5: Fair-Trade Farmer Quality Rating & Review Submission Form",
        width_inches=6.0
    )

    # =========================================================================
    # 7. SYSTEM ADMINISTRATOR GOVERNANCE MANUAL
    # =========================================================================
    add_heading_1(doc, "7. System Administrator Governance & Compliance Manual (admin/)")
    add_body_paragraph(
        doc,
        "The Administrator Portal serves as the central command bridge for platform governance, regulatory biosecurity accreditation, dispute resolution, user registry oversight, and financial feasibility auditing."
    )

    add_screenshot(
        doc,
        "04_admin_governance_architecture.png",
        "Figure 7.1: Multi-Module Administrative Governance Architecture",
        width_inches=6.2
    )

    add_heading_2(doc, "7.1 Admin Command Center & Live Telemetry (admin/dashboard.html)")
    add_body_paragraph(
        doc,
        "The main dashboard provides high-level platform telemetry: total registered stakeholders, pending wholesaler accreditation queues, active produce listings, and cumulative gross merchandise volume (GMV) in AUD."
    )
    add_screenshot(
        doc,
        "admin_01_dashboard.png",
        "Figure 7.2: Central Administration Command Center & Platform Metrics Telemetry",
        width_inches=6.0
    )

    add_heading_2(doc, "7.2 Wholesaler Accreditation & Approvals Hub (admin/approvals.html)")
    add_body_paragraph(
        doc,
        "This critical governance module displays all registered wholesale entities awaiting biosecurity vetting. The Administrator can inspect legal trading names, business premises, and phone records before executing 1-click approvals or revoking credentials if standards are breached."
    )
    add_bullet_point(doc, "Review Pending Applications: Displays unaccredited wholesalers with amber badges.", "• ")
    add_bullet_point(doc, "Click 'Approve Wholesaler': Instantly grants full stock verification permissions in Firestore.", "• ")
    add_bullet_point(doc, "Revoke Accreditation: If compliance issues arise, clicking 'Revoke' immediately locks the wholesaler's verification capabilities.", "• ")

    add_screenshot(
        doc,
        "admin_02_approvals.png",
        "Figure 7.3: Wholesaler Accreditation & Regulatory Approvals Management Hub",
        width_inches=6.0
    )

    add_heading_2(doc, "7.3 Master Stakeholder User Directory (admin/users.html)")
    add_body_paragraph(
        doc,
        "The User Management console lists every stakeholder profile across all roles (Farmer, Wholesaler, Driver, Customer, Admin). Administrators can filter by role, audit contact phone numbers, and verify registration timestamps."
    )
    add_screenshot(
        doc,
        "admin_03_users.png",
        "Figure 7.4: Master Stakeholder Registry and Role Management Workspace",
        width_inches=6.0
    )

    add_heading_2(doc, "7.4 Global Product Catalog & Biosecurity Audit (admin/products.html)")
    add_body_paragraph(
        doc,
        "Administrators can audit all produce batches listed on the platform to prevent fraudulent origin claims, monitor fair AUD farm-gate pricing, and verify that produce origins comply with Australian state biosecurity regulations."
    )
    add_screenshot(
        doc,
        "admin_04_products.png",
        "Figure 7.5: Global Produce Catalog Audit & Biosecurity Verification Ledger",
        width_inches=6.0
    )

    add_heading_2(doc, "7.5 Master Supply Chain Order Audit Ledger (admin/orders.html)")
    add_body_paragraph(
        doc,
        "The Master Order Ledger records every commercial transaction across the platform, displaying current lifecycle status, purchasing customer, grower entity, order total in AUD, and full timestamp history."
    )
    add_screenshot(
        doc,
        "admin_05_orders.png",
        "Figure 7.6: Master Supply Chain Transaction & Custody Audit Ledger",
        width_inches=6.0
    )

    add_heading_2(doc, "7.6 Commercial Evaluation & Financial Telemetry (admin/evaluation.html)")
    add_body_paragraph(
        doc,
        "The administrative financial evaluation module analyzes platform profitability, operating expenditures, and serverless hosting fees against four primary commercial revenue streams:"
    )
    add_bullet_point(doc, "Commercial Wholesaler Accreditation Fee: $299 AUD annual audit certification.", "1. ")
    add_bullet_point(doc, "Farmer Cooperative SaaS Subscription: $49 AUD monthly farm management fee.", "2. ")
    add_bullet_point(doc, "Fair-Trade Transaction Commission: 3.5% transaction levy (compared to 50%+ duopoly markups).", "3. ")
    add_bullet_point(doc, "Enterprise Provenance API Access: $450 AUD monthly quota for institutional food distributors.", "4. ")

    add_screenshot(
        doc,
        "admin_06_evaluation.png",
        "Figure 7.7: Administrative Commercial Evaluation & Operational Expenditure Telemetry",
        width_inches=6.0
    )

    add_screenshot(
        doc,
        "05_commercial_revenue_model.png",
        "Figure 7.8: Commercial Revenue Flow & Multi-Stream Monetization Model",
        width_inches=6.2
    )

    # =========================================================================
    # 8. OPERATIONAL TROUBLESHOOTING & SUPPORT MATRIX
    # =========================================================================
    add_heading_1(doc, "8. Operational Troubleshooting & Support Matrix")
    add_body_paragraph(
        doc,
        "This section outlines rapid diagnostic and corrective procedures for common operational scenarios encountered by platform users."
    )

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
    print(f"Successfully generated comprehensive User Manual: {output_path}")

if __name__ == "__main__":
    build_usermanual_doc()
