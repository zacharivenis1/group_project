import pandas as pd
import os
import constraints  # Import the constraints.py file that contains bank constraint data


def save_constraints_to_excel(filename="constraints_data.xlsx"):
    """
    Saves bank constraints from the constraints module to an Excel file.

    Parameters:
        filename (str): The name of the Excel file to save data to.
    """
    # Retrieve bank data from the constraints module.
    banks_data = constraints.banks

    # If there is no bank data, print a warning and exit the function.
    if not banks_data:
        print("⚠️ No bank data available to save.")
        return

    # Create a list of dictionaries, where each dictionary holds details for one bank.
    bank_list = [
        {
            "Bank Name": bank,
            "Base Interest Rate": details["base_interest_rate"],
            "Max Loan to Income": details["max_loan_to_income"],
            "Min Credit Score": details["min_credit_score"],
            "Down Payment (%)": details["down_payment"] * 100  # Convert fraction to percentage for readability.
        }
        for bank, details in banks_data.items()
    ]

    # Create a DataFrame from the list of bank dictionaries.
    df_banks = pd.DataFrame(bank_list)

    # Write the DataFrame to an Excel file with a specific sheet name, without row indices.
    df_banks.to_excel(filename, sheet_name="Bank Constraints", index=False)
    print(f"✅ Bank constraints saved to {filename}")


def read_constraints_from_excel(filename="constraints_data.xlsx"):
    """
    Reads the bank constraints data from an Excel file and returns a DataFrame.

    Parameters:
        filename (str): The name of the Excel file to read from.

    Returns:
        pandas.DataFrame: A DataFrame containing bank constraints.
    """
    # Check if the specified Excel file exists.
    if not os.path.exists(filename):
        print("⚠️ Bank constraints file not found. Creating a new one...")
        # If the file doesn't exist, create it by saving the current bank constraints.
        save_constraints_to_excel(filename)
    # Read the Excel file and return its contents as a DataFrame.
    return pd.read_excel(filename, sheet_name="Bank Constraints")


def analyze_eligibility(loan_amount, annual_income, capital, credit_score):
    """
    Analyzes mortgage eligibility based on the user's financial details and bank constraints.

    Parameters:
        loan_amount (float): The desired loan amount.
        annual_income (float): The user's annual income.
        capital (float): The user's available capital.
        credit_score (int): The user's credit score.

    Returns:
        str: A detailed message indicating which banks the user qualifies for or explaining why they don't.
    """
    # Load bank constraints from the Excel file.
    df = read_constraints_from_excel()

    # If the DataFrame is empty, return an error message.
    if df.empty:
        return "❌ No bank constraints found. Please check the data file."

    eligible_banks = []  # List to store messages for banks where the user is eligible.
    ineligible_reasons = {}  # Dictionary to store ineligibility reasons for each bank.

    # Iterate over each row (bank) in the DataFrame.
    for _, row in df.iterrows():
        reasons = []  # List to collect reasons for ineligibility for the current bank.

        # Calculate the maximum loan allowed based on the bank's loan-to-income ratio.
        max_loan_allowed = row["Max Loan to Income"] * annual_income
        # Calculate the required down payment for the requested loan amount.
        required_down_payment = (row["Down Payment (%)"] / 100) * loan_amount
        # Get the minimum credit score required by the bank.
        min_credit_score = row["Min Credit Score"]

        # Check if the desired loan amount exceeds the bank's maximum allowed loan.
        if loan_amount > max_loan_allowed:
            reasons.append(f"Loan amount exceeds maximum allowed (${max_loan_allowed:,.2f}).")
        # Check if the user's credit score is below the bank's minimum requirement.
        if credit_score < min_credit_score:
            reasons.append(f"Credit score {credit_score} is below the required {min_credit_score}.")
        # Check if the user has sufficient capital for the required down payment.
        if capital < required_down_payment:
            reasons.append(f"Insufficient capital: Need ${required_down_payment:,.2f}, but have ${capital:,.2f}.")

        # If no reasons for ineligibility were found, the bank is eligible.
        if not reasons:
            eligible_banks.append(
                f"🏦 {row['Bank Name']}\n  - Interest Rate: {row['Base Interest Rate']}%\n  - Max Loan Allowed: ${max_loan_allowed:,.2f}\n  - Required Down Payment: ${required_down_payment:,.2f}\n"
            )
        else:
            # Otherwise, store the reasons for ineligibility under the bank's name.
            ineligible_reasons[row["Bank Name"]] = reasons

    # Return a detailed message based on eligibility results.
    if eligible_banks:
        return "✅ You qualify for loans from the following banks:\n" + "\n".join(eligible_banks)
    else:
        return "❌ You do not qualify for any loan at this time.\n\nReasons:\n" + "\n".join(
            [f"🔻 {bank}: \n - " + "\n - ".join(reasons) for bank, reasons in ineligible_reasons.items()]
        )
