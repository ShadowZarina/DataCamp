import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def prepare_smartphone_data(file_path):
    """
    To prepare the smartphone data for visualization, a number of transformations 
    will be applied after reading in the raw DataFrame to memory, including:
        - reducing the number of columns to only those needed for later analysis
        - removing records without a battery_capacity value
        - divide the price column by 100 to find the dollar amount
    
    :param file_path: the file path where the raw smartphone data is stored
    :return: a cleaned dataset having had the operations above applied to it
    """

    # Check first if the file exists
    if os.path.exists(file_path):
        raw_data = pd.read_csv(file_path)
        # Update 1: Variable name 'raw Data' changed to 'raw_data' for Python snake_case naming convention.
    else:
        raise Exception(f"File containing smartphone data not found at path {file_path}")

    # Keep only necessary columns for analysis
    features = [
        "brand_name",
        "os",
        "price",
        "avg_rating",
        "processor_speed",
        "battery_capacity",
        "screen_size"
    ]

    # Update 2: Renamed 'columns_to_keep_in_clean data' to 'feature_set' for clarity and succinctness.
    clean_data = raw_data.loc[:, features]
    
    # Remove entries without 'battery_capacity' or 'os'
    clean_data = clean_data.dropna(subset=["battery_capacity", "os"])
    # Update 3: Adjusted spacing in 'dropna' function call to improve readability.
    
    # Convert 'price' column to reflect dollar amounts
    clean_data["price"] = clean_data["price"] / 100
    # Update 4: Added spaces around '/' operator for better code readability.
    
    return clean_data


# Call the function to prepare data
cleaned_data = prepare_smartphone_data("./data/smartphones.csv")




def column_to_label(column_name):
    """
    Converts a column name in a pandas DataFrame to a string that can be
    used as a label in a plot.
    
    :param column_name: string containing original column name
    :return: string that is ready to be presented on a plot
    """
    
    # Validate that column_name is a string
    if isinstance(column_name, str):
        return " ".join(column_name.split("_")).title()
        # Update 5: Encapsulated logic into 'column_to_label' function in accordance to DRY principles
    else:
        raise Exception("Please makes sure to pass a value of type 'str'.")


def visualize_versus_price(clean_data, x):
    """
    Use seaborn and matplotlib to identify a pattern between avg_rating and 
    battery_capacity.
    
    :param clean_data: a pandas DataFrame containing cleaned smartphone data
    :param x: variable to be plotted on the x-axis
    :return: None
    """
    x_title = column_to_label(x)
    # Update 6: Used 'column_to_label' function to remove duplicated code.
    
    # Create the scatterplot
    sns.scatterplot(x=x, y="price", data=clean_data, hue="os")
    
    # Add x and y labels
    plt.xlabel(x_title)
    plt.ylabel("Price ($)")
    
    # Add a title to the plot
    plt.title(f"{x_title} vs. Price")
    
    
# Call the function to visualize data
visualize_versus_price(cleaned_data, "processor_speed")




# Import required packages
import pytest
import ipytest

ipytest.config.rewrite_asserts = True
__file__ = "notebook.ipynb"


# Create a clean DataFrame fixture
@pytest.fixture()
def clean_smartphone_data():
    return prepare_smartphone_data("./data/smartphones.csv")

    
def test_nan_values(clean_smartphone_data):
    """
    Test for no NaN value for "battery_capacity" or "os"
    """
    
    # Assert there are no NaN value in "battery_capacity" or "os"
    assert clean_smartphone_data["battery_capacity"].isnull().sum() == 0
    assert clean_smartphone_data["os"].isnull().sum() == 0
    # Update 7: Corrected logical error by ensuring correct assertion syntax for checking NaN values.

