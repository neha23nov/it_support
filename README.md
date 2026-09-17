# Veridian Corp — Internal Service Agent (IT Support)
**AIONOS Assignment 2:**

An autonomous, policy-grounded IT Support Agent built for **Veridian Corp** (set in the week of 21–25 September 2026). The agent interprets employee queries, strictly enforces the 10 corporate policies (`KB-01` to `KB-10`) and Asset Management Policy, performs instant self-service resolutions, prompts for clarification on ambiguous inputs, intercepts critical security threats (e.g. phishing email forwarding), creates structured tickets, and records an immutable audit trail.

---

## 🚀 One-Command Local Run

### Prerequisites
- [Node.js](https://nodejs.org/) (v16 or higher)

### Quick Start
```bash
# 1. Clone repository
git clone <YOUR_GITHUB_REPO_URL>
cd it-support-mern

# 2. Install backend dependencies
cd backend
npm install
cd ..

# 3. Start the application
npm start
```

Open your browser and navigate to:
👉 **`http://localhost:5050`**

---

## 🛠️ Technology Stack (MERN)

- **M — MongoDB / State Layer**: Ticket records (`TK-1042` to `TK-1051` + active tickets) and audit trails stored with persistent document schemas.
- **E — Express.js**: REST API engine handling chat requests, ticket routing, policy retrieval, and compliance logging.
- **R — React.js (React 18)**: Interactive dashboard featuring live chat, 1-click test triggers for all 15 employee requests, ticket queue management, and audit log inspection.
- **N — Node.js**: High-performance runtime powering the agent decision engine, policy matching, and guardrail interception.

---

## 🏛️ System Architecture

```
+-----------------------------------------------------------------------+
|                         REACT.JS FRONTEND                             |
|  - Modern Dashboard with Tailwind CSS                                 |
|  - 1-Click Request Tester (REQ-01 to REQ-15)                          |
|  - Chat UI + Ticket Queue Table + Audit Trail Logs + Policy Explorer  |
+-----------------------------------------------------------------------+
                                   │  HTTP REST (Axios / Fetch)
                                   ▼
+-----------------------------------------------------------------------+
|                        NODE.JS / EXPRESS BACKEND                      |
|  - POST /api/chat     -> Evaluates query, checks guardrails & policies|
|  - GET  /api/tickets  -> Returns active + historical tickets          |
|  - GET  /api/audit    -> Returns immutable decision log               |
|  - GET  /api/policies -> Returns KB-01 to KB-10 ground truth          |
+-----------------------------------------------------------------------+
                                   │  Document Store (MongoDB Style)
                                   ▼
+-----------------------------------------------------------------------+
|                            DATABASE STORE                             |
|  - Tickets Collection (TK-1042 ... + live tickets)                    |
|  - Audit Logs Collection (every conversation turn & citation)         |
|  - Policies Collection (KB-01 to KB-10 ground truth)                  |
+-----------------------------------------------------------------------+
```

---

## 🎯 Coverage of the 15 Employee Cases

| Case | Employee | Request Summary | Agent Action | Grounded Policy |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Aditi Sharma | Dead laptop (3.5 yrs old) | Replacement ticket opened (aligned with TK-1043) | KB-03 & Asset Policy |
| **REQ-02** | Vikram Chawla | Guest Wi-Fi access | Self-service kiosk guidance (24h validity, no ticket) | KB-07 |
| **REQ-03** | Karan Mehta | Account lockout (6 attempts) | Manual IT unlock ticket queued | KB-01 |
| **REQ-04** | Ritu Bhatia | Non-catalog software | Routed to IT Security review (3-5 day SLA) | KB-04 |
| **REQ-05** | Sanjay Oberoi | VPN credential expired | Self-service 90-day renewal portal resolution | KB-02 |
| **REQ-06** | Meera Iyer | Printer false paper jam | Spooler restart & asset tag collection | KB-05 |
| **REQ-07** | Farhan Ali | WFH monitor allowance | Routed for Manager sign-off & Finance processing | KB-10 |
| **REQ-08** | Ananya Reddy | Phishing email forwarding | **Critical Alert**: Stopped forwarding, alerted Security | KB-09 |
| **REQ-09** | Rohit Desai | Mailbox full (25GB) | Archiving guidance & manager approval for >25GB | KB-06 |
| **REQ-10** | Kavya Pillai | Urgent finance admin access | Escalated for business justification (ref TK-1050) | Governance / TK-1050 |
| **REQ-11** | Nikhil Bansal | Contractor VPN access | Manager approval via Access Request Form required | KB-02 |
| **REQ-12** | Sneha Kulkarni | Expense tool invalid login | Clarified Finance grants access; requested screenshot | KB-08 |
| **REQ-13** | Aman Gupta | Screen flickering (2 yrs old) | Repair & diagnostics ticket opened (no replace) | KB-03 & Asset Policy |
| **REQ-14** | Tanya Chopra | Browser extension approval | Non-catalog security review ticket opened | KB-04 |
| **REQ-15** | Rahul Menon | *"hey can you help, its not working"* | Diagnostic triage follow-up questionnaire | IT Triage Protocol |
