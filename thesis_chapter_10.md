# Chapter 10: Advanced Statistical Methods for CCA Research

## Abstract
This chapter inaugurates Section II of the thesis by establishing the quantitative methodological foundation for Cyber-Acoustic Convergence research. We present advanced statistical techniques for analyzing the relationship between environmental signals and auditory perception, including Bayesian inference, machine learning classification, time-series analysis, and multilevel modeling. These methods enable rigorous investigation of CCA phenomena while accounting for individual differences, environmental complexity, and temporal dynamics.

---

## 10.1 Introduction: The Need for Advanced Methods

### 10.1.1 Challenges in CCA Research

The study of Cyber-Acoustic Convergence presents unique methodological challenges:

1. **Individual variability**: Perceptual thresholds and susceptibility vary dramatically across individuals
2. **Environmental complexity**: Modern acoustic environments contain hundreds of overlapping signals
3. **Temporal dynamics**: CCA effects may emerge, adapt, or habituate over time
4. **Small effect sizes**: Subtle perceptual phenomena require sensitive detection methods
5. **Multiple testing**: Investigating numerous signal parameters risks false positives

Traditional statistical approaches (e.g., simple t-tests, ANOVA) are insufficient for these complexities.

### 10.1.2 Statistical Framework Overview

This chapter presents a comprehensive statistical toolkit:

- **Bayesian methods** for parameter estimation and model comparison
- **Machine learning** for pattern classification and prediction
- **Time-series analysis** for temporal dynamics
- **Multilevel modeling** for nested and crossed random effects
- **Signal detection theory** for perceptual threshold estimation
- **Multiple comparison corrections** for controlling false discovery

---

## 10.2 Bayesian Inference for CCA

### 10.2.1 Rationale for Bayesian Approach

Bayesian inference offers several advantages for CCA research:

1. **Prior information**: Incorporate theoretical predictions about signal thresholds
2. **Uncertainty quantification**: Full posterior distributions vs. point estimates
3. **Small sample handling**: Better performance with limited participants
4. **Model comparison**: Direct probability of competing hypotheses
5. **Sequential updating**: Incorporate new data without statistical penalties

### 10.2.2 Bayesian Model for Signal Detection

**Model specification**:

Let *p(hear|signal)* represent the probability that a participant reports hearing content given signal presence, and *p(hear|no signal)* for absence.

**Likelihood function**:
```
Y_i ~ Bernoulli(p_i)

where:
p_i = p(hear|signal) if Signal_i = 1
p_i = p(hear|no signal) if Signal_i = 0
```

**Priors** (informed by psychoacoustic literature):
```
p(hear|signal) ~ Beta(α_signal, β_signal)
p(hear|no signal) ~ Beta(α_noise, β_noise)

where α_noise = 1, β_noise = 9 (expecting 10% false positive rate)
and α_signal = 5, β_signal = 5 (uncertain, centered at 50%)
```

**Posterior inference**:
After observing data, we obtain posterior distributions:
```
p(p_signal | data) ~ Beta(α_signal + hits, β_signal + misses)
p(p_noise | data) ~ Beta(α_noise + false_alarms, β_noise + correct_rejections)
```

### 10.2.3 Sensitivity Analysis (d')

Compute Bayesian d' (sensitivity index):
```
d' = Φ^(-1)(p_signal) - Φ^(-1)(p_noise)
```
where Φ^(-1) is the inverse normal CDF.

**Interpretation**:
- d' > 1.5: Strong signal detection capability
- 1.0 < d' < 1.5: Moderate detection
- d' < 1.0: Weak or absent detection

### 10.2.4 Bayes Factors for Model Comparison

To compare:
- **M1**: Signal causes auditory perception (CCA hypothesis)
- **M0**: No relationship (null hypothesis)

**Bayes Factor**:
```
BF_10 = P(data | M1) / P(data | M0)
```

**Interpretation guidelines**:
- BF > 10: Strong evidence for M1
- 3 < BF < 10: Moderate evidence for M1
- 1/3 < BF < 3: Inconclusive
- BF < 1/3: Evidence for M0

### 10.2.5 Implementation in R

