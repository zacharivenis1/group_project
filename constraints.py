def get_mortgage_inputs():
    """
    Collects user inputs for mortgage calculation with error handling.

    Returns:
        dict: User input data including loan amount, annual income, capital, and credit score.
    """
    print("Welcome to the Mortgage Calculator!")

    while True:
        try:
            loan_amount = float(input("How much do you want to borrow? (USD): "))
            if loan_amount <= 0:
                raise ValueError("Loan amount must be greater than 0.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}. Please enter a valid amount.")

    while True:
        try:
            annual_income = float(input("What is your annual income? (USD): "))
            if annual_income <= 0:
                raise ValueError("Income must be greater than 0.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}. Please enter a valid income.")

    while True:
        try:
            capital = float(input("How much capital do you have? (USD): "))
            if capital < 0:
                raise ValueError("Capital cannot be negative.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}. Please enter a valid amount.")

    while True:
        try:
            credit_score = int(input("What is your credit score? (300-850): "))
            if credit_score < 300 or credit_score > 850:
                raise ValueError("Credit score must be between 300 and 850.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}. Please enter a valid credit score.")

    return {
        "loan_amount": loan_amount,
        "annual_income": annual_income,
        "capital": capital,
        "credit_score": credit_score
    }


# Define bank data with constraints
banks = {
    "Nordea": {
        "base_interest_rate": 6.1,
        "max_loan_to_income": 4.0,
        "min_credit_score": 720,
        "down_payment": 0.10
    },
    "DNB": {
        "base_interest_rate": 5.5,
        "max_loan_to_income": 5.0,
        "min_credit_score": 650,
        "down_payment": 0.15
    },
    "SPAREBANK 1": {
        "base_interest_rate": 4.5,
        "max_loan_to_income": 4.5,
        "min_credit_score": 700,
        "down_payment": 0.125
    }
}


def calculate_monthly_payment(loan_amount, annual_rate, years):
    """
    Calculates the monthly installment for a mortgage.

    Parameters:
        loan_amount (float): The total amount borrowed.
        annual_rate (float): The annual interest rate in percentage.
        years (int): The loan repayment period in years.

    Returns:
        float: The calculated monthly payment.
    """
    monthly_rate = (annual_rate / 100) / 12
    total_months = years * 12
    if monthly_rate == 0:
        return loan_amount / total_months  # Avoid division by zero
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)


def check_financial_sustainability(monthly_payment, annual_income):
    """
    Checks if the monthly installment is sustainable based on income.

    Parameters:
        monthly_payment (float): The monthly installment payment.
        annual_income (float): The user's annual income.

    Returns:
        str: "✅ Sustainable" if below 30% of income, otherwise "⚠️ Unhealthy Financing".
    """
    monthly_income = annual_income / 12
    return "✅ Sustainable" if monthly_payment < 0.3 * monthly_income else "⚠️ Unhealthy Financing"


def check_bank_eligibility(user_data, banks):
    """
    Determines which banks the user qualifies for and calculates loan terms.

    Parameters:
        user_data (dict): User input data including loan amount, income, capital, and credit score.
        banks (dict): Dictionary of bank constraints.

    Returns:
        tuple: (eligible_banks, alternative_banks) - Banks that approve the request and max possible loan offers.
    """
    loan_amount = user_data["loan_amount"]
    annual_income = user_data["annual_income"]
    capital = user_data["capital"]
    credit_score = user_data["credit_score"]

    eligible_banks = {}
    alternative_banks = {}

    for bank, details in banks.items():
        max_loan = details["max_loan_to_income"] * annual_income
        required_down_payment = details["down_payment"] * loan_amount
        max_possible_down_payment = details["down_payment"] * max_loan

        if credit_score >= details["min_credit_score"]:
            if loan_amount <= max_loan and capital >= required_down_payment:
                eligible_banks[bank] = {
                    "base_interest_rate": details["base_interest_rate"],
                    "max_loan_allowed": max_loan,
                    "required_down_payment": required_down_payment,
                    "loan_options": {}
                }

                for term in [15, 25, 30]:
                    monthly_payment = calculate_monthly_payment(loan_amount, details["base_interest_rate"], term)
                    sustainability = check_financial_sustainability(monthly_payment, annual_income)

                    eligible_banks[bank]["loan_options"][term] = {
                        "monthly_payment": monthly_payment,
                        "sustainability": sustainability
                    }

            elif capital >= max_possible_down_payment:
                alternative_banks[bank] = {
                    "base_interest_rate": details["base_interest_rate"],
                    "max_loan_allowed": max_loan,
                    "required_down_payment": max_possible_down_payment,
                    "loan_options": {}
                }

                for term in [15, 25, 30]:
                    monthly_payment = calculate_monthly_payment(max_loan, details["base_interest_rate"], term)
                    sustainability = check_financial_sustainability(monthly_payment, annual_income)

                    alternative_banks[bank]["loan_options"][term] = {
                        "monthly_payment": monthly_payment,
                        "sustainability": sustainability
                    }

    return eligible_banks, alternative_banks


# User Input
user_data = get_mortgage_inputs()
eligible_banks, alternative_banks = check_bank_eligibility(user_data, banks)

# Display Results
if eligible_banks:
    print("\n🏦 You qualify for loans from the following banks:")
    for bank, details in eligible_banks.items():
        print(f"\n{bank}:")
        print(f"   - Interest Rate: {details['base_interest_rate']}%")
        print(f"   - Max Loan Allowed: ${details['max_loan_allowed']:,.2f}")
        print(f"   - Required Down Payment: ${details['required_down_payment']:,.2f}")
        print("   - Loan Options:")
        for term, option in details["loan_options"].items():
            print(f"     🔹 {term} years: ${option['monthly_payment']:,.2f}/month → {option['sustainability']}")
elif alternative_banks:
    print("\n⚠️ You do not qualify for your requested loan amount, but here are the maximum amounts you can borrow:")
    for bank, details in alternative_banks.items():
        print(f"\n{bank}:")
        print(f"   - Interest Rate: {details['base_interest_rate']}%")
        print(f"   - Maximum Loan Allowed: ${details['max_loan_allowed']:,.2f}")
        print(f"   - Required Down Payment: ${details['required_down_payment']:,.2f}")
        print("   - Loan Options:")
        for term, option in details["loan_options"].items():
            print(f"     🔹 {term} years: ${option['monthly_payment']:,.2f}/month → {option['sustainability']}")
else:
    print("\n❌ Unfortunately, you do not qualify for any loan at this time.")
