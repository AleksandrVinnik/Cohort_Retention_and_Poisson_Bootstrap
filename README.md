# 📊 Cohort Retention & Poisson Bootstrap A/B Testing

## 📁 Repository Overview

This repository provides Python solutions for two important analytical tasks:

### 1. Cohort Retention Analysis
Calculate user retention rates over time with customizable cohort granularity (daily, weekly, or monthly). This allows you to track how different user groups behave and retain over specific time intervals, enabling deeper insights into user engagement patterns.

Sequence Diagram: Cohort Retention Analysis


```mermaid
sequenceDiagram
    autonumber
    participant J as Notebook
    participant R as retention.py
    participant D as Data Store
    participant V as visualisation.py
    
    J->>D: Load registration.csv
    activate D
    D-->>J: Return reg_data
    deactivate D
    
    J->>D: Load auth_data.csv
    activate D
    D-->>J: Return auth_data
    deactivate D
    
    J->>R: calculate_cohort_retention(reg_data, auth_data)
    activate R
    R->>R: Compute registration cohorts
    R->>R: Calculate day-n retention
    R-->>J: Return cohort_df
    deactivate R
    
    J->>V: plot_retention_curves(cohort_df)
    activate V
    V->>V: Configure plot style
    V->>V: Generate retention heatmap
    V->>V: Add annotations
    V-->>J: Output chart
    deactivate V
```

This workflow calculates **player retention rates** using **cohort analysis**.


#### 📥 Data Loading

- **Registration Data**:  
  `problem1-reg_data.csv` containing player signup timestamps

- **Authentication Data**:  
  `problem1-auth_data.csv` tracking player login activity

---

#### 📊 Retention Calculation

- Groups players into cohorts based on **registration date**
- Computes **day-by-day retention rates** from registration
- Supports both:
  - **Classic cohorts** (fixed registration windows)
  - **Rolling cohorts** (dynamic cohort windows)
- Supports **custom cohort frequency**:
  - **Daily**, **Weekly**, or **Monthly** cohorts
- Retention window is **fully configurable** for different periods

---

#### 📈 Visualization

- Generates **heatmap-style retention matrices**
- Produces **retention curve comparisons**
- Adds:
  - **Cohort size annotations**
  - **Trendlines**
- Applies **consistent styling** for **publication-ready** outputs

---

#### 🔧 Key Features

- Efficiently handles large datasets (**10M+ rows**)
- Flexible period handling: **day / week / month**
- **Memory-optimized** cohort processing


### 2. Poisson Bootstrap A/B Testing
Evaluate A/B test metrics — such as Average Revenue Per User (ARPU), Average Revenue Per Paying User (ARPPU), and Conversion Rate (CR) — using Poisson bootstrapping.  
Poisson bootstrap is an efficient variant of traditional bootstrapping that assigns random Poisson-distributed weights to each data point instead of resampling entire datasets. This approach:

- Enables fast, vectorized computations with minimal memory overhead  
- Facilitates parallel processing, making it scalable for large datasets  
- Provides robust confidence intervals and hypothesis tests without strong parametric assumptions

#### A/B Test Analysis Workflow using Poisson Bootstrap

```mermaid
sequenceDiagram
    autonumber
    participant J as Notebook
    participant B as bootstrap.py
    participant D as Data Store
    participant V as visualisation.py

    J->>D: Load A/B test data
    activate D
    D-->>J: Return ab_test_df
    deactivate D

    J->>B: poisson_bootstrap(ab_test_df, B=10000)
    activate B
    B->>B: Resample with Poisson weights
    B->>B: Compute ARPU/CR/ARPPU
    B->>B: Calculate differences
    B->>B: Determine confidence intervals
    B-->>J: Return results_df
    deactivate B

    J->>V: plot_bootstrap_dists(results_df)
    activate V
    V->>V: Generate KDE plots
    V->>V: Add confidence intervals
    V->>V: Mark null hypothesis
    V-->>J: Output comparison chart
    deactivate V
```



#### Description