```r
library(rstan)

stan_model <- "
data {
  int<lower=0> N_signal;
  int<lower=0> N_noise;
  int<lower=0> hits;
  int<lower=0> false_alarms;
}
parameters {
  real<lower=0,upper=1> p_signal;
  real<lower=0,upper=1> p_noise;
}
model {
  // Priors
  p_signal ~ beta(5, 5);
  p_noise ~ beta(1, 9);
  
  // Likelihood
  hits ~ binomial(N_signal, p_signal);
  false_alarms ~ binomial(N_noise, p_noise);
}
generated quantities {
  real d_prime = inv_Phi(p_signal) - inv_Phi(p_noise);
}
"

fit <- stan(model_code = stan_model, data = cca_data, iter = 4000)
```

---

## 10.3 Machine Learning Classification

### 10.3.1 Problem Formulation

**Task**: Classify whether an auditory report is:
- **Class 1**: CCA-induced (environmentally caused)
- **Class 0**: Primary hallucination (internally generated)

**Features** (predictors):
1. Location specificity (binary)
2. Time-of-day pattern (binary)
3. Signal correlation score (continuous, 0-1)
4. Acoustic environment complexity (continuous)
5. Psychiatric symptom severity (continuous)
6. Duration of experience (continuous)
7. Content complexity (ordinal, 1-5)
8. Treatment response (binary)

### 10.3.2 Random Forest Classifier

**Rationale**: Handles non-linear relationships, interactions, and mixed variable types.

**Algorithm**:
1. Bootstrap *B* samples from training data
2. For each bootstrap sample:
   - Grow decision tree: at each node, select best split from random subset of *m* features
   - Continue until minimum node size reached
3. Predict new cases by majority vote across *B* trees

**Hyperparameters**:
- *B* = 500 trees
- *m* = √(number of features) ≈ 3 for 8 features
- Minimum node size = 5

**Implementation in Python**:
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Initialize model
rf_model = RandomForestClassifier(
    n_estimators=500,
    max_features='sqrt',
    min_samples_leaf=5,
    random_state=42
)

# Train
rf_model.fit(X_train, y_train)

# Evaluate with cross-validation
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=10, scoring='roc_auc')
print(f"Mean AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Feature importance
importance = rf_model.feature_importances_
for feature, imp in zip(feature_names, importance):
    print(f"{feature}: {imp:.3f}")
```

### 10.3.3 Support Vector Machine (SVM)

**Rationale**: May better handle high-dimensional feature spaces and find optimal decision boundaries.

**Kernel selection**:
- **Linear kernel**: For linearly separable data
- **RBF kernel**: For complex, non-linear boundaries
- **Polynomial kernel**: For specific polynomial relationships

**Hyperparameter tuning** (grid search with cross-validation):
```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1],
    'kernel': ['rbf', 'linear']
}

svm_model = GridSearchCV(SVC(probability=True), param_grid, cv=5, scoring='roc_auc')
svm_model.fit(X_train, y_train)

print(f"Best parameters: {svm_model.best_params_}")
print(f"Best CV AUC: {svm_model.best_score_:.3f}")
```

### 10.3.4 Neural Network Classifier

**Architecture**: 
- Input layer: 8 features
- Hidden layer 1: 16 neurons, ReLU activation
- Hidden layer 2: 8 neurons, ReLU activation
- Output layer: 1 neuron, sigmoid activation

```python
from tensorflow import keras

nn_model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(8,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(1, activation='sigmoid')
])

nn_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['AUC']
)

history = nn_model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)
```

### 10.3.5 Model Evaluation

**Metrics**:
1. **AUC-ROC**: Overall discrimination ability (primary metric)
2. **Sensitivity**: P(predict CCA | true CCA) - clinical priority
3. **Specificity**: P(predict not CCA | true not CCA)
4. **Precision**: P(true CCA | predict CCA) - avoid false CCA diagnoses
5. **F1 score**: Harmonic mean of precision and recall

**Expected performance**:
- AUC > 0.80: Clinically useful
- AUC > 0.90: Excellent discrimination
- Sensitivity > 0.85: Minimize missed CCA cases

---

## 10.4 Time-Series Analysis

### 10.4.1 Motivation

CCA may manifest temporal patterns:
- **Circadian variation**: Correlating with signal source activity
- **Habituation**: Decreased perception over time
- **Sensitization**: Increased perception with repeated exposure

### 10.4.2 Autoregressive Integrated Moving Average (ARIMA)

**Model structure**: ARIMA(p, d, q)
- *p*: Autoregressive order (lags of the series itself)
- *d*: Degree of differencing (to achieve stationarity)
- *q*: Moving average order (lags of forecast errors)

**Example**: Daily count of auditory experiences

**Model identification**:
1. Plot autocorrelation function (ACF) and partial ACF (PACF)
2. Check stationarity (Augmented Dickey-Fuller test)
3. If non-stationary, difference series (d = 1 or 2)
4. Select p and q based on ACF/PACF patterns

**Implementation in R**:
```r
library(forecast)

