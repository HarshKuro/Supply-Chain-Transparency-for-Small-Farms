import os
import sys
from docx.shared import Inches, Pt, RGBColor
from doc_utils import (
    init_document, add_title_header, add_heading_1, add_heading_2, add_heading_3,
    add_body_paragraph, add_bullet_point, add_callout,
    add_styled_table, add_screenshot
)

def build_sitemap_doc():
    doc = init_document("System Architecture & Site Map", "System Architecture")
    add_title_header(
        doc,
        title="Interactive Site Map & Navigation Architecture",
        subtitle="A structural directory, visual flow diagrams, and user journey taxonomy for the AgriTrace platform.",
        category_tag="Site Map Specification"
    )

    # 1. Introduction & Concept
    add_heading_1(doc, "1. Executive Overview & Sitemap Definition")
    add_body_paragraph(
        doc,
        "A site map is a structured visual diagram and categorized index showing the pages on a website and how they are organized, interlinked, and connected. In modern enterprise web applications, sitemaps serve two distinct functions:"
    )
    add_bullet_point(doc, "Visual / Navigational Sitemap: Used by software architects, product managers, evaluators, and end users to understand information architecture, hierarchy, role access boundaries, and workflow trajectories.", "1. ")
    add_bullet_point(doc, "Machine-Readable XML Sitemap: Used by web search crawlers (Google, Bing) to discover public indexable URLs, canonical structures, update frequencies, and crawling priorities.", "2. ")
    add_body_paragraph(
        doc,
        "For AgriTrace Australia, the site map encompasses 18 distinct pages spanning five authenticated stakeholder domains (Farmers, Wholesalers, Drivers, Consumers, Administrators) plus public landing portals, deployment documentation, and developer utility suites."
    )

    add_callout(
        doc,
        "All internal portal routes enforce client-side role authorization guards. If an unauthorized role attempts direct URL access, the authentication router in js/auth.js intercepts the request and safely reroutes the user to their designated dashboard.",
        "Role Guarding Guarantee",
        "info"
    )

    # 2. Visual Hierarchy & Architecture Flow Diagram (REAL IMAGE)
    add_heading_1(doc, "2. Visual Hierarchy & Page Connection Flow Diagram")
    add_body_paragraph(
        doc,
        "Below is the complete visual diagram illustrating how every page connects to the entry landing page, the authentication hub, and the respective stakeholder sub-domains:"
    )

    # Embedded high-res visual image diagram (NO text signs)
    add_screenshot(doc, "flow_sitemap_hierarchy.png", "AgriTrace Complete Hierarchical Navigation & Role Routing Flow Diagram", width_inches=6.2)

    add_screenshot(doc, "11_browser_sitemap.png", "AgriTrace Interactive Site Map UI (sitemap.html) with Real-Time Search Filtering", width_inches=6.0)

    # 3. Complete Page Directory
    add_heading_1(doc, "3. Exhaustive Platform Page Catalog")
    add_body_paragraph(
        doc,
        "Every page in the AgriTrace system is categorized below with its role permission requirement, key functional modules, input parameters, and generated output:"
    )

    headers = ["Page Path", "Stakeholder Role", "Primary Capabilities", "Data Security Guard"]
    rows = [
        ["index.html", "Public / All", "Fair-trade mission, feature showcase, portal entry points", "Public Access"],
        ["login.html", "Public / All", "Email/Password login, 1-Click Australian Demo toolbar", "Auth State Guard"],
        ["register.html", "Public / All", "Role onboarding (Farmer, Wholesaler, Driver, Customer)", "Public Access"],
        ["sitemap.html", "Public / All", "Visual searchable directory of all 18 platform modules", "Public Access"],
        ["farmer/dashboard.html", "Farmer", "Active harvest counts, pending orders counter, AUD revenue", "Role: farmer"],
        ["farmer/products.html", "Farmer", "Produce batch registration, stock limits, AUD pricing", "Role: farmer"],
        ["farmer/orders.html", "Farmer", "Inbound order confirmation, dispatch preparation trigger", "Role: farmer"],
        ["wholesaler/dashboard.html", "Wholesaler", "Quality inspection metrics, accreditation status banner", "Role: wholesaler"],
        ["wholesaler/orders.html", "Wholesaler", "Inbound stock verification, batch quality certification", "Role: wholesaler (Approved)"],
        ["driver/dashboard.html", "Driver", "Active dispatches, route handover schedule, status alerts", "Role: driver"],
        ["driver/deliveries.html", "Driver", "Transit checkpoints: Picked Up -> In Transit -> Delivered", "Role: driver"],
        ["customer/dashboard.html", "Customer", "Recent order history, spending in AUD, review alerts", "Role: customer"],
        ["customer/products.html", "Customer", "Catalog exploration, farm origin transparency, add-to-cart", "Role: customer"],
        ["customer/cart.html", "Customer", "Item quantities, atomic stock deduction, checkout in AUD", "Role: customer"],
        ["customer/orders.html", "Customer", "7-stage live timeline tracker for transparent custody", "Role: customer"],
        ["customer/feedback.html", "Customer", "5-star rating submission and public farmer feedback", "Role: customer"],
        ["admin/dashboard.html", "Administrator", "Global platform telemetry, order counts, AUD turnover", "Role: admin"],
        ["admin/approvals.html", "Administrator", "Wholesaler accreditation hub (Approve / Revoke controls)", "Role: admin"],
        ["admin/users.html", "Administrator", "User registry, role elevation, wholesaler status badges", "Role: admin"],
        ["admin/products.html", "Administrator", "Global catalog audit, price & batch inspection", "Role: admin"],
        ["admin/orders.html", "Administrator", "Complete order ledger audit across all Australian nodes", "Role: admin"],
        ["admin/evaluation.html", "Administrator", "Commercial feasibility, CAPEX/OPEX model in AUD", "Role: admin"],
        ["user-manual.html", "Public / Docs", "Step-by-step operational handbook for all 5 roles", "Public Access"],
        ["installation-manual.html", "Public / Docs", "Technical setup, Firebase configuration, seed instructions", "Public Access"],
        ["evaluation-report.html", "Public / Docs", "Full commercial ROI model ($75,400 CAPEX, $1,790 OPEX)", "Public Access"],
        ["seed.html", "Developer / Admin", "One-click Australian database populator (farms, AUD items)", "Public / Dev"],
        ["test_runner.html", "Developer / QA", "Automated in-browser test runner verifying 22 assertions", "Public / Dev"]
    ]
    add_styled_table(doc, headers, rows, [1.3, 1.1, 2.7, 1.4])

    # 4. User Journey Navigation Workflows (REAL IMAGE)
    add_heading_1(doc, "4. Cross-Portal User Journey Workflows & Custody Transition")
    add_body_paragraph(
        doc,
        "The power of AgriTrace lies in the synchronized handover of custody between portals. Below is the visual custody lifecycle diagram tracing an order from farm listing to consumer fulfillment:"
    )

    # Embedded high-res visual flowchart (NO text signs)
    add_screenshot(doc, "flow_supply_chain_custody.png", "7-Stage End-to-End Supply Chain Transparency & Custody Flowchart", width_inches=6.2)

    # Embedded artistic Infographic
    add_screenshot(doc, "supply_chain_infographic.jpg", "Fair Trade Agricultural Supply Chain Overview in Australia", width_inches=6.0)

    add_screenshot(doc, "07_browser_landing_page_seo.png", "AgriTrace Landing Page (index.html) Establishing Platform Brand & Access Pathways", width_inches=6.0)

    # 5. Search Engine Discovery & Crawler Architecture
    add_heading_1(doc, "5. Search Engine Indexing Architecture (XML Sitemap & Robots.txt)")
    add_body_paragraph(
        doc,
        "In addition to the human-navigable sitemap.html, the platform incorporates strict search engine crawler directives to ensure optimal indexation and privacy compliance:"
    )
    add_bullet_point(doc, "robots.txt: Instructs compliant web crawlers (Googlebot, Bingbot) to index public storefront and documentation pages while explicitly disallowing crawling of private administrative dashboards (/admin/, /farmer/, /wholesaler/, /driver/).", "Crawler Governance: ")
    add_bullet_point(doc, "sitemap.xml: High-performance XML schema conforming to the sitemaps.org 0.9 protocol, listing canonical URLs, change frequencies (daily for store, weekly for manuals), and priority scores (1.0 for index.html, 0.8 for documentation).", "Schema Compliance: ")
    add_bullet_point(doc, "Zero Third-Party Dependency: All sitemap directives refer strictly to standardized paths without referencing staging domains or dead links.", "Domain Hygiene: ")

    add_screenshot(doc, "10_browser_seo_elements_inspection.png", "DevTools Meta Tag and Search Crawler Directive Inspection", width_inches=6.0)

    output_path = os.path.join("docx", "sitemap.docx")
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    build_sitemap_doc()
