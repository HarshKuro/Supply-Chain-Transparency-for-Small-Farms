import os
import sys
from docx.shared import Inches, Pt, RGBColor
from doc_utils import (
    init_document, add_title_header, add_heading_1, add_heading_2, add_heading_3,
    add_body_paragraph, add_bullet_point, add_callout,
    add_styled_table, add_screenshot
)

def build_usermanual_doc():
    doc = init_document("Stakeholder User Manual", "Operational Manual")
    add_title_header(
        doc,
        title="Multi-Stakeholder Operational User Manual",
        subtitle="Comprehensive operational handbook and step-by-step procedures for Farmers, Wholesalers, Logistics Drivers, Consumers, and Administrators.",
        category_tag="User Operations Guide"
    )

    # 1. Platform Purpose & Overview
    add_heading_1(doc, "1. Platform Mission & Australian Agricultural Context")
    add_body_paragraph(
        doc,
        "AgriTrace is a decentralized digital transparency platform engineered specifically for Australian family farms, regional cooperatives, accredited commercial distributors, and direct consumers. Traditional supermarket duopolies take up to 60% markups while obscuring farm provenance. AgriTrace restores transparency and fair trade by recording every physical handover in the supply chain."
    )
    
    # Embedded visual infographic
    add_screenshot(doc, "supply_chain_infographic.jpg", "Australian Fair Trade Agricultural Supply Chain Overview (Farm to Doorstep)", width_inches=6.0)

    # Embedded custody workflow diagram
    add_screenshot(doc, "flow_supply_chain_custody.png", "7-Stage Digital Custody Verification Sequence Flowchart", width_inches=6.2)

    add_body_paragraph(
        doc,
        "This manual details how each stakeholder operates their dedicated web portal, executes stage-specific actions, and contributes to the permanent custody ledger."
    )

    # 2. Quick Demo Credentials & 1-Click Login
    add_heading_1(doc, "2. Quick Test Credentials & 1-Click Demo Bar")
    add_body_paragraph(
        doc,
        "To allow instant user acceptance testing without manual credential registration, AgriTrace features an integrated 1-Click Demo Login bar directly on login.html. All test accounts are pre-seeded with Australian regional profiles and utilize the uniform test password:"
    )

    add_callout(
        doc,
        "Uniform Demo Password for all seeded stakeholder accounts: password123\nClicking any demo button on login.html immediately auto-fills the credentials and initiates the authenticated session.",
        "Quick Access Security Key",
        "success"
    )

    cred_headers = ["Role Domain", "Stakeholder Entity", "Test Email", "Initial Account Status"]
    cred_rows = [
        ["🛡️ Administrator", "AgriTrace Admin (Canberra ACT)", "admin@example.com", "Full Platform Governance"],
        ["🌾 Small Farmer", "Jack Miller (Yarra Valley Harvests VIC)", "farmer@example.com", "Active Catalog & Orders"],
        ["🏢 Wholesaler (Approved)", "Liam Wilson (Sydney Central Markets NSW)", "wholesaler@example.com", "Accredited for QA Verification"],
        ["⏳ Wholesaler (Pending)", "Matilda Evans (Melbourne Produce Hub VIC)", "wholesaler.pending@example.com", "Pending Admin Approval (Locked)"],
        ["🚚 Transit Driver", "Lucas Brown (Outback Cold Logistics)", "driver@example.com", "Active Route Queue"],
        ["🛒 Direct Consumer", "Chloe Taylor (Melbourne VIC)", "customer@example.com", "Cart & Order Tracking"]
    ]
    add_styled_table(doc, cred_headers, cred_rows, [1.4, 2.0, 1.8, 1.3])

    add_screenshot(doc, "19_browser_login_demo_buttons.png", "1-Click Demo Login Toolbar on login.html Providing Immediate Access to All Roles", width_inches=6.0)
    add_screenshot(doc, "08_browser_login_portal.png", "Secure Authentication Portal with High-Contrast Responsive Controls", width_inches=6.0)

    # 3. Farmer Manual
    add_heading_1(doc, "3. Farmer Operations Manual (farmer/)")
    add_body_paragraph(
        doc,
        "The Farmer Portal empowers small producers to manage product catalogs, set fair farm-gate pricing in Australian Dollars ($ AUD), and confirm order preparation."
    )
    add_heading_2(doc, "Step 3.1: Listing Fresh Harvest Batches")
    add_bullet_point(doc, "Navigate to 'Produce Catalog' (farmer/products.html) via the sidebar.", "1. ")
    add_bullet_point(doc, "Click '+ Add New Produce' to launch the batch modal.", "2. ")
    add_bullet_point(doc, "Specify Produce Name (e.g., 'Yarra Valley Strawberries'), Category (Fruit/Vegetable/Grains), Batch Quantity (e.g., 250), Unit (kg/punnet/bunch), and Farm-Gate Price in AUD (e.g., 6.50).", "3. ")
    add_bullet_point(doc, "Enter Farm Origin details (e.g., 'Coldstream, Yarra Valley VIC') to ensure consumer transparency.", "4. ")
    add_bullet_point(doc, "Click 'Save Produce'. The item immediately enters the active marketplace.", "5. ")

    add_heading_2(doc, "Step 3.2: Confirming Inbound Consumer Orders")
    add_bullet_point(doc, "When an order arrives, open 'Incoming Orders' (farmer/orders.html).", "1. ")
    add_bullet_point(doc, "Inspect the item breakdown, quantities reserved, and customer destination.", "2. ")
    add_bullet_point(doc, "Once produce is picked and packaged, click 'Confirm Order'.", "3. ")
    add_bullet_point(doc, "The order status transitions to 'Farmer Confirmed' and automatically routes into the Wholesaler Quality Audit queue.", "4. ")

    # 4. Wholesaler Manual
    add_heading_1(doc, "4. Wholesaler Accreditation & Audit Manual (wholesaler/)")
    add_body_paragraph(
        doc,
        "Wholesalers serve as accredited quality auditors in the Australian supply chain. Under Australian biosecurity standards, unaccredited entities are prohibited from certifying produce."
    )
    add_heading_2(doc, "The Mandatory Accreditation Gate")
    add_body_paragraph(
        doc,
        "Upon initial registration, a wholesaler's status is set to 'Pending Approval'. If you log in with unaccredited credentials (e.g. wholesaler.pending@example.com), the system renders an amber warning banner:"
    )
    add_callout(
        doc,
        "WARNING: Account Pending Administrator Approval\nYour wholesale business credentials must be validated by an Administrator before you can audit stock and certify farm produce shipments. The 'Verify Stock' control remains locked until approval is granted.",
        "Regulatory Biosecurity Restriction",
        "warning"
    )

    add_heading_2(doc, "Step 4.1: Stock Verification (Accredited Wholesalers)")
    add_bullet_point(doc, "Log in with an approved wholesaler account (wholesaler@example.com).", "1. ")
    add_bullet_point(doc, "Navigate to 'Stock Verification' (wholesaler/orders.html).", "2. ")
    add_bullet_point(doc, "Orders in 'Farmer Confirmed' status are listed with batch numbers, quantities, and origin farm.", "3. ")
    add_bullet_point(doc, "Conduct physical/digital quality inspection against Australian grade standards.", "4. ")
    add_bullet_point(doc, "Click 'Verify Stock'. The order transitions to 'Wholesaler Verified' and dispatches to logistics drivers.", "5. ")

    # 5. Logistics Driver Manual
    add_heading_1(doc, "5. Logistics & Cold-Chain Driver Manual (driver/)")
    add_body_paragraph(
        doc,
        "Drivers maintain physical custody between the farm/hub and the consumer's doorstep, updating milestone checkpoints in real time."
    )
    add_bullet_point(doc, "View Dispatch Queue (driver/deliveries.html): Lists all orders verified by wholesalers ready for transport.", "Step 1: ")
    add_bullet_point(doc, "Trigger 'Pickup': Click 'Mark as Picked Up' upon loading produce into the refrigerated vehicle.", "Step 2: ")
    add_bullet_point(doc, "Trigger 'In Transit': Click 'Mark as In Transit' upon departing the regional distribution hub.", "Step 3: ")
    add_bullet_point(doc, "Final Handover: Upon physical handover at the destination address, click 'Confirm Delivery'. The order completes.", "Step 4: ")

    # 6. Customer Marketplace Manual
    add_heading_1(doc, "6. Customer Marketplace & Transparency Tracking (customer/)")
    add_body_paragraph(
        doc,
        "Customers enjoy farm-fresh regional Australian harvests with full transparency on origin, price breakdown, and delivery progress."
    )
    add_heading_2(doc, "Step 6.1: Discovery & Cart Checkout")
    add_bullet_point(doc, "Browse 'Fresh Produce' (customer/products.html) filtered by regional Australian origin.", "1. ")
    add_bullet_point(doc, "Click 'Add to Cart'. Open 'Shopping Cart' (customer/cart.html) to adjust quantities.", "2. ")
    add_bullet_point(doc, "Click 'Proceed to Fair-Trade Checkout'. Stock is atomically decremented in Firestore.", "3. ")

    add_heading_2(doc, "Step 6.2: 7-Stage Live Order Tracker")
    add_body_paragraph(
        doc,
        "On 'My Orders' (customer/orders.html), the customer can track their shipment across 7 distinct visual stages: Order Placed -> Farmer Confirmed -> Wholesaler Verified -> Picked Up -> In Transit -> Out for Delivery -> Delivered."
    )

    add_heading_2(doc, "Step 6.3: Submitting Fair-Trade Feedback")
    add_body_paragraph(
        doc,
        "Once marked delivered, the customer navigates to 'Feedback & Ratings' (customer/feedback.html) to submit a 1-to-5 star rating and comment directly associated with the grower's batch."
    )

    # 7. Administrator Governance
    add_heading_1(doc, "7. System Administrator Manual (admin/)")
    add_body_paragraph(
        doc,
        "The Administrator portal provides governance, dispute resolution, financial auditing, and wholesaler accreditation management."
    )
    add_bullet_point(doc, "Wholesaler Approvals Hub (admin/approvals.html): Review pending wholesaler registrations and click 'Approve Wholesaler' or 'Revoke Accreditation'.", "Governance 1: ")
    add_bullet_point(doc, "User Directory (admin/users.html): Inspect all registered accounts, change roles, or audit contact numbers.", "Governance 2: ")
    add_bullet_point(doc, "Financial Evaluation (admin/evaluation.html): Review operational expenditures, recurring cloud fees, and farm margin improvements.", "Governance 3: ")

    add_screenshot(doc, "12_browser_user_manual.png", "Official User Manual Web Guide (user-manual.html) Featuring Sticky Navigation & Role Breakdowns", width_inches=6.0)

    output_path = os.path.join("docx", "usermanual.docx")
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    build_usermanual_doc()
