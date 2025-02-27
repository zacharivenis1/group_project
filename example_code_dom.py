def mortgage_calculator():
    """Calculates monthly mortgage payments."""

    print("Mortgage Calculator")

    try:
        principal_str = input("Enter the principal loan amount: ")
        principal = float(principal_str)

        annual_interest_rate_str = input("Enter the annual interest rate (e.g., 0.05 for 5%): ")
        annual_interest_rate = float(annual_interest_rate_str)

        loan_term_years_str = input("Enter the loan term in years: ")
        loan_term_years = int(loan_term_years_str)

        credit_score_str = input("Enter your credit score: ")
        credit_score = int(credit_score_str)

        annual_income_str = input("Enter your annual income: ")
        annual_income = float(annual_income_str)

        # Adjust interest rate based on credit score (simplified example)
        if credit_score < 600:
            annual_interest_rate = annual_interest_rate + 0.02  # Higher rate for low credit
        elif credit_score > 750:
            annual_interest_rate = annual_interest_rate - 0.01  # Lower rate for high credit

        # Monthly interest rate
        monthly_interest_rate = annual_interest_rate / 12

        # Total number of payments
        num_payments = loan_term_years * 12

        # Mortgage calculation formula
        monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / \
                          ((1 + monthly_interest_rate)**num_payments - 1)

        print("Monthly mortgage payment: $" + str(round(monthly_payment, 2)))

        # Basic affordability check (simplified)
        monthly_income = annual_income / 12
        if monthly_payment > monthly_income / 3: # 33% rule
            print("Warning: Monthly payment may be a significant portion of your income.")

    except ValueError:
        print("Invalid input. Please enter numeric values.")

mortgage_calculator()
