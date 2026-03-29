# Chapter 26: Physical Acoustics of the Environment

## 26.1 Introduction: Sound in the Real World

Before a signal reaches the ear, it travels through a complex acoustic environment that shapes, transforms, and potentially corrupts it. This chapter examines the physical acoustics of real-world environments—the spaces where SPIA experiences occur—and how they contribute to or mitigate the conditions for signal-induced pareidolia.

Understanding environmental acoustics is essential because:
1. Acoustic conditions determine what reaches the ear
2. Room characteristics can create speech-like modulation patterns
3. Mechanical sources generate structure that mimics prosody
4. The combination of environment and technology compounds effects

## 26.2 Mechanical and Electrical Sources

### 26.2.1 HVAC Systems

Heating, ventilation, and air conditioning (HVAC) systems are ubiquitous sources of acoustic energy with SPIA potential.

**Characteristics**:
| Parameter | Typical Range | SPIA Relevance |
|-----------|---------------|----------------|
| Frequency | 50-500 Hz fundamental | Overlaps speech F0 |
| Amplitude modulation | 0.5-10 Hz | Overlaps syllabic rate |
| Level | 30-60 dB SPL | Background masking |
| Temporal pattern | Periodic/quasi-periodic | Creates rhythm |

**SPIA Mechanism**: The modulation rate of HVAC systems (4-8 Hz from fan blade passage) coincidentally matches the syllabic rate of speech, creating amplitude envelopes that the perceptual system can interpret as prosodic contours.

### 26.2.2 Fans and Motors

Electric motors and fans produce tonal and modulated noise:
- **Blade passage frequency**: Number of blades × RPM/60
- **Cogging**: Electromagnetic irregularities create AM/FM
- **Bearing noise**: Adds high-frequency content

**Example**: A 5-blade fan at 1200 RPM produces 100 Hz blade passage, with AM at 5-10 Hz from slight imbalances—precisely in the speech modulation range.

### 26.2.3 Electrical Interference

Power lines, transformers, and electronics generate:
- 50/60 Hz hum and harmonics
- Switching noise from power supplies
- Radio frequency interference (RFI) demodulated by audio circuits

**Note**: While EMI/IMD is listed as "contextual" in this project, documented cases of demodulation exist.

### 26.2.4 Flow Noise

Moving air and water create broadband noise with spectral shaping:
- Turbulent flow in ducts
- Water in pipes
- Wind around structures

This noise provides the spectral substrate upon which modulation can create speech-like patterns.

## 26.3 Room Acoustics and Geometry

### 26.3.1 Room Modes and Resonances

Every enclosed space has resonant frequencies determined by dimensions:

**Axial mode formula**: f = c/(2L)

Where c = speed of sound (~343 m/s), L = room dimension

**Example**: A 4m room has fundamental at 43 Hz, with modes at 86, 129, 172 Hz—overlapping with speech harmonics.

**SPIA relevance**: Room modes amplify specific frequencies, creating spectral peaks that may enhance formant-like structures in noise.

### 26.3.2 Nodes and Antinodes

