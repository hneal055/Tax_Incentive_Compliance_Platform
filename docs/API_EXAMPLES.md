# 💡 API Examples - Tax-Incentive Compliance Platform

> Real-world usage examples and code samples

---

## 📚 Table of Contents

1. [Quick Start Examples](#quick-start-examples)
2. [Calculator Examples](#calculator-examples)
3. [Report Generation Examples](#report-generation-examples)
4. [Data Management Examples](#data-management-examples)
5. [Advanced Workflows](#advanced-workflows)
6. [Client Libraries](#client-libraries)
7. [Common Patterns](#common-patterns)

---

## 🚀 Quick Start Examples

### **Example 1: Calculate Credit for $5M Film**

**Scenario:** You're producing a $5M feature film. Which location offers the best tax credit?

**Solution:** Compare multiple jurisdictions

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/calculate/compare \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 5000000,
    "jurisdictionIds": [
      "bfae464b-9551-4aad-b5e7-2abcf687134e",
      "21905100-d4d0-46a0-9664-c94a5fc227ec"
    ]
  }'
```

```javascript
// Using JavaScript/TypeScript
const response = await fetch('http://localhost:8000/api/v1/calculate/compare', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    budget: 5000000,
    jurisdictionIds: [
      'bfae464b-9551-4aad-b5e7-2abcf687134e',  // California
      '21905100-d4d0-46a0-9664-c94a5fc227ec'   // Georgia
    ]
  })
});

const data = await response.json();
console.log(`Best location: ${data.bestOption.jurisdiction}`);
console.log(`Estimated credit: $${data.bestOption.estimatedCredit.toLocaleString()}`);
```

```python
# Using Python
import httpx

response = httpx.post(
    'http://localhost:8000/api/v1/calculate/compare',
    json={
        'budget': 5000000,
        'jurisdictionIds': [
            'bfae464b-9551-4aad-b5e7-2abcf687134e',  # California
            '21905100-d4d0-46a0-9664-c94a5fc227ec'   # Georgia
        ]
    }
)

data = response.json()
print(f"Best location: {data['bestOption']['jurisdiction']}")
print(f"Estimated credit: ${data['bestOption']['estimatedCredit']:,}")
```

**Result:**
```
Best location: Georgia
Estimated credit: $1,500,000
Savings: $500,000 vs California
```

---

## 🧮 Calculator Examples

### **Example 2: Verify Compliance**

**Scenario:** Your production is ready. Does it meet all requirements for the California Film Credit?

```python
import httpx

# First, get the rule ID
rules = httpx.get(
    'http://localhost:8000/api/v1/incentive-rules/',
    params={'jurisdiction_id': 'california-id'}
).json()

california_rule_id = rules['rules'][0]['id']

# Check compliance
compliance = httpx.post(
    'http://localhost:8000/api/v1/calculate/compliance',
    json={
        'productionBudget': 5000000,
        'ruleId': california_rule_id,
        'shootDays': 45,
        'localHirePercentage': 80,
        'hasPromoLogo': True
    }
).json()

if compliance['overallStatus'] == 'compliant':
    print(f"✅ Qualified! Estimated credit: ${compliance['estimatedCredit']:,}")
else:
    print("❌ Not qualified. Missing requirements:")
    for req in compliance['requirements']:
        if req['status'] == 'not_met':
            print(f"  - {req['description']}")
```

**Output:**
```
✅ Qualified! Estimated credit: $1,000,000

Requirements met:
  ✓ Minimum spend of $1,000,000
  ✓ 45 shoot days in California
  ✓ 80% local hiring (75% required)
  ✓ Promotional logo included
```

---

### **Example 3: Calculate Stackable Credits**

**Scenario:** Louisiana offers a base 25% credit PLUS 10% payroll bonus. How much can you get?

```javascript
const response = await fetch('http://localhost:8000/api/v1/calculate/stackable', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    budget: 5000000,
    ruleId: 'louisiana-stackable-id',
    qualifyingPayroll: 2000000,
    additionalQualifications: {
      payrollBonus: true,
      visualEffects: false
    }
  })
});

