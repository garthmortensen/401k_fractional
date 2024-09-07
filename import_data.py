import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_stata("resources/k401.dta")
df_headers = df.columns  # ["prate", "mrate", "totemp", "age", "sole"]
df.rename(columns={"totemp": "emp"}, inplace=True)
# Participation Rate: % of employees eligible for a 401(k) plan who have an active account, whether or not they contributed to it in the current year.
# Match Rate: Estimate of how much the employer contributes to the employee’s 401(k), compared to what the employee contributes. Includes matching contributions, fixed amounts, etc. "Overall generosity" of the plan.
# emp: Total firm employment.
# age: Plan age.
# sole: Binary where 1 means this is the firms only pension fund.

# given equation, add additional data transformation columns
df["log_emp"] = np.log(df["emp"])
df["log_emp2"] = np.log(df["log_emp"]) ** 2
df["age2"] = df["age"] ** 2

# reorder columns to align with equation for easier mental processing
column_reorder = ["prate", "mrate", "log_emp", "log_emp2", "age", "age2", "sole"]
df = df[column_reorder]
print(df.head(5))

# dependent
y = df["prate"]
# independent
x = df[["mrate", "log_emp", "log_emp2", "age", "age2", "sole"]]  # [[]] for df, [] for series
x = sm.add_constant(x)  # adds intercept term (β1)

# formula 22
# E(PRATE∣X)=β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE
# https://www.geeksforgeeks.org/ordinary-least-squares-ols-using-statsmodels/
eq_22 = sm.OLS(y, x)
eq_22_fitted = eq_22.fit()
print(eq_22_fitted.summary())

# formula 23
# E(PRATE∣X)=G(β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE)
eq_23 = sm.Logit(y, x)  # results [0, 1]
eq_23_fitted = eq_23.fit()
print(eq_23_fitted.summary())
# ~1.5 hours?

# TODO: what next...plug these values into equation and check results?
# - total employees = 20,000
# - On average, employees contribute 21% of salary
# - Employer contributes 7% of salary.
# - The 401k is not the sole pension plan for the employer.
# - Age of account = 12 years.
# - Don’t worry about IRS limits or other outside factors.