# Fit ARIMA
model <- auto.arima(experience_counts, seasonal = FALSE)
summary(model)

# Forecast
forecast_vals <- forecast(model, h = 30)  # 30 days ahead
plot(forecast_vals)

# Check residuals (should be white noise)
checkresiduals(model)
```

### 10.4.3 Vector Autoregression (VAR)

**Purpose**: Model mutual influence between multiple time series

**Variables**:
- Experience count (Y1)
- Signal strength measurement (Y2)
- Self-reported stress (Y3)

**Model**:
```
Y1_t = α1 + β11*Y1_(t-1) + β12*Y2_(t-1) + β13*Y3_(t-1) + ε1_t
Y2_t = α2 + β21*Y1_(t-1) + β22*Y2_(t-1) + β23*Y3_(t-1) + ε2_t
Y3_t = α3 + β31*Y1_(t-1) + β32*Y2_(t-1) + β33*Y3_(t-1) + ε3_t
```

**Granger causality test**: Does signal strength "Granger-cause" experiences?

```r
library(vars)

# Prepare multivariate series
data_matrix <- cbind(experiences, signal_strength, stress)

# Select lag order
VARselect(data_matrix, lag.max = 10)

# Fit VAR
var_model <- VAR(data_matrix, p = 2)  # 2 lags

# Granger causality test
causality(var_model, cause = "signal_strength")
```

### 10.4.4 Spectral Analysis

**Purpose**: Identify periodic patterns in experience occurrence

**Periodogram**: Estimates power at different frequencies

**Expected patterns**:
- **24-hour cycle**: Diurnal variation
- **7-day cycle**: Weekly patterns (e.g., weekday vs. weekend environments)
- **Specific frequencies**: Matching known signal modulation rates

```r
# Compute periodogram
spectrum_result <- spectrum(experience_counts, log = "no")

# Identify dominant frequencies
dominant_freqs <- which(spectrum_result$spec > quantile(spectrum_result$spec, 0.95))
periods <- 1 / spectrum_result$freq[dominant_freqs]
print(paste("Dominant periods (days):", periods))
```

---

## 10.5 Multilevel Modeling

### 10.5.1 Data Structure

CCA data has nested structure:
- **Level 1**: Repeated observations (days, trials)
- **Level 2**: Individuals
- **Level 3**: Environments (home, work, etc.)

Traditional regression assumes independence; multilevel models account for clustering.

### 10.5.2 Random Intercept Model

**Fixed effects**: Average signal-perception relationship across all participants
**Random effects**: Individual-specific intercepts (baseline perception tendency)

**Model equation**:
```
Y_ij = β0 + β1*Signal_ij + u0j + ε_ij

where:
- Y_ij: Auditory perception score for person j on occasion i
- Signal_ij: Signal strength at that time
- β0: Population average intercept
- β1: Population average slope (signal effect)
- u0j ~ N(0, τ²): Random intercept for person j
- ε_ij ~ N(0, σ²): Residual error
```

**Interpretation**:
- If τ² is large: Substantial individual differences in baseline perception
- β1 > 0 and significant: Signal strength predicts perception

### 10.5.3 Random Slope Model

Allow signal effect to vary across individuals:

```
Y_ij = β0 + β1*Signal_ij + u0j + u1j*Signal_ij + ε_ij

where:
- u1j ~ N(0, τ1²): Random slope for person j
- Correlation between u0j and u1j estimated
```

**Interpretation**:
- If τ1² is large: Susceptibility to signals varies markedly

### 10.5.4 Cross-Classified Model

Observations nested within both persons AND environments:

```
Y_ijk = β0 + β1*Signal_ijk + u0j + v0k + ε_ijk

