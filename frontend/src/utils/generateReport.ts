/**
 * Generates a professional Tax Incentive Report as a downloadable HTML document
 * that can be printed to PDF via the browser's native print dialog.
 */

export interface ReportData {
  production: string;
  jurisdiction: string;
  totalExpenses: number;
  qualifiedExpenses: number;
  incentiveAmount: number;
  effectiveRate: number;
  ruleName?: string;
  incentiveRate?: number;
}

const fmtCurrency = (n: number) =>
  `$${n.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

const fmtPct = (n: number) => `${n}%`;

function buildReportHTML(data: ReportData, generatedDate: string): string {
  const qualRate = ((data.qualifiedExpenses / data.totalExpenses) * 100).toFixed(1);
  const reportId = `PF-${Date.now().toString(36).toUpperCase()}`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Tax Incentive Report - ${data.production}</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,sans-serif;color:#1a1a2e;background:#fff;line-height:1.6;padding:0}
.page{max-width:800px;margin:0 auto;padding:48px 40px}
.header{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid #2563eb;padding-bottom:24px;margin-bottom:32px}
.header-brand h1{font-size:28px;font-weight:800;color:#1e293b;letter-spacing:-0.5px}
.header-brand span{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:2px}
.header-meta{text-align:right;font-size:13px;color:#64748b}
.header-meta strong{color:#1e293b;display:block;font-size:14px}
.section-title{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#2563eb;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e2e8f0}
.hero{background:linear-gradient(135deg,#eff6ff 0%,#f0fdf4 100%);border:1px solid #bfdbfe;border-radius:12px;padding:32px;text-align:center;margin-bottom:32px}
.hero-label{font-size:14px;color:#3b82f6;font-weight:600;margin-bottom:4px}
.hero-amount{font-size:48px;font-weight:800;color:#16a34a;letter-spacing:-1px}
.hero-sub{font-size:13px;color:#64748b;margin-top:8px}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:32px}
.info-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px}
.info-card-label{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
.info-card-value{font-size:18px;font-weight:700;color:#1e293b}
.breakdown-table{width:100%;border-collapse:collapse;margin-bottom:32px}
.breakdown-table th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#64748b;padding:12px 16px;border-bottom:2px solid #e2e8f0}
.breakdown-table th:last-child{text-align:right}
.breakdown-table td{padding:14px 16px;border-bottom:1px solid #f1f5f9;font-size:14px;color:#334155}
.breakdown-table td:last-child{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
.breakdown-table tr:last-child td{border-bottom:none}
.breakdown-table .total-row td{border-top:2px solid #1e293b;border-bottom:none;font-weight:800;font-size:16px;color:#1e293b;padding-top:16px}
.bar-section{margin-bottom:32px}
.bar-container{background:#f1f5f9;border-radius:8px;height:32px;position:relative;overflow:hidden;margin-top:8px}
.bar-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#3b82f6 0%,#16a34a 100%);display:flex;align-items:center;justify-content:flex-end;padding-right:12px;color:#fff;font-size:12px;font-weight:700;min-width:60px}
.bar-labels{display:flex;justify-content:space-between;margin-top:6px;font-size:12px;color:#94a3b8}
.assumptions{background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:20px;margin-bottom:32px}
.assumptions h3{font-size:14px;font-weight:700;color:#92400e;margin-bottom:8px}
.assumptions ul{list-style:none;padding:0}
.assumptions li{font-size:13px;color:#78350f;padding:4px 0 4px 20px;position:relative}
.assumptions li::before{content:'\\2022';position:absolute;left:6px;color:#d97706}
.footer{border-top:1px solid #e2e8f0;padding-top:20px;margin-top:40px;display:flex;justify-content:space-between;font-size:12px;color:#94a3b8}
@media print{
  body{padding:0}.page{padding:24px 20px}.no-print{display:none!important}
  .hero,.bar-fill,.info-card,.assumptions{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>
</head>
<body>
<div class="page">
  <div class="header">
    <div class="header-brand"><h1>PilotForge</h1><span>Tax Incentive Intelligence</span></div>
    <div class="header-meta"><strong>Tax Incentive Estimate Report</strong>Generated: ${generatedDate}<br/>Report ID: ${reportId}</div>
  </div>
  <div class="hero">
    <div class="hero-label">Estimated Tax Incentive</div>
    <div class="hero-amount">${fmtCurrency(data.incentiveAmount)}</div>
    <div class="hero-sub">Based on ${fmtCurrency(data.totalExpenses)} total production budget with ${fmtPct(data.effectiveRate)} effective rate</div>
  </div>
  <div class="section-title">Production Details</div>
  <div class="info-grid">
    <div class="info-card"><div class="info-card-label">Production</div><div class="info-card-value">${data.production}</div></div>
    <div class="info-card"><div class="info-card-label">Jurisdiction</div><div class="info-card-value">${data.jurisdiction}</div></div>
    <div class="info-card"><div class="info-card-label">Total Budget</div><div class="info-card-value">${fmtCurrency(data.totalExpenses)}</div></div>
    <div class="info-card"><div class="info-card-label">Effective Rate</div><div class="info-card-value">${fmtPct(data.effectiveRate)}</div></div>
  </div>
  <div class="section-title">Financial Breakdown</div>
  <table class="breakdown-table">
    <thead><tr><th>Line Item</th><th>Amount</th></tr></thead>
    <tbody>
      <tr><td>Total Production Expenses</td><td>${fmtCurrency(data.totalExpenses)}</td></tr>
      <tr><td>Qualified Expenses (${qualRate}%)</td><td>${fmtCurrency(data.qualifiedExpenses)}</td></tr>
      <tr><td>Non-Qualifying Expenses</td><td>${fmtCurrency(data.totalExpenses - data.qualifiedExpenses)}</td></tr>
      <tr><td>Incentive Rate Applied</td><td>${data.incentiveRate != null ? fmtPct(data.incentiveRate) : fmtPct(data.effectiveRate)}</td></tr>
      <tr class="total-row"><td>Estimated Incentive</td><td>${fmtCurrency(data.incentiveAmount)}</td></tr>
    </tbody>
  </table>
  <div class="bar-section">
    <div class="section-title">Budget Utilization</div>
    <div class="bar-container"><div class="bar-fill" style="width:${qualRate}%">${qualRate}%</div></div>
    <div class="bar-labels"><span>0%</span><span>Qualified Spend: ${qualRate}%</span><span>100%</span></div>
  </div>
  <div class="assumptions">
    <h3>Assumptions &amp; Disclaimers</h3>
    <ul>
      <li>Qualification rate of ${qualRate}% applied based on standard industry classification</li>
      <li>Incentive rate of ${data.incentiveRate != null ? data.incentiveRate : data.effectiveRate}% based on current ${data.jurisdiction} program guidelines${data.ruleName ? ` (${data.ruleName})` : ''}</li>
      <li>Actual incentive may vary based on final audit of qualifying expenditures</li>
      <li>This estimate does not constitute tax advice - consult a licensed tax professional</li>
      <li>Subject to program caps, availability, and legislative changes</li>
    </ul>
  </div>
  <div class="footer">
    <span>PilotForge - Tax Incentive Compliance Platform</span>
    <span>Confidential - ${generatedDate}</span>
  </div>
</div>
<div class="no-print" style="text-align:center;padding:20px">
  <button onclick="window.print()" style="padding:12px 32px;font-size:15px;font-weight:600;background:#2563eb;color:#fff;border:none;border-radius:8px;cursor:pointer;font-family:inherit">Print / Save as PDF</button>
  <button onclick="window.close()" style="padding:12px 32px;font-size:15px;font-weight:600;background:#f1f5f9;color:#475569;border:1px solid #e2e8f0;border-radius:8px;cursor:pointer;margin-left:12px;font-family:inherit">Close</button>
</div>
</body>
</html>`;
}

export function openReportWindow(data: ReportData): void {
  const now = new Date();
  const generatedDate = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const html = buildReportHTML(data, generatedDate);
  const win = window.open('', '_blank', 'width=900,height=700');
  if (win) { win.document.write(html); win.document.close(); }
}

export function downloadReport(data: ReportData): void {
  const now = new Date();
  const generatedDate = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const html = buildReportHTML(data, generatedDate);
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const safeName = data.production.replace(/[^a-zA-Z0-9]/g, '_');
  a.download = `PilotForge_Tax_Report_${safeName}_${now.toISOString().slice(0, 10)}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
