# Chapter 21: Psychoacoustics of Speech in Noise and Perceptual Pattern Detection

## 21.1 Introduction: The Bridge Between Signal and Perception

The phenomenon of Signal-Induced Algorithmic Pareidolia (SPIA) cannot be fully understood without a deep dive into psychoacoustics—the scientific study of how humans perceive sound. This chapter examines the specific perceptual mechanisms that allow (and sometimes compel) the auditory system to extract speech-like patterns from non-speech signals. Understanding these mechanisms is essential for both explaining SPIA and designing interventions to mitigate it.

## 21.2 Auditory Thresholds and Signal Detection

### 21.2.1 Absolute Threshold vs. Functional Threshold

The **absolute threshold of hearing** (ATH) defines the minimum sound pressure level (SPL) detectable in laboratory silence (~0-20 dB SPL at 1 kHz for young adults). However, real-world hearing operates under vastly different conditions.

**Functional Threshold**: In everyday environments, the effective threshold is determined by:
- Ambient noise level (masking)
- Attention/expectation
- Frequency content of target vs. masker
- Listener's hearing sensitivity

**Implication for SPIA**: When audio signals operate near the functional threshold (as occurs with heavily compressed, low-bitrate audio), the auditory system enters a "guessing" mode where top-down predictions strongly influence perception.

### 21.2.2 Signal-to-Noise Ratio (SNR) and Intelligibility

Speech intelligibility follows a sigmoid curve relative to SNR:

| SNR (dB) | Intelligibility | SPIA Risk |
|----------|-----------------|-----------|
| > +10 | >95% | LOW (clear signal dominates) |
| 0 to +10 | 70-95% | MODERATE |
| -5 to 0 | 30-70% | HIGH (ambiguity zone) |
| < -5 | <30% | VERY HIGH (pattern-searching activated) |

**The "Negative SNR" Danger Zone**: When SNR drops below 0 dB (noise louder than signal), the listener cannot rely on bottom-up information alone. The brain compensates by:
1. Increasing reliance on linguistic predictions (top-down processing)
2. Filling in missing phonemes (phonemic restoration)
3. Biasing toward expected or feared content

### 21.2.3 The Role of Attention and Expectation

