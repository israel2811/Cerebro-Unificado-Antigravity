# Chapter 5: Laboratory Methods and Simulation

## Abstract
This chapter describes experimental methodologies for studying Cyber-Acoustic Convergence (CCA) and Synergistic Pareidolia In Algorithmic Systems (SPIA) under controlled laboratory conditions. We present protocols for generating calibrated stimuli, measuring perceptual responses, and quantifying individual differences in CCA susceptibility.

---

## 5.1 Introduction to Laboratory Investigation

While field forensic work (Chapter 4) addresses real-world CCA cases, laboratory study enables controlled manipulation of variables. Key advantages include:
- **Stimulus control**: Precise specification of signal characteristics
- **Response quantification**: Standardized measurement protocols
- **Mechanistic investigation**: Isolation of specific factors
- **Individual differences**: Characterization of susceptibility

### 5.1.1 Research Questions

Laboratory methods address:
1. What signal characteristics maximize SPIA (false speech detection)?
2. What individual factors predict CCA susceptibility?
3. Can training reduce spurious pattern detection?
4. What neural mechanisms underlie CCA?

---

## 5.2 Stimulus Generation

### 5.2.1 Noise Synthesis

**Gaussian White Noise**: 
- Equal power across all frequencies
- Maximum entropy (no structure)
- Baseline for SPIA testing

**Colored Noise**:
- Pink noise (1/f): Natural acoustic environment
- Brown noise (1/f²): Low-frequency emphasis
- Blue noise: High-frequency emphasis

**Synthetic Algorithm**:
```python
import numpy as np
from scipy import signal

def generate_colored_noise(samples, fs, color='pink'):
    white = np.random.randn(samples)
    if color == 'white':
        return white
    elif color == 'pink':
        # 1/f spectrum
        freqs = np.fft.rfftfreq(samples, 1/fs)
        freqs[0] = 1  # Avoid division by zero
        spectrum = np.fft.rfft(white) / np.sqrt(freqs)
        return np.fft.irfft(spectrum, samples)
    elif color == 'brown':
        # 1/f² spectrum
        freqs = np.fft.rfftfreq(samples, 1/fs)
        freqs[0] = 1
        spectrum = np.fft.rfft(white) / freqs
        return np.fft.irfft(spectrum, samples)
```

### 5.2.2 Speech-Like Stimuli

To study the perception threshold where noise becomes "speech":

**Vocoded Speech**: Real speech processed through noise vocoder, degrading intelligibility in controlled steps.

**Speech-Modulated Noise**: Noise amplitude-modulated with speech envelope but no spectral detail.

**Babble Noise**: Multiple overlapping speech signals creating semantic unintelligibility while preserving prosodic cues.

**Reverse Speech**: Temporal reversal disrupts phonetic content while preserving spectral characteristics.

### 5.2.3 Signal Parameter Space

Key variables for systematic investigation:

| Parameter | Range | Relevance |
|-----------|-------|-----------|
| Bandwidth | 100 Hz - 20 kHz | Frequency content |
| Modulation rate | 0.5 - 10 Hz | Speech-like temporal patterns |
| SNR | -20 to +10 dB | Signal in noise |
| Duration | 100 ms - 10 s | Temporal integration |
| Presentation level | 30 - 70 dB SPL | Loudness effects |

---

## 5.3 Perceptual Testing Paradigms

### 5.3.1 Signal Detection Theory Framework

Classical SDT provides the framework for measuring perceptual sensitivity:

**Hit**: Correctly detecting speech when present
**Miss**: Failing to detect speech when present
**False Alarm**: Detecting speech when absent (SPIA)
**Correct Rejection**: Correctly identifying noise-only

**Measures**:
- d' (d-prime): Sensitivity, ability to discriminate
- c (criterion): Response bias toward "yes" or "no"

### 5.3.2 The SPIA Detection Task

**Protocol**:
1. Present brief stimulus (1-3 seconds)
2. Subject indicates: "Speech present" or "Noise only"
3. Vary proportion of speech-containing trials
4. Calculate false alarm rate for SPIA quantification

**Critical manipulation**: In some sessions, include no speech trials. Persistent "speech detected" responses indicate SPIA.

### 5.3.3 Phenomenological Assessment

Beyond binary detection, assess qualitative aspects:

- **Intelligibility rating**: "How clearly could you understand words?" (0-100)
- **Confidence rating**: "How sure are you?" (0-100)
- **Content transcription**: "Write what you heard"
- **Source attribution**: "Where did the voice come from?"

### 5.3.4 Continuous Monitoring

**Dial task**: Subject continuously adjusts dial to indicate current perception (noise ↔ speech).

**Think-aloud**: Verbal description of experience during extended listening.

**Retrospective timeline**: After session, mark timeline when voices were perceived.

---

## 5.4 Physiological Measures

### 5.4.1 Electroencephalography (EEG)

EEG provides temporal resolution for tracking rapid perceptual processes:

**N1/P2 Complex**: Auditory evoked potentials indicating early processing.

**N400**: Associated with semantic processing; may activate during SPIA episodes.

**MMN (Mismatch Negativity)**: Pre-attentive change detection; tests predictive processing.

