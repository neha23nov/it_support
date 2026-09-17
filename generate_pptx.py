import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BLANK_LAYOUT = prs.slide_layouts[6]

COLOR_BG = RGBColor(15, 23, 42)        # Slate 900
COLOR_CARD = RGBColor(30, 41, 59)      # Slate 800
COLOR_PRIMARY = RGBColor(37, 99, 235)  # Blue 600
COLOR_ACCENT = RGBColor(96, 165, 250)  # Blue 400
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(148, 163, 184)  # Slate 400
COLOR_SUCCESS = RGBColor(52, 211, 153) # Emerald 400
COLOR_WARN = RGBColor(251, 191, 36)    # Amber 400
COLOR_DANGER = RGBColor(248, 113, 113) # Rose 400

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    return bg

def add_header(slide, tag, title, slide_num):
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = f"{tag.upper()}  |  SLIDE {slide_num} OF 10"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(4)

def add_card(slide, left, top, width, height, title, items, title_color=COLOR_WHITE, border_color=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.color.rgb = RGBColor(51, 65, 85)
        card.line.width = Pt(1)
        
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.22)
    tf.margin_right = Inches(0.25)
    tf.margin_bottom = Inches(0.2)
    
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(15)
    p0.font.bold = True
    p0.font.color.rgb = title_color
    
    for item in items:
        p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(8)

# -------------------------------------------------------------
# SLIDE 1: Title
# -------------------------------------------------------------
s1 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s1)

tbox1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
tf1 = tbox1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "AIONOS ASSIGNMENT 2: INTERNAL SERVICE AGENT"
p1.font.size = Pt(13)
p1.font.bold = True
p1.font.color.rgb = COLOR_ACCENT

p2 = tf1.add_paragraph()
p2.text = "Veridian Corp IT Support Agent"
p2.font.size = Pt(40)
p2.font.bold = True
p2.font.color.rgb = COLOR_WHITE
p2.space_before = Pt(12)

p3 = tf1.add_paragraph()
p3.text = "Autonomous, Policy-Grounded Internal Helpdesk built with the MERN Stack"
p3.font.size = Pt(18)
p3.font.color.rgb = COLOR_MUTED
p3.space_before = Pt(10)

p4 = tf1.add_paragraph()
p4.text = "Context: Week of 21–25 September 2026  |  Time Limit: 6 Hours  |  15-Minute Defense"
p4.font.size = Pt(13)
p4.font.color.rgb = COLOR_SUCCESS
p4.space_before = Pt(24)

# -------------------------------------------------------------
# SLIDE 2: Business Problem & Objectives
# -------------------------------------------------------------
s2 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s2)
add_header(s2, "Business Case", "Problem Statement & Solution Objectives", 2)

add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "The Operational Challenge",
         [
             "High volume of repetitive tier-1 IT tickets (guest Wi-Fi, password reset, VPN renewal).",
             "Severe security risk from employee behavior (e.g. forwarding phishing emails to colleagues).",
             "Ambiguous, vague requests stalling technician triage (e.g. 'its not working').",
             "Departmental boundary confusion (IT vs. Finance ownership for expense software and equipment)."
         ],
         COLOR_DANGER, COLOR_DANGER)

add_card(s2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
         "Agent Solution Mandate",
         [
             "Instant Self-Service Deflection: Resolves routine issues immediately without opening tickets.",
             "Strict Zero-Hallucination Grounding: Restricts all reasoning to provided policies KB-01 to KB-10.",
             "Active Safety Guardrails: Immediately halts dangerous user actions (phishing forwarding).",
             "Structured Escalation & Audit Trail: Generates standardized tickets and logs immutable rationale."
         ],
         COLOR_SUCCESS, COLOR_SUCCESS)

# -------------------------------------------------------------
# SLIDE 3: Knowledge Base & Ground Truth
# -------------------------------------------------------------
s3 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s3)
add_header(s3, "Domain Knowledge", "Veridian Corp Policy & Ground Truth Mapping", 3)

add_card(s3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(2.4),
         "Account & Access",
         [
             "KB-01: Password reset self-service anytime; locked after 5 failed tries requires manual IT unlock.",
             "KB-07: Guest Wi-Fi pass from front kiosk (24h valid, no ticket needed)."
         ],
         COLOR_ACCENT)

add_card(s3, Inches(4.85), Inches(1.8), Inches(3.6), Inches(2.4),
         "Network & Hardware",
         [
             "KB-02: VPN automatic for FTEs (90-day renewal); contractors require manager form approval.",
             "KB-03: Laptop replacement eligible after 3 yrs or verified hardware failure."
         ],
         COLOR_ACCENT)

