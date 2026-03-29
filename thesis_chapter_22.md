# Chapter 22: Real-Time Communications (RTC) and Voice DSP: The Technological Substrate of SPIA

## 22.1 Introduction: Inside the Voice Pipeline

When a human speaks into a smartphone, their voice undergoes a complex transformation before reaching the listener's ear. This chapter examines the complete Real-Time Communications (RTC) pipeline—from microphone input to speaker output—with specific attention to the processing stages that generate the artifacts capable of triggering Signal-Induced Algorithmic Pareidolia (SPIA). Understanding this pipeline is essential for both forensic audio analysis and the design of SPIA-mitigation technologies.

## 22.2 The Modern Voice Communication Pipeline

### 22.2.1 End-to-End Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VOICE COMMUNICATION PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SENDER SIDE                    NETWORK                 RECEIVER SIDE   │
│  ┌───────────┐                                         ┌───────────┐   │
│  │ Microphone│                                         │  Speaker  │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐                                         ┌───────────┐   │
│  │    ADC    │                                         │    DAC    │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐                                         ┌───────────┐   │
│  │   AEC     │  (Echo Cancellation)                    │   AGC     │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐                                         ┌───────────┐   │
│  │    NS     │  (Noise Suppression)                    │    NS     │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐                                         ┌───────────┐   │
│  │   AGC     │  (Automatic Gain Control)               │   AEC     │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐                                         ┌───────────┐   │
│  │   VAD     │  (Voice Activity Detection)             │    PLC    │   │
│  └─────┬─────┘                                         └─────▲─────┘   │
│        ▼                                                     │         │
│  ┌───────────┐     ┌───────────────┐     ┌───────┐    ┌───────────┐   │
│  │  Encoder  │────▶│  NETWORK      │────▶│Jitter │───▶│  Decoder  │   │
│  │ (Codec)   │     │ (IP, 3G/4G/5G)│     │Buffer │    │  (Codec)  │   │
│  └───────────┘     └───────────────┘     └───────┘    └───────────┘   │
│                                                                         │
│  ★ Each stage can generate SPIA-triggering artifacts ★                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 22.2.2 Protocol Variants

| Protocol | Use Case | Typical Codecs | SPIA Risk Notes |
|----------|----------|----------------|-----------------|
| PSTN (analog) | Traditional landlines | PCM 64 kbps | Low risk (uncompressed) |
| GSM/2G | Mobile voice | HR/FR/EFR 6-13 kbps | HIGH risk (aggressive compression) |
| 3G (AMR) | Mobile voice | AMR 4.75-12.2 kbps | HIGH risk (adaptive, can hit very low bitrates) |
| VoLTE/4G | HD Voice | EVS / AMR-WB 6.6-23.85 kbps | Moderate risk (wideband usually cleaner) |
| VoNR/5G | HD+ Voice | EVS 5.9-128 kbps | Low-moderate (depends on network conditions) |
| VoIP (WebRTC) | Internet calling | Opus 6-510 kbps | Variable (depends on network) |
| Zoom/Teams | Conference | Opus + proprietary | Variable (can degrade under load) |

## 22.3 Voice Codecs and Compression Artifacts

### 22.3.1 Codec Classification

**Waveform Codecs**: Attempt to reproduce the original waveform (e.g., G.711 PCM)
- High bitrate (64+ kbps)
- Low artifact risk
- Rarely used in modern mobile

**Parametric Codecs**: Model the vocal tract and transmit parameters (e.g., GSM-FR, AMR)
- Low bitrate (4-13 kbps)
- HIGH artifact risk
- Dominant in mobile telephony

**Hybrid Codecs**: Combine waveform and parametric approaches (e.g., Opus, EVS)
- Variable bitrate
- Variable artifact risk
- Modern standard

### 22.3.2 How Compression Creates Artifacts

| Compression Stage | Artifact Type | SPIA Trigger Risk |
|-------------------|---------------|-------------------|
| Downsampling | Loss of high frequencies | LOW (removes harmonics, makes audio "dull") |
| LPC Analysis | Spectral smoothing | MEDIUM (can create formant-like peaks in noise) |
| Quantization | Step distortion, "roughness" | MEDIUM (adds texture to silence) |
| Vector Quantization | Codebook mismatch | HIGH (can create periodic patterns) |
| Bandwidth Extension | Synthetic high frequencies | HIGH (hallucinates content) |