Attention modulates auditory thresholds by 6-10 dB in experimental settings. A listener who *expects* to hear speech will:
- Lower their effective threshold for speech-like sounds
- Increase pattern-matching sensitivity
- Increase false alarm rate (detecting speech that isn't there)

**Clinical Relevance**: Patients who have experienced SPIA previously may develop anticipatory hypervigilance, increasing their susceptibility in future exposures.

## 21.3 Masking and Release from Masking

### 21.3.1 Simultaneous Masking

When noise and target signal occur simultaneously, the noise *masks* the signal. Masking is strongest when:
- Masker and target share frequency content
- Masker is louder than target
- Masker is continuous (no temporal gaps)

**Codec Artifact Implication**: Audio compression algorithms often create masking noise that partially overlaps with the speech frequency range (300-3400 Hz), creating exactly the conditions for ambiguous perception.

### 21.3.2 Temporal Masking

**Forward Masking**: A loud sound can mask a softer sound occurring up to 200ms later.
**Backward Masking**: To a lesser degree, a loud sound can affect perception of sounds up to 50ms earlier.

**Packet Loss Implication**: When Voice over IP (VoIP) systems experience packet loss, the resulting temporal gaps and their compensation (Packet Loss Concealment) create complex temporal masking patterns that can:
- Fragment speech perception
- Create illusory phonemic boundaries
- Trigger perceptual "filling in"

### 21.3.3 Release from Masking: "Glimpses"

Speech perception in noise does not require continuous audibility. Listeners can achieve high intelligibility from brief "glimpses"—temporal or spectral windows where the signal momentarily exceeds the masker.

**Glimpsing Model of SPIA**:
1. Degraded audio provides random "glimpses" of acoustic energy
2. The brain attempts to link these glimpses into coherent speech
3. In the absence of actual speech, the brain constructs illusory patterns
4. Result: Perception of words or phrases that "fit" the glimpse pattern

### 21.3.4 Comodulation Masking Release (CMR)

When masker fluctuations are correlated across frequency channels, the auditory system achieves better signal extraction. VoIP comfort noise generators typically produce *uncorrelated* noise, paradoxically impairing the release-from-masking mechanisms that evolved for natural acoustic environments.

## 21.4 Modulation and Phonetic Structure

### 21.4.1 The Modulation Spectrum of Speech

Human speech has a characteristic amplitude modulation (AM) pattern:
- **4-8 Hz**: Syllable rate (most critical for intelligibility)
- **15-30 Hz**: Phoneme rate
- **>50 Hz**: Pitch and harmonic structure

**Critical Observation**: Many audio artifacts (codec jitter, buffer underruns, AGC pumping) produce modulations in the 2-10 Hz range—exactly overlapping with the syllable rate the brain uses to segment speech.

### 21.4.2 Frequency Modulation (FM) and Formant Transitions

Formants—the resonance frequencies of the vocal tract—define vowel identity. Formant *transitions* (the movement from one formant pattern to another) distinguish consonants.

**Codec Artifact FM Patterns**: Audio compression algorithms, particularly those using linear predictive coding (LPC), can create artificial formant-like patterns in noise. These "pseudo-formants" may trigger phoneme recognition in the absence of actual speech.

### 21.4.3 Envelope vs. Fine Structure

| Component | Information Carried | SPIA Trigger Risk |
|-----------|--------------------|--------------------|
| Envelope (AM) | Rhythm, syllable structure | HIGH (easily mimicked by artifacts) |
| Fine Structure (FM) | Pitch, tone, phoneme identity | MODERATE |

Research shows that speech intelligibility depends primarily on envelope information, particularly in noise. Unfortunately, this is precisely what codec artifacts most readily simulate.

## 21.5 Phonemic Restoration and Perceptual Filling-In

### 21.5.1 The Classic Phonemic Restoration Effect

Warren's (1970) classic experiments demonstrated that when a phoneme is replaced by noise, listeners:
1. Do not notice the replacement
2. "Hear" the missing phoneme
3. Cannot identify which segment was replaced

**The brain fills in what was never present, based on linguistic expectation.**

### 21.5.2 Conditions Favoring Phonemic Restoration

| Factor | Effect on Restoration |
|--------|----------------------|
| High linguistic predictability | ↑ Stronger restoration |
| Self-referential content (e.g., own name) | ↑ Much stronger |
| Noise similar in amplitude to speech | ↑ Stronger |
| Prior speech context | ↑ Stronger |
| Attention/expectation | ↑ Stronger |
| Native language phonotactics | ↑ Biased toward native phonemes |

### 21.5.3 Phonemic Restoration as SPIA Engine

In SPIA, we hypothesize a "runaway" phonemic restoration process:

1. Codec artifacts create acoustically ambiguous noise
2. Listener's brain segments the noise using 4-8 Hz AM cues
3. For each "segment," the brain generates candidate phonemes
4. Phonemic restoration fills gaps between segments
5. Result: Perception of coherent (but hallucinatory) speech

**Key Insight**: The brain cannot distinguish between filling in a briefly masked phoneme and constructing a phoneme from pure noise—both use the same neural machinery.

## 21.6 Auditory Scene Analysis (ASA)

### 21.6.1 Streaming and Segregation

The auditory system must solve the "cocktail party problem"—separating multiple sound sources in a complex acoustic mixture. ASA principles include:

| Principle | Mechanism | SPIA Relevance |
|-----------|-----------|----------------|
| Common onset | Sounds starting together group together | Codec packet boundaries create artificial grouping |
| Harmonicity | Sounds with related harmonics group together | LPC artifacts may create spurious harmonic patterns |
| Continuity | Continuous sounds persist perceptually | Comfort noise creates illusion of continuous source |
| Common AM | Sounds with correlated modulation group together | VAD transitions create correlated modulation |

### 21.6.2 Auditory Ventriloquism

When visual and auditory information conflict about sound source location, the visual modality typically dominates ("ventriloquism effect"). In the absence of visual anchoring (e.g., phone calls), auditory localization becomes more labile.

**SPIA Localization**: Patients often report SPIA voices as having ambiguous or shifting spatial locations—consistent with ASA struggling without visual confirmation.

### 21.6.3 Perceptual Continuity Illusion

When a sound is briefly masked, listeners perceive the sound as continuing through the mask (rather than stopping and restarting). This continuity illusion:
- Is stronger for ongoing sounds than transients
- Is modulated by expectation
- Can create illusory sustained speech from intermittent glimpses

## 21.7 Prosody, Rhythm, and Speech Segmentation

### 21.7.1 Prosodic Cues in Speech

Prosody—the rhythm, stress, and intonation of speech—is carried by:
- Fundamental frequency (F0) contour
- Amplitude contour
- Duration patterns

**Prosodic Mimicry by Artifacts**: Many codec artifacts produce quasi-periodic amplitude and frequency fluctuations that can mimic prosodic contours. The brain may interpret these as emotional tone or sentence structure, even in the absence of lexical content.

### 21.7.2 Metrical Segmentation

Listeners segment speech based on rhythmic cues—stressed syllables in English, syllable boundaries in French. The brain applies these segmentation strategies automatically to any quasi-periodic sound stream.

**Implication**: When codec artifacts produce rhythmic patterns, they are automatically parsed using language-specific segmentation rules, increasing the likelihood of perceiving language-like structure.

### 21.7.3 The "Speech Envelope Following Response"

Neural tracking of the speech envelope (measurable via EEG) demonstrates that the brain phase-locks to 4-8 Hz modulations. This same neural mechanism will track any 4-8 Hz modulation—including codec artifacts—setting up the perceptual interpretation of non-speech as speech.

## 21.8 Musical Perception as Comparative Framework

### 21.8.1 Why Music Matters for SPIA

Musical perception shares many mechanisms with speech perception:
- Rhythm and meter (cf. prosody)
- Pitch patterns (cf. intonation)
- Expectation and surprise
- Parsing of continuous input into discrete units

**Musical Ear Syndrome** (MES)—hearing music in silence—serves as a clinical analogy to SPIA, demonstrating that the brain can generate complex auditory percepts from minimal or absent input.

### 21.8.2 Harmonicity and Speech-Like Timbre

Speech fundamentally differs from most environmental sounds in its harmonic structure. The vocal tract produces sounds with:
- Strong harmonic series
- Formant resonances
- Regular F0

When artifacts create periodic or quasi-harmonic patterns, they acquire a "voice-like" timbre even without speech content.

## 21.9 Implications for SPIA Understanding and Intervention

### 21.9.1 Psychoacoustic Risk Profile

Based on this chapter, individuals at highest SPIA risk exhibit:
- High pattern-seeking tendency (translates to aggressive phonemic restoration)
- Expectation of hearing specific content (self-name, threat-related)
- Exposure to audio with SNR near 0 dB
- Exposure to audio with 4-8 Hz modulations
- Limited visual anchoring (phone calls, headphone use)

### 21.9.2 Psychoacoustically-Informed Interventions

| Principle | Intervention |
|-----------|--------------|
| Increase SNR | Higher bitrate codecs |
| Reduce predictive weight | Psychoeducation about SPIA mechanism |
| Disrupt 4-8 Hz mimicry | Anti-Pareidolia Filter (Chapter 14) |
| Provide alternative ASA streams | Background music during calls |
| Reduce expectation | Mindfulness-based attention training |

### 21.9.3 Toward a Quantitative SPIA Risk Calculator

Future work should develop a calculator incorporating:
- Codec specifications (bitrate, PLC algorithm)
- Transmission quality metrics (packet loss, jitter)
- Ambient noise level
- Individual SPIA susceptibility (SPIA-SS score)
- Contextual risk factors (fatigue, stress)

This would enable prediction and prevention of SPIA before it occurs.

## 21.10 Conclusion: The Auditory System Is Not a Tape Recorder

The psychoacoustic evidence is clear: human auditory perception is not passive recording—it is *active construction*. The brain:
- Fills in missing information
- Imposes linguistic structure on noise
- Cannot distinguish internally generated from externally generated speech patterns

SPIA is not a failure of this system—it is the system working exactly as designed, but in an acoustic environment (degraded digital audio) that our evolution never anticipated.

---
**Status**: Draft - v1.0
**Word Count**: ~2,200 words
**References**: Warren (1970), Bregman (1990), Mattys et al. (2012), Cooke & Meyer (2015)
**Next Steps**: Add quantitative models and spectrograms; develop SPIA risk calculator.
