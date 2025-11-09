'''
All data is sourced from df_train.csv and df_test.csv

Predict daily power_consumption by experimenting with various supervised regression models trained on the training dataset.

1. Evaluate their performance on the test dataset by measuring their Root Mean Squared Error (RMSE).
  - Save the lowest RMSE achieved on the test set as a numeric variable selected_rmse, which should not be greater than 450 kW.

2. Plot the power_consumption predictions and actual daily power_consumption for the test dataset and assess whether the predictions follow a similar trend as the original data.
  - Save your answer "Yes" or "No" as a string variable trend_similarity.
'''

# Load necessary libraries
library(dplyr)     
library(lubridate) 
library(ranger)    
library(xgboost)   
library(ggplot2)   

# Read training and testing data from CSV files
df_train <- read.csv("df_train.csv")
df_test <- read.csv("df_test.csv")

# Display structure of the training data
glimpse(df_train)

# Convert 'date' column to Date type and 'day_in_week' column to factor in both datasets
df_train <- df_train %>%
  mutate(date = as.Date(date, format = "%m/%d/%Y"),
         day_in_week = factor(day_in_week)) 
df_test <- df_test %>%
  mutate(date = as.Date(date, format = "%m/%d/%Y"),
         day_in_week = factor(day_in_week))

# Convert categorical variable 'day_in_week' to indicator variables using one-hot encoding in both datasets
df_onehot_train <- model.matrix(~ day_in_week - 1, data = df_train) %>%
  as.data.frame()
df_onehot_test <- model.matrix(~ day_in_week - 1, data = df_test) %>%
  as.data.frame()

# Combine one-hot encoded columns with the original datasets and remove the 'day_in_week' column
df_train <- mutate(df_train, df_onehot_train) %>% select(-c(day_in_week))
df_test <- mutate(df_test, df_onehot_test) %>% select(-c(day_in_week))

# Separate features and target variable for both training and testing datasets
train_x <- df_train %>% select(-power_consumption, -date)  
train_y <- df_train[["power_consumption"]]  
test_x <- df_test %>% select(-power_consumption, -date)  
test_y <- df_test[["power_consumption"]]  

# Train models, predict on test dataset and calculate RMSE for each model.
## Linear regression
lm_model <- lm(train_y ~ ., data = train_x)   
lm_pred <- predict(lm_model, newdata = test_x)  
lm_rmse <- sqrt(mean((test_y - lm_pred)^2))  

## Random forest
rf_model <- ranger(power_consumption ~., data = df_train %>% select(-date), num.trees = 1000)
rf_pred <- predict(rf_model, data = df_test %>% select(-date))$predictions  
rf_rmse <- sqrt(mean((test_y - rf_pred)^2))  

## XGBoost
xgb_model <- xgboost(
  data = as.matrix(train_x),  
  label = train_y,  
  nrounds = 500, 
  objective = "reg:squarederror",  
  eta = 0.1,  
  max_depth = 1,  
  verbose = FALSE
)
xgb_pred <- predict(xgb_model, newdata = as.matrix(test_x))  
xgb_rmse <- sqrt(mean((test_y - xgb_pred)^2))  

# RMSE scores
data.frame(
  Model = c("Linear Regression", "Random Forest", "XGBoost"),  
  RMSE = c(lm_rmse, rf_rmse, xgb_rmse)  
)

# Get the lowest RMSE and assign it to selected_rmse
selected_rmse <- min(lm_rmse, rf_rmse, xgb_rmse)
cat("selected_rmse:", selected_rmse, "kW\n")

# Add predictions to the test dataset for plotting
df_test <- df_test %>%
  mutate(Predicted = rf_pred)

# Plot actual vs predicted power consumption over time to check for trend similarity
ggplot(df_test) +
  geom_line(aes(x = date, y = power_consumption), color = "green", linewidth = 1.1) +
  geom_line(aes(x = date, y = Predicted), color = "brown", linewidth = 1) +
  labs(title = "Power Consumption: Original and Predicted", x = "Date", y = "Power Consumption", caption = "Green is original and brown is predicted data") +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  theme_minimal() +
  theme(panel.grid.major.x = element_line(color = "grey80"))

trend_similarity <- "Yes"

cat("trend_similarity:", trend_similarity, "\n")
