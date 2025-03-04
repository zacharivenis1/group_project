# Mortgage Calculator Application
The Mortgage Calculator Application is a Python-based tool designed to help users determine their eligibility for home loans from various banks. It analyzes user inputs such as loan amount, annual income, capital, and credit score to provide detailed loan options and eligibility criteria. The application also saves user data and bank constraints to Excel files for easy reference.

# Features
## User Input Collection: Collects user inputs for loan amount, annual income, capital, and credit score with error handling.

## Bank Eligibility Analysis: Checks user eligibility for loans from multiple banks based on predefined constraints.

## Loan Options: Displays detailed loan options, including monthly payments and financial sustainability for 15, 25, and 30-year terms.

## Excel Integration: Saves user data and bank constraints to Excel files for record-keeping.

## Interactive Interface: Allows users to retry calculations with different inputs.

# Prerequisites
Before running the application, ensure you have the following installed:

Python 3.x: The application is built using Python. Download and install Python from python.org.

PyCharm IDE: Recommended for running and debugging the application. Download PyCharm from jetbrains.com.

Required Python Libraries:

pandas: For handling Excel files.

openpyxl: For Excel file operations.

# You can install the required libraries using the following command:

bash
Copy
pip install pandas openpyxl

## How to Use
Step 1: Clone or Download the Project
Clone this repository or download the project files (back_end.py and constraints.py) to your local machine.

Step 2: Open the Project in PyCharm
Open PyCharm and load the project directory containing the two Python files.

Ensure the required libraries (pandas and openpyxl) are installed in your Python environment.

Step 3: Run the Application
Open the back_end.py file in PyCharm.

Right-click anywhere in the editor and select Run 'back_end'.

The application will start, and you will be prompted to input your mortgage details in the PyCharm Run console.

Step 4: Input Your Details
The application will ask for the following inputs:

Loan Amount (USD): The amount you wish to borrow.

Annual Income (USD): Your yearly income.

Capital (USD): The amount of money you have available for a down payment.

Credit Score (300-850): Your credit score.

Step 5: View Results
If you qualify for loans, the application will display the bank name, interest rate, maximum loan allowed, required down payment, and monthly payment options for 15, 25, and 30-year terms.

If you do not qualify, the application will explain why, detailing the shortfalls in loan amount, credit score, or down payment for each bank.

Step 6: Save Data
User inputs are saved to user_information.xlsx.

Bank constraints are saved to constraints_data.xlsx.

Step 7: Retry or Exit
After viewing the results, you can choose to retry with different values or exit the application.

# Example Interaction
Here’s an example of how the application works:

Copy
Welcome to the Mortgage Calculator!
How much do you want to borrow? (USD): 200000
What is your annual income? (USD): 60000
How much capital do you have? (USD): 30000
What is your credit score? (300-850): 750

✅ You qualify for loans from the following banks:

🏦 Nordea:
   - Interest Rate: 6.1%
   - Max Loan Allowed: $240,000.00
   - Required Down Payment: $20,000.00
   - Loan Options:
     🔹 15 years: $1,694.51/month → ✅ Sustainable
     🔹 25 years: $1,303.21/month → ✅ Sustainable
     🔹 30 years: $1,209.59/month → ✅ Sustainable

🔄 Would you like to try again with different values? (yes/no): no
✅ Process complete. Thank you for using the mortgage calculator!
File Structure
The project consists of two main files:

# back_end.py:

Contains the main logic for user interaction, data saving, and eligibility analysis.

Saves user data and bank constraints to Excel files.

# constraints.py:

Defines bank constraints (interest rates, loan-to-income ratios, credit score requirements, etc.).

Contains functions for calculating monthly payments and checking financial sustainability.

# Customization
Adding or Modifying Banks
You can add or modify banks in the constraints.py file. Each bank is defined with the following parameters:

base_interest_rate: The bank's base interest rate.

max_loan_to_income: The maximum loan amount as a multiple of the user's annual income.

min_credit_score: The minimum credit score required.

down_payment: The required down payment as a percentage of the loan amount.

## Example:

python
Copy
banks = {
    "Bank Name": {
        "base_interest_rate": 5.0,
        "max_loan_to_income": 4.5,
        "min_credit_score": 700,
        "down_payment": 0.10
    }
}
