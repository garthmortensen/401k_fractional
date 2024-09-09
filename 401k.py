# 401k_fractional coding challenge

# logging
import logging
import time

# stats functionality
import pandas as pd
import numpy as np
import statsmodels.api as sm
import yaml

# TODO: carve logging out of this script
timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
handlers = [  # write stdout and errout
    logging.StreamHandler(),  # stream to console
    logging.FileHandler(
        filename=f"./logs/{timestamp}_401k.log", mode="w"
    ),  # write to file
]

# 20240202_154449 INFO practice.py:56 log_meta| pid:    10629
log_format = (
    "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s| %(message)s"
)
logging.basicConfig(
    level=logging.INFO, format=log_format, datefmt="%Y%m%d_%H%M%S", handlers=handlers
)

ascii_banner = """\n
 /$$   /$$  /$$$$$$    /$$   /$$
| $$  | $$ /$$$_  $$ /$$$$  | $$
| $$  | $$| $$$$\ $$|_  $$  | $$   /gm
| $$$$$$$$| $$ $$ $$  | $$  | $$  /$$/
|_____  $$| $$\ $$$$  | $$  | $$$$$$/
      | $$| $$ \ $$$  | $$  | $$_  $$
      | $$|  $$$$$$/ /$$$$$$| $$ \  $$
      |__/ \______/ |______/|__/  \__/\n
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PARTICIPATION RATE: % of employees eligible for a 401(k) plan who have an active account, whether or not they contributed to it in the current year.
Match Rate: Estimate of how much the employer contributes to the employee’s 401(k), compared to what the employee contributes. Includes matching contributions, fixed amounts, etc. "Overall generosity" of the plan.
emp: Total firm employment.
age: Plan age.
sole: Binary where 1 means this is the firms only pension fund.
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
"""
logging.info(ascii_banner)

# ["prate", "mrate", "totemp", "age", "sole"]
df = pd.read_stata("inputs/k401.dta")
df.rename(columns={"totemp": "emp"}, inplace=True)

# add additional data transformations needed for equations
df["log_emp"] = np.log(df["emp"])
# squared terms capture non-linear relationships.
# they allow relationships to curved or change direction.
df["log_emp2"] = np.log(df["log_emp"]) ** 2
df["age2"] = df["age"] ** 2

# reorder columns to align with equations for easier comparisons
column_reorder = ["prate", "mrate", "log_emp", "log_emp2", "age", "age2", "sole"]
df = df[column_reorder]

# dependent
y = df["prate"]
# independents
x = df[
    ["mrate", "log_emp", "log_emp2", "age", "age2", "sole"]
]  # [[]] for df, [] for series
x = sm.add_constant(x)  # β1
logging.info(f"x dimensions: {x.shape}")

# equation 22
# E(PRATE∣X)=β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE
# https://www.geeksforgeeks.org/ordinary-least-squares-ols-using-statsmodels/
eq_22 = sm.OLS(y, x)
eq_22_fitted = eq_22.fit()

# TODO: functionalize this
# r squared
r_squared = eq_22_fitted.rsquared
logging.info(f"r_squared: {r_squared}")

# loop through each param in equation, logging.info coef, statistical significance
for each_x in x:
    # Get coefficient and p-value for the variable
    coef = eq_22_fitted.params[each_x]
    pvalue = eq_22_fitted.pvalues[each_x]

    if pvalue < 0.001:
        significance = "statistically significant (P < 0.001)."
    else:
        significance = f"not statistically significant (P = {pvalue:.4f})."

    logging.info(
        f"A 1% increase in this {each_x} results in a {coef:.4f} change in the participation rate."
    )
    logging.info(f"{each_x} is {significance}")

# write results
# FIXME: table output does not match Table III
with open("output_tables/eq_22_summary.html", "w") as f:
    f.write(eq_22_fitted.summary().as_html())

# equation 23
# E(PRATE∣X)=G(β1​+β2​MRATE+β3​log(EMP)+β4​(log(EMP))^2+β5​AGE+β6​AGE^2+β7​SOLE)
eq_23 = sm.Logit(y, x)  # results [0, 1]
eq_23_fitted = eq_23.fit()

# TODO: functionalize this
# r squared
r_squared = eq_22_fitted.rsquared
logging.info(f"r_squared: {r_squared}")

# loop through each param in equation, logging.info coef, statistical significance
for each_x in x:
    # Get coefficient and p-value for the variable
    coef = eq_23_fitted.params[each_x]
    pvalue = eq_23_fitted.pvalues[each_x]

    if pvalue < 0.001:
        significance = "statistically significant (P < 0.001)."
    else:
        significance = f"not statistically significant (P = {pvalue:.4f})."

    logging.info(
        f"A 1% increase in this {each_x} results in a {coef:.4f} change in the participation rate."
    )
    logging.info(f"{each_x} is {significance}")

# write results
# FIXME: table output does not match Table III
with open("output_tables/eq_23_summary.html", "w") as f:
    f.write(eq_23_fitted.summary().as_html())

# predict
# https://stackoverflow.com/questions/13218461/predicting-values-using-an-ols-model-with-statsmodels

# yaml > json
with open("./inputs/assumed_df.yaml", "r") as file:
    assumed_df = yaml.safe_load(file)

# define variables imported from yaml
mrate = assumed_df["employer"]["mrate"]
emp = assumed_df["employees"]["total"]
age = assumed_df["account"]["age"]
sole = assumed_df["plan"]["sole"]

# transformations
log_emp = np.log(emp)
log_emp2 = log_emp ** 2
age2 = age ** 2

# build dictionary from imported values
data = {
    "mrate": [mrate],
    "log_emp": [log_emp],
    "log_emp2": [log_emp2],
    "age": [age],
    "age2": [age2],
    "sole": [sole],
}
assumed_df = pd.DataFrame(data)
assumed_df["const"] = 1  # β1
model_columns = ["const", "mrate", "log_emp", "log_emp2", "age", "age2", "sole"]
assumed_df = assumed_df[model_columns]

logging.info(f"assumed_df dimensions: {assumed_df.shape}")

# predict
eq_22_pred = eq_22_fitted.predict(assumed_df)
logging.info(f"eq_22_pred prate: {eq_22_pred}")
eq_23_pred = eq_23_fitted.predict(assumed_df)
logging.info(f"eq_23_pred prate: {eq_23_pred}")

# TODO: functionalize the code
# TODO: Add unit testing
# TODO: Replace filesystem with db via sqlalchemy
# TODO: Add API via flask
# TODO: Output a graph of the OLS line, observations
