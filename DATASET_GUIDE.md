# NyayaSahaya — Dataset Preparation Guide

This guide explains how to prepare and add your own legal documents to the RAG system.

## Supported Document Formats

- **Plain Text (.txt)** ✅ Recommended
- **PDF (.pdf)** ✅ Supported

## Document Structure Guidelines

### Best Practice Format

```
[ACT NAME AND YEAR]

SECTION [NUMBER] — [TITLE]
[Full section text with definitions and explanations]

SECTION [NUMBER] — [TITLE]
[Full section text]

IMPORTANT POINTS / SUMMARY / KEY PROVISIONS
- Point 1
- Point 2
- Point 3

HOW TO APPLY
[Practical steps for citizens]
```

### Example Document

```
PROTECTION OF WOMEN FROM DOMESTIC VIOLENCE ACT, 2005

SECTION 2 — DEFINITIONS
(a) "Aggrieved Person" means any woman who is, or has been, in an intimate 
relationship with the respondent and who alleges to have been subjected to 
any act of domestic violence by the respondent.

(b) "Domestic Violence" includes:
- Acts of physical violence
- Acts of sexual abuse
- Acts of verbal and emotional abuse
- Acts of economic abuse

SECTION 3 — RIGHT TO PROTECTION FROM DOMESTIC VIOLENCE
(1) Every woman who is subjected to domestic violence has the right to protection 
from domestic violence.

HOW TO FILE A COMPLAINT
1. Approach the Magistrate Court in your district
2. Or file with the Protection Officer appointed under this Act
3. Can be filed orally or in writing
```

## Chunking Strategy

The system automatically chunks documents. Optimal chunk sizes:

| Document Type | Chunk Size | Overlap | Notes |
|---|---|---|---|
| Complex Acts | 500 words | 50 words | Legal terminology needs context |
| Simple Guides | 300 words | 30 words | Consumer-friendly content |
| Q&A Format | 200 words | 20 words | Already structured |

**Default Configuration:**
```python
chunk_size = 500
chunk_overlap = 50
separators = ["\n\n", "\n", "SECTION", "Section", ". ", " ", ""]
```

## Content Organization Tips

### 1. Use Clear Section Headers
```
✅ GOOD:
SECTION 302 — PUNISHMENT FOR MURDER
What this means: ...

❌ BAD:
Sec 302 punishment murder
means ...
```

### 2. Include Practical Examples
```
✅ GOOD:
SECTION 375 — RAPE
[Definition]
Examples: A person who has sexual intercourse against will of woman

❌ BAD:
SECTION 375 — RAPE
[Definition only]
```

### 3. Separate Definitions & Implementation
```
✅ GOOD:
DEFINITIONS:
- Term 1: meaning
- Term 2: meaning

HOW TO APPLY:
1. Step 1
2. Step 2

❌ BAD:
Everything mixed together
```

### 4. Include Remedies & Rights
```
✅ GOOD:
RIGHTS UNDER THIS ACT:
- Right to protection
- Right to compensation
- Right to legal aid

HOW TO FILE COMPLAINT:
1. Contact authority
2. Provide details
3. Get case number
```

## Dataset Expansion Plan

### Phase 1: Core Acts (Already Included)
- ✅ Indian Penal Code (IPC) - Criminal
- ✅ Consumer Protection Act, 2019
- ✅ Protection of Women from Domestic Violence Act, 2005
- ✅ Transfer of Property Act, 1882 - Tenancy

### Phase 2: Important Acts (To Add)
- [ ] Code of Criminal Procedure (CrPC)
- [ ] Hindu Marriage Act, 1955
- [ ] Muslim Personal Law (Shariat) Application Act, 1937
- [ ] Land Acquisition Act, 2013
- [ ] Right to Information Act, 2005
- [ ] Factories Act, 1948
- [ ] Industrial Disputes Act, 1947
- [ ] Persons with Disabilities Act, 2016
- [ ] Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989