This workflow analyzes **A/B test results** using **Poisson bootstrap resampling**.

---

#### 🧹 Data Preparation

- Requires experimental data with columns:
  - `user_id`
  - `revenue`
  - `testgroup`


---

#### 📊 Statistical Analysis

- Performs **Poisson resampling** (default: 10,000 iterations)
- Computes key metrics:
  - **ARPU** – Average Revenue Per User
  - **CR** – Conversion Rate
  - **ARPPU** – Average Revenue Per Paying User
- Calculates:
  - **Effect sizes**
  - **Confidence intervals (CIs)**


---

#### 📈 Visualization

- Generates **distribution plots** of metric differences
- Highlights:
  - **Confidence intervals**
  - **Null hypothesis values**
- Compares:
  - **Test vs. Control** distributions
- Adds:
  - **Statistical significance annotations**

---

#### 🔧 Key Features

- **Non-parametric method** (no assumptions about underlying distributions)
- Effectively handles **skewed revenue distributions**
- **Computationally efficient** implementation
- Supports **multiple comparison correction**
- Provides **comprehensive diagnostic outputs**


## This dependency graph illustrates the separation of concerns in our analytics pipeline:

```mermaid
graph LR
    A[Analysis Notebook] -->|Calls Functions| B[retention.py]
    A -->|Calls Functions| C[visualisation.py]
    A -->|Calls Functions| D[bootstrap.py]
    B -->|Reads| E[(Registration Data)]
    B -->|Reads| F[(Authentication Data)]
    B -->|Processes| G[Cohort Metrics]
    D -->|Analyzes| H[A/B Test Data]
    C -->|Visualizes| G
    C -->|Visualizes| H
    G -->|Input For| A
    H -->|Input For| A

    classDef notebook fill:#f9f7ff,stroke:#7e57c2,stroke-width:2px;
    classDef module fill:#e3f2fd,stroke:#2196f3,stroke-width:2px;
    classDef data fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef output fill:#fff8e1,stroke:#ffc107,stroke-width:2px;
    class A notebook;
    class B,C,D module;
    class E,F data;
    class G,H output;
```
### Analytics Pipeline Architecture

#### Diagram Description

This dependency graph illustrates the **separation of concerns** in our analytics pipeline:

- **Data Layer** (🟩 Green):  
  Raw data sources remain isolated.

- **Processing Layer** (🟦 Blue):  
  Specialized modules handle distinct tasks.

- **Orchestration Layer** (🟪 Purple):  
  Notebooks control the workflow sequence.

- **Output Layer** (🟨 Yellow):  
  Analysis-ready datasets are preserved.

#### Key Architectural Features

- ✅ **Unidirectional data flow** prevents circular dependencies  
- 🔄 **Stateless modules** ensure reproducible outputs  
- 🧪 **Input/Output isolation** enables pipeline testing  
- 📊 **Visualization decoupling** allows plot reuse across projects


---

## 🔢 1. Player Cohort Retention Analysis Function

**Retention** measures how many users return to the product after their first experience, helping teams understand user engagement and product stickiness.

**Cohort analysis** groups users based on their start date (e.g., registration date) and tracks their behavior (e.g., logins) over time. This highlights patterns and retention trends within specific user groups, allowing you to:

- Compare different user onboarding cohorts  
- Evaluate product changes by tracking newer vs. older cohorts  
- Identify when churn occurs and respond with tailored actions  

Implementation of cohort analysis allows teams to quantify retention using two core methods:

- **Classic Retention**: Users active in each period after their cohort start  
- **Rolling Retention**: Users who return at least once *after* a given period  

Cohort retention can be visualized in **daily, weekly, or monthly** granularity, and supports both **classic** (discrete period-based) and **rolling** (cumulative) retention calculations.

---

### 📊 Daily Rolling Cohort Retention Rate

![Daily Rolling Cohort Retention Rate - Line Plot](Images/Daily%20Rolling%20Cohort%20Retention%20Rate%20-%20Line%20Plot.png)

