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

    print(f"✔️ Bank constraints saved to {filename}.")

def read_constraints_from_excel(filename="constraints_data.xlsx"):
    """ Reads the bank constraints data from an Excel file and returns a DataFrame. """
    try:
        return pd.read_excel(filename, sheet_name="Bank Constraints")
    except FileNotFoundError:
        print(f"⚠️ Error: {filename} not found.")
        return None

def save_user_info_to_excel(user_data, filename="user_information.xlsx"):
    """ Saves user input data into an Excel file, appending new entries without overwriting previous data. """
    new_entry = pd.DataFrame([user_data])

    # Check if file exists
    if os.path.exists(filename):
        try:
            # Read existing data
            existing_data = pd.read_excel(filename, sheet_name="User Inputs")
            updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        except Exception as e:
            # If sheet does not exist or any other error, start fresh
            print(f"⚠️ Error reading existing file: {e}. Creating a new file.")
            updated_data = new_entry
    else:
        # Create a new file with the first entry
        updated_data = new_entry

    # Write to Excel
    with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
        updated_data.to_excel(writer, sheet_name="User Inputs", index=False)

    print(f"📝 User information saved to {filename}.")

def analyze_eligibility(user_data):
    """ Checks if the user qualifies for a loan and explains why if they do not. """
    eligible_banks, alternative_banks = constraints.check_bank_eligibility(user_data, constraints.banks)

    if eligible_banks:
        print("\n✅ You qualify for loans from the following banks:")
        for bank, details in eligible_banks.items():
            print(f"\n🏦 {bank}:")
            print(f"   - Interest Rate: {details['base_interest_rate']}%")
            print(f"   - Max Loan Allowed: ${details['max_loan_allowed']:,.2f}")
            print(f"   - Required Down Payment: ${details['required_down_payment']:,.2f}")
            print("   - Loan Options:")
            for term, option in details["loan_options"].items():
                print(f"     🔹 {term} years: ${option['monthly_payment']:,.2f}/month → {option['sustainability']}")
    else:
        print("\n❌ You do not qualify for any loan at this time. Here’s why:")
        df_constraints = read_constraints_from_excel()

        explanations = []
        for _, row in df_constraints.iterrows():
            bank_name = row["Bank Name"]
            max_loan = row["Max Loan to Income"] * user_data["annual_income"]
            min_credit = row["Min Credit Score"]
            min_down_payment = row["Down Payment (%)"] * user_data["loan_amount"]

            loan_shortfall = max(0, user_data["loan_amount"] - max_loan)
            credit_shortfall = max(0, min_credit - user_data["credit_score"])
            down_payment_shortfall = max(0, min_down_payment - user_data["capital"])

            explanation = f"\n🔻 **{bank_name}**:"
            if loan_shortfall > 0:
                explanation += f"\n   - You requested ${user_data['loan_amount']:,.2f}, but the max allowed is ${max_loan:,.2f}."
            if credit_shortfall > 0:
                explanation += f"\n   - Your credit score is {user_data['credit_score']}, but the minimum required is {min_credit}."
            if down_payment_shortfall > 0:
                explanation += f"\n   - You need at least ${min_down_payment:,.2f} in capital, but you only have ${user_data['capital']:,.2f}."

            explanations.append(explanation)

        print("\n".join(explanations))

# Save bank constraints to Excel
save_constraints_to_excel()

while True:
    # Get user input
    user_data = constraints.get_mortgage_inputs()

    # Save user data to an Excel file
    save_user_info_to_excel(user_data)

    # Analyze eligibility
    analyze_eligibility(user_data)

    # Ask user if they want to try again
    retry = input("\n🔄 Would you like to try again with different values? (yes/no): ").strip().lower()
    if retry != "yes":
        print("✅ Process complete. Thank you for using the mortgage calculator!")
        break