add_card(s3, Inches(8.9), Inches(1.8), Inches(3.6), Inches(2.4),
         "Security & Assets",
         [
             "KB-09: Phishing reported immediately to security; NEVER forward to other employees.",
             "Asset Policy: Standard 4-year refresh; early replacement requires Finance sign-off."
         ],
         COLOR_ACCENT)

add_card(s3, Inches(0.8), Inches(4.5), Inches(3.6), Inches(2.3),
         "Software & Quotas",
         [
             "KB-04: Approved catalog self-installed; non-catalog takes 3-5 days security review.",
             "KB-06: Mailbox quota 25GB; archive old mail; >25GB requires manager sign-off (cap 50GB)."
         ],
         COLOR_ACCENT)

add_card(s3, Inches(4.85), Inches(4.5), Inches(3.6), Inches(2.3),
         "Hardware & WFH",
         [
             "KB-05: Printer issues require queue check and spooler restart before asset tag ticket.",
             "KB-10: Remote >3 days eligible for monitor; needs Manager + Finance approval."
         ],
         COLOR_ACCENT)

add_card(s3, Inches(8.9), Inches(4.5), Inches(3.6), Inches(2.3),
         "Cross-Dept Scope",
         [
             "KB-08: Expense tool access granted by Finance, not IT. IT only assists with credentials.",
             "Precedents TK-1042 to TK-1051: Past records guide consistency (e.g. rejecting admin access)."
         ],
         COLOR_ACCENT)

# -------------------------------------------------------------
# SLIDE 4: System Architecture (MERN Stack)
# -------------------------------------------------------------
s4 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s4)
add_header(s4, "System Architecture", "MERN Stack Design & Technical Components", 4)

add_card(s4, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "React 18 Frontend",
         [
             "Single Page Dashboard.",
             "Interactive chat feed.",
             "1-Click test buttons for all 15 employee requests (REQ-01 to REQ-15).",
             "Live Ticket Queue table.",
             "Real-time Audit Trail viewer.",
             "Knowledge Base browser."
         ],
         COLOR_ACCENT)

add_card(s4, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "Express.js REST API",
         [
             "POST /api/chat: Message triage & decision engine.",
             "GET /api/tickets: Full active & historical queue.",
             "GET /api/audit: Tamper-evident interaction logs.",
             "GET /api/policies: Ground truth policy retriever.",
             "Static asset delivery on port 5050."
         ],
         COLOR_ACCENT)

add_card(s4, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "Node.js Agent Engine",
         [
             "Intent classification & entity extraction.",
             "Deterministic security interceptor (KB-09).",
             "Policy retriever & citation generator.",
             "Ambiguity triage logic.",
             "Automated ticket routing (SLA & team assignment)."
         ],
         COLOR_ACCENT)

add_card(s4, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "Database Layer",
         [
             "Structured document state.",
             "Tickets collection (TK-1042 ... + new cases).",
             "Audit collection recording session, input, intent, action, policy, and reasoning.",
             "Persistent JSON fallback guaranteeing 100% demo reliability."
         ],
         COLOR_ACCENT)

# -------------------------------------------------------------
# SLIDE 5: Agent Decision Engine & Triage Matrix
# -------------------------------------------------------------
s5 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s5)
add_header(s5, "Agent Decision Engine", "Core Action Pathways & Operational Guardrails", 5)

add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
         "1. Self-Service Resolution (Deflection)",
         [
             "Applies when policy empowers employee self-service.",
             "Guest Wi-Fi (KB-07): 24h kiosk credentials; no ticket needed.",
             "VPN Expiry (KB-02): Guides to 90-day renewal portal self-service."
         ],
         COLOR_SUCCESS, COLOR_SUCCESS)

add_card(s5, Inches(6.9), Inches(1.8), Inches(5.6), Inches(2.3),
         "2. Diagnostic Clarification (Anti-Hallucination)",
         [
             "Triggers when request is underspecified or ambiguous.",
             "REQ-15 ('hey can you help, its not working'): Prompts for device, error message, and onset time instead of guessing."
         ],
         COLOR_WARN, COLOR_WARN)

add_card(s5, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3),
         "3. Security Guardrail Interception",
         [
             "Catches dangerous, risky user behavior immediately.",
             "REQ-08: Ananya forwarding phishing email -> Agent commands 'DO NOT forward', alerts security team, opens urgent incident ticket (KB-09)."
         ],
         COLOR_DANGER, COLOR_DANGER)