### 22.3.3 Narrowband vs. Wideband vs. Super-Wideband

| Bandwidth | Frequency Range | Purpose | SPIA Notes |
|-----------|-----------------|---------|------------|
| Narrowband | 300-3400 Hz | Legacy telephony | HIGHEST RISK (exactly speech formant range) |
| Wideband | 50-7000 Hz | HD Voice | Lower risk (more context) |
| Super-Wideband | 50-14000 Hz | EVS/Opus Hi-Fi | Lowest risk (full spectrum) |

**Critical Insight**: The narrowband telephone band (300-3400 Hz) was designed to capture *only* the frequencies necessary for speech intelligibility. When codec artifacts occur in this band, they are maximally confusable with speech because they occupy exactly the same spectral region.

### 22.3.4 The "Codec Starvation" Phenomenon

Under poor network conditions, adaptive codecs may:
1. Drop to minimum bitrate (4.75 kbps for AMR)
2. Increase compression ratio dramatically
3. Lose ability to represent non-speech accurately
4. Attempt to model environmental noise as if it were speech
5. Produce "texturized" silence that mimics phonetic structure

## 22.4 Voice Activity Detection (VAD) and Discontinuous Transmission (DTX)

### 22.4.1 Why VAD Matters

VAD algorithms detect whether the current frame contains speech or silence. During detected silence:
- No speech frames are transmitted (DTX - Discontinuous Transmission)
- Network bandwidth is saved
- Receiver generates **Comfort Noise** to fill the gap

**The VAD Binary**: At every 10-20ms frame, VAD makes a binary decision:
- Speech = Transmit
- Silence = Switch to Comfort Noise

### 22.4.2 Comfort Noise Generation (CNG)

Instead of transmitting silence (which sounds unnatural), receivers generate synthetic "comfort noise" matching the estimated background noise level.

**CNG Artifacts**:
- Sudden onset/offset when VAD switches states
- Spectral discontinuities between speech and comfort noise
- Slightly different spectral shape than original background
- Periodic "updates" when sender transmits SID (Silence Insertion Descriptor) frames

### 22.4.3 VAD Errors and SPIA

| VAD Error Type | Occurrence | SPIA Effect |
|----------------|------------|-------------|
| Hang-over (speech → silence) | End of utterance | Abrupt transition, perceptual discontinuity |
| Clip (start of speech) | Low-energy speech beginnings | Missed phonemes, triggering restoration |
| Music detection failure | Background music | Chopped, rhythmic artifacts |
| Noise detection failure | Loud environments | Comfort noise mismatched to actual noise |

### 22.4.4 The "DTX Silence" Is Not Silent

A common misconception is that muting or DTX creates true silence. In reality:

| "Silence" Source | What Listener Actually Receives |
|------------------|--------------------------------|
| Sender mutes | Comfort noise pattern from last SID |
| VAD detects silence | CNG generated by receiver |
| Packet loss during silence | Interpolated comfort noise |
| True zero signal | Codec minimum noise floor |

**Implication**: There is no true silence in modern voice calls. The listener always receives *something*, and that something can trigger SPIA.

## 22.5 Packet Loss Concealment (PLC)

### 22.5.1 Why Packets Get Lost

In IP-based voice transmission, packets may be:
- Lost in transit (router overload, congestion)
- Arrive too late (exceeding jitter buffer timeout)
- Discarded due to corruption

Typical packet loss rates:
- Ideal network: <0.1%
- Acceptable: 1-2%
- Degraded: 3-5%
- Severely degraded: >5%

### 22.5.2 PLC Strategies

| Strategy | Description | SPIA Risk |
|----------|-------------|-----------|
| Silence substitution | Replace lost packet with silence | LOW (obvious gap) |
| Repeat last packet | Replay previous frame | MEDIUM (creates echo-like effect) |
| Interpolation | Predict missing frame from neighbors | HIGH (generates synthetic content) |
| Waveform extrapolation | Extend previous pitch cycles | HIGH (creates pseudo-speech) |
| Model-based | Use LPC parameters to synthesize | VERY HIGH (hallucinates plausible audio) |

### 22.5.3 The SPIA Risk of Advanced PLC

