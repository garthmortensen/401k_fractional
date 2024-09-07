# 401k_fractional coding challenge

## Intro

Replicate the Quasi-Maximum Likelihood Estimation (QMLE) models from *Papke and Wooldridge (1996)*, Section 4, equations (22) and (23), using `k401.dta`. This involves reproducing the results in Table III and analyzing the relationship between the participation rate and other 401k variables.

## Overview

### Dataset: `k401.dta`

|   prate   |   mrate   |  totemp  |  age  |  sole  |
|-----------|-----------|----------|-------|--------|
| 0.658784  | 0.580822  |  353.0   |   7   |    0   |
| 0.843350  | 0.218458  | 4130.0   |  22   |    0   |
| 1.000000  | 0.767652  |  177.0   |  21   |    1   |
| 0.941003  | 0.365554  | 2309.0   |  11   |    0   |
| 0.830149  | 0.407965  | 2309.0   |   7   |    0   |
| 1.000000  | 1.174729  |  452.0   |  34   |    1   |

### Variables Explained

- **`participation_rate (prate)`**: % of employees eligible for a 401(k) plan who have an active account, whether or not they contributed to it in the current year.
- **`match_rate (mrate)`**: Estimate of how much the employer contributes to the employee’s 401k, vs. what the employee contributes.
- **`totemp`**: Total firm employees.
- **`age`**: The age of 401k plan.
- **`sole_plan`**: Binary where 1 means this is the firm's only pension fund.


### Equations

22

`E(part_rate∣x) = β1 + β2​match_rate + β3log(emp) + β4log(EMP)^2 + β5age + β6age^2 + β7​sole_plan`

23

`E(part_rate∣x) = G(β1 + β2match_rate + β3log(emp) + β4log(emp)^2 + β5age + β6age^2 + β7​sole_plan)`

## Analysis

**Assumptions:** 
- total employees = 20,000
- On average, employees contribute 21% of salary to 401k
- Employer contributes 7% of salary.
- The 401k is not the only pension plan.
- Age of account = 12 years.
- Ignore other factors.

1. How do you think predictions from (22) and (23) will match with the employer's participation rate?

2. Which model seems more reasonable and why?

## Deliverables

Submit a .zip archive of the following:
1. The code.
2. Replicated Table III output (.pdf, .docx, .html).
3. 2-3 paragraphs summarizing your analysis aimed at a non-technical policy maker audience (.pdf, .docx, .html).

## Time

=< 8 hours. If more time, how to improve?

## Links

[Econometric Methods for Fractional Response Variables with an Application to 401(K) Plan Participation Rates](https://econpapers.repec.org/article/jaejapmet/v_3a11_3ay_3a1996_3ai_3a6_3ap_3a619-32.htm).

[Data description](http://qed.econ.queensu.ca/jae/1996-v11.6/papke-wooldridge/readme.pw.txt).

### Table 3: Replicate this

| Variable     | (1) OLS     | (2) QMLE    | (3) OLS     | (4) QMLE    |
|--------------|-------------|-------------|-------------|-------------|
| **MRATE**    | 0.034       | 0.542       | 0.143       | 1.665       |
|              | (0.003)     | (0.045)     | (0.008)     | (0.089)     |
|              | [0.003]     | [0.079]     | [0.008]     | [0.104]     |
| **MRATE²**   | -           | -           | -0.029      | -0.332      |
|              |             |             | (0.002)     | (0.021)     |
|              |             |             | [0.002]     | [0.026]     |
| **log(EMP)** | -0.101      | -1.038      | -0.099      | -1.030      |
|              | (0.012)     | (0.121)     | (0.012)     | (0.112)     |
|              | [0.012]     | [0.110]     | [0.012]     | [0.110]     |
| **log(EMP)²**| 0.0051      | 0.0540      | 0.0050      | 0.0536      |
|              | (0.0008)    | (0.0078)    | (0.0008)    | (0.0072)    |
|              | [0.0008]    | [0.0071]    | [0.0008]    | [0.0071]    |
| **AGE**      | 0.0064      | 0.0621      | 0.0056      | 0.0548      |
|              | (0.0008)    | (0.0089)    | (0.0008)    | (0.0082)    |
|              | [0.0007]    | [0.0078]    | [0.0007]    | [0.0077]    |
| **AGE²**     | -0.00008    | -0.00071    | -0.00007    | -0.00063    |
|              | (0.00002)   | (0.00021)   | (0.00002)   | (0.00019)   |
|              | [0.00002]   | [0.00018]   | [0.00001]   | [0.00018]   |
| **SOLE**     | 0.0140      | 0.1190      | 0.0066      | 0.0642      |
|              | (0.0050)    | (0.0510)    | (0.0049)    | (0.0471)    |
|              | [0.0052]    | [0.0503]    | [0.0051]    | [0.0498]    |
| **ONE**      | 1.213       | 5.429       | 1.170       | 5.105       |
|              | (0.045)     | (0.467)     | (0.044)     | (0.431)     |
|              | [0.044]     | [0.422]     | [0.042]     | [0.416]     |
| **Observations** | 4734    | 4734        | 4734        | 4734        |
| **R-squared**| 0.144       | 0.168       | 0.182       | 0.197       |
