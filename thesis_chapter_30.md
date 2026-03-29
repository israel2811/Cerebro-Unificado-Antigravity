# Chapter 30: Reproducible Methodology — The P0-P4 Protocol in Detail

## 30.1 Introduction: Why Protocol Matters

The cornerstone of scientific credibility is reproducibility. This chapter provides a complete, step-by-step guide to the P0-P4 Protocol—a reproducible methodology for assessing Cyber-Acoustic Convergence that any trained investigator can follow to obtain consistent, comparable results.

## 30.2 Protocol Philosophy

### 30.2.1 Core Principles

1. **Neutral starting point**: No assumption of etiology
2. **Evidence accumulation**: Build from E0 toward higher levels
3. **Falsifiability**: Each step can disconfirm hypotheses
4. **Reversibility**: Conclusions can be revised with new evidence
5. **Transparency**: Full documentation of methods and findings
6. **Anti-iatrogenia**: Minimize harm from the assessment process itself

### 30.2.2 What the Protocol Is NOT

- Not a diagnostic tool (informs, doesn't replace clinical judgment)
- Not an investigation of third parties (defensive only)
- Not a legal proceeding (standard of evidence differs)
- Not definitive (provides probability, not certainty)

## 30.3 P0: Phenomenological and Clinical Triage

### 30.3.1 Purpose

Structured documentation of the reported experience without presuming etiology.

### 30.3.2 P0 Components

#### P0-A: Experience Description

| Variable | Prompt | Format |
|----------|--------|--------|
| Content | "What do the voices say?" | Verbatim if possible |
| Clarity | "How clear/understandable?" | 1-10 scale |
| Volume | "Whisper? Normal? Loud?" | Categorical |
| Location | "Where does it seem to come from?" | Internal/external/mixed |
| Frequency | "How often?" | Count per day/week |
| Duration | "How long does each episode last?" | Minutes/hours |
| Timing | "When does it typically occur?" | Pattern description |

#### P0-B: Contextual Factors

| Variable | Prompt | Format |
|----------|--------|--------|
| Device association | "Which devices/settings?" | List |
| Environmental conditions | "Noise level? Location?" | Description |
| State factors | "Tired? Stressed? Substances?" | Checklist |
| Temporal pattern | "Time of day? Day of week?" | Pattern |
| Modulation | "What makes it better/worse?" | List |

#### P0-C: Background and Risk

| Variable | Assessment | Action |
|----------|------------|--------|
| Psychiatric history | Prior diagnoses, treatment | Document |
| Substance use | Current, recent | Document |
| Medical conditions | Hearing, neuro | Document, refer if needed |
| Risk assessment | Harm to self/others | Safety protocol if indicated |
| Social context | IPV, conflict, isolation | Document, refer if needed |

### 30.3.3 P0 Outputs

1. Structured phenomenological profile
2. Risk assessment determination
3. Preliminary FPI layer distribution (tentative)
4. Indication for P1-P4 continuation

### 30.3.4 P0 Stop Rules

**Proceed to P1** if:
- Device/technology association present
- No immediate safety concerns requiring escalation
- Subject consents to continued assessment

**Do NOT proceed** if:
- Active psychosis requiring immediate treatment
- Imminent risk to self/others
- Subject does not consent
- Adequate clinical explanation already present

## 30.4 P1: Defensive Device Audit

### 30.4.1 Purpose

Document the technological landscape associated with the experience.

### 30.4.2 P1 Components

#### P1-A: Device Inventory

| Data Point | Method | Documentation |
|------------|--------|---------------|
| Devices used | Subject report | Make, model, OS |
| Primary devices | Identify 1-3 key devices | Photographs |
| Software/apps | Subject walk-through | App list export |
| Accounts | Subject report | Account names, sync status |

#### P1-B: Permission Audit

| Permission | Check | Flag |
|------------|-------|------|
| Microphone | Which apps? | Unknown apps = concern |
| Camera | Which apps? | Unnecessary access = concern |
| Location | Which apps? | Unexpected = concern |
| Contacts | Which apps? | Unusual = document |
| Background activity | Which apps? | High = investigate |

#### P1-C: Behavioral Indicators

| Indicator | Assessment | Significance |
|-----------|------------|--------------|
| Battery drain | Compared to baseline | Medium |
| Data usage | Compared to baseline | Medium |
| Unknown apps | Not recalled by subject | High |
| Delayed shutdown | Persists after power button | Medium |
| Unusual notifications | Unrecognized | Medium |

#### P1-D: Documentation

- Screenshots of all permission settings
- App lists with install dates
- Photos of devices
- Hash of any exported data

### 30.4.3 P1 Outputs

1. Device inventory document
2. Permission risk summary
3. Indicators of concern checklist
4. Recommendation for further forensic analysis (if indicated)

### 30.4.4 P1 Limits

P1 provides descriptive inventory, NOT:
- Definitive detection of surveillance
- Exoneration from surveillance concern
- Technical diagnosis

## 30.5 P2: Environmental Acoustic Audit

### 30.5.1 Purpose

Characterize the acoustic environment where experiences occur.

### 30.5.2 P2 Components

#### P2-A: Site Survey

| Element | Documentation |
|---------|---------------|
| Room dimensions | Measured |
| Surface materials | Catalogued |
| HVAC sources | Identified, photographed |
| Electronic devices | Listed |
| Windows/doors | Noted |
| Noise sources | Interior and exterior |

#### P2-B: Acoustic Measurement

| Measurement | Equipment | Parameters |
|-------------|-----------|------------|
| SPL | Calibrated meter | dB(A), dB(C) |
| Frequency spectrum | Analyzer | 20 Hz - 20 kHz |
| Modulation spectrum | Analysis software | 1-20 Hz |
| Spatial variation | Multiple positions | At least 4 points |

#### P2-C: Recording Session

| Parameter | Specification |
|-----------|---------------|
| Duration | Minimum 15 minutes |
| Channels | Minimum 2 (stereo) |
| Sample rate | 44.1 kHz or higher |
| Bit depth | 16-bit or higher |
| Calibration | Pre- and post-session |

#### P2-D: SPIA Potential Analysis

Apply SPIA metrics (Chapter 12):
- Spectral formant-likeness (PC1)
- Modulation envelope (PC2)
- Combined SPIA potential score

### 30.5.3 P2 Outputs

1. Site survey document with diagrams
2. Measurement data with calibration record
3. SPIA potential score for environment
4. Identified high-SPIA sources
5. Recommendations for environmental modification

## 30.6 P3: Contrast and Manipulation Testing

### 30.6.1 Purpose

Establish causal relationships through controlled manipulation.

### 30.6.2 P3-A: ABAB Design

**Structure**:
| Phase | Condition | Duration | Measurement |
|-------|-----------|----------|-------------|
| A1 | Baseline | 1 week | Experience logging |
| B1 | Intervention | 1 week | Experience logging |
| A2 | Withdrawal | 1 week | Experience logging |
| B2 | Reintervention | 1 week | Experience logging |

**Possible interventions**:
- Change device/codec
- Add environmental intervention
- Modify call settings
- Remove identified SPIA source

### 30.6.3 P3-B: Isolation Tests

| Test | Procedure | Interpretation |
|------|-----------|----------------|
| Device swap | Change to different phone | Effect = device-related |
| Environment change | Different location | Effect = environment-related |
| Faraday cage | RF-shielded room | Effect = RF-related |
| Landline test | Non-VoIP comparison | Effect = VoIP-specific |

### 30.6.4 P3-C: Blind Panel Evaluation

For recorded audio:
1. Extract segments of interest
2. Remove identifiers
3. Present to 5+ naïve listeners
4. Collect transcription attempts
5. Calculate inter-rater reliability (κ)

**Interpretation**:
| κ Value | Interpretation |
|---------|----------------|
| < 0.20 | Poor agreement (no semantic consensus) |
| 0.21-0.40 | Fair (partial pattern) |
| 0.41-0.60 | Moderate (some agreement) |
| 0.61-0.80 | Substantial (likely real content) |
| > 0.80 | Almost perfect (definitely real speech) |

### 30.6.5 P3 Outputs

1. ABAB results with effect sizes
2. Isolation test outcomes
3. Blind panel κ values
4. Pattern summary across tests

## 30.7 P4: FPI Integration and Scenario Assignment

### 30.7.1 Purpose

Synthesize P0-P3 findings into integrated assessment.

### 30.7.2 P4-A: Layer Synthesis

| FPI Layer | P0-P3 Evidence | Strength (E0-E4) |
|-----------|----------------|------------------|
| Source | P1 + P2 findings | Assign level |
| Perception | P0 + P3 results | Assign level |
| Interpretation | P0 + P3 panel | Assign level |

### 30.7.3 P4-B: Scenario Classification

Apply criteria (Chapter 24):

| Pattern | Scenario Assignment |
|---------|---------------------|
| Structure + Agreement | A (Exogenous) |
| Structure + No Agreement | B (SPIA) |
| No Structure + Consistency | C (Endogenous) |
| Mixed/Incomplete | D (Indeterminate) |

### 30.7.4 P4-C: Evidence Level Determination

| Criterion | Evidence Level |
|-----------|----------------|
| Only subject report | E1 |
| Plus objective measurement | E2 |
| Plus convergent multi-layer | E3 |
| Plus experimental confirmation (ABAB) | E4 |

### 30.7.5 P4-D: Recommendations

Based on scenario and evidence:

| Scenario | E-Level | Recommendation |
|----------|---------|----------------|
| A | E3+ | Technical fix, document |
| B | E2+ | Tier 1-2 SPIA intervention |
| B | E4 | Full SPIA protocol confidently |
| C | E3+ | Psychiatric referral |
| D | Any | Continue assessment, multimodal |

### 30.7.6 P4 Outputs

1. Integrated FPI assessment document
2. Scenario assignment with confidence
3. Evidence level determination
4. Recommendations matched to findings
5. Documentation for clinical record

## 30.8 Documentation Standards

### 30.8.1 Required Documentation

| Element | Format | Storage |
|---------|--------|---------|
| P0 interview | Narrative + structured | Secure clinical record |
| P1 inventory | Checklist + photos | Encrypted storage |
| P2 measurements | Data files + report | Calibration attached |
| P3 results | Statistical summary | With raw data |
| P4 integration | Formal report | Shared with subject |

### 30.8.2 Data Security

- Encrypted storage for all data
- Minimum necessary access
- Clear retention policy
- Subject has right to access their own data

### 30.8.3 Report Template

A standardized P0-P4 report template should include:
1. Subject identifier (pseudonymized)
2. Assessment dates and locations
3. Personnel involved
4. P0 summary
5. P1 findings
6. P2 measurements and SPIA scores
7. P3 experimental results
8. P4 integration and recommendations
9. Limitations and uncertainties
10. Signature and credentials

## 30.9 Training Requirements

### 30.9.1 Who Can Conduct P0-P4

| Phase | Required Training |
|-------|-------------------|
| P0 | Mental health professional, CCA training |
| P1 | Technical training, security awareness |
| P2 | Acoustic measurement certification |
| P3 | Research methods, statistical training |
| P4 | Integrative assessment, CCA model mastery |

### 30.9.2 Inter-Rater Reliability Goals

For research purposes:
- P0 structured interview: κ > 0.6
- P2 SPIA scoring: ICC > 0.8
- P4 scenario assignment: κ > 0.7

## 30.10 Conclusion: Reproducibility as Foundation

The P0-P4 Protocol provides:
- Standardized, reproducible methodology
- Clear documentation requirements
- Explicit decision criteria
- Trainable, auditable procedures

This protocol transforms CCA assessment from intuitive judgment to systematic science.

---
**Status**: Draft - v1.0
**Word Count**: ~2,200 words
**Integration**: All assessment chapters (16-18), FPI (23), Scenarios (24)
