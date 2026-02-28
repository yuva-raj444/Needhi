# NyayaSahaya — Classifier Prompt Examples

This document provides examples for how the legal issue classifier works and how to prompt it for best results.

## Supported Categories

| Category | Emoji | Keywords | Examples |
|---|---|---|---|
| **Criminal** | 🔴 | FIR, assault, theft, fraud, cybercrime, murder | "Someone stole my phone", "I was robbed", "He threatened me" |
| **Civil** | 🔵 | contract, property, tort, injunction, lawsuit | "Dispute over payment", "Someone owes me money", "I signed a contract" |
| **Family** | 💜 | divorce, custody, marriage, maintenance | "My husband wants divorce", "Child support", "Alimony" |
| **Consumer** | 🟢 | defective product, service complaint, refund | "Appliance is broken", "Service was not delivered", "Wrong product received" |
| **Land** | 🟤 | property, title, tenant, land acquisition | "Property dispute", "Encroachment", "Tenant issues" |
| **Welfare** | 🟠 | government scheme, labor, RTI, social security | "Not getting government pension", "Labor dispute", "RTI request" |

---

## Example Inputs & Classifier Outputs

### Example 1: Domestic Violence
```
Input (English):
"My husband drinks alcohol every day and beats me. He calls me names and doesn't let me meet my family. 
This has been going on for 2 years."

Detected Category: Family
Confidence: High
Explanation: This describes domestic violence with physical and emotional abuse within a marriage.
```

### Example 2: Tenant Dispute
```
Input (Tamil):
"என் வீட்டு உரிமையாளர் என் பாதுகாப்புத் தொகையை திருப்பி தர மறுக்கிறார். 
மாதாந்திர வாடகை கட்டுவதற்கு எனக்கு பெரிய சிரமம் ஆகிறது."

Translation: "My landlord is refusing to return my security deposit. I'm struggling to pay 
monthly rent."

Detected Category: Land
Confidence: High
Explanation: This is a tenant-landlord dispute regarding security deposit refund and rent.
```

### Example 3: Product Defect
```
Input (English):
"I bought a refrigerator from ABC Electronics last week. The cooling is not working properly. 
They refuse to repair or replace it. It cost me ₹50,000."

Detected Category: Consumer
Confidence: High
Explanation: This is a consumer complaint regarding a defective product under Consumer Protection Act.
```

### Example 4: Workplace Harassment
```
Input (English):
"My boss always gives me extra work but doesn't pay me the promised bonus. 
Other employees get promotions but I don't even though I work harder."

Detected Category: Welfare
Confidence: High
Explanation: This involves labor rights and workplace fairness covered under labor laws.
```

### Example 5: Fraud
```
Input (English):
"A man pretended to be a bank official and convinced me to give him my ATM details. 
He withdrew ₹1,00,000 from my account without permission."

Detected Category: Criminal
Confidence: High
Explanation: This is a cyber fraud crime that should be reported as an FIR.
```

---

## RAG Q&A Example Prompts

### Example 1: Section-Specific Question
```
Q: "What is Section 498A of IPC?"
A: Section 498A of the IPC addresses cruelty by husband or his relatives. It defines:
   - Acts of physical, sexual, verbal, emotional, or economic abuse
   - Punishment: Up to 3 years imprisonment + fine up to ₹1,000
   - Can be filed as both cognizable and non-bailable offense
   [Retrieved from IPC_Sample.txt]
```

### Example 2: Rights-Based Question
```
Q: "What are my rights if my landlord refuses to return security deposit?"
A: Under the Transfer of Property Act:
   - Security deposit is held in trust for you
   - Landlord must return it within 30 days of lease termination
   - Deductions only allowed for actual damages or unpaid rent
   - You can claim interest (8-12% per annum as per state law)
   - Non-refund is grounds for legal action in district court
   [Retrieved from Tenancy_Rights.txt]
```

### Example 3: Tamil-Language Question
```
Q (Tamil): "குற்ற வழக்கில் FIR பதிவு செய்ய என் உரிமைகள் என்ன?"
Translation: "What are my rights to file an FIR in a criminal case?"

A (Tamil): [Response in Tamil about FIR process]
   - நீங்கள் பொலிஸ் நிலையத்தில் செல்லலாம்
   - எழுத்துப்பூர்வமாக அல்லது வாய்மொழியாக புகார் தெரிவிக்கலாம்
   - பொலிஸ் FIR பதிவு செய்ய கட்டாயமாக வேண்டும்
```

### Example 4: Consumer Rights
```
Q: "Can I get a refund for a defective phone?"
A: Yes, under Consumer Protection Act 2019:
   - If product has manufacturing defect within warranty period
   - Consumer can claim:
     * Replacement of goods
     * Refund of price
     * Compensation for loss
     * Cost of repair
   - File complaint with District Consumer Protection Commission
   - No fee charged for filing
```

---

## Tips for Accurate Classification

1. **Be descriptive** - More details help classifier understand better
2. **Mention key facts** - Names, dates, amounts help
3. **Use clear language** - Simple Tamil or English works best
4. **Ask specific questions** - "What is my right?" vs "I have a problem"
5. **Provide context** - Relationships, timeline, amounts matter

---

## Common Ambiguous Cases

### Case 1: Could be Civil or Consumer
```
Q: "A shop sold me damaged goods. Can I sue?"
Classification: Consumer (90% confidence)
Reason: Involves product quality/defect under Consumer Protection Act first
Alternative: Could also involve civil contract if custom goods involved
```

### Case 2: Could be Family or Criminal
```
Q: "My ex-husband abused me and stole my jewelry."
Classification: Family (70%), Criminal (30%)
Recommendation: File both - DV Act case + FIR for theft
```

### Case 3: Could be Land or Civil
```
Q: "My neighbor is claiming my land as theirs."
Classification: Land (80%), Civil (20%)
Recommendation: Handle as property/land dispute in district court
```

---

## Deployment Notes

- Classifier runs via LLM (GPT-4) for accuracy
- Fallback: If LLM fails, defaults to "Civil" category
- Confidence levels: High > Medium > Low
- Works in both English and Tamil
- Context window allows complex descriptions