add_card(s5, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.3),
         "4. Structured Ticket Escalation",
         [
             "For issues requiring approvals, physical action, or SLAs.",
             "Non-catalog software (KB-04): Routed to Security (3-5 day SLA).",
             "Hardware failure (KB-03): Replacement ticket opened per TK-1043."
         ],
         COLOR_ACCENT, COLOR_ACCENT)

# -------------------------------------------------------------
# SLIDE 6: Handling Edge Cases & Boundaries
# -------------------------------------------------------------
s6 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s6)
add_header(s6, "Policy Edge Cases", "Cross-Departmental Scope & Governance Boundaries", 6)

add_card(s6, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
         "IT vs. Finance Boundaries",
         [
             "KB-08 (Expense Software Access): Access is granted by Finance, not IT.",
             "IT only troubleshoots credentials once the account exists.",
             "Agent actively prevents useless IT tickets by clarifying ownership with the employee."
         ],
         COLOR_ACCENT)

add_card(s6, Inches(4.85), Inches(1.8), Inches(3.6), Inches(5.0),
         "Employee vs. Contractor Rights",
         [
             "KB-02 (VPN Access): Full-time employees receive automatic VPN access.",
             "Contractors require explicit manager approval submitted via the formal Access Request Form.",
             "Agent enforces compliance before initiating VPN provisioning."
         ],
         COLOR_ACCENT)

add_card(s6, Inches(8.9), Inches(1.8), Inches(3.6), Inches(5.0),
         "Hardware Lifecycle vs. Repair",
         [
             "Aman Gupta (2-year laptop, flickering screen): Ineligible for replacement (min 3 years); routed for repair diagnostics.",
             "Aditi Sharma (3.5-year laptop, dead): Eligible for replacement under verified hardware failure (aligned with precedent TK-1043)."
         ],
         COLOR_ACCENT)

# -------------------------------------------------------------
# SLIDE 7: Complete Auditability & Transparency
# -------------------------------------------------------------
s7 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s7)
add_header(s7, "Governance & Compliance", "Explicit Source Citations & Immutable Audit Trail", 7)

add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Mandatory Source Citations",
         [
             "The agent never outputs a resolution without displaying the authoritative policy code.",
             "Examples: 'Source Policy: KB-07 (Guest Wi-Fi Access)', 'Source Policy: KB-09 (Security Incident Reporting)'.",
             "Ensures complete transparency so employees and IT managers can trace the ground truth.",
             "Eliminates ambiguity in policy interpretation."
         ],
         COLOR_ACCENT)

add_card(s7, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
         "Tamper-Evident Audit Trail",
         [
             "Every conversation turn is logged in the database collection.",
             "Recorded Fields:",
             "  • Session ID & Employee Identity",
             "  • Exact Raw User Input",
             "  • Classified Intent & Action Taken",
             "  • Policy Code Cited & Ticket ID Created",
             "  • Full Decision Rationale & Timestamp",
             "Provides supervisory oversight and compliance readiness."
         ],
         COLOR_SUCCESS)

# -------------------------------------------------------------
# SLIDE 8: Prototype Demonstration & Test Scenarios
# -------------------------------------------------------------
s8 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s8)
add_header(s8, "Verification & Testing", "Live Demonstration Scenarios (REQ-01 to REQ-15)", 8)

add_card(s8, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "REQ-02 (Self-Service)",
         [
             "Employee: Vikram Chawla.",
             "Query: Wi-Fi access for visiting guest.",
             "Agent Action: Resolves immediately; directs to front-desk kiosk (24h pass).",
             "Result: 0 IT tickets created."
         ],
         COLOR_SUCCESS)

add_card(s8, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "REQ-08 (Security)",
         [
             "Employee: Ananya Reddy.",
             "Query: Forwarding phishing email to teammates.",
             "Agent Action: Halts forwarding, alerts security@veridian, creates incident ticket.",
             "Result: Viral breach prevented."
         ],
         COLOR_DANGER)

add_card(s8, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "REQ-15 (Clarification)",
         [
             "Employee: Rahul Menon.",
             "Query: 'hey can you help, its not working'.",
             "Agent Action: Asks 3 diagnostic questions (device, error, time).",
             "Result: Zero guesswork."
         ],
         COLOR_WARN)

