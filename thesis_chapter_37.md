# Chapter 37: Electroacoustics and Device Audio Pathways

## 37.1 Introduction: The Device as Acoustic System

Modern electronic devices are complex acoustic systems with multiple input and output pathways. Understanding how these pathways can generate, modify, or mask audio signals is essential for CCA assessment. This chapter examines the electroacoustic properties of common devices.

## 37.2 Transducer Fundamentals

### 37.2.1 Microphones

| Type | Principle | Characteristics |
|------|-----------|-----------------|
| MEMS | Capacitor/diaphragm | Small, low power, in phones |
| Condenser | Capacitor | High sensitivity, studio use |
| Dynamic | Electromagnetic | Robust, less sensitive |
| Piezoelectric | Crystal deformation | Contact microphones |

**Key Parameters**:
- Sensitivity (mV/Pa)
- Frequency response (Hz)
- Signal-to-noise ratio (dB)
- Self-noise floor (dBA)

### 37.2.2 Speakers and Earphones

| Component | Function | SPIA Relevance |
|-----------|----------|----------------|
| Driver | Electromechanical transducer | Can emit ultrasonic artifacts |
| Enclosure | Acoustic resonator | Modifies frequency response |
| Port (if present) | Bass extension | Can cause turbulent noise |
| Crossover | Frequency division | May create phase artifacts |

### 37.2.3 Distortion Mechanisms

- **Harmonic distortion**: Creates overtones not in original signal
- **Intermodulation distortion**: Creates sum/difference frequencies
- **Clipping**: Hard limiting creates complex harmonics
- **Mechanical noise**: Physical rubbing, buzzing, rattling

These distortions can create acoustic content that was not in the original signal.

## 37.3 Smartphone as Acoustic System

### 37.3.1 Multiple Microphone Arrays

Modern smartphones have 2-4 microphones for:
- Voice capture
- Noise reference
- Beamforming
- Echo cancellation

**Microphone Locations**:
- Bottom (primary voice)
- Top (secondary/video)
- Back (camera)
- Side (auxiliary)

### 37.3.2 Beamforming

**Purpose**: Enhance voice, suppress background
**Method**: Phase-aligned combination of multiple mics
**SPIA Relevance**: Can create spatial nulls and enhance off-axis sounds unexpectedly

### 37.3.3 Active Noise Cancellation (ANC)

**In earphones/headphones**:
- Captures external sound
- Generates anti-phase signal
- Creates "silence zone"

**SPIA Relevance**:
- Imperfect cancellation creates artifacts
- Residual sounds have altered timbre
- Some frequencies cancelled more than others

### 37.3.4 Transparency Mode

**Purpose**: Allow environmental sounds while wearing earphones
**Method**: Microphone pass-through with latency correction
**SPIA Relevance**: 
- Adds processing artifacts
- May alter voice characteristics
- Can cause comb filtering with direct sound

## 37.4 The Ambiguity of "Mute"

### 37.4.1 Levels of Mute

| Level | Meaning | Audio Status |
|-------|---------|--------------|
| App mute | App doesn't transmit | May still capture |
| OS mute | System blocks transmission | Hardware may still run |
| Hardware mute | Physical switch | Truly stops capture |
| Privacy shutter | Physical mic cover | Physically blocked |

### 37.4.2 Implications

- App-level mute ≠ microphone is off
- Background apps may still access mic
- System sounds may still be captured
- VoIP apps may send comfort noise during "mute"

**For CCA Assessment**: Document what "mute" means in each context.

## 37.5 Video Conferencing Audio

### 37.5.1 Complex Audio Routing

A typical video call involves:
1. Local microphone → DSP preprocessing
2. Encoding → Network transmission
3. Jitter buffer → Decoding
4. Playback → Speaker/headphones
5. Echo from speaker → Back to microphone
6. Echo cancellation in DSP

Each stage can introduce artifacts.

### 37.5.2 Common Issues

| Issue | Cause | Perception |
|-------|-------|------------|
| Echo | Incomplete cancellation | Voice repeats |
| Feedback | Loop amplification | Howl or squeal |
| Pumping | AGC overreaction | Volume fluctuation |
| Musical noise | NS artifacts | "Underwater" quality |
| Dropouts | Packet loss | Missing segments |
| Garbling | Severe degradation | Unintelligible |

### 37.5.3 Bluetooth Audio

**Latency Issues**:
- A2DP (music): ~150-300ms
- HFP (calls): ~50-100ms
- aptX Low Latency: ~40ms

**SPIA Relevance**:
- Latency can cause echo/confusion
- Codec switching (SBC → AAC → aptX) changes quality
- Multiple Bluetooth devices can interfere

## 37.6 Signal Leakage and Accidental Mixing

### 37.6.1 Cross-Talk

Electrical or acoustic coupling between channels:
- Stereo crosstalk in cheap hardware
- RF interference picked up by cables
- Ground loop hum (50/60 Hz)

### 37.6.2 Accidental Audio Routing

In complex systems, audio can be routed unexpectedly:
- Monitor output routed to stream
- Virtual audio cables misconfigured
- Multiple apps capturing same source
- Hardware mixer routing errors

**Result**: Unintended audio in the signal.

## 37.7 Environmental Electromagnetic Interference

### 37.7.1 Common Sources

| Source | Frequency | Mechanism |
|--------|-----------|-----------|
| Power lines | 50/60 Hz | Magnetic induction |
| Switching supplies | 20-200 kHz | Radiated EMI |
| WiFi | 2.4/5 GHz | RF interference |
| Cellular | Various bands | RF interference |
| Nearby devices | Various | Inductive coupling |

### 37.7.2 Demodulation Effects

Poorly shielded audio circuits can demodulate RF:
- AM radio picked up by amplifier
- GSM buzz (217 Hz pattern)
- WiFi packet sounds

**SPIA Relevance**: These can be perceived as voices or patterns.

## 37.8 Measurement Considerations

### 37.8.1 Equipment for Device Assessment

| Tool | Purpose |
|------|---------|
| Oscilloscope | Waveform analysis |
| Spectrum analyzer | Frequency content |
| SDR (Software Defined Radio) | RF detection |
| EMI scanner | Field mapping |
| Reference microphone | Calibrated measurement |

### 37.8.2 P1 Protocol Application

During device audit:
1. List all audio-capable devices
2. Document microphone/speaker locations
3. Test each mode (mute, ANC, transparency)
4. Look for unexpected audio outputs
5. Check for EMI susceptibility

## 37.9 Practical Implications for SPIA

### 37.9.1 High-Risk Configurations

- Multiple active Bluetooth devices
- Video conferencing with external speakers
- Poor quality earphones with transparency mode
- Devices near strong EMI sources

### 37.9.2 Low-Risk Configurations

- Wired headphones, no processing
- Hardware mute switch engaged
- Airplane mode active
- Shielded environment

## 37.10 Conclusion: Devices Shape What We Hear

Modern electronic devices are not neutral conduits of sound. They:
- Process audio through multiple stages
- Introduce artifacts at each stage
- Can route audio unexpectedly
- Are susceptible to environmental interference

Understanding device acoustics is essential for determining whether perceived sounds have a technological origin.

---
**Status**: Draft - v1.0
**Word Count**: ~1,600 words
**Integration**: RTC/DSP (22), Physical Acoustics (26), P1 Protocol (28)
