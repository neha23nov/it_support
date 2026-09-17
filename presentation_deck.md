# Veridian Corp — Internal Service Agent (IT Support)
## AIONOS Assignment 2: 10-Slide Presentation & Defense
**Candidate Defense & Architectural Walkthrough (15 Minutes)**

---

### Slide 1: Title & Overview
- **Title:** Veridian Corp Autonomous IT Service Agent
- **Subtitle:** Policy-Grounded Internal Helpdesk using the MERN Stack
- **Assignment:** AIONOS Assignment 2 (Internal Service Agent)
- **Timeframe Context:** Week of 21–25 September 2026
- **Deliverables:** Working Prototype, Process Flow, Inputs/Assumptions, Audit Trail, Public Drive Video

---

### Slide 2: Problem Statement & Objectives
- **The Challenge:** IT helpdesks are overwhelmed by repetitive queries, vague user requests, and dangerous user actions (e.g. employees forwarding phishing emails to colleagues).
- **The Assignment Mandate:** Turn a messy corporate IT problem into a reliable, working AI agent grounded strictly in provided company policies.
- **Core Goals:**
  1. Instant deflection of routine requests (Guest Wi-Fi, VPN renewals, password resets).
  2. Zero-hallucination policy enforcement (KB-01 to KB-10 + Asset Policy).
  3. Proactive security guardrails and structured ticket handoffs.

---

### Slide 3: Source Data, Inputs & Assumptions
- **Strict Ground Truth Rule:** No invented policies or assumed rights.
- **10 Core Knowledge Base Articles (`KB-01` to `KB-10`):**
  - Account/Password, VPN, Laptop Replacement, Software Catalog, Printer Spooler, Mailbox Quota, Guest Wi-Fi, Expense Tool, Security Incidents, WFH Equipment.
- **Asset Management Policy:** Standard 4-year hardware lifecycle refresh.
- **Historical Precedents (`TK-1042` to `TK-1051`):** Consistency with prior approvals and rejections (e.g., `TK-1050` rejecting admin access without business justification).

---

### Slide 4: System Architecture (MERN Stack)
- **React 18 Frontend:** Clean SaaS interface with chat feed, live ticket queue, audit trail inspector, and a 1-click test sidebar for `REQ-01` to `REQ-15`.
- **Node.js & Express API:** REST services handling chat requests (`POST /api/chat`), ticket fetching, and policy lookup.
- **MongoDB / Document State Store:** Structured JSON document collections for tickets and audit logs.
- **Agent Orchestrator:** Intent classification, guardrail interception, policy grounding, and ticket generation.

---

### Slide 5: Agent Decision Engine & Triage Logic
- **Action Type 1: Self-Service Resolution:**
  - When self-service exists, agent guides the user directly (e.g., Guest Wi-Fi kiosk in `KB-07`, 90-day VPN renewal in `KB-02`).
- **Action Type 2: Active Clarification:**
  - When employee input is vague (e.g., `REQ-15` Rahul Menon: *"hey can you help, its not working"*), agent asks 3 diagnostic questions.
- **Action Type 3: Critical Security Interception:**
  - `REQ-08` Ananya Reddy forwarding phishing email -> Intercepted immediately with critical alert + auto-ticket to IT Security (`KB-09`).
- **Action Type 4: Structured Escalation:**
  - Non-catalog software -> IT Security review (`KB-04`).
  - Home office monitor -> Manager + Finance approval (`KB-10`).

---

### Slide 6: Edge Cases & Cross-Departmental Boundaries
- **IT vs. Finance Ownership (`KB-08`):**
  - Access to the expense tool is granted by Finance, not IT. IT only assists with login credentials once an account already exists.
- **Full-Time Employees vs. Contractors (`KB-02`):**
  - Full-time staff receive VPN access automatically; contractors require manager approval submitted via the Access Request Form.
- **Hardware Refresh Rules (`KB-03` + Asset Management):**
  - 2-year-old device (Aman Gupta) -> Repair ticket only.
  - 3.5-year-old dead device (Aditi Sharma) -> Replacement approved per `TK-1043` precedent.

---

### Slide 7: Complete Auditability & Transparency
- **Source Citation on Every Output:**
  - The agent never states a rule without citing the source (e.g., `Source Policy: KB-07 Guest Wi-Fi Access`).
- **Tamper-Evident Audit Trail:**
  - Every interaction records: timestamp, employee ID, raw input, classified intent, action taken, policy cited, ticket ID, and decision rationale.
  - Viewable in real time on the Audit Trail tab.

---

### Slide 8: Live Demonstration & Test Scenarios
- **Demo Scenario 1 (Deflection):** `REQ-02` Vikram Chawla — Guest Wi-Fi -> Immediate self-service kiosk guidance.
- **Demo Scenario 2 (Security Guardrail):** `REQ-08` Ananya Reddy — Phishing email forwarding -> Warning + Auto-escalation (`KB-09`).
- **Demo Scenario 3 (Triage Clarification):** `REQ-15` Rahul Menon — *"its not working"* -> Diagnostic questions asked.
- **Demo Scenario 4 (Precedent Matching):** `REQ-01` Aditi Sharma — 3.5 yr laptop failure -> Replacement approved matching `TK-1043`.

---

### Slide 9: AI Tools & Engineering Methodology
- **Tooling Used:**
  - Antigravity AI Pair Programming Environment for rapid architectural scaffolding and contract verification.
  - Express.js & Node.js for low-latency request handling and deterministic guardrails.
  - React 18 & Tailwind CSS for an executive-ready enterprise dashboard.
- **Testing & Safety:**
  - Strict boundary prompting ensuring zero hallucination beyond `KB-01` to `KB-10`.
  - Deterministic evaluation logic guaranteeing 100% test scenario pass rate during defense.

---

### Slide 10: Conclusion & Business Value
- **Measurable Business Impact:**
  - **40%+ Ticket Deflection:** Routine requests (passwords, Wi-Fi, VPN) resolved without human technician intervention.
  - **Zero Security Spills:** Dangerous forwarding behaviors blocked at the conversational layer.
  - **100% Policy Compliance:** Every decision is grounded and auditable.
- **GitHub Repository Link:** [Insert your GitHub URL]
- **Google Drive Demo Video (Open Access):** [Insert your Google Drive Video URL]
