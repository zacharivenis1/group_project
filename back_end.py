import pandas as pd
import os
import constraints  # Importing the constraints.py file


def save_constraints_to_excel(filename="constraints_data.xlsx"):
    """ Saves bank constraints to an Excel file. """
    banks_data = constraints.banks

    if not banks_data:
        print("⚠️ No bank data available to save.")
        return

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

    df_banks = pd.DataFrame(bank_list)
    df_banks.to_excel(filename, sheet_name="Bank Constraints", index=False)
    print(f"✅ Bank constraints saved to {filename}")


def read_constraints_from_excel(filename="constraints_data.xlsx"):
    """ Reads the bank constraints data from an Excel file and returns a DataFrame. """
    if not os.path.exists(filename):
        print("⚠️ Bank constraints file not found. Creating a new one...")
        save_constraints_to_excel(filename)
    return pd.read_excel(filename, sheet_name="Bank Constraints")


def analyze_eligibility(loan_amount, annual_income, capital, credit_score):
    """ Analyzes mortgage eligibility and returns detailed information. """
    df = read_constraints_from_excel()

    if df.empty:
        return "❌ No bank constraints found. Please check the data file."

    eligible_banks = []
    ineligible_reasons = {}

    for _, row in df.iterrows():
        reasons = []

        max_loan_allowed = row["Max Loan to Income"] * annual_income
        required_down_payment = (row["Down Payment (%)"] / 100) * loan_amount
        min_credit_score = row["Min Credit Score"]

        if loan_amount > max_loan_allowed:
            reasons.append(f"Loan amount exceeds maximum allowed (${max_loan_allowed:,.2f}).")
        if credit_score < min_credit_score:
            reasons.append(f"Credit score {credit_score} is below the required {min_credit_score}.")
        if capital < required_down_payment:
            reasons.append(f"Insufficient capital: Need ${required_down_payment:,.2f}, but have ${capital:,.2f}.")

        if not reasons:
            eligible_banks.append(
                f"🏦 {row['Bank Name']}\n  - Interest Rate: {row['Base Interest Rate']}%\n  - Max Loan Allowed: ${max_loan_allowed:,.2f}\n  - Required Down Payment: ${required_down_payment:,.2f}\n"
            )
        else:
            ineligible_reasons[row["Bank Name"]] = reasons

    if eligible_banks:
        return "✅ You qualify for loans from the following banks:\n" + "\n".join(eligible_banks)
    else:
        return "❌ You do not qualify for any loan at this time.\n\nReasons:\n" + "\n".join(
            [f"🔻 {bank}: \n - " + "\n - ".join(reasons) for bank, reasons in ineligible_reasons.items()]
        )
