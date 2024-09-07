import pandas as pd

df = pd.read_stata('resources/k401.dta')
df_headers = df.columns  # ['prate', 'mrate', 'totemp', 'age', 'sole']
# prate (Participation Rate): % of employees eligible for a 401(k) plan who have an active account, whether or not they contributed to it in the current year.
# mrate (Match Rate): Estimate of how much the employer contributes to the employee’s 401(k), compared to what the employee contributes. Includes matching contributions, fixed amounts, etc. "Overall generosity" of the plan.
# totemp: Total firm employment.
# age: Plan age.
# sole: Binary where 1 means this is the firms only pension fund.
print(df.head(10))

# formula 22
# E(PRATE∣X)=β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))2+β5​AGE+β6​AGE2+β7​SOLE

# formula 23
# E(PRATE∣X)=G(β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))2+β5​AGE+β6​AGE2+β7​SOLE)

# - total employees = 20,000
# - On average, employees contribute 21% of salary
# - Employer contributes 7% of salary.
# - The 401k is not the sole pension plan for the employer.
# - Age of account = 12 years.
# - Don’t worry about IRS limits or other outside factors.