### Phase 3: State-Specific Laws
- [ ] Tamil Nadu Building Rules
- [ ] State Tenancy Acts
- [ ] State-specific labor laws

## Adding Documents

### Method 1: Upload via UI
1. Open NyayaSahaya frontend
2. Go to "Upload Documents" tab
3. Drag & drop .txt or .pdf file
4. System auto-chunks and indexes

### Method 2: Manual Addition
1. Place files in `backend/app/data/sample_docs/`
2. Restart backend or call `POST /api/documents/index-all`

### Method 3: API Upload
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@IPC_Section_300_to_500.txt"
```

## Quality Metrics

Track document quality with these metrics:

| Metric | Target | Why |
|---|---|---|
| Avg Chunk Size | 400-600 words | Balanced retrieval |
| Vocabulary Difficulty | 8-10th grade level | Citizens understand |
| Examples per Section | 1-2 | Practical understanding |
| Section Clarity | >90% sentences complete | Prevents mid-sentence cuts |

## Search Performance

After adding documents, test with queries:

```
Q: "What is my right as a tenant?"
Expected: Returns Tenancy_Rights.txt sections

Q: "சிறுமையை அதிகாரப்பூர்வமாக எதிர்க்க முடியுமா?"
Expected: Returns Domestic Violence Act sections (in Tamil)

Q: "What compensation can I claim for a defective product?"
Expected: Returns Consumer Protection Act sections
```

## Maintenance

### Regular Updates
- Review documents quarterly for legal changes
- Update outdated sections with new amendments
- Add landmark court rulings

### Performance Monitoring
- Track query response times (target: <3s)
- Monitor embedding quality (cosine similarity > 0.7)
- Check user satisfaction (feedback widget)

### Backup Strategy
```bash
# Backup FAISS index
cp -r backend/app/data/vector_store /backup/vector_store_$(date +%Y%m%d)

# Backup source documents
cp -r backend/app/data/sample_docs /backup/sample_docs_$(date +%Y%m%d)
```

## Document Verification Checklist

Before adding a document:

- [ ] Document is from official/authoritative source
- [ ] Sections are complete and not truncated
- [ ] Definitions are included
- [ ] Practical application is explained
- [ ] Links to related sections are clear
- [ ] Language is simple and accessible
- [ ] Examples are provided where helpful
- [ ] Amendment status is current (as of 2025)
- [ ] No copyright issues (public domain/government docs)
- [ ] Formatted consistently with other documents

## Tamil Language Documents

For Tamil documents:

1. **Use proper Unicode encoding** (UTF-8)
2. **Maintain English section numbers** for searchability
3. **Include both Tamil and English** key terms
4. **Test with Tamil language detector** (langdetect)

Example:
```
பிரிவு 498A — கணவன் அல்லது அவனது உறவினரால் கொடுமை

SECTION 498A — CRUELTY BY HUSBAND OR HIS RELATIVE

இந்தப் பிரிவின் கீழ் வரையறை:
"கொடுமை" என்பது பெண்ணுக்கு உடல் அல்லது மன வலி கொடுக்கும் எந்த செயலையும் குறிக்கிறது.
```

## Performance Optimization

### Reduce Retrieval Latency
1. **Index only critical sections** - Don't index preambles
2. **Remove redundant content** - Deduplicate similar sections
3. **Use smaller chunks** for frequently accessed sections
4. **Pre-compute common queries** in cache

### Improve Answer Quality
1. **Add context** to sections (related acts/amendments)
2. **Include court rulings** that interpret the law
3. **Add FAQ-style explanations** for complex sections
4. **Use metadata tags** (civil/criminal/time-bound)

---

**Next Steps:**
1. Add 5-10 more core Indian laws
2. Implement state-specific filtering
3. Add legal precedent database
4. Enable multilingual searches (Tamil, Telugu, Kannada, Malayalam)

