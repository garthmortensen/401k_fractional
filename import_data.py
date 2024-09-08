# 401k_fractional coding challenge

ascii_banner = """
 /$$   /$$  /$$$$$$    /$$   /$$
| $$  | $$ /$$$_  $$ /$$$$  | $$
| $$  | $$| $$$$\ $$|_  $$  | $$   /gm
| $$$$$$$$| $$ $$ $$  | $$  | $$  /$$/
|_____  $$| $$\ $$$$  | $$  | $$$$$$/
      | $$| $$ \ $$$  | $$  | $$_  $$
      | $$|  $$$$$$/ /$$$$$$| $$ \  $$
      |__/ \______/ |______/|__/  \__/"""
print(ascii_banner)

import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_stata("resources/k401.dta")
df_headers = df.columns  # ["prate", "mrate", "totemp", "age", "sole"]
df.rename(columns={"totemp": "emp"}, inplace=True)
# PARTICIPATION RATE: % of employees eligible for a 401(k) plan who have an active account, whether or not they contributed to it in the current year.
# Match Rate: Estimate of how much the employer contributes to the employee’s 401(k), compared to what the employee contributes. Includes matching contributions, fixed amounts, etc. "Overall generosity" of the plan.
# emp: Total firm employment.
# age: Plan age.
# sole: Binary where 1 means this is the firms only pension fund.

# add additional data transformations needed for equations
df["log_emp"] = np.log(df["emp"])
df["log_emp2"] = np.log(df["log_emp"]) ** 2
df["age2"] = df["age"] ** 2

# reorder columns to align with equations for easier comparisons
column_reorder = ["prate", "mrate", "log_emp", "log_emp2", "age", "age2", "sole"]
df = df[column_reorder]

# dependent
y = df["prate"]
# independents
x = df[["mrate", "log_emp", "log_emp2", "age", "age2", "sole"]]  # [[]] for df, [] for series
x = sm.add_constant(x)  # β1
print(f"x dimensions: {x.shape}")

# equation 22
# E(PRATE∣X)=β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE
# https://www.geeksforgeeks.org/ordinary-least-squares-ols-using-statsmodels/
eq_22 = sm.OLS(y, x)
eq_22_fitted = eq_22.fit()

# write results
with open("results/eq_22_summary.html", "w") as f:
    f.write(eq_22_fitted.summary().as_html())
# TODO: Interpret significant variables.

# equation 23
# E(PRATE∣X)=G(β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE)
eq_23 = sm.Logit(y, x)  # results [0, 1]
eq_23_fitted = eq_23.fit()

# write results
with open("results/eq_23_summary.html", "w") as f:
    f.write(eq_23_fitted.summary().as_html())
# TODO: Interpret significant variables.

# predict
# https://stackoverflow.com/questions/13218461/predicting-values-using-an-ols-model-with-statsmodels

# prep new data
assumed_df = pd.DataFrame({
    # - Employer contributes 7% of salary.
    "mrate": [0.07],
    # - total employees = 20,000
    "log_emp": [np.log(20000)],
    "log_emp2": [np.log(np.log(20000)) ** 2],
    # - Age of account = 12 years.
    "age": [12],
    "age2": [12 ** 2],
    # - The 401k is not the sole pension plan for the employer.
    "sole": [0],
})
# assumed_df = sm.add_constant(assumed_df)  # FIXME: Not working!
assumed_df['const'] = 1  # β1

print(f"assumed_df dimensions: {assumed_df.shape}")

# TODO: whats this for?
# - On average, employees contribute 21% of salary. Is this participation rate?

# predict
eq_22_pred = eq_22_fitted.predict(assumed_df)
print(f"eq_22_pred prate: {eq_22_pred}")
eq_23_pred = eq_23_fitted.predict(assumed_df)
print(f"eq_23_pred prate: {eq_23_pred}")

