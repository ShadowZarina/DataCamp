'''
You will be working with historical food sales data. The data has been split into training and test sets (historicsales_fastfooditems_train.csv and historicsales_fastfooditems_train.csv) that contain the following columns:

restaurant - the name of the restaurant (chr)
item_name - the food item (chr)
date - the date of the sale (chr)
baseprice_USD - the price of the item before discount in USD (int)
discount_percent - the percentage discount (int)
sales_quantity - the quantity of item sold on a given date (int)
is_weekend - 1 if the sale date is Saturday or Sunday, otherwise 0 (int)
is_friday - 1 if the sale date is Friday, otherwise 0 (int)
is_holiday - 1 if the sale date is a holiday (that is not a weekend), otherwise 0 (int)
'''

'''
Help these fast-food restaurants improve their sales predictions by answering the following questions:

1. What is the correlation between the discount and sales quantity for the full training data? Store this value in a numeric variable named correlation.
  - Which restaurant and item pair have the highest correlation? Save your answer as a character vector highest_cor where the first item is the restaurant, and the second is the food item.

2. Build and train a regression model using the training data to predict sales_quantity and find the best adjusted r-squared. Store this as numeric variable adj_rsquared.
3. Generate predictions with your best model on the test data and calculate the RMSE. Store this as a numeric variable rmse.
'''

# Run this cell to load the libraries and data
# Load required libraries: dplyr, gplot2
library(dplyr)
library(ggplot2)

# Load the data
train <- read.csv("historicsales_fastfooditems_train.csv")
test <- read.csv("historicsales_fastfooditems_test.csv")

# Review the first few rows of your data
head(train)

# Check the data types
str(train)

# Fill in missing values in the discount_percent column
train$discount_percent[is.na(train$discount_percent)] <- 0
test$discount_percent[is.na(test$discount_percent)] <- 0

# Convert the date column into date format
train$date <- as.Date(train$date, format = "%d-%b-%Y")
test$date <- as.Date(test$date, format = "%d-%b-%Y")

head(train)

# Find correlation between the discount and sales quantity on the full training data
correlation <- cor(train$discount_percent, train$sales_quantity)
correlation

# Find the same correlation for different subsets of restaurant and food item
r1_burger <- train %>%
  filter(restaurant == 'R1' & item_name == 'Burger')

r1_burger_cor <- cor(r1_burger$discount_percent, r1_burger$sales_quantity)
r1_burger_cor 

r1_salad <- train %>%
  filter(restaurant == 'R1' & item_name == 'Salad')

r1_salad_cor <- cor(r1_salad$discount_percent, r1_salad$sales_quantity)
r1_salad_cor

r2_burger <- train %>%
  filter(restaurant == 'R2' & item_name == 'Burger')

r2_burger_cor <- cor(r2_burger$discount_percent, r2_burger$sales_quantity)
r2_burger_cor

r2_salad <- train %>%
  filter(restaurant == 'R2' & item_name == 'Salad')

r2_salad_cor <- cor(r2_salad$discount_percent, r2_salad$sales_quantity)
r2_salad_cor

# Save the highest correlation pair
highest_cor <- c('R1', 'Salad')
highest_cor

# Optional: plot time series data for each restaurant-item pair 
ggplot(train, aes(x = date, y = sales_quantity, color = interaction(item_name, restaurant, sep = "-"))) +
  geom_line() +
  labs(title = "Time Series of Sales Quantity by Restaurant and Item", x = "Date", y = "Sales Quantity (Units)", color = "Item, Restaurant")

# Build a regression model using the full training data
lm_sales_global <- lm(sales_quantity ~ discount_percent, data = train)

# Get the summary of the model
broom::glance(lm_sales_global)

# Try out different subsets of the data or predictors to get a better adjusted r-squared score. Here's one example:
lm_r1_burger_multi <- lm(sales_quantity ~ discount_percent + is_weekend + is_friday + is_holiday, data = r1_burger)

broom::glance(lm_r1_burger_multi)

# Store your best Adjusted R-Squared score
adj_rsquared = summary(lm_r1_burger_multi)$adj.r.squared

# Subset the test data to match training set
r1_burger_test <- train %>%
  filter(restaurant == 'R1' & item_name == 'Burger')

# Generate sales predictions using the test set
r1_burger_test$predicted_sales<- predict(lm_r1_burger_multi, newdata = r1_burger_test)

# Capture residuals for the data
r1_burger_test$residuals <- r1_burger_test$sales_quantity - r1_burger_test$predicted_sales

# Calculate the RMSE for the residuals
residuals <- r1_burger_test$sales_quantity - r1_burger_test$predicted_sales
residuals

rmse <- sqrt(mean(residuals^2))
rmse
