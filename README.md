# 📊 Cohort Retention & A/B Testing Analysis Toolkit

This repository contains Python functions for:

**Cohort Retention Analysis** — Calculate user retention rates over time.
**Poisson Bootstrap A/B Testing** — Evaluate A/B test metrics (ARPU, ARPPU, CR) using Poisson bootstrapping.

## 📁 Contents

cohort_retention(...): Computes user retention by cohort (daily, weekly, etc.).
poisson_bootstrap(...): Performs Poisson bootstrap for A/B testing metrics.
bootstrap_result_check(...): Evaluates bootstrap output for statistical significance.


## 🔢 1. Player Cohort Retention Analysis Function
```mermaid
graph TD
  A[Start Assignment 1] --> B[Read reg_data.csv & auth_data.csv]
  B --> C[Convert timestamps to datetime];
  C --> D[Exploratory Data Analysis];
  D --> E[Check for duplicates & ranges];
  E --> F[Call rt.cohort_retention];
  F --> G[Monthly Classic Retention];
  F --> H[Weekly Classic Retention];
  F --> I[Daily Rolling Retention];
  G --> J[Visualize with viz.retention_plot];
  H --> K[Visualize with viz.retention_plot];
  I --> L[Visualize with viz.retention_plot];
```
cohort_retention(reg_data, auth_data, start_date, end_date, cohort_type, number_of_periods, retention_type='classic')

### ✅ Inputs
Parameter	Type	Description
reg_data	DataFrame	User registration data with uid and reg_ts columns
auth_data	DataFrame	Authentication data with uid and auth_ts columns
start_date	str	Start date of cohorts (format: YYYY-MM-DD)
end_date	str	End date of cohorts (format: YYYY-MM-DD)
cohort_type	str	One of: day, week, month, quarter, year
number_of_periods	int	Number of periods to track retention after registration
retention_type	str	'classic' or 'rolling' retention calculation

### 📤 Output

Returns a pandas.DataFrame where:

Each row is a cohort (start_date formatted).
Columns include:
'Cohort': Cohort name
'Users': Number of users
'0': Initial cohort size
'1', '2', ...: Retention rates for each period
Last row: "All Users" aggregated retention across cohorts

### 🧠 Notes
Metadata is stored as attributes in the result:
result_df.start_date
result_df.end_date
result_df.cohort_type
result_df.retention_type


## 🧪 2. Poisson Bootstrap A/B Testing

```mermaid
graph TD
  A[Start Assignment 2] --> B[Download CSV from Yandex];
  B --> C[Read ab_test_data];
  C --> D[Initial EDA head, info, unique values];
  D --> E[Check duplicate user_ids per group];
  E --> F[Plot group sizes];
  F --> G[Check for overlapping users];
  G --> H[Revenue Distribution Plot];
  H --> I[Annotate Whales, Dolphins, Minnows];
  I --> J[Revenue Segmentation: Freeloaders → Whales];
  J --> K[Further statistical testing / conclusions];
```

poisson_bootstrap(ab_test_data, B)

### ✅ Inputs
Parameter	Type	Description
ab_test_data	DataFrame	Must contain:
testgroup: 'a' or 'b'
revenue: numeric revenue value |
| B | int | Number of bootstrap iterations |

### 📤 Output

A DataFrame with B rows, and the following columns:

Column	Description
revenue_a/b	Total revenue per group
count_users_a/b	Number of users in group
count_paying_users_a/b	Number of paying users
ARPU_difference	Avg. Revenue Per User (B - A)
ARPPU_difference	Avg. Revenue Per Paying User (B - A)
CR_difference	Conversion Rate (B - A)

## 📉 3. Hypothesis Testing

This flow visualizes how to evaluate event performance in the game, adjusting metrics based on event complexity (e.g., level regression after failure).

```mermaid
graph TD
  A[Start Assignment 3] --> B[Identify Event Type];
  B --> C[Define Goals - Complete Levels, Rewards];
  C --> D[Evaluate Metrics];
  D --> E[Participation Rate];
  D --> F[Completion Rate];
  D --> G[Time Spent];
  D --> H[Number of Attempts per Player];
  D --> I[Items Collected / Rewards Unlocked];
  B --> J{Was event made harder?};
  J --> K[Yes: Add metrics for Regression Events];
  K --> L[Avg. Level Lost After Failure];
  K --> M[Drop-off Rate Increase];
  K --> N[Frustration vs. Retention Analysis];
  J --> O[No: Continue with standard metrics];
```

bootstrap_result_check(bootstrap_data, alpha)
### ✅ Inputs

Parameter	Type	Description
bootstrap_data	Series	Metric difference across bootstrap samples
alpha	float	Significance level (e.g. 0.05)

### 📤 Output

Prints:

Sample mean
Confidence interval
Decision about rejecting the null hypothesis