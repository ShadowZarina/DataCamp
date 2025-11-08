import pandas as pd
import numpy as np

# Read csv
df = pd.read_csv("bank_marketing.csv")

# Create 3 tables
client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]]
campaign = df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "month", "day"]]
economics = df[["client_id", "cons_price_idx", "euribor_three_months"]]

## Editing client dataset

# Clean education column
client["education"] = client["education"].str.replace(".","_")
# Fix: Use .replace() instead of .str.replace() to replace 'unknown' with np.NaN
client["education"] = client["education"].replace("unknown", np.NaN)

# Clean job column
client["job"] = client["job"].str.replace(".","_")

# Clean and convert client columns to bool data type
for col in ["credit_default", "mortgage"]:
    client[col] = client[col].map({"yes": 1, "no": 0, "unknown": 0})
    client[col] = client[col].astype(bool)

## Editing the campaign dataset
# Change campaign_outcome to binary values
campaign["campaign_outcome"] = campaign["campaign_outcome"].map({"yes": 1, "no": 0})

# Convert previous_outcome to binary values
campaign["previous_outcome"] = campaign["previous_outcome"].map({"success": 1, "failure": 0, "nonexistent": 0})

# Add year column to campaign
campaign["year"] = "2022"

# Convert data type of day to string
campaign["day"] = campaign["day"].astype(str)

# Add last_contact_date column to campaign
campaign["last_contact_date"] = campaign["year"] + "-" + campaign["month"] + "-" + campaign["day"]

# Convert last_contact_date to datetime
campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"], format="%Y-%b-%d")

# Clean and convert outcome columns to bool
for col in ["campaign_outcome", "previous_outcome"]:
    campaign[col] = campaign[col].astype(bool)

# Drop month, day, year columns
campaign.drop(columns=["month", "day", "year"], inplace=True)

# Save tables to respective csv files
client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False)
economics.to_csv("economics.csv", index=False)


# Sample Code to Print Tables
for col in ["credit_default", "mortgage", "previous_outcome", "campaign_outcome"]:
    print(col)
    print("--------------")
    print(df[col].value_counts())

''' 
Sample Output:

credit_default
--------------
no         32588
unknown     8597
yes            3
Name: credit_default, dtype: int64
mortgage
--------------
yes        21576
no         18622
unknown      990
Name: mortgage, dtype: int64
previous_outcome
--------------
nonexistent    35563
failure         4252
success         1373
Name: previous_outcome, dtype: int64
campaign_outcome
--------------
no     36548
yes     4640
Name: campaign_outcome, dtype: int64

'''