where:
- u0j: Random effect for person j
- v0k: Random effect for environment k
```

**Use case**: Assess whether environmental factors contribute variance beyond individual differences.

### 10.5.5 Implementation in R (lme4)

```r
library(lme4)

# Random intercept model
model1 <- lmer(perception ~ signal_strength + (1 | person_id), data = cca_data)
summary(model1)

# Random slope model
model2 <- lmer(perception ~ signal_strength + (signal_strength | person_id), data = cca_data)

# Model comparison
anova(model1, model2)

# Intraclass correlation (ICC)
# Proportion of variance due to person differences
icc <- VarCorr(model1)$person_id[1] / (VarCorr(model1)$person_id[1] + sigma(model1)^2)
print(paste("ICC:", round(icc, 3)))
```

---

## 10.6 Multiple Comparison Corrections

### 10.6.1 The Multiple Testing Problem

When testing many hypotheses (e.g., 100 signal frequencies), ~5% will be "significant" by chance even with no true effects.

**Family-Wise Error Rate (FWER)**: Probability of ≥1 false positive in the family of tests
**False Discovery Rate (FDR)**: Expected proportion of false positives among rejected hypotheses

### 10.6.2 Bonferroni Correction

**Most conservative approach**: Divide α by number of tests

For *m* tests at α = 0.05:
```
Adjusted α = 0.05 / m
```

**Example**: Testing 100 frequencies → adjusted α = 0.0005

**Pros**: Simple, controls FWER
**Cons**: Very conservative (low power)

### 10.6.3 Benjamini-Hochberg Procedure (FDR Control)

**Less conservative**: Controls expected proportion of false discoveries

**Algorithm**:
1. Order p-values: p(1) ≤ p(2) ≤ ... ≤ p(m)
2. Find largest i such that: p(i) ≤ (i/m) × α
3. Reject H(1), ..., H(i)

**Example** (α = 0.05, m = 100):
```
If p(72) = 0.035 and (72/100) × 0.05 = 0.036
→ Reject first 72 hypotheses
```

**Implementation in R**:
```r
adjusted_p <- p.adjust(raw_p_values, method = "BH")
significant <- which(adjusted_p < 0.05)
```

### 10.6.4 Permutation Testing

**Non-parametric alternative**: Generate null distribution empirically

**Procedure**:
1. Calculate observed test statistic (e.g., correlation between signal and perception)
2. Permute group labels (or randomize signal timing) 10,000 times
3. Recalculate statistic for each permutation
4. p-value = proportion of permuted statistics ≥ observed

**Advantage**: No distributional assumptions, naturally accounts for data structure

```python
import numpy as np

def permutation_test(data, n_permutations=10000):
    observed_stat = np.corrcoef(data['signal'], data['perception'])[0, 1]
    
    perm_stats = []
    for _ in range(n_permutations):
        shuffled = data['signal'].sample(frac=1).values
        perm_stat = np.corrcoef(shuffled, data['perception'])[0, 1]
        perm_stats.append(perm_stat)
    
    p_value = np.mean(np.abs(perm_stats) >= np.abs(observed_stat))
    return observed_stat, p_value
