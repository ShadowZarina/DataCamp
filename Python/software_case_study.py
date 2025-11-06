"""
A module to implement the BasicCalcualtor.
"""
import numpy as np

class BasicCalculator:
    # A class for arithmetic operations on numbers    
    
    def add(self, x, y):
        return np.add(x, y)

    def subtract(self, x, y):
        return np.subtract(x, y)

    def multiply(self, x, y):
        return np.multiply(x, y)

    def divide(self, x, y):
        return np.divide(x, y)

    def power(self, x, y):
        return np.power(x, y)

"""
A module to implement the FinancialCalculator
"""

class FinancialCalculator(BasicCalculator):
    def monthly_interest(self, annual_interest_rate):
        return self.divide(annual_interest_rate, 12)

    def months_from_years(self, years):
        return self.multiply(years, 12)

'''
Define a class named MortgageCalculator
'''

class MortgageCalculator(FinancialCalculator):
  def __init__(self, loan_amount, annual_interest_rate, years):
    super().__init__()
    self.loan_amount = loan_amount
    self.monthly_interest_rate = self.monthly_interest(annual_interest_rate)
    self.months = self.multiply(years, 12)
    self.monthly_payment = self.calculate_monthly_payment()

  # Calculate the monthly payment
  def calculate_monthly_payment(self):
    numerator = self.monthly_interest_rate * (1 + self.monthly_interest_rate) ** self.months
    denominator = (1 + self.monthly_interest_rate) ** self.months - 1
    multiplier = self.divide(numerator, denominator)
    monthly_payment = round(self.multiply(self.loan_amount, multiplier), 2)
    return monthly_payment

  # Calculate loan amount after calculating monthly payment, interest rate, and using the number of payments
  def calculate_loan_amount(monthly_payment, monthly_interest_rate, nbr_payments):
      """
      Calculate the loan amount based on the monthly payment, monthly interest rate, and total number of payments.
      """	
      # Raise an error if the number of total payment is less than zero
      if nbr_payments <= 0:
          raise ValueError("The number of payments must be greater than zero.")
  
      loan_amount = (monthly_payment * ((1 + monthly_interest_rate) ** nbr_payments - 1)) / \
                    (monthly_interest_rate * (1 + monthly_interest_rate) ** nbr_payments)
      
      # Return the loan amount
      return loan_amount

