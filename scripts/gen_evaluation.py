import os
import sys
from docx.shared import Inches, Pt, RGBColor
from doc_utils import (
    init_document, add_title_header, add_heading_1, add_heading_2, add_heading_3,
    add_body_paragraph, add_bullet_point, add_callout, add_diagram_box,
    add_styled_table, add_screenshot
)

def build_evaluation_doc():
    doc = init_document("Commercial Evaluation & Financial Feasibility Report", "Financial Evaluation")
    add_title_header(
        doc,
        title="Project Commercial Evaluation & Financial Revenue Realization",
        subtitle="Comprehensive financial feasibility report detailing platform charges, real money revenue streams, CAPEX development expenditures, ongoing OPEX, and small farm ROI in Australian Dollars ($ AUD).",
        category_tag="Commercial Feasibility & Financial Model"
    )

    # 1. Executive Summary: Real Money Realization
    add_heading_1(doc, "1. Executive Summary & The Core Financial Question")
    add_body_paragraph(
        doc,
        "A critical question for investors, cooperative leaders, and government grant evaluators is: 'How much real money will this platform generate, what are the platform charges, and how do we sustain commercial profitability while empowering small family farms?'"
    )
    add_body_paragraph(
        doc,
        "AgriTrace operates on a sustainable multi-stream revenue model in Australian Dollars ($ AUD). By eliminating predatory supermarket middlemen (who capture 50–60% markups), AgriTrace charges modest, transparent utility fees that generate strong recurring operational profit while increasing small farmer take-home earnings by +36%."
    )

    summary_headers = ["Key Financial Metric", "Value (AUD $)", "Strategic Meaning"]
    summary_rows = [
        ["Initial Development Cost (CAPEX)", "$75,400 AUD", "One-time complete software build and testing budget"],
        ["Monthly Cloud & Operating Cost (OPEX)", "$1,790 AUD / month", "Recurring Firebase, domain, security, and ops run-rate"],
        ["Monthly Gross Revenue Inflow", "$9,812.50 AUD / month", "Real money collected across 4 diversified platform revenue streams"],
        ["Monthly Net Cash Profit", "$8,022.50 AUD / month", "Net operating profit after deducting all cloud and operational expenses"],
        ["Annual Net Recurring Profit", "$96,270 AUD / year", "Sustained net cash flow generated at initial regional capacity"],
        ["Commercial Payback Period", "9.4 Months", "Time required to fully recoup initial $75,400 AUD CAPEX"],
        ["Farmer Margin Uplift", "+36% Net Gain", "Additional profit captured by small growers vs. supermarket duopolies"]
    ]
    add_styled_table(doc, summary_headers, summary_rows, [2.2, 1.8, 2.5])

    add_screenshot(doc, "14_browser_evaluation_report.png", "AgriTrace Project Financial Evaluation Report Interface (evaluation-report.html)")

    # 2. Platform Charges & Monetization Breakdown
    add_heading_1(doc, "2. Platform Charge Streams: How Real Money is Earned")
    add_body_paragraph(
        doc,
        "The platform does not rely on intrusive advertising or data brokerage. Revenue is earned through four transparent commercial charges:"
    )

    add_heading_2(doc, "Charge Stream 1: Fair-Trade Transaction Commission (2.5%)")
    add_body_paragraph(
        doc,
        "A 2.5% fair-trade processing fee is applied to the gross merchandise value (GMV) of every produce batch sold through the customer marketplace. Compared to the 50–60% deductions taken by major supermarket chains (Coles and Woolworths), a 2.5% transparent fee is universally embraced by growers."
    )
    add_bullet_point(doc, "Average Regional Order Size: $45.00 AUD (e.g. 2 punnets strawberries, 1kg carrots, avocados, honey).", "Calculation: ")
    add_bullet_point(doc, "Monthly Transaction Volume: 1,500 customer orders across 20 participating Victorian family farms.", "Volume: ")
    add_bullet_point(doc, "Monthly Gross Merchandise Value (GMV): 1,500 orders × $45.00 = $67,500.00 AUD.", "Gross GMV: ")
    add_bullet_point(doc, "Real Money Revenue: $67,500 × 2.5% = $1,687.50 AUD / month ($20,250 AUD / year).", "Platform Take: ")

    add_heading_2(doc, "Charge Stream 2: Wholesaler Commercial Accreditation Fee ($120 AUD / mo)")
    add_body_paragraph(
        doc,
        "Accredited commercial wholesalers pay a monthly subscription fee for access to the verified grower directory, automated batch quality certificates, and priority logistics routing."
    )
    add_bullet_point(doc, "Standard Wholesaler Monthly Fee: $120.00 AUD / month (or $1,200 AUD / year billed annually).", "Pricing: ")
    add_bullet_point(doc, "Participating Accredited Wholesalers: 25 commercial regional distributors (Melbourne, Sydney, Geelong).", "Client Base: ")
    add_bullet_point(doc, "Real Money Revenue: 25 wholesalers × $120.00 = $3,000.00 AUD / month ($36,000 AUD / year).", "Platform Take: ")

    add_heading_2(doc, "Charge Stream 3: Farm Cooperative Enterprise SaaS Tiers")
    add_body_paragraph(
        doc,
        "To ensure fair access, micro-farms pay nothing. Larger family farms and regional cooperatives subscribe to advanced SaaS tools for batch traceability, temperature sensor telemetry, and export reporting:"
    )
    add_bullet_point(doc, "Micro Grower Tier (Under $2,000 AUD/mo GMV): $0 / month (Free entry tier).", "Tier 1: ")
    add_bullet_point(doc, "Commercial Family Farm Tier: $49.00 AUD / month. 30 subscribing commercial farms = $1,470.00 AUD / month.", "Tier 2: ")
    add_bullet_point(doc, "Regional Cooperative Hub Tier: $149.00 AUD / month. 20 subscribing regional cooperatives = $2,980.00 AUD / month.", "Tier 3: ")
    add_bullet_point(doc, "Real Money Revenue: $1,470 + $2,980 = $4,450.00 AUD / month ($53,400 AUD / year).", "Platform Take: ")

    add_heading_2(doc, "Charge Stream 4: Cold-Chain Logistics Coordination Fee (1.0%)")
    add_body_paragraph(
        doc,
        "Refrigerated freight partners utilize AgriTrace dispatch tools for cold-chain proof of delivery, paying a 1.0% digital coordination fee on all managed freight movements."
    )
    add_bullet_point(doc, "Monthly Freight Movement Turnover: $67,500.00 AUD managed delivery volume.", "Base: ")
    add_bullet_point(doc, "Real Money Revenue: $67,500 × 1.0% = $675.00 AUD / month ($8,100 AUD / year).", "Platform Take: ")

    # Monthly Summary Table
    add_heading_2(doc, "Summary of Monthly Inflow (Real Money)")
    stream_headers = ["Charge Stream", "Pricing Structure", "Monthly Volume / Subscriptions", "Gross Revenue (AUD $)"]
    stream_rows = [
        ["Fair-Trade Transaction Fee", "2.5% of GMV", "$67,500 GMV (1,500 orders)", "$1,687.50 AUD"],
        ["Wholesaler Accreditation Fee", "$120.00 AUD / month", "25 commercial distributors", "$3,000.00 AUD"],
        ["Farm Cooperative SaaS Tiers", "$49 / $149 AUD / month", "30 farms + 20 cooperatives", "$4,450.00 AUD"],
        ["Cold-Chain Logistics Coordination", "1.0% dispatch fee", "$67,500 logistics volume", "$675.00 AUD"],
        ["TOTAL MONTHLY REVENUE", "Consolidated Inflow", "All Revenue Channels", "$9,812.50 AUD / mo"]
    ]
    add_styled_table(doc, stream_headers, stream_rows, [2.1, 1.7, 1.6, 1.1])

    # 3. Development Expenditures (CAPEX)
    add_heading_1(doc, "3. Initial Capital Expenditure (CAPEX) — Total: $75,400 AUD")
    add_body_paragraph(
        doc,
        "Initial software development, security hardening, user experience design, and testing were costed based on prevailing Australian engineering contractor rates ($120 AUD/hr):"
    )

    capex_headers = ["Development Phase", "Deliverables & Scope", "Effort", "Cost (AUD $)"]
    capex_rows = [
        ["System Architecture & Design", "Database schema, security models, biosecurity compliance", "70 hrs", "$8,400 AUD"],
        ["UI/UX Design & Prototyping", "Responsive design system, WCAG 2.1 AA accessibility", "50 hrs", "$6,000 AUD"],
        ["Core Software Engineering", "5 stakeholder portals, real-time Firestore tracking, auth guards", "240 hrs", "$28,800 AUD"],
        ["Quality Assurance & Audit Suite", "31 automated tests (Unit, System, UAT, SEO audit)", "128 hrs", "$15,400 AUD"],
        ["Australian Regional Seed & Docs", "seed.html, User Manual, Installation Manual, Site Map", "60 hrs", "$7,200 AUD"],
        ["Contingency & Deployment Buffer", "15% technical buffer for production hardening", "80 hrs", "$9,600 AUD"],
        ["TOTAL DEVELOPMENT (CAPEX)", "Full Production Turnkey Release", "628 hrs", "$75,400 AUD"]
    ]
    add_styled_table(doc, capex_headers, capex_rows, [1.9, 2.5, 0.9, 1.2])

    # 4. Recurring Operating Costs (OPEX)
    add_heading_1(doc, "4. Monthly Recurring Operating Costs (OPEX) — Total: $1,790 AUD / mo")
    add_body_paragraph(
        doc,
        "AgriTrace operates serverless architecture, drastically minimizing fixed monthly overheads:"
    )

    opex_headers = ["Operating Expense Item", "Vendor / Provider", "Monthly Cost (AUD $)", "Annual Cost (AUD $)"]
    opex_rows = [
        ["Cloud Hosting & Firestore Database", "Google Cloud / Firebase Blaze (Sydney region)", "$420.00 AUD", "$5,040 AUD"],
        ["Domain Name & Automated SSL", "Australian .com.au registrar + Cloudflare DNS", "$20.00 AUD", "$240 AUD"],
        ["Application Telemetry & Sentry", "Sentry Performance & Error Tracking", "$150.00 AUD", "$1,800 AUD"],
        ["Quarterly Security & Biosecurity Audit", "Australian independent cybersecurity firm", "$450.00 AUD", "$5,400 AUD"],
        ["Part-Time DevOps & Operations Support", "System administration, database backups, support", "$750.00 AUD", "$9,000 AUD"],
        ["TOTAL MONTHLY OPEX", "All Infrastructure & Operating Services", "$1,790.00 AUD / mo", "$21,480 AUD / yr"]
    ]
    add_styled_table(doc, opex_headers, opex_rows, [2.2, 2.0, 1.2, 1.1])

    # 5. Profit & Loss Statement (P&L) and 3-Year Projections
    add_heading_1(doc, "5. Profit & Loss (P&L) Statement & 3-Year Growth Projections")
    add_body_paragraph(
        doc,
        "Below is the commercial 3-year financial model detailing platform expansion from initial Victorian rollout to national Australian adoption:"
    )

    pnl_headers = ["Financial Item", "Year 1 (Regional VIC)", "Year 2 (VIC + NSW)", "Year 3 (National Australia)"]
    pnl_rows = [
        ["Participating Family Farms", "50 Farms", "180 Farms", "500 Farms"],
        ["Accredited Wholesalers", "25 Wholesalers", "75 Wholesalers", "180 Wholesalers"],
        ["Annual Gross Merchandise Value (GMV)", "$810,000 AUD", "$3,240,000 AUD", "$10,800,000 AUD"],
        ["Transaction Fees (2.5%)", "$20,250 AUD", "$81,000 AUD", "$270,000 AUD"],
        ["Wholesaler Subscriptions", "$36,000 AUD", "$108,000 AUD", "$259,200 AUD"],
        ["Farm SaaS Subscriptions", "$53,400 AUD", "$165,000 AUD", "$420,000 AUD"],
        ["Logistics Coordination Fees", "$8,100 AUD", "$32,400 AUD", "$108,000 AUD"],
        ["GROSS ANNUAL REVENUE", "$117,750 AUD", "$386,400 AUD", "$1,057,200 AUD"],
        ["Less: Annual OPEX Infrastructure", "($21,480 AUD)", "($48,000 AUD)", "($120,000 AUD)"],
        ["NET OPERATING CASH PROFIT", "$96,270 AUD", "$338,400 AUD", "$937,200 AUD"]
    ]
    add_styled_table(doc, pnl_headers, pnl_rows, [2.3, 1.4, 1.4, 1.4])

    # 6. Farmer Economic ROI
    add_heading_1(doc, "6. Small Family Farm Economic Impact & Payback")
    add_body_paragraph(
        doc,
        "The economic benefit to small family producers is profound:"
    )
    add_bullet_point(doc, "Supermarket Duopoly Baseline: A small strawberry grower in the Yarra Valley typically receives $2.20 AUD per 500g punnet from duopoly buyers, while retail consumers are charged $6.50 AUD (Grower margin: ~33%).", "Supermarket Model: ")
    add_bullet_point(doc, "AgriTrace Direct Model: The grower lists at $4.60 AUD per punnet. The consumer pays $5.50 AUD (cheaper than supermarkets). After the 2.5% platform fee ($0.11 AUD), the farmer nets $4.49 AUD per punnet — a +104% increase in net revenue per unit.", "AgriTrace Model: ")
    add_bullet_point(doc, "Annual Farm Income Gain: An average family producer harvesting 8,000 units annually gains +$18,320 AUD in additional net profit, completely transforming rural farm viability.", "Net Farmer Gain: ")

    add_screenshot(doc, "17_browser_admin_financial_eval.png", "Administrator In-Portal Financial Evaluation Dashboard (admin/evaluation.html)")
    add_screenshot(doc, "16_browser_admin_dashboard.png", "Administrator Platform Dashboard Tracking Cumulative Revenue in Australian Dollars")

    output_path = os.path.join("docx", "evaluation_report.docx")
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    build_evaluation_doc()