add_card(s8, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
         "REQ-01 (Precedent)",
         [
             "Employee: Aditi Sharma.",
             "Query: Dead laptop, 3.5 yrs old.",
             "Agent Action: Replacement approved aligned with precedent TK-1043.",
             "Result: Consistent governance."
         ],
         COLOR_ACCENT)

# -------------------------------------------------------------
# SLIDE 9: AI Tools Used & Engineering Methodology
# -------------------------------------------------------------
s9 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s9)
add_header(s9, "Engineering Methodology", "AI Tooling Utilized & Production Quality Standards", 9)

add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "AI Tools Used & Roles",
         [
             "Antigravity AI Coding Environment: Used for rapid architecture scaffolding, policy schema definition, and API contract verification.",
             "Strict Boundary Prompting: Constrained agent inference boundaries exclusively to the Veridian Data Pack to guarantee 0% hallucination.",
             "Synthetic Edge Case Validation: Used AI models to simulate complex phrasing of REQ-01 through REQ-15."
         ],
         COLOR_ACCENT)

add_card(s9, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
         "Production Engineering Standards",
         [
             "Deterministic Safety Layer: Security-critical actions (phishing) bypass heuristic paths and hit deterministic guardrails.",
             "Resilient Fallbacks: Self-contained document state ensures the evaluator can test locally without database configuration barriers.",
             "One-Command Execution: Single command 'npm start' or 'node backend/server.js' launches both backend and frontend."
         ],
         COLOR_SUCCESS)

# -------------------------------------------------------------
# SLIDE 10: Conclusion & Submission Links
# -------------------------------------------------------------
s10 = prs.slides.add_slide(BLANK_LAYOUT)
set_slide_background(s10)
add_header(s10, "Summary & Impact", "Business Outcomes & Mandatory Deliverables", 10)

add_card(s10, Inches(0.8), Inches(1.8), Inches(3.6), Inches(2.4),
         "40%+ Deflection",
         [
             "Routine queries (passwords, Wi-Fi, VPN renewals) resolved self-service without IT staff time."
         ],
         COLOR_SUCCESS)

add_card(s10, Inches(4.85), Inches(1.8), Inches(3.6), Inches(2.4),
         "100% Policy Grounded",
         [
             "Every resolution cites official KB codes; no fabricated advice or unauthorized permissions."
         ],
         COLOR_ACCENT)

add_card(s10, Inches(8.9), Inches(1.8), Inches(3.6), Inches(2.4),
         "Zero Security Breaches",
         [
             "Immediate guardrail interception of phishing forwards and unauthorized admin requests."
         ],
         COLOR_DANGER)

sub_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.3))
sub_box.fill.solid()
sub_box.fill.fore_color.rgb = COLOR_CARD
sub_box.line.color.rgb = COLOR_ACCENT
sub_box.line.width = Pt(1.5)

tf_sub = sub_box.text_frame
tf_sub.word_wrap = True
tf_sub.margin_left = Inches(0.4)
tf_sub.margin_top = Inches(0.25)
tf_sub.margin_right = Inches(0.4)
tf_sub.margin_bottom = Inches(0.25)

p_sub0 = tf_sub.paragraphs[0]
p_sub0.text = "MANDATORY SUBMISSION LINKS & DEFENSE REFERENCES"
p_sub0.font.size = Pt(14)
p_sub0.font.bold = True
p_sub0.font.color.rgb = COLOR_ACCENT

p_sub1 = tf_sub.add_paragraph()
p_sub1.text = "• Working Prototype: http://localhost:5050 (React 18 + Node.js Backend)"
p_sub1.font.size = Pt(12)
p_sub1.font.color.rgb = COLOR_WHITE
p_sub1.space_before = Pt(6)

p_sub2 = tf_sub.add_paragraph()
p_sub2.text = "• GitHub Repository: https://github.com/<YOUR_USERNAME>/aionos-it-support-agent"
p_sub2.font.size = Pt(12)
p_sub2.font.color.rgb = COLOR_WHITE
p_sub2.space_before = Pt(4)

p_sub3 = tf_sub.add_paragraph()
p_sub3.text = "• Demo Video on Google Drive (Public / Open Access): https://drive.google.com/file/d/<YOUR_FILE_ID>/view?usp=sharing"
p_sub3.font.size = Pt(12)
p_sub3.font.color.rgb = COLOR_WHITE
p_sub3.space_before = Pt(4)

output_path = "Veridian_IT_Support_Agent_Presentation.pptx"
prs.save(output_path)
print(f"Presentation saved successfully to {output_path}!")
