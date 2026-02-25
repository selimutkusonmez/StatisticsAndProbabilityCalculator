# 📊 Comprehensive Statistical Calculator

A powerful and intuitive desktop application built with Python and PyQt6. Designed for engineers, data scientists, and students, this tool provides a robust suite of calculators for descriptive statistics, probability rules, distribution functions, and complex hypothesis testing.

Beyond simple calculations, the application features dynamic HTML-based formula rendering, showing users exactly how their data is being processed in real-time.

## ✨ Key Features

* **Vast Analytical Suite:** Covers everything from basic sample means to advanced One-Way ANOVA and Bayesian probability.
* **Dynamic Formula Display:** Mathematical formulas update instantly as you type, rendering complex fractions, square roots, and statistical variables interactively.
* **Dark & Light Mode Support:** Fully integrated theme toggling to ensure an optimal and comfortable viewing experience in any lighting condition.
* **Interactive Information Panels:** Context-aware side panels that explain the theoretical definitions and variable meanings for every selected test.
* **Bulletproof Error Handling:** Prevents crashes from division by zero, mismatched array lengths, and invalid data types.

---

## 🧮 Supported Operations

The application is divided into four main analytical modules:

### 1. Descriptive Statistics

Calculates core metrics to summarize and describe data sets.

* **Mean:** Population Mean, Sample Mean
* **Variance:** Population Variance, Sample Variance
* **Standard Deviation:** Population Standard Deviation, Sample Standard Deviation
* **Percentile:** Percentile calculation
* **Covariance:** Population Covariance, Sample Covariance
* **Correlation:** Pearson Correlation Coefficient

### 2. Probability Rules

Evaluates the likelihood of combined events.

* **Addition Rule:** Mutually Exclusive Events, Non-Mutually Exclusive Events
* **Multiplication Rule:** Independent Events, Dependent Events

### 3. Distribution Functions

Calculates probabilities using Probability Mass Functions (PMF), Probability Density Functions (PDF), and Cumulative Distribution Functions (CDF).

* **Bernoulli Distribution**
* **Binomial Distribution**
* **Poisson Distribution:** PMF, CDF
* **Normal Distribution:** PDF, CDF
* **Standard Normal Distribution**
* **Uniform Distribution:** PDF, CDF
* **Log-Normal Distribution:** PDF, CDF
* **Pareto Distribution:** PDF, CDF

### 4. Hypothesis Testing

Performs inferential statistics to draw conclusions about populations based on sample data.

* **Central Limit Theorem (CLT)**
* **Confidence Interval**
* **Margin of Error**
* **Z-Test**
* **t-Test:** Single Sample, Independent Samples, Paired Samples
* **Chi-Square Test**
* **One-Way ANOVA**
* **Bayes' Theorem**

---

## 🛠️ Built With

* **Language:** Python 3.x
* **GUI Framework:** PyQt6
* **Scientific Libraries:** `scipy.stats`, `math`, `statistics`