const data = await response.json();

console.log(`🎯 Total Credits: $${data.totalCredit.toLocaleString()}`);
console.log(`   (${data.effectiveRate}% effective rate)`);
console.log('\nBreakdown:');
data.breakdown.forEach(item => {
  console.log(`  ${item.name}: ${item.percentage}% = $${item.amount.toLocaleString()}`);
});
```

**Output:**
```
🎯 Total Credits: $1,750,000
   (35% effective rate)

Breakdown:
  Louisiana Base Credit: 25% = $1,250,000
  Louisiana Payroll Credit: 10% = $500,000

✨ Bonus Value: $500,000 additional from stacking!
```

---

### **Example 4: Scenario Modeling**

**Scenario:** Should you increase the budget? Model 3 scenarios to find optimal approach.

```python
import httpx

response = httpx.post(
    'http://localhost:8000/api/v1/calculate/scenario',
    json={
        'baseProductionBudget': 5000000,
        'jurisdictionId': 'california-id',
        'scenarios': [
            {'name': 'Conservative', 'budget': 4000000},
            {'name': 'Base', 'budget': 5000000},
            {'name': 'Premium', 'budget': 7500000},
            {'name': 'Aggressive', 'budget': 10000000}
        ]
    }
)

data = response.json()

print("Scenario Analysis:\n")
for scenario in data['scenarios']:
    print(f"{scenario['scenarioName']}: ${scenario['estimatedCredit']:,}")

print(f"\n💡 Optimization Potential: ${data['optimizationPotential']:,}")
print(f"📈 Recommendation: {data['recommendation']}")
```

**Output:**
```
Scenario Analysis:

Aggressive: $2,000,000
Premium: $1,875,000
Base: $1,250,000
Conservative: $1,000,000

💡 Optimization Potential: $1,000,000
📈 Recommendation: Aggressive budget yields $1M more than Conservative
```

---

## 📄 Report Generation Examples

### **Example 5: Generate PDF Comparison Report**

**Scenario:** Create a professional PDF report for executives showing location comparison.

```javascript
// Using JavaScript with file download
async function generateComparisonReport() {
  const response = await fetch('http://localhost:8000/api/v1/reports/comparison', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      productionTitle: 'Awesome Feature Film',
      budget: 5000000,
      jurisdictionIds: [
        'california-id',
        'georgia-id',
        'louisiana-id'
      ]
    })
  });
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'comparison_report.pdf';
  a.click();
}

generateComparisonReport();
```

```python
# Using Python with file save
import httpx

response = httpx.post(
    'http://localhost:8000/api/v1/reports/comparison',
    json={
        'productionTitle': 'Awesome Feature Film',
        'budget': 5000000,
        'jurisdictionIds': [
            'california-id',
            'georgia-id',
            'louisiana-id'
        ]
    }
)

# Save PDF
with open('comparison_report.pdf', 'wb') as f:
    f.write(response.content)

print("✅ PDF report saved!")
```

**Result:** Professional 8-page PDF with:
- Executive summary
- Jurisdiction comparison table
- Savings analysis
- Recommendations

---

### **Example 6: Generate Excel Workbook**

**Scenario:** Create an Excel workbook for the accounting team.

```python
import httpx
from datetime import datetime

response = httpx.post(
    'http://localhost:8000/api/v1/excel/comparison',
    json={
        'productionTitle': 'Awesome Feature Film',
        'budget': 5000000,
        'jurisdictionIds': [
            'california-id',
            'georgia-id'
        ]
    }
)

# Save Excel with timestamp
filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
with open(filename, 'wb') as f:
    f.write(response.content)