Modern PLC algorithms are designed to be *perceptually invisible*—they synthesize audio that sounds like the original. This is precisely the problem for SPIA:

1. Lost packet during speech → PLC generates plausible phoneme
2. Lost packet during silence → PLC generates "consistent" background
3. Multiple consecutive losses → PLC struggles, generates increasingly synthetic content
4. Result: Audio that contains synthesized elements indistinguishable from real audio

**Forensic Challenge**: PLC-generated content cannot be easily distinguished from transmitted content without access to network-level logs.

## 22.6 Noise Suppression (NS) and Acoustic Echo Cancellation (AEC)

### 22.6.1 Noise Suppression Artifacts

NS algorithms estimate and remove environmental noise. Artifacts include:

| Artifact | Cause | SPIA Trigger |
|----------|-------|--------------|
| Musical noise ("twinkling") | Over-aggressive spectral subtraction | MODERATE (rhythmic pattern) |
| Breathing modulation | NS reacting to breath sounds | MODERATE (creates AM pattern) |
| Robotic voice | Over-processing of vocal harmonics | HIGH (uncanny valley effect) |
| Noise pumping | Gain variation with speech presence | HIGH (4-8 Hz AM pattern) |

### 22.6.2 Echo Cancellation Artifacts

AEC removes acoustic echoes from speaker-to-microphone paths. When misconfigured:

