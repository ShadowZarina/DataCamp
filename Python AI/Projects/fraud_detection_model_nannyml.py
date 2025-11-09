'''
DATA:
They have provided you with a reference(test data) and analysis set(production data). A summary and preview are provided below.

reference.csv and analysis.csv

'timestamp'	->  Date of the transaction.
'time_since_login_min'	->	Time since the user logged in to the app.
'transaction_amount'	->	The amount of Pounds(£) that users sent to another account.
'transaction_type'	->	Transaction type:
CASH-OUT - Withdrawing money from an account.
PAYMENT - Transaction where a payment is made to a third party.
CASH-IN - This is the opposite of a cash-out. It involves depositing money into an account.
TRANSFER - Transaction which involves moving funds from one account to another.

'is_first_transaction'	->	A binary indicator denoting if the transaction is the user's first (1 for the first transaction, 0 otherwise).
'user_tenure_months'	->	The duration in months since the user's account was created or since they became a member.
'is_fraud'	->	A binary label indicating whether the transaction is fraudulent (1 for fraud, 0 otherwise).
'predicted_fraud_proba'	->	The probability assigned by a detection model indicates the likelihood of a fraudulent transaction.
'predicted_fraud'	->	The predicted classification label is calculated based on predicted fraud probability by the detection model 
                      (1 for predicted fraud, 0 otherwise).

INSTRUCTIONS:
Use the reference.csv and analysis.csv datasets to monitor a fraud detection model and address the following questions:

- Identify the months in which the estimated(expected) and realized(actual) accuracy of the model triggers alerts. 
  Put these months in a list named months_with_performance_alerts, using lowercase and separating the month and year with an underscore. 
  For example: months_with_performance_alerts = ["january_2018", "march_2018"].

- Determine the feature that shows the most drift between the reference and analysis sets, thereby impacting the drop in realized accuracy the most. 
  Historically, Poundbank's data science team used the Kolmogorov-Smirnov and Chi-square methods to detect this drift. Store the name of this feature in a 
  variable named highest_correlation_feature.

- Look for instances where the monthly average transaction amount differs from the usual, causing an alert. 
  Save this amount in a variable named alert_avg_transaction_amount, ensuring it has a minimum of one decimal place in the results.
'''

# Import required libraries
import pandas as pd
import nannyml as nml
nml.disable_usage_logging()

reference = pd.read_csv("reference.csv")
analysis = pd.read_csv("analysis.csv")

## Identifing the months when both the estimated and realized ROC AUC of the model have alerts. Store the names of these months as lowercase strings in a list named months_with_performance_alerts. 

# Get the estimated performance using CBPE algorithm
cbpe = nml.CBPE(
    timestamp_column_name="timestamp",
    y_true="is_fraud",
    y_pred="predicted_fraud",
    y_pred_proba="predicted_fraud_proba",
    problem_type="classification_binary",
    metrics=["accuracy"],
    chunk_period="m"
)

cbpe.fit(reference)
est_results = cbpe.estimate(analysis)

# Calculate the realized performance
calculator = nml.PerformanceCalculator(
    y_true="is_fraud",
    y_pred="predicted_fraud",
    y_pred_proba="predicted_fraud_proba",
    timestamp_column_name="timestamp",
    metrics=["accuracy"],
    chunk_period="m",
    problem_type="classification_binary",
)
calculator = calculator.fit(reference)
calc_results = calculator.calculate(analysis)

# Compare the results and find the months with alerts
est_results.compare(calc_results).plot().show()
months_with_performance_alerts = ["april_2019", "may_2019", "june_2019"]
print(months_with_performance_alerts)

## Determining which alerting feature has the strongest correlation with the model’s realized performance. Store the name of this feature in a variable named highest_correlation_feature. 

features = ["time_since_login_min", "transaction_amount",
            "transaction_type", "is_first_transaction", 
            "user_tenure_months"]

# Calculate the univariate drift results
udc = nml.UnivariateDriftCalculator(
    timestamp_column_name="timestamp",
    column_names=features,
    chunk_period="m",
    continuous_methods=["kolmogorov_smirnov"],
    categorical_methods=["chi2"]
)

udc.fit(reference)
udc_results = udc.calculate(analysis)

# Use the correlation ranker
ranker = nml.CorrelationRanker()
ranker.fit(
    calc_results.filter(period="reference"))

correlation_ranked_features = ranker.rank(udc_results, calc_results)

# Find the highest correlating feature
display(correlation_ranked_features)
highest_correlation_feature = "time_since_login_min"
print(highest_correlation_feature)

## Use the summary average statistics calculator to find out what were the monthly average transactions amounts, and if there's any alert. Record this value in a variable called alert_avg_transaction_amount.

# Calculate average monthly transactions
calc = nml.SummaryStatsAvgCalculator(
    column_names=["transaction_amount"],
    chunk_period="m",
    timestamp_column_name="timestamp",
)

calc.fit(reference)
stats_avg_results = calc.calculate(analysis)

# Find the month
stats_avg_results.plot().show()
alert_avg_transaction_amount = 3069.8184
print(alert_avg_transaction_amount)