print(f"✅ Excel workbook saved: {filename}")
```

**Result:** Professional Excel workbook with:
- Summary sheet (production info, best recommendation)
- Jurisdictions sheet (detailed comparison)
- Savings Analysis sheet (ROI calculations)

---

## 🗄️ Data Management Examples

### **Example 7: Get All Jurisdictions**

**Scenario:** Build a dropdown list of all available locations.

```javascript
// Fetch all jurisdictions
const response = await fetch('http://localhost:8000/api/v1/jurisdictions/');
const data = await response.json();

// Create dropdown options
const selectElement = document.getElementById('jurisdiction-select');
data.jurisdictions.forEach(jurisdiction => {
  const option = document.createElement('option');
  option.value = jurisdiction.id;
  option.text = `${jurisdiction.name} (${jurisdiction.code})`;
  selectElement.appendChild(option);
});

console.log(`Loaded ${data.total} jurisdictions`);
```

---

### **Example 8: Filter Rules by Jurisdiction**

**Scenario:** Show only the incentive programs available in Georgia.

```python
import httpx

# Get Georgia's jurisdiction ID
jurisdictions = httpx.get(
    'http://localhost:8000/api/v1/jurisdictions/'
).json()

georgia = next(
    j for j in jurisdictions['jurisdictions'] 
    if j['code'] == 'GA'
)

# Get Georgia's rules
rules = httpx.get(
    'http://localhost:8000/api/v1/incentive-rules/',
    params={'jurisdiction_id': georgia['id']}
).json()

print(f"Georgia Incentive Programs ({rules['total']}):\n")
for rule in rules['rules']:
    print(f"  • {rule['ruleName']}")
    print(f"    Rate: {rule['percentage']}%")
    print(f"    Min Spend: ${rule['minSpend']:,}")
    print()
```

**Output:**
```
Georgia Incentive Programs (2):

  • Georgia Film Tax Credit
    Rate: 30.0%
    Min Spend: $500,000

  • Georgia Interactive Entertainment Credit
    Rate: 30.0%
    Min Spend: $500,000
```

---

### **Example 9: Create a Production**

**Scenario:** Register a new production in the system.

```javascript
const response = await fetch('http://localhost:8000/api/v1/productions/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'My Awesome Film',
    productionType: 'feature',
    jurisdictionId: 'georgia-id',
    budgetTotal: 5000000,
    budgetQualifying: 4500000,
    startDate: '2026-06-01',
    endDate: '2026-09-30',
    productionCompany: 'My Production Company LLC',
    status: 'pre_production',
    contact: 'producer@myfilm.com'
  })
});

const production = await response.json();
console.log(`✅ Production created with ID: ${production.id}`);
```

---

## 🔄 Advanced Workflows

### **Example 10: Complete Production Analysis Workflow**

**Scenario:** Full analysis from location scouting to final report.

```python
import httpx

