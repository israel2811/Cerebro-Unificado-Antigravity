# Chapter 27: Artificial Intelligence in Voice Pipelines

## 27.1 Introduction: AI Meets Audio

Artificial Intelligence has revolutionized voice processing, from noise suppression to transcription to generation. However, these powerful tools introduce new potential sources of SPIA and new methodological challenges. This chapter examines AI in voice pipelines, its benefits, its risks for SPIA generation, and guidelines for responsible use.

## 27.2 AI in Modern Voice Processing

### 27.2.1 Where AI Appears in the Pipeline

```
┌────────────────────────────────────────────────────────────────────┐
│                    MODERN VOICE PIPELINE WITH AI                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  CAPTURE → [AI NS] → [AI VAD] → ENCODE → TRANSMIT → DECODE         │
│                                                                    │
│           → [AI PLC] → [AI Enhancement] → RENDER → HEAR            │
│                                                                    │
│  [AI Transcription] ← RECORD                                       │
│                                                                    │
│  NS = Noise Suppression  |  VAD = Voice Activity Detection        │
│  PLC = Packet Loss Concealment                                     │
└────────────────────────────────────────────────────────────────────┘
```

### 27.2.2 AI-Enhanced Components

| Component | Traditional | AI-Enhanced | SPIA Implication |
|-----------|-------------|-------------|------------------|
| Noise Suppression | Spectral subtraction | Deep neural network | May create or remove structure |
| VAD | Energy threshold | Classifier network | May misclassify artifacts as speech |
| PLC | Linear interpolation | Generative model | Synthesizes speech-like content |
| Enhancement | Filtering | Neural reconstruction | Creates detail not in original |
| Transcription | HMM-based | Transformer models | May "hallucinate" text |

## 27.3 AI Noise Suppression

### 27.3.1 How It Works

Modern AI noise suppression (e.g., NVIDIA RTX Voice, Krisp, RNNoise):
1. Input: Noisy audio segment
2. Neural network predicts clean speech
3. Output: Noise reduced/removed

**Training data**: Usually clean speech + synthetic noise → learn mapping

### 27.3.2 SPIA-Relevant Behaviors

**Beneficial**:
- Removes ambient noise that could serve as SPIA substrate
- Reduces acoustic complexity
- May eliminate speech-like artifacts

**Problematic**:
- Trained to find speech → biased toward speech interpretation
- Can create "musical noise" (tonal artifacts)
- May generate speech structure from pure noise (hallucination)
- Removes signal but preserves envelope → pseudo-phonetic structure

### 27.3.3 Experimental Evidence

Studies have shown:
- AI NS can make non-speech sound more speech-like in some conditions
- Degraded speech + AI NS → different percept than original degraded speech
- Effect is model-dependent and unpredictable

**Recommendation**: Document whether AI NS was active during SPIA experience.

## 27.4 AI Voice Activity Detection

### 27.4.1 Traditional vs. AI VAD

**Traditional VAD**: Energy threshold, spectral flux
- Prone to false positives (noise classified as speech)
- Simple, predictable behavior

**AI VAD**: Neural classifier
- More accurate in normal conditions
- Can misclassify novel sounds as speech
- Behavior depends on training data

### 27.4.2 SPIA Implications

If AI VAD incorrectly classifies noise as speech:
- DTX is deactivated → full codec path applied
- Codec may introduce different artifacts
- System "believes" there is speech

More concerning: AI VAD trained on speech may activate for speech-like artifacts, reinforcing SPIA in the pipeline.

## 27.5 Neural Packet Loss Concealment

### 27.5.1 The Revolution in PLC

Traditional PLC: Repeat last packet, linear interpolation
- Creates obvious artifacts
- Identifiable as technical glitch

Neural PLC (e.g., Google's WaveNetEQ, Amazon's neural PLC):
- Generative model synthesizes missing audio
- Trained to produce natural-sounding speech
- **Literally generates speech that was never there**

### 27.5.2 SPIA Critical Risk

Neural PLC represents a fundamental shift:
- Previous: Artifacts are detectable degradation
- Neural: Artifacts are synthetic speech

**If a packet is lost and neural PLC generates a phoneme, that phoneme is entirely artificial—yet indistinguishable from real transmission.**

### 27.5.3 Implications for Forensics

Traditional forensic audio analysis cannot detect neural PLC:
- No spectral signature of concealment
- Output sounds like authentic speech
- Provenance is unknowable without packet-level logs

**Recommendation**: For SPIA cases involving VoIP, obtain packet-level data if possible to identify concealed segments.

## 27.6 AI Audio Enhancement

### 27.6.1 Super-Resolution and Reconstruction

AI can enhance degraded audio:
- Bandwidth extension (narrowband → wideband)
- Noise reduction
- De-reverberation
- "Restoration" of damaged audio

These systems are trained to produce speech-like output.

### 27.6.2 The Hallucination Problem

When input lacks sufficient information, AI enhancement may:
- Generate plausible but false detail
- Create formant structure from noise
- Insert phonemes based on language priors

**Example**: Heavily distorted audio enhanced by AI may emerge with clear "words" that were never in the original signal.

### 27.6.3 Forensic Implications

**Never use AI-enhanced audio as primary evidence.**
- AI output reflects training data + input, not truth
- Enhancement is inference, not recovery
- Original audio must be preserved and analyzed first

