import pandas as pd
import os
import constraints  # Importing the constraints.py file


def save_constraints_to_excel(filename="constraints_data.xlsx"):
    """ Saves bank constraints to an Excel file. """
    banks_data = constraints.banks

    bank_list = [
        {
            "Bank Name": bank,
            "Base Interest Rate": details["base_interest_rate"],
            "Max Loan to Income": details["max_loan_to_income"],
            "Min Credit Score": details["min_credit_score"],
            "Down Payment (%)": details["down_payment"]
        }
        for bank, details in banks_data.items()
    ]

    df_banks = pd.DataFrame(bank_list)
    df_banks.to_excel(filename, sheet_name="Bank Constraints", index=False)


def read_constraints_from_excel(filename="constraints_data.xlsx"):
    """ Reads the bank constraints data from an Excel file and returns a DataFrame. """
    if not os.path.exists(filename):
        return pd.DataFrame(
            columns=["Bank Name", "Base Interest Rate", "Max Loan to Income", "Min Credit Score", "Down Payment (%)"])
    return pd.read_excel(filename, sheet_name="Bank Constraints")


def analyze_eligibility(loan_amount, annual_income, capital, credit_score):
    """ Analyzes mortgage eligibility and returns detailed information. """
    df = read_constraints_from_excel()
    eligible_banks = []
    ineligible_reasons = {}

    for _, row in df.iterrows():
        reasons = []

        if loan_amount / annual_income > row["Max Loan to Income"]:
            reasons.append(f"Loan-to-income ratio too high (max: {row['Max Loan to Income']})")
        if credit_score < row["Min Credit Score"]:
            reasons.append(f"Credit score too low (min: {row['Min Credit Score']})")
        if capital / loan_amount < row["Down Payment (%)"] / 100:
            reasons.append(f"Not enough capital for down payment (min: {row['Down Payment (%)']}%)")

        if not reasons:
            eligible_banks.append(
                f"{row['Bank Name']}\n  - Interest Rate: {row['Base Interest Rate']}%\n  - Max Loan Allowed: ${loan_amount:,.2f}\n  - Required Down Payment: ${loan_amount * (row['Down Payment (%)'] / 100):,.2f}\n"
            )
        else:
            ineligible_reasons[row["Bank Name"]] = reasons

    if eligible_banks:
        return "✅ You qualify for loans from the following banks:\n" + "\n".join(eligible_banks)
    else:
        return "❌ You do not qualify for any loan at this time.\n\nReasons:\n" + "\n".join(
            [f"{bank}: {', '.join(reasons)}" for bank, reasons in ineligible_reasons.items()])