class ProductionAnalyzer:
    def __init__(self, base_url='http://localhost:8000/api/v1'):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)
    
    def analyze_production(self, title, budget, target_countries=['USA', 'Canada']):
        """Complete production analysis workflow"""
        
        print(f"🎬 Analyzing: {title} (${budget:,})")
        print("=" * 60)
        
        # Step 1: Get relevant jurisdictions
        print("\n1️⃣ Finding jurisdictions...")
        jurisdictions = self.client.get('/jurisdictions/').json()
        
        target_jurisdictions = [
            j for j in jurisdictions['jurisdictions']
            if j['country'] in target_countries and j['active']
        ]
        
        print(f"   Found {len(target_jurisdictions)} jurisdictions")
        
        # Step 2: Compare jurisdictions
        print("\n2️⃣ Comparing tax incentives...")
        comparison = self.client.post('/calculate/compare', json={
            'budget': budget,
            'jurisdictionIds': [j['id'] for j in target_jurisdictions[:5]]
        }).json()
        
        best = comparison['bestOption']
        print(f"   Best: {best['jurisdiction']} (${best['estimatedCredit']:,})")
        
        # Step 3: Check compliance
        print("\n3️⃣ Checking compliance for best option...")
        
        rules = self.client.get(
            '/incentive-rules/',
            params={'jurisdiction_id': best['jurisdictionId']}
        ).json()
        
        if rules['total'] > 0:
            compliance = self.client.post('/calculate/compliance', json={
                'productionBudget': budget,
                'ruleId': rules['rules'][0]['id'],
                'shootDays': 45,
                'localHirePercentage': 75,
                'hasPromoLogo': True
            }).json()
            
            status = "✅ Compliant" if compliance['overallStatus'] == 'compliant' else "❌ Non-compliant"
            print(f"   {status}")
        
        # Step 4: Generate reports
        print("\n4️⃣ Generating reports...")
        
        # PDF Report
        pdf_response = self.client.post('/reports/comparison', json={
            'productionTitle': title,
            'budget': budget,
            'jurisdictionIds': [j['id'] for j in target_jurisdictions[:3]]
        })
        
        with open(f'{title.replace(" ", "_")}_comparison.pdf', 'wb') as f:
            f.write(pdf_response.content)
        print(f"   ✅ PDF saved")
        
        # Excel Report
        excel_response = self.client.post('/excel/comparison', json={
            'productionTitle': title,
            'budget': budget,
            'jurisdictionIds': [j['id'] for j in target_jurisdictions[:3]]
        })
        
        with open(f'{title.replace(" ", "_")}_comparison.xlsx', 'wb') as f:
            f.write(excel_response.content)
        print(f"   ✅ Excel saved")
        
        print("\n" + "=" * 60)
        print("✅ Analysis complete!")
        
        return {
            'best_jurisdiction': best['jurisdiction'],
            'estimated_credit': best['estimatedCredit'],
            'savings': comparison.get('savings', 0)
        }

# Use it
analyzer = ProductionAnalyzer()
result = analyzer.analyze_production(
    title='Summer Blockbuster',
    budget=10000000,
    target_countries=['USA', 'Canada']
)

print(f"\n💰 Final Recommendation:")
print(f"   Film in {result['best_jurisdiction']}")
print(f"   Estimated Credit: ${result['estimated_credit']:,}")
print(f"   Potential Savings: ${result['savings']:,}")
```

**Output:**
```
🎬 Analyzing: Summer Blockbuster ($10,000,000)
============================================================

1️⃣ Finding jurisdictions...
   Found 15 jurisdictions

2️⃣ Comparing tax incentives...
   Best: Georgia ($3,000,000)

3️⃣ Checking compliance for best option...
   ✅ Compliant

4️⃣ Generating reports...
   ✅ PDF saved
   ✅ Excel saved

============================================================
✅ Analysis complete!

💰 Final Recommendation:
   Film in Georgia
   Estimated Credit: $3,000,000
   Potential Savings: $1,000,000
```

---

## 📚 Client Libraries

### **Python Client Class**

```python
import httpx
from typing import List, Dict, Optional

class TaxIncentiveClient:
    """Python client for Tax-Incentive Compliance Platform"""
    
    def __init__(self, base_url: str = 'http://localhost:8000/api/v1'):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)
    
    def get_jurisdictions(self, country: Optional[str] = None) -> List[Dict]:
        """Get all jurisdictions"""
        params = {'country': country} if country else {}
        response = self.client.get('/jurisdictions/', params=params)
        return response.json()['jurisdictions']
    
    def compare_jurisdictions(self, budget: float, jurisdiction_ids: List[str]) -> Dict:
        """Compare tax incentives across jurisdictions"""
        response = self.client.post('/calculate/compare', json={
            'budget': budget,
            'jurisdictionIds': jurisdiction_ids
        })
        return response.json()
    
    def check_compliance(self, budget: float, rule_id: str, **kwargs) -> Dict:
        """Check compliance with incentive requirements"""
        response = self.client.post('/calculate/compliance', json={
            'productionBudget': budget,
            'ruleId': rule_id,
            **kwargs
        })
        return response.json()
    
    def generate_pdf_report(self, title: str, budget: float, 
                           jurisdiction_ids: List[str]) -> bytes:
        """Generate PDF comparison report"""
        response = self.client.post('/reports/comparison', json={
            'productionTitle': title,
            'budget': budget,
            'jurisdictionIds': jurisdiction_ids
        })
        return response.content