| Artifact | Cause | SPIA Trigger |
|----------|-------|--------------|
| Residual echo | Incomplete cancellation | MODERATE (doubled voice perception) |
| Echo return | Filter divergence | HIGH (hearing "response" to one's own voice) |
| Cross-talk | Multi-party leakage | HIGH (unexpected voice fragments) |

### 22.6.3 The "Processed Silence" Problem

When all DSP algorithms are applied to silence:
1. NS estimates noise floor
2. AEC monitors for echo
3. AGC adjusts gain
4. Result: A highly processed "nothing" that contains:
   - Filter residuals
   - Gain variations
   - Spectral shaping
   - Temporal structure

This "processed silence" is not silence—it is a complex synthetic signal that can contain speech-like patterns.

## 22.7 Automatic Gain Control (AGC) and Its Psychoacoustic Effects

### 22.7.1 AGC Function

AGC automatically adjusts audio volume to maintain consistent perceived loudness despite:
- Speaker moving closer/farther from mic
- Speaking loudness variations
- Environmental noise changes

### 22.7.2 AGC Artifacts

| Artifact | Mechanism | SPIA Effect |
|----------|-----------|-------------|
| Pumping | Level changes visible in waveform envelope | Creates 1-5 Hz AM pattern (syllable-rate mimicry) |
| Noise floor lift | Gain increased during silence | Background noise becomes more audible |
| Attack/release audibility | Fast gain changes are perceptible | Creates rhythmic "breathing" pattern |
| Non-stationarity | Background noise level varies with speech | Listener perceives "something" in the noise |

### 22.7.3 AGC as SPIA Amplifier

AGC can amplify SPIA risk:
1. During speech pauses, AGC increases gain
2. Low-level artifacts become more audible
3. Background noise enters the "perceptual foreground"
4. Listener's attention is drawn to previously inaudible details
5. Pattern-matching engages on amplified noise

## 22.8 AI-Based Audio Enhancement and Its Paradoxes

### 22.8.1 Neural Network Enhancement

Modern systems increasingly use deep learning for:
- Super-resolution (bandwidth extension)
- Noise removal
- Speech enhancement
- Voice separation

### 22.8.2 The "Hallucination" Risk

Neural networks can generate plausible audio that was never present:

| Enhancement | Benefit | SPIA Risk |
|-------------|---------|-----------|
| Bandwidth extension | Fuller sound | Synthesizes high frequencies that may contain speech-like content |
| Noise removal | Clearer voice | May partially reconstruct speech from noise patterns |
| Voice separation | Focus on target speaker | May generate speech-like residuals from non-voice |

**Ironic Paradox**: AI designed to make audio "clearer" may inadvertently increase SPIA risk by adding synthesized content.

### 22.8.3 ASR "Hallucinations" as Analogous Phenomenon

Automatic Speech Recognition (ASR) systems can generate phantom transcripts from non-speech audio. This is the text-domain analog of SPIA and demonstrates that even sophisticated AI systems "hear" speech in noise.

## 22.9 Platform-Specific Considerations

### 22.9.1 Mobile Phone Voice Calls

| Platform | Pipeline Characteristics | SPIA Risk Factors |
|----------|-------------------------|-------------------|
| Android | OEM-customized DSP, variable quality | Fragmented; some devices aggressive compression |
| iOS | Consistent Apple DSP stack | Moderate; relatively consistent |
| Feature phones | Older codecs, limited DSP | HIGH (legacy compression) |

### 22.9.2 VoIP Applications

| Application | Audio Processing | SPIA Notes |
|-------------|------------------|------------|
| Zoom | Opus + proprietary enhancement | Moderate; quality-dependent on network |
| Microsoft Teams | SILK/Opus + AI enhancement | Variable; AI enhancement may introduce artifacts |
| WhatsApp | Opus, relatively clean | Lower risk when network good |
| Discord | Opus, gaming-optimized | Moderate; may prioritize latency over quality |

### 22.9.3 Smart Speaker and IoT Audio

Devices like Alexa, Google Home introduce additional processing:
- Far-field microphone arrays
- Aggressive beamforming
- Always-on keyword detection
- Limited speaker quality

SPIA risk: MODERATE-HIGH in devices with low-quality audio chains.

## 22.10 Forensic Audio Analysis: Identifying Processing Artifacts

### 22.10.1 Spectral Signatures of Common Artifacts

| Artifact Source | Spectral Signature |
|-----------------|-------------------|
| Codec quantization | Broadband "roughness," harmonics not precisely aligned |
| VAD transition | Abrupt spectral change, often with transient |
| Comfort noise | Flat or slowly varying spectrum, lacks natural modulation |
| PLC | Periodic structure that doesn't match surrounding context |
| NS musical noise | Sparse, time-varying tonal peaks |
| AGC pumping | Correlated AM across frequency bands |

### 22.10.2 Tools for Forensic Analysis

| Tool | Application | Limitation |
|------|-------------|------------|
| STFT / Spectrogram | Visual inspection of time-frequency content | Requires expertise to interpret |
| Modulation spectrum | Reveals AM/FM patterns | Computationally intensive |
| Long-term average spectrum | Identifies spectral anomalies | Loses temporal information |
| Packet capture (if available) | Ground truth for lost packets | Often inaccessible |

## 22.11 Designing SPIA-Resistant Communications

### 22.11.1 Engineering Recommendations

| Recommendation | Technical Implementation |
|----------------|-------------------------|
| Use wideband+ codecs when possible | Prefer EVS, Opus over narrowband |
| Prefer higher bitrates | Trade bandwidth for lower artifact risk |
| Smooth VAD transitions | Implement gradual CNG onset/offset |
| Conservative PLC | Prefer obvious gaps over synthetic content |
| User-visible quality indicator | Show when quality is degraded |
| APF integration | Apply Anti-Pareidolia Filter (Chapter 14) |

### 22.11.2 User-Level Mitigations

| Action | Effect |
|--------|--------|
| Ensure strong network connection | Fewer lost packets, higher bitrates |
| Use quality headphones | Better reproduction reveals true audio |
| Avoid calls in noisy environments | Less aggressive NS processing |
| Use video when possible | Visual anchoring reduces SPIA |

## 22.12 Conclusion: The Technological Inevitability of SPIA

Modern voice communication is a marvel of engineering—transmitting intelligible speech at remarkably low bitrates across unreliable networks. But this efficiency comes at a cost: every stage of the pipeline generates artifacts that can be perceptually confusable with speech.

SPIA is not a bug in the human auditory system—it is an emergent consequence of the interaction between:
1. Compression algorithms that model the world as if it were speech
2. Concealment algorithms that synthesize plausible audio
3. Enhancement algorithms that add content to noise
4. A human auditory system that actively seeks speech patterns

Understanding this technological substrate is essential for clinicians, engineers, and policymakers working to mitigate the unintended perceptual consequences of the digital voice era.

---
**Status**: Draft - v1.0
**Word Count**: ~2,600 words
**Technical References**: 3GPP TS 26.190 (AMR), RFC 6716 (Opus), ITU-T G.722
**Next Steps**: Add codec comparison spectrograms; develop real-time artifact detector.
