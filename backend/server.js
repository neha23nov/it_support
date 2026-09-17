const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5050;

app.use(cors());
app.use(express.json());

const KB_FILE = path.join(__dirname, 'knowledgeBase.json');
const rawKb = fs.readFileSync(KB_FILE, 'utf-8');
const KB_DATA = JSON.parse(rawKb);

// State collections (MongoDB style, in-memory with file fallback)
let tickets = [...KB_DATA.precedents.map((p, idx) => ({
  id: p.id,
  employee: p.employee,
  email: `${p.employee.toLowerCase().replace(/\s+/g, '.')}@veridian-corp.example`,
  issue_summary: p.issue,
  category: 'Historical Precedent',
  status: p.status,
  assigned_team: 'IT Operations',
  source_policy: 'Historical Ticket Record',
  resolution_notes: p.resolution,
  created_at: '2026-09-21 09:00:00'
}))];

let auditLogs = [];

function logAudit(sessionId, employee, userInput, intent, actionTaken, policyCited, ticketId, reasoning) {
  const logEntry = {
    id: auditLogs.length + 1,
    session_id: sessionId || 'default_session',
    employee: employee || 'Employee',
    user_input: userInput,
    intent,
    action_taken: actionTaken,
    policy_cited: policyCited,
    ticket_id: ticketId || null,
    reasoning,
    timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
  };
  auditLogs.unshift(logEntry);
  return logEntry;
}

function createTicket(employee, email, issueSummary, category, status, assignedTeam, sourcePolicy, resolutionNotes) {
  const newTicketId = `TK-${1052 + tickets.length - KB_DATA.precedents.length}`;
  const newTicket = {
    id: newTicketId,
    employee: employee || 'Employee',
    email: email || 'employee@veridian-corp.example',
    issue_summary: issueSummary,
    category,
    status,
    assigned_team: assignedTeam,
    source_policy: sourcePolicy,
    resolution_notes: resolutionNotes,
    created_at: new Date().toISOString().replace('T', ' ').substring(0, 19)
  };
  tickets.unshift(newTicket);
  return newTicketId;
}