![Daily Rolling Cohort Retention Rate - Table](Images/Daily%20Rolling%20Cohort%20Retention%20Rate%20-%20Table.png)

---

### ⚙️ Pipeline Overview
```mermaid
graph TD
  A[Read reg_data.csv & auth_data.csv];
  A --> B[Convert timestamps to datetime];
  B --> C[Exploratory Data Analysis];
  C --> D[Check for duplicates & ranges];
  D --> E[Call rt.cohort_retention];
  E --> F[Monthly Classic Retention];
  E --> G[Weekly Classic Retention];
  E --> H[Daily Rolling Retention];
  F --> I[Visualize with viz.retention_plot];
  G --> J[Visualize with viz.retention_plot];
  H --> K[Visualize with viz.retention_plot];
```

---

### 🔁 Why It Matters

Implementing retention and cohort analysis allows product teams to:

- Benchmark performance of new player funnels  
- Understand when and why users churn  
- Test the impact of design or difficulty changes  
- Align product decisions with long-term engagement metrics  

> 🔍 **Retention** is not just about *"how many come back"* — it's about **who** comes back, **when**, and **why**.

---

### cohort_retention(reg_data, auth_data, start_date, end_date, cohort_type, number_of_periods, retention_type='classic')

#### ✅ Inputs

| Parameter          | Type       | Description                                             |
|--------------------|------------|---------------------------------------------------------|
| reg_data           | DataFrame  | User registration data with `uid` and `reg_ts` columns  |
| auth_data          | DataFrame  | Authentication data with `uid` and `auth_ts` columns    |
| start_date         | str        | Start date of cohorts (format: YYYY-MM-DD)              |
| end_date           | str        | End date of cohorts (format: YYYY-MM-DD)                |
| cohort_type        | str        | One of: day, week, month, quarter, year                 |
| number_of_periods  | int        | Number of periods to track retention after registration |
| retention_type     | str        | 'classic' or 'rolling' retention calculation            |


#### 📤 Output

Returns a `pandas.DataFrame` where:

- Each row is a cohort (start_date formatted).
- Columns include:
  - `'Cohort'`: Cohort name
  - `'Users'`: Number of users
  - `'0'`: Initial cohort size
  - `'1'`, `'2'`, ...: Retention rates for each period
- Last row: `"All Users"` aggregated retention across cohorts

---

#### 🧠 Notes

Metadata is stored as attributes in the result:

- `result_df.start_date`
- `result_df.end_date`
- `result_df.cohort_type`
- `result_df.retention_type`

---

## 🧪 2. Poisson Bootstrap A/B Testing

Bootstrapping is a robust statistical method used to estimate the sampling distribution of a statistic by repeatedly resampling the observed data with replacement. It is especially valuable when the theoretical distribution is unknown or when calculating analytical confidence intervals is difficult or impractical.

![Poisson bootstrap result analysis - ARPU](Images/Poisson%20bootstrap%20result%20analysis%20-%20ARPU.png)

---

### 🔁 Why Bootstrapping?

In A/B testing, bootstrapping allows us to simulate thousands of potential outcomes of the experiment by creating many pseudo-samples from the observed data. This helps to:

- Estimate confidence intervals for KPIs (like **ARPU**, **ARPPU**, **CR**)
- Perform hypothesis testing without strict assumptions (e.g., **normality**)
- Improve robustness, especially with **skewed revenue distributions** (whales vs. minnows)

---

### 🧮 Poisson Bootstrap in Particular

Poisson bootstrapping is a **memory- and compute-efficient** variant of traditional bootstrap. Instead of explicitly resampling entire datasets, it assigns **Poisson(λ = 1)** random weights to each data point. This makes it ideal for:

- **Vectorized operations**: Efficient row-wise multiplication using NumPy arrays  
- **Parallel computing**: Each bootstrap iteration is independent, allowing distribution across CPU cores or compute nodes  
- **Low memory usage**: Avoids large temporary datasets common in classic resampling  

This method is especially helpful for **large-scale A/B tests** with millions of users and revenue entries.