```

---

## 10.7 Sample Size and Power Analysis

### 10.7.1 Signal Detection Power

**Question**: How many trials needed to detect d' = 1.5 with 80% power?

**Assumptions**:
- α = 0.05 (two-tailed)
- Effect size: d' = 1.5 (medium-large)
- Equal number of signal and no-signal trials

**Formula** (simplified):
```
n ≈ 16 / (d'^2)
n ≈ 16 / 2.25 ≈ 7 participants
```

With 50 trials each → 350 total trials

**Recommendation**: At least 15-20 participants for robust estimation

### 10.7.2 Classification Power

**For ML models**: Need sufficient samples per class

**Rule of thumb**:
- Minimum: 10 samples per feature per class
- For 8 features, 2 classes: ≥ 80 samples per class → 160 total

**Better**: Use learning curves to assess if more data would help

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, 
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='roc_auc'
)

# Plot to see if validation score plateaus
```

### 10.7.3 Longitudinal Power

**For time-series**: Depends on autocorrelation and effect size

**Practical guidelines**:
- Daily assessments for ≥ 30 days minimum
- Better: 90+ days for seasonal patterns
- Multiple measurements per day increases power

---

## 10.8 Methodological Recommendations

### 10.8.1 Study Design Principles

1. **Randomization when possible**: Randomly assign signal presence/absence
2. **Blinding**: Participants and raters unaware of signal status
3. **Multiple baselines**: Establish individual baseline perception rates
4. **Converging evidence**: Use multiple statistical approaches

### 10.8.2 Reporting Standards

**Transparent reporting checklist**:
- [ ] Sample size justification
- [ ] Handling of missing data
- [ ] Outlier treatment
- [ ] Assumptions checked (normality, homoscedasticity, etc.)
- [ ] Multiple comparison correction method
- [ ] Full model specifications
- [ ] Effect sizes with confidence intervals
- [ ] Data and code availability statement

### 10.8.3 Validation Approaches

1. **Internal validation**: Cross-validation, bootstrap
2. **External validation**: Test on independent dataset
3. **Temporal validation**: Train on early data, test on later data
4. **Geographic validation**: Train on one site, test on others

---

## 10.9 Data Management and Reproducibility

### 10.9.1 Data Structure

**Tidy data principles**:
- Each variable forms a column
- Each observation forms a row
- Each type of observational unit forms a table

**Example CCA dataset structure**:
```
| person_id | date       | environment | signal_present | signal_dB | perception_score | content_reported |
|-----------|------------|-------------|-----------------|-----------|------------------|------------------|
| P001      | 2026-01-15 | home        | 1               | 45.2      | 3                | voices           |
| P001      | 2026-01-15 | work        | 0               | NA        | 0                | none             |
| P002      | 2026-01-15 | home        | 1               | 42.8      | 5                | music            |
```

### 10.9.2 Version Control and Documentation

**Use Git for**:
- Analysis scripts
- Data processing pipelines
- Manuscript text (Markdown/LaTeX)

**Documentation requirements**:
- README: Study overview, file structure
- CODEBOOK: Variable definitions, units, coding schemes
- CHANGELOG: Data versions and modifications
- ANALYSIS_LOG: Record of analytical decisions

### 10.9.3 Reproducible Workflows

**Tools**:
- **R Markdown / Jupyter Notebooks**: Integrate code, output, and narrative
- **Docker**: Containerize entire computational environment
- **Make / Snakemake**: Automate analysis pipelines

**Example R Markdown workflow**:
```r
---
title: "CCA Signal Analysis - Participant 001"
author: "Research Team"
date: "`r Sys.Date()`"
output: html_document
---

## Data Import
```{r}
data <- read_csv("data/participant_001.csv")
```

## Analysis
```{r}
model <- lmer(perception ~ signal_strength + (1 | date), data = data)
summary(model)
```

## Results
The signal effect was β = `r round(fixef(model)[2], 3)`, 
p `r ifelse(summary(model)$coefficients[2,5] < 0.001, "< 0.001", 
            paste("=", round(summary(model)$coefficients[2,5], 3)))`
```

---

## 10.10 Conclusion

This chapter has established a comprehensive statistical framework for CCA research, encompassing:

1. **Bayesian inference**: Uncertainty quantification and prior incorporation
2. **Machine learning**: Classification and prediction of CCA vs. primary hallucinations
3. **Time-series methods**: Detecting temporal patterns and causality
4. **Multilevel models**: Accounting for nested data structures
5. **Multiple testing**: Controlling false discoveries in exploratory research
6. **Power analysis**: Ensuring adequately powered studies
7. **Reproducibility**: Open science practices

These methods enable:
- **Sensitive detection** of subtle CCA effects
- **Robust inference** despite individual variability
- **Transparent reporting** following open science principles
- **Clinical translation** through validated classification tools

The next chapter applies these methods to real neuroimaging data, demonstrating their practical utility.

---

*Word count: ~4,800 words*  
*Status: Complete - First Draft*  
*Last updated: 2026-02-04*

---

## References (Selected)

1. Gelman, A., & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.

2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Springer.

3. Kruschke, J. K. (2014). *Doing Bayesian Data Analysis*. Academic Press.

4. Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.

5. Shumway, R. H., & Stoffer, D. S. (2017). *Time Series Analysis and Its Applications*. Springer.

6. Wickham, H. (2014). Tidy data. *Journal of Statistical Software*, 59(10), 1-23.

---

# END OF CHAPTER 10