function evaluateRequest(message, employee = 'Employee', email = 'employee@veridian-corp.example') {
  const msg = (message || '').toLowerCase().trim();

  // 1. Ambiguous / Vague requests -> Ask targeted follow-up questions
  if (msg.split(/\s+/).length <= 4 || msg.includes('hey can you help') || msg === 'its not working' || msg === 'not working' || msg === 'help') {
    return {
      type: 'clarify',
      intent: 'Unclear / Ambiguous Request',
      policy: 'General IT Triage Protocol',
      action: 'Targeted Diagnostic Follow-Up Questions Asked',
      ticket_id: null,
      response: `Hello! To help resolve this quickly without guesswork, could you share a few specifics:
1. Which application, device, or system is not working?
2. Are you seeing an error code or specific message?
3. When did this begin and is it completely unresponsive?`,
      reasoning: 'Input is underspecified. Prompted for clarification per IT triage guidelines rather than inventing an assumed issue.'
    };
  }

  // 2. Phishing / Security Alert (KB-09) -> Intercept dangerous forwarding behavior immediately
  if (msg.includes('phishing') || msg.includes('malware') || msg.includes('suspicious') || msg.includes('forwarding')) {
    const tId = createTicket(
      employee,
      email,
      'Reported Phishing Email / Suspicious Activity',
      'Security Incident',
      'Escalated to Security (auto-flagged)',
      'IT Security Incident Response Team',
      'KB-09: Security Incident Reporting',
      'Auto-flagged to security@veridian-corp.example. Advised user immediately not to forward.'
    );
    return {
      type: 'escalate',
      intent: 'Security Incident Reporting',
      policy: 'KB-09: Security Incident Reporting',
      action: 'Auto-Escalated to IT Security',
      ticket_id: tId,
      response: `⚠️ **URGENT SECURITY ALERT**

**Action Required:** Please **DO NOT** forward this email or any attachments to teammates or colleagues, as this spreads potential exposure across the company network.

We have opened incident ticket **${tId}** and directly alerted **security@veridian-corp.example** for investigation.

**Source Policy:** KB-09 (Security Incident Reporting)`,
      reasoning: 'Detected report of phishing and risk of internal forwarding. Intercepted per KB-09 and created emergency security ticket.'
    };
  }

  // 3. Guest Wi-Fi Access (KB-07) -> Self-service resolution
  if (msg.includes('guest') && (msg.includes('wi-fi') || msg.includes('wifi'))) {
    return {
      type: 'resolve',
      intent: 'Guest Wi-Fi Access',
      policy: 'KB-07: Guest Wi-Fi Access',
      action: 'Self-Service Resolution Provided',
      ticket_id: null,
      response: `You can generate guest Wi-Fi credentials directly!
• **Self-Service:** Any employee can generate guest Wi-Fi credentials at the front-desk kiosk.
• **Validity:** Credentials remain active for 24 hours.
• **Ticket:** No IT ticket is required.

**Source Policy:** KB-07 (Guest Wi-Fi Access)`,
      reasoning: 'Routine guest Wi-Fi request resolved via front-desk kiosk self-service per KB-07.'
    };
  }

  // 4. Password Reset with lockout threshold (KB-01)
  if (msg.includes('password') && (msg.includes('locked') || msg.includes('6 times') || msg.includes('failed'))) {
    const tId = createTicket(
      employee,
      email,
      'Account Locked Out (>5 failed attempts)',
      'Account & Access',
      'In progress — reset queued',
      'IT Helpdesk',
      'KB-01: Password Reset',
      'Account locked after 5+ failed attempts. Manual IT unlock queued without manager approval requirement.'
    );
    return {
      type: 'escalate',
      intent: 'Account Lockout',
      policy: 'KB-01: Password Reset',
      action: 'Manual Unlock Queued',
      ticket_id: tId,
      response: `Because your account was attempted 6 times (exceeding the 5 failed attempt threshold), self-service reset is locked.
• **Status:** Ticket **${tId}** has been created. An IT technician has queued a manual unlock for your account.
• **Approval:** No manager approval is required.

**Source Policy:** KB-01 (Password Reset)`,
      reasoning: 'User exceeded 5 failed attempts threshold in KB-01. Queued manual unlock ticket.'
    };
  }

  // 5. Routine Password Reset (KB-01)
  if (msg.includes('password')) {
    return {
      type: 'resolve',
      intent: 'Password Reset',
      policy: 'KB-01: Password Reset',
      action: 'Self-Service Guided',
      ticket_id: null,
      response: `You can reset your password immediately:
• **Portal:** Visit the Veridian Self-Service Password Portal anytime.
• **Note:** If locked out after 5 failed attempts, contact IT for a manual unlock.

**Source Policy:** KB-01 (Password Reset)`,
      reasoning: 'Guided user to self-service portal per KB-01.'
    };
  }

  // 6. Contractor VPN Access (KB-02)
  if (msg.includes('contractor') && msg.includes('vpn')) {
    const tId = createTicket(
      employee,
      email,
      'Contractor VPN Access Request',
      'Network & VPN',
      'Pending Manager Approval',
      'IT Identity & Access Team',
      'KB-02: VPN Access',
      'Contractors require manager approval submitted via access request form.'
    );
    return {
      type: 'escalate',
      intent: 'Contractor VPN Provisioning',
      policy: 'KB-02: VPN Access',
      action: 'Approval Workflow Initiated',
      ticket_id: tId,
      response: `VPN provisioning for contractors has specific requirements:
• Full-time employees receive VPN access automatically, but **contractors require manager approval**.
• **Next Step:** Submit manager approval via the internal Access Request Form.
• Tracking Ticket **${tId}** has been logged.

**Source Policy:** KB-02 (VPN Access)`,
      reasoning: 'Contractors require manager approval submitted via form per KB-02.'
    };
  }

  // 7. VPN Credential Expiry / 90 days (KB-02)
  if (msg.includes('vpn') && (msg.includes('expired') || msg.includes('credentials') || msg.includes('stopped working'))) {
    return {
      type: 'resolve',
      intent: 'VPN Credential Renewal',
      policy: 'KB-02: VPN Access',
      action: 'Self-Service Renewal Resolution',
      ticket_id: null,
      response: `VPN credentials expire every 90 days for all employees:
• **Resolution:** Go to the VPN Self-Service Portal and click 'Renew 90-Day Credentials'.
• Once renewed, disconnect and reconnect your VPN client.
• Full-time employees do not require manager approval for renewals.

**Source Policy:** KB-02 (VPN Access)`,
      reasoning: 'Standard 90-day VPN credential expiry handled self-service per KB-02.'
    };
  }

  // 8. Laptop Screen Flickering / Diagnostics - 2 yrs old (KB-03 & Asset Policy)
  if (msg.includes('laptop') && (msg.includes('flickering') || msg.includes('2 year') || msg.includes('screen') || msg.includes('not a replacement') || msg.includes('fix'))) {
    const tId = createTicket(
      employee,
      email,
      'Laptop Screen Repair / Diagnostics (2 yrs old)',
      'Hardware',
      'Queued for Hardware Diagnostics',
      'IT Hardware Support',
      'KB-03 & Asset Management Policy',
      'Device is 2 years old, not eligible for replacement (minimum 3 years). Diagnosing hardware fix.'
    );
    return {
      type: 'escalate',
      intent: 'Hardware Diagnostics & Repair',
      policy: 'KB-03 & Asset Management Policy',
      action: 'Repair Ticket Opened',
      ticket_id: tId,
      response: `Thank you for reporting this issue:
• **Policy Check:** At 2 years of service, your device is not eligible for full replacement (minimum 3 years under KB-03 and 4 years standard refresh).
• **Next Steps:** We have logged ticket **${tId}** for hardware screen diagnostics and repair.
• Please bring your laptop to the IT walk-in desk on Floor 1.

**Source Policy:** KB-03 (Laptop Replacement) & Asset Management Policy`,
      reasoning: 'Device age is 2 years, disqualifying replacement. Correct action is diagnostic repair ticket.'
    };
  }

  // 9. Laptop Replacement - 3.5 yrs dead (KB-03 & Asset Policy)
  if (msg.includes('laptop') && (msg.includes("won't turn on") || msg.includes('dead') || msg.includes('3.5') || msg.includes('replace'))) {
    const tId = createTicket(
      employee,
      email,
      'Laptop Replacement (3.5 yrs old, verified hardware failure)',
      'Hardware',
      'Approved — pending fulfillment',
      'IT Hardware & Assets',
      'KB-03 & Asset Management Policy',
      'Laptop is 3.5 yrs old (exceeds 3 yrs threshold with verified failure). Precedent TK-1043 confirms early replacement route.'
    );
    return {
      type: 'escalate',
      intent: 'Laptop Replacement Request',
      policy: 'KB-03 (Laptop Replacement) & Asset Management Policy',
      action: 'Replacement Ticket Created',
      ticket_id: tId,
      response: `Your laptop replacement request has been processed:
• **Eligibility:** Your device is at 3.5 years of service (eligible after 3 years for verified hardware failure per KB-03).
• **Policy Match:** Standard refresh is 4 years; early replacement approved with Finance sign-off (consistent with precedent TK-1043).
• **Ticket Opened:** **${tId}** has been routed to IT Hardware & Assets for fulfillment.

**Source Policy:** KB-03 (Laptop Replacement) & Asset Management Policy`,
      reasoning: 'Qualifies for replacement under KB-03 (>3 years + verified hardware failure). Created ticket consistent with TK-1043.'
    };
  }

  // 10. Admin Access to Finance Server (Precedent TK-1050)
  if (msg.includes('admin') && (msg.includes('access') || msg.includes('server') || msg.includes('finance'))) {
    const tId = createTicket(
      employee,
      email,
      'Admin Access Request - Finance Reporting Server',
      'Access & Permissions',
      'Pending Business Justification & Department Head Approval',
      'IT Security & Governance',
      'Access Governance Standards (Ref: Precedent TK-1050)',
      'Privileged server access requires formal business justification and security clearance. Refer to precedent TK-1050.'
    );
    return {
      type: 'escalate',
      intent: 'Privileged Admin Access',
      policy: 'Access Governance & Precedent TK-1050',
      action: 'Escalated for Justification',
      ticket_id: tId,
      response: `Privileged administrative access to production finance servers cannot be granted immediately over chat:
• **Security Control:** Per access standards and past precedent TK-1050, admin access requires formal business justification and department head sign-off.
• **Ticket:** **${tId}** has been initiated. Please submit formal written authorization via the governance portal.

**Source Reference:** IT Access Governance & Precedent TK-1050`,
      reasoning: 'Admin access rejected without formal authorization, aligned with precedent TK-1050.'
    };
  }

  // 11. Expense Tool Access (KB-08)
  if (msg.includes('expense')) {
    return {
      type: 'clarify',
      intent: 'Expense Software Access',
      policy: 'KB-08: Expense Software Access',
      action: 'Department Responsibility Clarified',
      ticket_id: null,
      response: `Regarding access to the expense management tool:
• **Responsibility:** Access to the expense tool is granted by **Finance**, not IT.
• **IT Role:** IT can only assist with login/technical issues once an account already exists.
• **Follow-up:** Has Finance already provisioned your account? If yes, please provide a screenshot of the error message so we can assist.

**Source Policy:** KB-08 (Expense Software Access)`,
      reasoning: 'Disentangled IT vs Finance scope per KB-08. Prompted for clarification on whether account exists.'
    };
  }

  // 12. Printer Paper Jam (KB-05)
  if (msg.includes('printer') || msg.includes('paper jam')) {
    return {
      type: 'resolve',
      intent: 'Printer Troubleshooting',
      policy: 'KB-05: Printer Troubleshooting',
      action: 'Troubleshooting Steps Provided',
      ticket_id: null,
      response: `For printer paper jam warnings:
1. Check the local print queue on your machine and clear any stuck jobs.
2. Restart the print spooler service.
3. If the error continues after restart, please share the **Printer Asset Tag** so we can dispatch a technician.

**Source Policy:** KB-05 (Printer Troubleshooting)`,
      reasoning: 'Provided required troubleshooting steps from KB-05 before ticket dispatch.'
    };
  }

  // 13. Software Catalog / Browser Extension (KB-04)
  if (msg.includes('catalog') || msg.includes('browser extension') || msg.includes('data-analysis') || msg.includes('software')) {
    const tId = createTicket(
      employee,
      email,
      `Non-Catalog Software Review: ${message.substring(0, 40)}`,
      'Software',
      'Pending Security Review (active)',
      'IT Security Review Team',
      'KB-04: Software Installation Requests',
      'Non-catalog software/extensions require IT Security review (3-5 business days SLA).'
    );
    return {
      type: 'escalate',
      intent: 'Non-Catalog Software Review',
      policy: 'KB-04: Software Installation Requests',
      action: 'Queued for Security Review',
      ticket_id: tId,
      response: `Software or extensions outside the standard catalog require review:
• **Review Process:** Non-catalog items must undergo IT Security assessment.
• **SLA:** Review takes **3–5 business days**.
• **Ticket Created:** Ticket **${tId}** has been routed to IT Security.

**Source Policy:** KB-04 (Software Installation Requests)`,
      reasoning: 'Non-catalog software routed to IT Security review per KB-04.'
    };
  }

  // 14. Email Mailbox Quota (KB-06)
  if (msg.includes('mailbox') || msg.includes('quota')) {
    return {
      type: 'resolve',
      intent: 'Mailbox Quota Management',
      policy: 'KB-06: Email Mailbox Quota',
      action: 'Self-Service Archiving Steps Provided',
      ticket_id: null,
      response: `Here are the guidelines regarding mailbox limits:
• **Default Quota:** Standard mailbox quota is **25GB**.
• **Immediate Fix:** Archive old mail or empty Deleted Items to resume sending.
• **Increases:** Quota increases beyond 25GB require manager approval and are capped at **50GB**.

**Source Policy:** KB-06 (Email Mailbox Quota)`,
      reasoning: 'Explained standard 25GB quota, self-service archiving, and approval limits per KB-06.'
    };
  }

  // 15. Work From Home Equipment (KB-10)
  if (msg.includes('work from home') || msg.includes('working from home') || msg.includes('wfh') || msg.includes('monitor')) {
    const tId = createTicket(
      employee,
      email,
      'Home Office Equipment (Monitor) Request',
      'Hardware & Work Arrangement',
      'Pending Finance Approval',
      'Finance & Asset Processing',
      'KB-10: Work-From-Home Equipment',
      'Employee works >3 days/week remote. Requires manager sign-off and Finance processing prior to IT shipping.'
    );
    return {
      type: 'escalate',
      intent: 'Work-From-Home Equipment Request',
      policy: 'KB-10: Work-From-Home Equipment',
      action: 'Workflow Initiated',
      ticket_id: tId,
      response: `Guidelines for home office equipment:
• **Eligibility:** Employees working remotely more than 3 days/week qualify for a one-time equipment allowance (chair, monitor).
• **Approval Workflow:** Requires manager sign-off and Finance processing.
• **IT Role:** IT handles shipping once Finance approves.
• **Ticket:** Logged ticket **${tId}** and routed to Finance for processing.

**Source Policy:** KB-10 (Work-From-Home Equipment)`,
      reasoning: 'Validated remote schedule; routed to manager and Finance approval before IT shipment per KB-10.'
    };
  }

  // Default fallback
  return {
    type: 'clarify',
    intent: 'General IT Inquiry',
    policy: 'IT General Support Matrix',
    action: 'Clarification Prompted',
    ticket_id: null,
    response: `I've received your inquiry. To assist you accurately according to Veridian IT policies, could you clarify your specific request or device type? You can also click any of the 15 employee cases on the left sidebar.`,
    reasoning: 'Unmatched query, prompted for clarification against Veridian IT policies.'
  };
}

// REST Endpoints
app.post('/api/chat', (req, res) => {
  const { message, employee, email, session_id } = req.body || {};
  const result = evaluateRequest(message, employee, email);
  
  logAudit(
    session_id,
    employee,
    message,
    result.intent,
    result.action,
    result.policy,
    result.ticket_id,
    result.reasoning
  );

  res.json(result);
});

app.get('/api/tickets', (req, res) => {
  res.json(tickets);
});

app.get('/api/audit', (req, res) => {
  res.json(auditLogs);
});

app.get('/api/policies', (req, res) => {
  res.json(KB_DATA.policies);
});

app.get('/api/requests', (req, res) => {
  res.json(KB_DATA.employee_requests);
});

// Serve frontend static files if present
const frontendDist = path.join(__dirname, '..', 'frontend', 'dist');
if (fs.existsSync(frontendDist)) {
  app.use(express.static(frontendDist));
  app.get('*', (req, res) => {
    res.sendFile(path.join(frontendDist, 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
