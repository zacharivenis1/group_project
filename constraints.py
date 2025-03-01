def get_mortgage_inputs():
    """Collects user inputs for mortgage calculation."""
    print("Welcome to the Mortgage Calculator!")

    # User inputs
    loan_amount = float(input("How much do you want to borrow? (USD): "))
    annual_income = float(input("What is your annual income? (USD): "))
    capital = float(input("How much capital do you have? (USD): "))
    credit_score = int(input("What is your credit score? (300-850): "))

    # Storing inputs
    mortgage_data = {
        "loan_amount": loan_amount,
        "annual_income": annual_income,
        "capital": capital,
        "credit_score": credit_score
    }

    return mortgage_data


# Define bank data with constraints
banks = {
    "Nordea": {
        "base_interest_rate": 6.1,  # Base rate before adjustments
        "max_loan_to_income": 4.0,  # Loan can be up to 4x income
        "min_credit_score": 720,  # Minimum score required
        "down_payment": 0.10  # 10% down payment required
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
    """Calculates the monthly installment using the mortgage formula."""
    monthly_rate = (annual_rate / 100) / 12
    total_months = years * 12
    if monthly_rate == 0:
        return loan_amount / total_months  # Avoid division by zero
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)


def check_financial_sustainability(monthly_payment, annual_income):
    """Checks if the monthly installment is sustainable based on income."""
    monthly_income = annual_income / 12
    return "✅ Sustainable" if monthly_payment < 0.3 * monthly_income else "⚠️ Unhealthy Financing"

def check_bank_eligibility(user_data, banks):
    """Determines which banks the user qualifies for and calculates loan terms."""
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
                # User qualifies for the requested loan amount
                eligible_banks[bank] = {
                    "base_interest_rate": details["base_interest_rate"],
                    "max_loan_allowed": max_loan,
                    "required_down_payment": required_down_payment,
                    "loan_options": {}
                }

                # Calculate monthly payments for different loan terms
                for term in [15, 25, 30]:  # Loan periods in years
                    monthly_payment = calculate_monthly_payment(loan_amount, details["base_interest_rate"], term)
                    sustainability = check_financial_sustainability(monthly_payment, annual_income)

                    eligible_banks[bank]["loan_options"][term] = {
                        "monthly_payment": monthly_payment,
                        "sustainability": sustainability
                    }

            elif capital >= max_possible_down_payment:
                # User cannot get the full requested loan but can borrow a smaller amount
                alternative_banks[bank] = {
                    "base_interest_rate": details["base_interest_rate"],
                    "max_loan_allowed": max_loan,
                    "required_down_payment": max_possible_down_payment,
                    "loan_options": {}
                }

                # Calculate monthly payments for the maximum possible loan
                for term in [15, 25, 30]:  # Loan periods in years
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

