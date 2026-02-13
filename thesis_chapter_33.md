# Chapter 33: Statistical Methods and Bayesian Analysis

## 33.1 Introduction: Quantifying Uncertainty

Rigorous statistical methodology is essential for CCA research. This chapter presents the statistical framework for analyzing CCA data, from base rates to Bayesian updating, ensuring that conclusions are appropriately calibrated to evidence strength.

## 33.2 Base Rates and Prior Probabilities

### 33.2.1 Why Base Rates Matter

Before interpreting any test result, we must know the prior probability of each condition:

| Condition | Estimated Base Rate | Source |
|-----------|---------------------|--------|
| Lifetime AVH (general population) | ~9.6% | Meta-analysis (de Leede-Smith & Barkus) |
| Schizophrenia spectrum | ~1% | DSM-5, epidemiological |
| Stalkerware exposure | ~0.1-1%? | Coalition estimates (uncertain) |
| Actual surveillance (IPV context) | Higher (10-30%) | DV research |
| Medical causes of hallucinations | Variable | Depends on population |

### 33.2.2 The Base Rate Fallacy

Ignoring base rates leads to diagnostic errors:
- A 99% accurate test for a 0.1% prevalence condition → 50% false positive rate
- Detection of "stalkerware indicators" requires knowing base rate of innocent explanations

**Rule**: Always compute positive predictive value (PPV) with actual base rates.

### 33.2.3 Adjusting Priors by Context

Base rates vary by context:
- Clinical referral population: Higher prevalence of disorders
- IPV context: Higher prevalence of surveillance
- Tech-savvy population: Different app installation patterns

## 33.3 Experimental Design Principles

### 33.3.1 ABAB / N-of-1 Designs

For individual CCA assessment:

| Phase | Condition | Purpose |
|-------|-----------|---------|
| A1 | Baseline | Establish natural rate |
| B1 | Intervention | Test effect |
| A2 | Withdrawal | Test reversibility |
| B2 | Re-intervention | Confirm effect |

**Statistical Analysis**:
- Compare rates between phases
- Use interrupted time series analysis
- Calculate effect size (standardized mean difference)

### 33.3.2 Controlling for Confounders

Major confounders in CCA research:
- Time of day effects
- Fatigue/stress state
- Medication changes
- Environmental changes

**Design solution**: Within-subject comparison, counterbalanced order, multiple replications.

### 33.3.3 Blinding Procedures

| Level | Who is blind | Purpose |
|-------|--------------|---------|
| Single-blind | Subject blind to condition | Reduce expectation effects |
| Double-blind | Subject + assessor | Reduce bias in measurement |
| Triple-blind | + analyst | Reduce analysis bias |

For SPIA assessment:
- Blind panel for audio evaluation (essential)
- Subject cannot always be blinded to environmental changes

### 33.3.4 Preregistration

To prevent p-hacking and HARKing:
- Preregister hypotheses, methods, and analysis plan
- Distinguish exploratory from confirmatory analyses
- Report all analyses, including null results

## 33.4 Effect Size and Power

### 33.4.1 Effect Size Metrics

| Metric | Use Case | Interpretation |
|--------|----------|----------------|
| Cohen's d | Continuous outcomes | 0.2 small, 0.5 medium, 0.8 large |
| Odds Ratio (OR) | Binary outcomes | 1.0 = no effect |
| Correlation (r) | Continuous associations | 0.1 small, 0.3 medium, 0.5 large |
| Number Needed to Treat (NNT) | Clinical significance | Lower = better |

### 33.4.2 Power Analysis

Before data collection, determine required sample size:

```
Power = 1 - β = P(reject H0 | H0 false)
```

For N-of-1 studies:
- Number of observations per phase
- Expected effect size from pilot data
- Autocorrelation in time series

**Minimum recommended**: 5 observations per phase for ABAB (20 total).

## 33.5 Reliability and Agreement

### 33.5.1 Cohen's Kappa (κ)

For categorical judgments (e.g., "speech present" yes/no):

```
κ = (Po - Pe) / (1 - Pe)
```

Where:
- Po = observed agreement
- Pe = expected agreement by chance

| κ Value | Interpretation |
|---------|----------------|
| < 0 | Less than chance |
| 0.01-0.20 | Slight |
| 0.21-0.40 | Fair |
| 0.41-0.60 | Moderate |
| 0.61-0.80 | Substantial |
| 0.81-1.00 | Almost perfect |

**Threshold for SPIA**: κ < 0.4 suggests SPIA (pareidolia); κ > 0.6 suggests real content.

### 33.5.2 Intraclass Correlation Coefficient (ICC)

For continuous ratings (e.g., SPIA potential score):

