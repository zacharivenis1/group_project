import pandas as pd
import os
import \
    constraints  # Importing the constraints.py file where we defined all the constraints that will be used for our programme


def save_constraints_to_excel(filename="constraints_data.xlsx"):
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
    if not os.path.exists(filename):
        print("⚠️ Bank constraints file not found. Creating a new one...")
        save_constraints_to_excel(filename)
    return pd.read_excel(filename, sheet_name="Bank Constraints")


def calculate_monthly_payment(loan_amount, annual_rate, years):
    monthly_rate = (annual_rate / 100) / 12  # Convert annual rate to monthly rate
    total_months = years * 12  # Convert years to months
    if monthly_rate == 0:
        return loan_amount / total_months  # Avoid division by zero
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)


def analyze_eligibility(loan_amount, annual_income, capital, credit_score):
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
            loan_terms = [15, 25, 30]
            payment_details = ""

            for term in loan_terms:
                monthly_payment = calculate_monthly_payment(loan_amount, row['Base Interest Rate'], term)
                sustainability = constraints.check_financial_sustainability(monthly_payment, annual_income)
                payment_details += f"    - {term} years: ${monthly_payment:,.2f}/month ({sustainability})\n"

            eligible_banks.append(
                f"🏦 {row['Bank Name']}\n  - Interest Rate: {row['Base Interest Rate']}%\n  - Max Loan Allowed: ${max_loan_allowed:,.2f}\n  - Required Down Payment: ${required_down_payment:,.2f}\n  - Monthly Payments:\n{payment_details}"
            )
        else:
            ineligible_reasons[row["Bank Name"]] = reasons

    if eligible_banks:
        return "✅ You qualify for loans from the following banks:\n" + "\n".join(eligible_banks)
    else:
        return "❌ You do not qualify for any loan at this time.\n\nReasons:\n" + "\n".join(
            [f"🔻 {bank}: \n - " + "\n - ".join(reasons) for bank, reasons in ineligible_reasons.items()]
        )