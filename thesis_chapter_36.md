# Chapter 36: Literature Review and Originality Verification

## 36.1 Introduction: Standing on Solid Ground

Before claiming originality, we must verify that the contribution is genuinely novel. This chapter documents the literature review strategy, search methodology, and gap analysis that establishes the originality of CCA research.

## 36.2 Research Questions for Literature Review

### 36.2.1 Primary Scoping Questions

1. **Has CCA been proposed before?**
   - Search: "cyber-acoustic" OR "techno-acoustic" OR "digital hallucination"
   - Expected: Novel term; convergence concept may be partially addressed

2. **Is "sin estímulo externo" critiqued in literature?**
   - Search: "without external stimulus" AND "hallucination" AND "criterion"
   - Expected: Methodological critiques exist but not systematically

3. **Are digital artifacts linked to voice perception?**
   - Search: ("codec" OR "VoIP" OR "packet loss") AND ("speech perception" OR "hallucination")
   - Expected: Engineering studies on quality; minimal clinical connection

4. **Is there a framework like FPI?**
   - Search: ("source" OR "perception" OR "interpretation") AND "hallucination" AND "model"
   - Expected: Related models exist; specific FPI formulation is novel

### 36.2.2 Secondary Questions

5. How is pareidolia studied in auditory domain?
6. What assessment tools exist for "device-related" hallucinations?
7. How is stalkerware implicated in mental health literature?
8. What forensic protocols exist for audio-related mental health claims?

## 36.3 Database Strategy

### 36.3.1 Clinical/Psychological Databases

| Database | Coverage | Access |
|----------|----------|--------|
| PubMed/MEDLINE | Biomedical | Free |
| PsycINFO | Psychology | Institutional |
| Cochrane | Systematic reviews | Free |
| Embase | European medical | Institutional |

### 36.3.2 Engineering/Technical Databases

| Database | Coverage | Access |
|----------|----------|--------|
| IEEE Xplore | Electrical engineering | Institutional |
| ACM Digital Library | Computing | Institutional |
| arXiv | Preprints (cs, eess) | Free |
| IETF RFCs | Internet standards | Free |

### 36.3.3 Interdisciplinary Sources

| Source | Coverage | Notes |
|--------|----------|-------|
| Google Scholar | Broad | Citation tracking |
| Semantic Scholar | AI-enhanced | Related papers |
| ResearchGate | Researcher profiles | Contact authors |
| Preprint servers | Emerging work | Not peer-reviewed |

## 36.4 Search Strategy

### 36.4.1 Search Terms by Domain

**Clinical**:
- "auditory hallucination" OR "voice hearing" OR "AVH"
- "differential diagnosis"
- "without external stimulus"
- "misattribution"

**Psychoacoustic**:
- "speech in noise"
- "auditory pareidolia"
- "phonemic restoration"
- "pattern perception"

**Telecom/DSP**:
- "voice codec" AND "artifact"
- "packet loss concealment"
- "comfort noise"
- "VAD" AND "DTX"

**Forensic/Security**:
- "stalkerware" OR "spyware"
- "digital forensics" AND "audio"
- "surveillance" AND "mental health"

### 36.4.2 Boolean Strategy

```
("auditory hallucination" OR "voice hearing" OR "AVH") 
AND 
("technology" OR "digital" OR "phone" OR "VoIP" OR "codec")
NOT
("cochlear implant") # Exclude implant literature
```

### 36.4.3 Snowballing Protocol

1. **Forward snowballing**: Who cited key papers?
2. **Backward snowballing**: What did key papers cite?
3. **Author tracking**: Other work by key authors
4. **Keyword extraction**: New terms from found papers

## 36.5 Inclusion/Exclusion Criteria

### 36.5.1 Inclusion

- Empirical studies on auditory hallucinations
- Theoretical frameworks for voice-hearing
- Technical literature on voice codecs and artifacts
- Forensic audio analysis methods
- Assessment tools for hallucinations
- Stalkerware/spyware prevalence studies

### 36.5.2 Exclusion

- Non-auditory hallucinations (unless comparative)
- Animal studies (unless mechanism relevant)
- Non-English without translation (note limitation)
- Case reports < 5 (insufficient evidence)
- Industry marketing materials

## 36.6 Documentation Method

### 36.6.1 Search Log Template

| Date | Database | Query | Results | Screened | Included | Notes |
|------|----------|-------|---------|----------|----------|-------|
| YYYY-MM-DD | PubMed | query string | N | N | N | observations |

### 36.6.2 PRISMA-Style Screening

```
Identification: N records from databases + N from other sources
         ↓
Screening: N records after duplicates removed
         ↓
         N records excluded (title/abstract)
         ↓
Eligibility: N full-text articles assessed
         ↓
         N excluded with reasons
         ↓
Included: N studies in synthesis
```

### 36.6.3 Reference Management

Tool: Zotero (free, open-source)
- Automatic citation import
- PDF attachment
- Tagging by theme
- Export to BibTeX for APA 7

## 36.7 Gap Mapping

### 36.7.1 What Exists

| Topic | Literature Status | Key References |
|-------|-------------------|----------------|
| AVH phenomenology | Well-developed | Waters et al., Larøi et al. |
| Predictive processing | Well-developed | Clark, Friston, Nazimek |
| Auditory pareidolia | Limited research | Belin, Pernet |
| Voice codec engineering | Technical standards | 3GPP, IETF RFC |
| Stalkerware prevalence | Industry reports | Coalition Against Stalkerware |
| Digital forensics | Procedures exist | NIST, SWGDE |

### 36.7.2 What's Missing (The Gap)

| Gap | Description | CCA Contribution |
|-----|-------------|------------------|
| **Integration** | No model connecting telecom artifacts to AVH | CCA + FPI |
| **Methodology** | No protocol for "device-related" AVH assessment | P0-P4 |
| **Critique** | "Sin estímulo" not systematically questioned | Epistemological analysis |
| **Tools** | No SPIA-specific screener | SPIA-SS, CCA-CIP |
| **Evidence framework** | No E0-E4 calibration | Evidence ladder |

### 36.7.3 Originality Statement

The literature review establishes that:

1. **The CCA model** is a novel integration of known components
2. **The FPI framework** formalizes implicit distinctions not previously codified
3. **The P0-P4 protocol** addresses an unmet methodological need
4. **The epistemological critique** extends existing concerns systematically
5. **The SPIA concept** names a phenomenon previously undescribed

## 36.8 Limitations of the Review

### 36.8.1 Language Bias

- Primarily English-language sources
- May miss relevant work in Spanish, Chinese, German, etc.
- Acknowledging limitation explicitly

### 36.8.2 Publication Bias

- Null results may be unpublished
- Industry research may be proprietary
- Preprints provide partial correction

### 36.8.3 Recency Bias

- Rapidly evolving field (AI, codecs)
- Recent preprints may not be peer-reviewed
- Balance recency with rigor

## 36.9 Updating the Review

### 36.9.1 Alert Services

- Google Scholar alerts for key terms
- PubMed email updates for saved searches
- arXiv notifications for relevant categories

### 36.9.2 Living Review Concept

- Maintain cumulative bibliography
- Update annually or at major milestones
- Document new findings and their implications

## 36.10 Conclusion: Establishing the Contribution

The literature review confirms:
1. **CCA addresses a genuine gap** in the literature
2. **The contribution is original** in its integration
3. **Methodology is needed** and not currently available
4. **The critique is timely** given technological changes

This positions the thesis as a defensible original contribution to knowledge.

---
**Status**: Draft - v1.0
**Word Count**: ~1,400 words
**Integration**: Methodology (30), Publication (34), All content chapters