| ICC Type | Use Case |
|----------|----------|
| ICC(1,1) | Single rater, random sample |
| ICC(2,1) | Single rater, all raters rate all |
| ICC(2,k) | Average of k raters |

**Minimum recommended**: ICC > 0.75 for acceptable reliability.

### 33.5.3 Inter-Rater Reliability for Blind Panels

Standard protocol:
1. Present audio segments to N raters (N ≥ 5)
2. Collect transcription attempts
3. Calculate agreement on presence of speech (κ)
4. If κ > 0.6: Real content likely
5. If κ < 0.4: SPIA likely (or pure noise)

## 33.6 Bayesian Analysis

### 33.6.1 Bayes' Theorem Applied

```
P(H|E) = P(E|H) × P(H) / P(E)
```

Where:
- P(H|E) = posterior probability of hypothesis given evidence
- P(E|H) = likelihood of evidence given hypothesis
- P(H) = prior probability of hypothesis
- P(E) = marginal probability of evidence

### 33.6.2 Bayesian Updating in CCA

**Example**: Probability of Scenario B (SPIA) given findings

Prior: P(Scenario B) = 0.3 (based on prevalence estimates)

Evidence 1: Device audit negative for stalkerware
- P(neg audit | B) = 0.95 (SPIA doesn't require malware)
- P(neg audit | A) = 0.2 (surveillance usually leaves traces)
- Updates posterior toward B

Evidence 2: Blind panel κ < 0.3
- P(low κ | B) = 0.8 (SPIA produces low agreement)
- P(low κ | A) = 0.2 (real content produces high agreement)
- Further updates toward B

**Final posterior**: P(Scenario B | all evidence) = compute sequentially

### 33.6.3 Bayes Factors

For hypothesis comparison:

```
BF = P(E|H1) / P(E|H0)
```

| BF Value | Evidence Strength |
|----------|-------------------|
| 1-3 | Anecdotal |
| 3-10 | Moderate |
| 10-30 | Strong |
| 30-100 | Very strong |
| > 100 | Extreme |

### 33.6.4 Advantages of Bayesian Approach

1. Incorporates prior knowledge explicitly
2. Updates with each new piece of evidence
3. Provides probability of hypothesis (not just reject/fail-to-reject)
4. Handles small samples better than frequentist methods
5. Naturally integrates multiple sources of evidence

## 33.7 Time Series Analysis

### 33.7.1 Autocorrelation

Observations close in time are often correlated:
- SPIA episodes may cluster
- Ignoring autocorrelation inflates Type I error

**Solution**: Model autocorrelation structure (AR, MA, ARIMA)

### 33.7.2 Interrupted Time Series

For ABAB designs:
- Model level change at intervention points
- Model slope change (gradual vs. immediate effect)
- Test significance of changes

**Key metrics**:
- Pre-intervention slope
- Level change at intervention
- Post-intervention slope

### 33.7.3 Changepoint Detection

Identify when episodes change in frequency:
- Bayesian changepoint detection
- CUSUM methods
- Correlate with known events (device change, move, etc.)

## 33.8 Causal Inference

### 33.8.1 Directed Acyclic Graphs (DAGs)

Visualize causal structure:

```
Environment → Signal → Perception → Report
                 ↑          ↑
              Device      State
```

Use DAGs to:
- Identify confounders (must control)
- Identify mediators (don't control if testing mediation)
- Identify colliders (don't control)

### 33.8.2 Mediation Analysis

Does signal quality mediate the effect of environment on perception?

```
Environment → Signal → Perception
         ↘         ↗
              (direct)
```

Test:
- Total effect: Environment → Perception
- Indirect effect: via Signal
- Direct effect: remaining

### 33.8.3 Limits of Observational Causal Inference

Without randomization:
- Confounding is always possible
- Causal claims require strong assumptions
- Report as "consistent with" not "proves"

## 33.9 Statistical Reporting Standards

### 33.9.1 What to Report

Following APA 7:
- Descriptive statistics (M, SD, range)
- Effect sizes with confidence intervals
- Exact p-values (not "<0.05")
- Power analysis (before study)
- All analyses conducted (avoid selective reporting)

### 33.9.2 Visualization

- Time series plots for ABAB data
- Forest plots for effect sizes
- Posterior distributions for Bayesian analyses
- DAGs for causal models

## 33.10 Conclusion: Rigor in Uncertainty

Statistical methods in CCA research serve to:
1. Quantify uncertainty explicitly
2. Update beliefs systematically with evidence
3. Prevent overconfident conclusions
4. Enable reproducible analysis

The goal is not certainty—it is calibrated uncertainty.

---
**Status**: Draft - v1.0  
**Word Count**: ~1,900 words
**Integration**: P0-P4 Protocol (30), Hypothesis testing (25), Assessment (16-18)
