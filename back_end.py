import pandas as pd
import os
import constraints  # Importing the constraints.py file where we defined all the constraints that will be used for our programme


def save_constraints_to_excel(filename="constraints_data.xlsx"):
    #Saves bank constraints to an Excel file that will be printed if requested in the programme
    banks_data = constraints.banks

    if not banks_data:
        print("⚠️ No bank data available to save.")
        return
    #defining parameters for the information from the bank
    bank_list = [
        {
            "Bank Name": bank,
            "Base Interest Rate": details["base_interest_rate"],
            "Max Loan to Income": details["max_loan_to_income"],
            "Min Credit Score": details["min_credit_score"],
            "Down Payment (%)": details["down_payment"] * 100  # Convert to percentage
        }
        for bank, details in banks_data.items()
    ]
    #updating the dataframe made using pandas
    df_banks = pd.DataFrame(bank_list)
    df_banks.to_excel(filename, sheet_name="Bank Constraints", index=False)
    print(f"✅ Bank constraints saved to {filename}")


def read_constraints_from_excel(filename="constraints_data.xlsx"):
    #Reads the bank constraints data from an Excel file and returns a DataFrame
    if not os.path.exists(filename):
        print("⚠️ Bank constraints file not found. Creating a new one...")
        save_constraints_to_excel(filename)
    return pd.read_excel(filename, sheet_name="Bank Constraints")


def calculate_monthly_payment(loan_amount, annual_rate, years):
    #Calculates the monthly payment based on loan amount, interest rate, and duration
    monthly_rate = (annual_rate / 100) / 12  # Convert annual rate to monthly rate
    total_months = years * 12  # Convert years to months
    if monthly_rate == 0:
        return loan_amount / total_months  # Avoid division by zero
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)


def analyze_eligibility(loan_amount, annual_income, capital, credit_score):
    #Analyzes mortgage eligibility and returns detailed information, including monthly payments.
    df = read_constraints_from_excel()

    if df.empty:
        return "❌ No bank constraints found. Please check the data file."

    eligible_banks = []
    ineligible_reasons = {}

    for _, row in df.iterrows():
        reasons = []  # List to store reasons if the user is ineligible for a bank

        # Extract key values from the bank's criteria
        max_loan_allowed = row["Max Loan to Income"] * annual_income  # Maximum loan based on income
        required_down_payment = (row["Down Payment (%)"] / 100) * loan_amount  # Required down payment calculation
        min_credit_score = row["Min Credit Score"]  # Minimum credit score requirement

        # Check if loan amount exceeds the bank's maximum limit
        if loan_amount > max_loan_allowed:
            reasons.append(f"Loan amount exceeds maximum allowed (${max_loan_allowed:,.2f}).")

        # Check if credit score is below the bank's requirement
        if credit_score < min_credit_score:
            reasons.append(f"Credit score {credit_score} is below the required {min_credit_score}.")

        # Check if the user has enough capital for the required down payment
        if capital < required_down_payment:
            reasons.append(f"Insufficient capital: Need ${required_down_payment:,.2f}, but have ${capital:,.2f}.")

        # If no issues were found, the user qualifies for this bank
        if not reasons:
            loan_terms = [15, 25, 30]  # Loan repayment terms in years
            payment_details = ""  # String to store monthly payment details

            # Calculate monthly payments for different loan terms
            for term in loan_terms:
                monthly_payment = calculate_monthly_payment(loan_amount, row['Base Interest Rate'], term)
                payment_details += f"    - {term} years: ${monthly_payment:,.2f}/month\n"

            # Store the eligible bank's information
            eligible_banks.append(
                f"🏦 {row['Bank Name']}\n  - Interest Rate: {row['Base Interest Rate']}%\n  - Max Loan Allowed: ${max_loan_allowed:,.2f}\n  - Required Down Payment: ${required_down_payment:,.2f}\n  - Monthly Payments:\n{payment_details}"
            )
        else:
            # Store reasons for ineligibility
            ineligible_reasons[row["Bank Name"]] = reasons

        # Return eligible banks if there are any
    if eligible_banks:
        return "✅ You qualify for loans from the following banks:\n" + "\n".join(eligible_banks)
    else:
        # If no banks qualify, return rejection reasons
        return "❌ You do not qualify for any loan at this time.\n\nReasons:\n" + "\n".join(
            [f"🔻 {bank}: \n - " + "\n - ".join(reasons) for bank, reasons in ineligible_reasons.items()]
        )