**Protocol**:
- 64-channel EEG during SPIA detection task
- Time-lock to stimulus onset and response
- Compare ERP waveforms for hits, misses, false alarms, correct rejections

### 5.4.2 Functional MRI

fMRI provides spatial resolution for network identification:

**Regions of Interest**:
- Primary auditory cortex (Heschl's gyrus)
- Secondary auditory cortex (superior temporal gyrus)
- Speech perception network (left lateralized)
- Frontal executive regions

**Design**:
- Event-related fMRI during SPIA task
- Compare BOLD response for speech vs. noise vs. SPIA (false alarm)
- Connectivity analysis for network dynamics

### 5.4.3 Autonomic Measures

Physiological arousal may predict or accompany SPIA:

- **Skin conductance**: Emotional/attentional arousal
- **Heart rate variability**: Autonomic state
- **Pupillometry**: Cognitive load and surprise

---

## 5.5 Individual Difference Measures

### 5.5.1 Audiometric Assessment

Rule out peripheral hearing factors:

- Pure tone audiometry (250 Hz - 8 kHz)
- Extended high-frequency audiometry (8 - 16 kHz)
- Speech-in-noise testing (HINT, QuickSIN)
- Tinnitus assessment (if present)

### 5.5.2 Cognitive Assessment

Factors that may influence SPIA:

**Working Memory**: Higher capacity may enable more complex pattern detection.

**Inhibitory Control**: Deficits may promote false pattern acceptance.

**Top-Down Expectations**: Prior beliefs about signal presence.

**Attentional Control**: Focused vs. diffuse listening.

Recommended battery: WAIS-IV subtests, Trail Making, Stroop.

### 5.5.3 Psychopathology Screening

Exclude or stratify by clinical factors:

- SCID for psychiatric diagnosis
- PDI (Peters Delusion Inventory) for subclinical experiences
- LSHS (Launay-Slade Hallucination Scale)
- AUDIT/DAST for substance use

### 5.5.4 Electromagnetic Sensitivity Beliefs

Paranormal Belief Scale (PBS) or custom scale assessing:
- Beliefs about RF/EMF health effects
- History of "electronic harassment" concerns
- Pre-existing explanatory frameworks

---

## 5.6 Experimental Designs

### 5.6.1 Basic SPIA Susceptibility Study

**Design**: Within-subjects, single session
**N**: 50-100 participants
**Stimuli**: 200 trials (50% noise, 50% vocoded speech at threshold)
**Outcome**: d', false alarm rate, response time

### 5.6.2 Manipulating Expectations

**Design**: Between-subjects
**Groups**: 
- Informed ("some trials contain hidden speech")
- Neutral ("listen to sounds")
- Skeptical ("all trials are pure noise")

**Outcome**: Compare false alarm rates across expectation conditions

### 5.6.3 Chronic Exposure Study

**Design**: Longitudinal, within-subjects
**Protocol**: Daily 30-minute exposure to speech-modulated noise for 4 weeks
**Measures**: Weekly SPIA testing, questionnaires
**Outcome**: Does chronic exposure increase SPIA?

### 5.6.4 Clinical Population Study

**Design**: Case-control
**Groups**:
- Patients with auditory verbal hallucinations (n=30)
- Patients with visual hallucinations only (n=30)
- Healthy controls (n=30)

**Outcome**: Compare SPIA susceptibility across groups

---

## 5.7 Data Analysis

### 5.7.1 Behavioral Analysis

- Signal detection metrics (d', c)
- Response time distributions
- Sequential effects (recent history influences)
- Psychometric functions (threshold estimation)

### 5.7.2 Neural Analysis

**EEG**:
- ERP averaging and comparison
- Time-frequency analysis (oscillatory power)
- Source localization (LORETA, beamforming)

**fMRI**:
- GLM activation analysis
- Multivariate pattern analysis (MVPA)
- Connectivity (PPI, DCM)

### 5.7.3 Predictive Modeling

- Logistic regression predicting SPIA from individual differences
- Machine learning classification of high vs. low SPIA susceptibility
- Factor analysis of susceptibility components

---

## 5.8 Ethical Considerations

### 5.8.1 Participant Safety

- Limit exposure duration to prevent auditory fatigue
- Screen for tinnitus/hyperacusis
- Avoid distressing content
- Provide debriefing about SPIA (normalize experience)

### 5.8.2 Vulnerable Populations

Extra care with participants experiencing:
- Active hallucinations
- Anxiety about technology
- History of trauma related to auditory experiences

### 5.8.3 De-identification

- Remove identifiers from recordings
- Aggregate data reporting
- Secure storage of sensitive measures

---

## 5.9 Summary

This chapter presented laboratory methods for systematic investigation of CCA and SPIA:

1. **Stimulus generation**: Controlled noise and speech-like signals
2. **Perceptual testing**: SDT-based detection paradigms
3. **Physiological measures**: EEG, fMRI, autonomic
4. **Individual differences**: Cognitive, audiometric, clinical
5. **Experimental designs**: Cross-sectional and longitudinal

Chapter 6 will apply these methods to analyze Algorithmic Pareidolia in High-Latency Systems—the specific conditions of modern digital audio.

---

*Word count: ~1,400 words*
*Status: Complete*
*Last updated: 2026-02-03*