## 27.7 Automatic Speech Recognition (ASR) and Hallucination

### 27.7.1 ASR Basics

Modern ASR (Whisper, Google Speech-to-Text, etc.):
1. Input: Audio waveform
2. Acoustic model: Audio → phoneme probabilities
3. Language model: Phoneme sequence → word sequence
4. Output: Text transcript

### 27.7.2 ASR Hallucination

ASR systems can produce text that is not in the audio:

**Types of hallucination**:
| Type | Description | Example |
|------|-------------|---------|
| Insertion | Adds words not present | "..." → "okay" |
| Substitution | Wrong word | "cat" → "car" |
| Confabulation | Plausible but false | Noise → coherent sentence |
| Language prior | Most likely phrase | Mumble → common phrase |

### 27.7.3 SPIA Interaction

**Danger**: A user transcribes a SPIA-inducing audio segment:
1. Audio contains CNG/PLC artifacts
2. ASR hallucinates text from artifacts
3. User sees text → confirms belief that speech was present
4. Text reinforces SPIA conviction

**The ASR transcript becomes "evidence" of content that was never there.**

### 27.7.4 Critical Rule

**Never accept ASR output as evidence without:**
- Original audio preserved
- Multiple transcription sources compared
- Blind human panel evaluation
- Acknowledgment that ASR can hallucinate

## 27.8 Dataset Bias in Speech AI

### 27.8.1 The Training Data Problem

AI systems learn from training data. Key biases:

**LibriSpeech** (common training set):
- 100% American English
- Predominantly male voices
- Read speech (not conversational)
- Clean recording conditions

**Implications**:
- Systems are biased toward English phonotactics
- May "find" English patterns in non-English noise
- Different performance on other languages/accents

### 27.8.2 Linguistic Bias and SPIA

An English-trained ASR may transcribe:
- Spanish speech → English-sounding nonsense
- Environmental noise → English words
- CNG artifacts → English phonemes

This creates systematic bias toward English SPIA content.

### 27.8.3 Recommendation

When using AI for SPIA assessment:
- Document the training language of the system
- Use multiple systems trained on different data
- Weight results accordingly
- Prefer human evaluation for final judgment

## 27.9 Responsible AI Use in SPIA Assessment

### 27.9.1 Principles

1. **AI is a tool, not a judge**: Use for screening, not conclusion
2. **Preserve originals**: Never analyze only AI-processed audio
3. **Document processing**: Full chain of custody for AI steps
4. **Compare outputs**: Multiple systems, multiple conditions
5. **Human verification**: Final assessment by trained listeners

### 27.9.2 Workflow

```
Original Audio
      │
      ├──→ [AI Enhancement] → Screen for patterns (TENTATIVE)
      │
      ├──→ [AI Transcription] → Screening hypothesis (TENTATIVE)
      │
      ├──→ [Spectral Analysis] → SPIA metrics (OBJECTIVE)
      │
      └──→ [Human Panel] → Final judgment (DEFINITIVE)
```

### 27.9.3 Red Flags

Be suspicious when:
- AI transcription is highly confident but audio is degraded
- Enhancement produces "clear" speech from noise
- Different AI systems produce different transcripts
- Content matches user's concerns exactly (confirmation bias)

## 27.10 AI as Source of SPIA vs. AI for SPIA Assessment

### 27.10.1 Dual Role

AI systems can be:
1. **SPIA generators**: Producing artifacts in voice pipelines
2. **SPIA assessors**: Analyzing audio for SPIA potential

This dual role creates complexity.

### 27.10.2 When AI Generates SPIA

If a user's voice pipeline includes AI components (neural NS, neural PLC):
- SPIA may emerge from AI processing
- The AI has literally generated speech-like content
- This is a technological etiology of voice-hearing

### 27.10.3 When AI Assesses SPIA

If we use AI to analyze SPIA audio:
- The AI may confirm SPIA by "finding" speech
- But this confirmation reflects AI bias, not reality
- Circular reasoning risk

**Solution**: Use AI for objective metrics (spectrum analysis, modulation), not for content determination.

## 27.11 Future Directions

### 27.11.1 AI-Specific SPIA Research Needs

1. Characterize SPIA potential of neural PLC outputs
2. Develop AI-aware forensic protocols
3. Create test sets of AI-generated vs. authentic speech
4. Study linguistic bias across AI systems

### 27.11.2 Potential Countermeasures

- APF (Anti-Pareidolia Filters) designed to disrupt AI speech-finding
- Watermarking for AI-generated/enhanced audio
- Transparency standards for voice pipeline AI
- User control over AI processing in calls

## 27.12 Conclusion: AI as Double-Edged Sword

AI has transformed voice communication and audio analysis. But its power comes with risk:

**Benefits**:
- Improved call quality
- Noise reduction
- Accessibility (transcription)

**Risks for SPIA**:
- Generates speech-like content from artifacts
- Confirms SPIA through biased transcription
- Obscures true audio provenance
- Creates unfalsifiable evidence

The principle is clear: **AI can create speech that was never spoken and confirm speech that was never heard.**

For SPIA assessment, AI is a powerful tool that must be used with extreme caution and never as the sole basis for conclusions.

---
**Status**: Draft - v1.0
**Word Count**: ~2,000 words
**Integration**: Links to Ethics (Ch 8), Forensics (Ch 15), ASR Hallucination research