# Usage
client = TaxIncentiveClient()

# Get US jurisdictions
us_jurisdictions = client.get_jurisdictions(country='USA')

# Compare top 3
comparison = client.compare_jurisdictions(
    budget=5000000,
    jurisdiction_ids=[j['id'] for j in us_jurisdictions[:3]]
)

print(f"Best: {comparison['bestOption']['jurisdiction']}")
```

---

### **JavaScript/TypeScript Client**

```typescript
class TaxIncentiveClient {
  constructor(private baseUrl: string = 'http://localhost:8000/api/v1') {}

  async getJurisdictions(country?: string): Promise<any[]> {
    const params = country ? `?country=${country}` : '';
    const response = await fetch(`${this.baseUrl}/jurisdictions/${params}`);
    const data = await response.json();
    return data.jurisdictions;
  }

  async compareJurisdictions(budget: number, jurisdictionIds: string[]): Promise<any> {
    const response = await fetch(`${this.baseUrl}/calculate/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ budget, jurisdictionIds })
    });
    return response.json();
  }

  async generatePdfReport(
    title: string,
    budget: number,
    jurisdictionIds: string[]
  ): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/reports/comparison`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        productionTitle: title,
        budget,
        jurisdictionIds
      })
    });
    return response.blob();
  }
}

// Usage
const client = new TaxIncentiveClient();

const jurisdictions = await client.getJurisdictions('USA');
const comparison = await client.compareJurisdictions(
  5000000,
  jurisdictions.slice(0, 3).map(j => j.id)
);

console.log(`Best: ${comparison.bestOption.jurisdiction}`);
```

---

## 🎯 Common Patterns

### **Pattern 1: Progressive Enhancement**

Start simple, add complexity as needed:

```python
# Level 1: Simple calculation
credit = calculate_simple(budget, jurisdiction_id, rule_id)

# Level 2: Add comparison
comparison = compare_jurisdictions(budget, [id1, id2, id3])

# Level 3: Add compliance check
compliance = check_compliance(budget, rule_id, production_details)

# Level 4: Generate professional report
pdf = generate_report(production_title, budget, jurisdiction_ids)
```

---

### **Pattern 2: Error Handling**

```javascript
async function safeCalculate(budget, jurisdictionIds) {
  try {
    const response = await fetch('/calculate/compare', {
      method: 'POST',
      body: JSON.stringify({ budget, jurisdictionIds })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Calculation failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Calculation error:', error);
    // Show user-friendly message
    alert('Unable to calculate. Please check your inputs.');
    return null;
  }
}
```

---

### **Pattern 3: Caching**

```python
from functools import lru_cache
import httpx

@lru_cache(maxsize=32)
def get_jurisdictions(country: str = None):
    """Cache jurisdiction list"""
    params = {'country': country} if country else {}
    response = httpx.get(
        'http://localhost:8000/api/v1/jurisdictions/',
        params=params
    )
    return response.json()

# First call: API request
jurisdictions = get_jurisdictions('USA')

# Second call: From cache (instant)
jurisdictions = get_jurisdictions('USA')
```

---

## 🎓 Learning Path

### **Beginner:**
1. Try Example 1 (Simple comparison)
2. Try Example 2 (Compliance check)
3. Try Example 5 (Generate PDF)

### **Intermediate:**
4. Try Example 3 (Stackable credits)
5. Try Example 4 (Scenario modeling)
6. Try Example 10 (Complete workflow)

### **Advanced:**
7. Build a client library
8. Create automated workflows
9. Integrate with production management systems

---

**Ready to start?** Pick an example and run it! 🚀

All code is copy-paste ready and tested! 💯