---

### ⚙️ Pipeline Overview
```mermaid
graph TD
  A[Download CSV from Yandex];
  A --> B[Read ab_test_data];
  B --> C[Initial EDA head, info, unique values];
  C --> D[Check duplicate user_ids per group];
  D --> E[Plot group sizes];
  E --> F[Check for overlapping users];
  F --> G[Revenue Distribution Plot];
  G --> H[Annotate Whales, Dolphins, Minnows];
  H --> I[Revenue Segmentation: Freeloaders → Whales];
  I --> J[Further statistical testing / conclusions];

```

---

### `poisson_bootstrap(ab_test_data, B)`

#### ✅ Inputs

| Parameter    | Type       | Description                   |
|--------------|------------|-------------------------------|
| ab_test_data | DataFrame  | Must contain:                 |
|              |            | - `testgroup`: 'a' or 'b'     |
|              |            | - `revenue`: numeric revenue  |
| B            | int        | Number of bootstrap iterations|

#### 📤 Output

A DataFrame with B rows, and the following columns:

| Column                 | Description                           |
|------------------------|---------------------------------------|
| revenue_a/b            | Total revenue per group               |
| count_users_a/b        | Number of users in group              |
| count_paying_users_a/b | Number of paying users                |
| ARPU_difference        | Avg. Revenue Per User (B - A)         |
| ARPPU_difference       | Avg. Revenue Per Paying User (B - A)  |
| CR_difference          | Conversion Rate (B - A)               |

---

### `bootstrap_result_check(bootstrap_data, alpha)`

#### ✅ Inputs

| Parameter       | Type   | Description                                |
|-----------------|--------|--------------------------------------------|
| bootstrap_data  | Series | Metric difference across bootstrap samples |
| alpha           | float  | Significance level (e.g. 0.05)             |

#### 📤 Output

Prints:

- `Sample mean`  
- `Confidence interval`  
- `Decision about rejecting the null hypothesis`

---

## 3. Metrics for Evaluating Themed Event Performance in Games

### 3.1. Metrics to Evaluate Event Results
- Participation rate
- Completion rate (players finishing the event)
- Average time to complete
- Average rewards earned
- Retention after event (did players come back after the event?)
- Revenue uplift during event

### 3.2. Impact of Increased Difficulty (Level Regression)
If event mechanics are made more challenging by regressing levels on failure:

- Metrics should include attempt counts per player to track difficulty.
- Failure rates per level.
- Drop-off points (levels where players quit).
- Time spent per level (indicates difficulty).
- Comparison of completion rate before and after difficulty change.
- Player frustration or satisfaction metrics if available (e.g., surveys).

---

### Metrics Flowchart
This flow visualizes how to evaluate event performance in the game, adjusting metrics based on event complexity (e.g., level regression after failure).

```mermaid
graph TD
  A[Identify Event Type];
  A --> B[Define Goals - Complete Levels, Rewards];
  B --> C[Evaluate Metrics];
  C --> D[Standard Metrics];
  D --> D1[Participation Rate];
  D --> D2[Completion Rate];
  D --> D3[Time Spent];
  D --> D4[Number of Attempts per Player];
  D --> D5[Items Collected / Rewards Unlocked];
  A --> I{Was event made harder?};
  I --> J[Yes: Add metrics for regression events];
  J --> J1[Avg. Level Lost After Failure];
  J --> J2[Drop-off Rate Increase];
  J --> J3[Frustration vs. Retention Analysis];
  I --> N[No: Continue with standard metrics];
```

---

## 📓 Full Jupyter Notebook

For a comprehensive, step-by-step walkthrough of the cohort retention analysis and Poisson bootstrap A/B testing, please refer to the full Jupyter notebook:

[Cohort_Retention_and_Poisson_Bootstrap.ipynb](./Cohort_Retention_and_Poisson_Bootstrap.ipynb)

This notebook includes detailed explanations, code implementation, visualizations, and results to help you understand and reproduce the analyses.