Standing waves create spatial variation in SPL:
- **Nodes**: Minimum amplitude (can't hear certain frequencies)
- **Antinodes**: Maximum amplitude (frequencies emphasized)

This creates "hot spots" where certain sounds are louder, potentially leading to:
- Location-dependent SPIA experiences
- Inconsistent reports ("I only hear it in this corner")
- Difficulty replicating experiences elsewhere

### 26.3.3 Reflection, Absorption, and Diffusion

**Reflection**:
- Hard surfaces reflect sound, creating echoes and reverberation
- Late reflections can be perceived as separate events
- Flutter echoes between parallel walls create metallic tones

**Absorption**:
- Soft materials absorb high frequencies preferentially
- Changes the timbre of sounds
- Creates "dead" zones with reduced SPIA potential

**Diffusion**:
- Irregular surfaces scatter sound
- Reduces focused reflections
- May reduce or increase SPIA depending on pattern

### 26.3.4 Diffraction and Sound Shadowing

Sound bends around obstacles:
- Low frequencies diffract easily (go around corners)
- High frequencies are blocked by small obstacles
- Creates frequency-dependent spatial patterns

**SPIA relevance**: A listener may hear only the low-frequency components of a sound (due to shadowing), losing the cues that would identify it as machinery rather than voice.

## 26.4 Non-Linear Phenomena

### 26.4.1 Stochastic Resonance

**Definition**: A phenomenon where adding noise to a weak signal can paradoxically improve detection.

**Mechanism**:
1. Signal is below detection threshold
2. Noise is added (e.g., background hum)
3. Signal + noise occasionally crosses threshold
4. Detection occurs at noise peaks coinciding with signal peaks

**Formula**: SNR_out = f(SNR_in, noise_level)

At optimal noise level, output SNR exceeds input SNR.

**SPIA relevance**: Moderate background noise may actually enhance detection of weak, speech-like patterns—not suppress them. This explains why SPIA may peak at intermediate noise levels (H3: SNR hypothesis).

### 26.4.2 Intermodulation and Beating

**Intermodulation Distortion (IMD)**:
When two frequencies (f1, f2) interact in a non-linear system:
- Sum: f1 + f2
- Difference: |f1 - f2|
- Harmonics: 2f1, 2f2, 3f1, etc.

**Beating**: Two close frequencies create amplitude modulation at their difference frequency: f_beat = |f1 - f2|

**Example**: Two fans at 97 Hz and 103 Hz create 6 Hz beating—in the speech prosody range.

**SPIA mechanism**: IMD and beating can create modulation patterns from sources that individually have no speech-like structure.

### 26.4.3 Acoustic Cavitation and Vortex Shedding

Advanced sources of quasi-periodic sound:
- **Cavitation**: Bubble collapse in liquids (plumbing)
- **Vortex shedding**: Periodic release of turbulent eddies

These create narrowband noise with modulation that can mimic voice.

## 26.5 Instrumentation and Calibration

### 26.5.1 Measurement Microphones

For valid acoustic assessment, calibrated equipment is required:

| Parameter | Requirement | Reason |
|-----------|-------------|--------|
| Frequency response | 20 Hz - 20 kHz ±2 dB | Full audible range |
| Self-noise | <20 dB(A) | Detect quiet signals |
| Dynamic range | >90 dB | Capture loud and quiet |
| Calibration | Traceable to standard | Valid measurements |

**Consumer microphones are insufficient** for SPIA assessment due to:
- Uncalibrated frequency response
- High self-noise
- AGC that distorts level information

### 26.5.2 Calibration Procedure

1. **SPL calibrator**: Known level (e.g., 94 dB SPL at 1 kHz)
2. **Apply to microphone**: Record calibration tone
3. **Calculate offset**: Difference from expected level
4. **Apply correction**: To all measurements

**Critical**: Without calibration, measurements are relative, not absolute.

### 26.5.3 Multichannel Recording

For SPIA assessment, multi-microphone setups provide:
- Spatial resolution of sources
- Correlation analysis (real source vs. artifact)
- Triangulation of origin

**Recommended setup**: Minimum 2 channels, ideally 4+ for room coverage.

## 26.6 Experimental Design in Environmental Acoustics

### 26.6.1 A/B Manipulation Designs

Controlled comparison of conditions:

| Condition A | Condition B | Comparison |
|-------------|-------------|------------|
| Fan ON | Fan OFF | Fan contribution |
| Window open | Window closed | External sources |
| Position 1 | Position 2 | Spatial variation |
| Day | Night | Temporal variation |

**Key principle**: Change one variable at a time while monitoring SPIA reports.

### 26.6.2 Negative Controls

Include conditions where SPIA should NOT occur:
- Anechoic chamber (no room effects)
- White noise (no modulation structure)
- Known non-speech (clearly mechanical)

If SPIA occurs in negative controls, reassess methodology.

### 26.6.3 Blinding Procedures

For valid assessment:
- **Assessor blind**: Evaluator doesn't know condition
- **Subject blind**: Participant doesn't know hypothesis
- **Double blind**: Neither knows condition

This prevents expectation effects from contaminating results.

## 26.7 Localization and Auditory Illusions

### 26.7.1 Ventriloquism Effect

Visual capture can shift perceived sound location:
- Sound "follows" moving visual object
- Can cause misattribution of source (e.g., attributing TV sound to phone)

**SPIA relevance**: When looking at a phone during SPIA experience, the voice may be attributed to the phone even if the acoustic source is elsewhere.

### 26.7.2 Precedence Effect

The first-arriving sound dominates localization:
- Reflections within ~40ms are integrated with direct sound
- Can create "phantom" sources at reflection points

### 26.7.3 Distance Perception Errors

Cues for distance perception:
- Level (louder = closer)
- Direct/reverberant ratio
- High-frequency content

In reverberant rooms, these cues become unreliable, potentially leading to misperception that a sound is "close" or "inside the head."

## 26.8 Integration with CCA Assessment

### 26.8.1 P2 Protocol: Environmental Audit

Following P0-P1, the P2 environmental audit includes:

1. **Room survey**: Dimensions, materials, sources
2. **Acoustic measurement**: Calibrated SPL at multiple positions
3. **Source identification**: All mechanical, electrical, and external sources
4. **Modulation analysis**: Temporal structure of noise sources
5. **SPIA potential scoring**: Based on spectral and temporal features

### 26.8.2 Environmental Modification

Based on assessment, potential interventions:

| Finding | Intervention | Expected Effect |
|---------|--------------|-----------------|
| High SPIA-potential source | Remove or shield | Reduce substrate |
| Room mode at speech frequency | Add absorption | Reduce resonance |
| Localized hot spot | Change listener position | Avoid antinodes |
| External source | Windows/barriers | Attenuate intrusion |

### 26.8.3 Documentation Standards

Environmental assessment should document:
- Measurement conditions (date, time, weather)
- Equipment used (with calibration date)
- Measurement positions (diagram)
- Background conditions (other occupants, activities)
- Any anomalies observed

## 26.9 Case Example: SPIA in an Office Environment

**Report**: Employee hears voices when alone in office during evening hours.

**Assessment**:
1. **Room survey**: 4m × 5m office, concrete walls, drop ceiling, HVAC vent
2. **SPL measurement**: 45 dB(A) background, 62 dB(A) peak during HVAC cycle
3. **Source ID**: HVAC system cycles every 15 min; fluorescent light ballast at 120 Hz
4. **Modulation analysis**: HVAC fan creates 6.3 Hz AM in 300-600 Hz band
5. **SPIA score**: High (PC1 = 0.72)

**Conclusion**: HVAC system creates acoustic conditions consistent with SPIA generation. Scenario B likely.

**Intervention**: Added absorption panels near HVAC vent; SPIA reports reduced by 80%.

## 26.10 Conclusion: The Acoustic Stage for SPIA

Environmental acoustics provides the physical substrate upon which SPIA occurs. Without understanding the acoustic environment, SPIA assessment is incomplete.

**Key principles**:
1. Measure before concluding—don't assume "silence"
2. Identify all sources of acoustic energy
3. Analyze modulation structure, not just SPL
4. Consider room effects and spatial variation
5. Document rigorously for reproducibility

The environment is not passive—it is an active participant in shaping what reaches the ear and what the brain perceives.

---
**Status**: Draft - v1.0
**Word Count**: ~2,100 words
**Integration**: Links to P2 Protocol (Ch 15), SPIA Metrics (Ch 12), FPI Model (Ch 23)
