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
