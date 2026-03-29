# Chapter 23: The FPI Integrative Model — From Signal Source to Clinical Interpretation

## 23.1 Introduction: A Unified Framework for Understanding CCA

The complexity of Signal-Induced Algorithmic Pareidolia (SPIA) and Cyber-Acoustic Convergence (CCA) demands a comprehensive analytical framework capable of integrating technical, perceptual, and interpretive domains. This chapter introduces the **FPI Model** (Fuente–Percepción–Interpretación / Source–Perception–Interpretation), an operational framework designed to structure assessment, guide research, and prevent inferential errors in cases where technology, perception, and meaning intersect.

## 23.2 The Three Layers of FPI

### 23.2.1 Layer 1: FUENTE (Source)

**Definition**: The physical origin of the auditory stimulus, encompassing both the ultimate source and the transformations it undergoes before reaching the ear.

**Observable Variables**:
| Variable | Measurement Method | Falsification Criterion |
|----------|-------------------|------------------------|
| Acoustic energy present | Calibrated recording, SPL meter | No detectable signal above noise floor |
| Spectral content | STFT, spectrograms | Absence of speech-frequency energy |
| Temporal structure | Modulation analysis | No 4-8 Hz modulation |
| Source location | Multi-channel triangulation | No consistent spatial origin |
| Technological transformation | Codec analysis, packet capture | No evidence of processing artifacts |

**Possible Source Categories**:
1. **Exogenous speech**: Actual human voice transmitted via technology
2. **Exogenous non-speech**: Environmental sound misperceived as speech
3. **Technological artifact**: Codec, PLC, CNG, or DSP-generated patterns
4. **Hybrid**: Combination of above
5. **Null**: No detectable external source at defined sensitivity

### 23.2.2 Layer 2: PERCEPCIÓN (Perception)

**Definition**: The neuroperceptual processes that detect, attend to, and preliminarily categorize the auditory signal.

**Observable Variables**:
| Variable | Measurement Method | Falsification Criterion |
|----------|-------------------|------------------------|
| Detection threshold | Audiometry, signal detection tasks | Normal threshold, no audibility |
| Attentional amplification | Eye-tracking, dual-task paradigms | No attention shift to stimulus |
| Pattern matching | Blind identification tasks | No consistent pattern extraction |
| Salience | Startle, GSR | No arousal response |
| State modulation | Sleep/stress/fatigue logs | No state correlation |

**Perceptual Vulnerability Factors**:
- Hearing loss (↑ top-down compensation)
- Fatigue (↓ bottom-up precision)
- Hypervigilance (↑ pattern-seeking)
- Prior exposure (↑ priming effects)
- Pharmacological state (variable effects)

### 23.2.3 Layer 3: INTERPRETACIÓN (Interpretation)

**Definition**: The cognitive-semantic processes that assign linguistic content, meaning, emotional valence, and agency/source attribution to the percept.

**Observable Variables**:
| Variable | Measurement Method | Falsification Criterion |
|----------|-------------------|------------------------|
| Linguistic content | Transcription, blind panels | No inter-observer agreement |
| Semantic coherence | Content analysis | Random/non-linguistic content |
| Emotional valence | Self-report, affect measures | Neutral valence |
| Agency attribution | Phenomenological interview | Self-generated attribution |
| Source belief | Conviction scales | Awareness of technological origin |

**Interpretation Drivers**:
- Linguistic priors (native language phonotactics)
- Self-referential content (own name, personal concerns)
- Threat detection system (fear-related content)
- Cultural/religious frameworks (spirits, demons, surveillance)
- Prior experience with similar phenomena

## 23.3 The FPI Operational Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FPI OPERATIONAL MATRIX                           │
├──────────┬───────────────┬───────────────┬──────────────────────────┤
│  LAYER   │  WHAT IT      │  WHAT IT      │  WHAT WOULD             │
│          │  OBSERVES     │  MEASURES     │  FALSIFY IT             │
├──────────┼───────────────┼───────────────┼──────────────────────────┤
│ SOURCE   │ External      │ Calibrated    │ No correlate at         │
│ (Fuente) │ trace         │ WAV,          │ defined sensitivity     │
│          │ (acoustic/    │ metadata,     │                         │
│          │ technical)    │ A/B conditions│                         │
├──────────┼───────────────┼───────────────┼──────────────────────────┤
│PERCEPTION│ Detection,    │ Blind tasks,  │ Effect independent of   │
│(Percep-  │ attention,    │ audiometry,   │ state or signal         │
│ ción)    │ salience      │ state logs    │ manipulation            │
├──────────┼───────────────┼───────────────┼──────────────────────────┤
│INTERPRET-│ Content,      │ Blind panels, │ High semantic consensus │
│ATION     │ attribution,  │ inter-rater   │ without acoustic        │
│(Interpr.)│ agency        │ reliability   │ structure, or vice versa│
├──────────┼───────────────┼───────────────┼──────────────────────────┤
│ DECISION │ A-D           │ Decision      │ Persistent contradictory│
│          │ classification│ matrix        │ results without         │
│          │ + E0-E4       │               │ explanation             │
└──────────┴───────────────┴───────────────┴──────────────────────────┘
```

## 23.4 The Key Principle: Double Dissociation

The FPI model rests on a critical insight: **physical signal structure and semantic interpretation can be dissociated**.

### 23.4.1 Dissociation Type A: Structure Without Meaning

A signal may have measurable acoustic structure (formant-like patterns, 4-8 Hz modulation) that multiple observers can agree exists, yet:
- No semantic content can be reliably extracted
- Different listeners "hear" completely different words
- Native speakers of different languages hear different phonemes

**Implication**: Acoustic structure is necessary but not sufficient for speech perception. The listener's priors complete the percept.

### 23.4.2 Dissociation Type B: Meaning Without Structure

A listener may consistently report specific semantic content (e.g., "I hear 'you're being watched'") yet:
- No acoustic structure is detectable at defined sensitivity
- Other listeners hear nothing or random content
- The signal is spectrally flat noise

**Implication**: Semantic content can be entirely generated by top-down processes without bottom-up support.

### 23.4.3 Clinical Application

This double dissociation is diagnostic:
- **High structure + high semantic agreement** → Likely exogenous speech (Scenario A)
- **High structure + low semantic agreement** → Likely SPIA (Scenario B)
- **Low structure + high semantic agreement** → Concerning for endogenous hallucination (Scenario C)
- **Variable/mixed** → Requires further analysis (Scenario D)

## 23.5 Mapping FPI to Clinical Questions

| Clinical Question | FPI Layer | Key Assessment |
|-------------------|-----------|----------------|
| "Is there a real sound?" | Source | Calibrated recording |
| "Can the patient hear it?" | Perception | Audiometry + signal detection |
| "What do they hear?" | Interpretation | Transcription + blind panel |
| "Why do they hear speech?" | Source + Perception | Artifact analysis + state factors |
| "Why that specific content?" | Interpretation | Prior analysis, threat content |
| "Is it harmful?" | All + Clinical | Distress, function, risk |

## 23.6 FPI in Forensic Audio Analysis

### 23.6.1 Source Layer Analysis

1. **Obtain calibrated recording** of the audio environment during reported experience
2. **Analyze spectral content** using STFT and modulation spectrum
3. **Identify potential artifact sources** (codec, environmental, device)
4. **Quantify SPIA potential** using metrics from Chapter 12

### 23.6.2 Perception Layer Analysis

1. **Assess listener vulnerability** using SPIA-SS (Chapter 16)
2. **Document state factors** at time of experience (fatigue, stress, substance)
3. **Conduct signal detection task** with original and processed audio

### 23.6.3 Interpretation Layer Analysis

1. **Blind panel transcription** of audio segments
2. **Calculate inter-rater reliability** (Cohen's κ or ICC)
3. **Content analysis** for self-referential or threat content
4. **Cultural context assessment** for alternative attribution frameworks

## 23.7 Preventing Inferential Errors with FPI

### 23.7.1 Error Type 1: Collapsing Layers

**Mistake**: Assuming that detectable signal structure implies specific semantic content
**Prevention**: Always independently assess interpretation layer with blind panels

### 23.7.2 Error Type 2: Skipping Source Assessment

**Mistake**: Proceeding directly to psychiatric diagnosis without environmental/technical assessment
**Prevention**: Protocol P0-P4 requires source layer assessment before interpretation

### 23.7.3 Error Type 3: Privileging Interpretation

**Mistake**: Accepting patient's reported content as evidence of corresponding signal
**Prevention**: Interpretation must be validated against source and perception evidence

### 23.7.4 Error Type 4: Confirmation Bias

**Mistake**: Seeking evidence for pre-determined conclusion (psychiatric or technological)
**Prevention**: Blind assessment, preregistered hypotheses, neutral reporting

## 23.8 FPI Integration with Evidence Levels (E0-E4)

The FPI model generates evidence that accumulates across levels:

| Level | Description | FPI Requirements |
|-------|-------------|------------------|
| E0 | No evidence | No source assessment performed |
| E1 | Anecdotal | Self-report only, no objective measurement |
| E2 | Correlational | Source or perception data without controlled comparison |
| E3 | Convergent | Multiple FPI layers show consistent pattern |
| E4 | Causal-verified | Experimental manipulation shows FPI-predicted effects |

**Principle**: Strong conclusions require evidence from multiple FPI layers at E3 or above.

## 23.9 Case Application: FPI Analysis of a SPIA Report

**Scenario**: Patient reports hearing "threat messages" during phone calls

### 23.9.1 Source Analysis
- Recording captured: VoIP with 3% packet loss
- Spectral analysis: High SPIA potential (PC1=0.78)
- Identified artifacts: PLC synthesis, CNG transitions

**Source Conclusion**: Technical substrate consistent with SPIA generation

### 23.9.2 Perception Analysis
- Audiometry: Mild high-frequency hearing loss
- State: Sleep-deprived (5h previous night), high anxiety
- Signal detection: Elevated false alarm rate

**Perception Conclusion**: Vulnerability factors present, consistent with enhanced pattern-matching

### 23.9.3 Interpretation Analysis
- Blind panel (n=5): 0/5 heard any speech content
- κ = 0 (no agreement)
- Content: Self-referential, threat-related
- Attribution: Initially attributed to surveillance; revised after psychoeducation

**Interpretation Conclusion**: No external semantic content; interpretation driven by top-down factors

### 23.9.4 Integrated FPI Diagnosis

- **Scenario**: B (acoustic/technological artifact + perceptual vulnerability)
- **Evidence Level**: E3 (convergent multi-layer)
- **Clinical Recommendation**: Tier 1-2 intervention (signal remediation + psychoeducation)

## 23.10 Conclusion: FPI as Diagnostic and Research Tool

The FPI model provides:
1. **Structured assessment** that prevents layer conflation
2. **Falsifiable predictions** at each layer
3. **Integration with evidence standards** (E0-E4)
4. **Clear clinical guidance** through scenario classification
5. **Research framework** for studying CCA mechanisms

By systematically separating source, perception, and interpretation, clinicians can avoid the twin errors of:
- Dismissing real technological factors as delusion
- Validating hallucinated content as evidence of external threat

The FPI model operationalizes the central thesis of this work: that cyber-acoustic convergence occurs at the intersection of signal, brain, and meaning.

---
**Status**: Draft - v1.0
**Word Count**: ~2,000 words
**Key References**: Predictive processing (Friston), Signal detection theory (Green & Swets)
