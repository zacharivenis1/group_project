import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import back_end

# Ensure interactive functions from back_end are not executed on import
if __name__ == "__main__":
    def load_bank_constraints():
        """ Load bank constraints and display them in the tree view """
        try:
            df = back_end.read_constraints_from_excel()
            for i in tree.get_children():
                tree.delete(i)
            for _, row in df.iterrows():
                tree.insert("", "end", values=row.tolist())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load constraints: {e}")


    def check_mortgage_eligibility():
        """ Checks mortgage eligibility based on user input and displays details on GUI """
        try:
            loan_amount = float(loan_amount_var.get())
            annual_income = float(annual_income_var.get())
            capital = float(capital_var.get())
            credit_score = int(credit_score_var.get())

            result_text = back_end.analyze_eligibility(loan_amount, annual_income, capital, credit_score)

            eligibility_result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")


    # GUI Setup
    root = tk.Tk()
    root.title("Mortgage Calculator")
    root.geometry("600x600")

    # Treeview for Bank Constraints
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10)
    tree = ttk.Treeview(tree_frame, columns=(
    "Bank Name", "Base Interest Rate", "Max Loan to Income", "Min Credit Score", "Down Payment (%)"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack()

    # Input Fields
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)
    tk.Label(input_frame, text="Loan Amount (USD):").grid(row=0, column=0)
    tk.Label(input_frame, text="Annual Income (USD):").grid(row=1, column=0)
    tk.Label(input_frame, text="Capital (USD):").grid(row=2, column=0)
    tk.Label(input_frame, text="Credit Score:").grid(row=3, column=0)

    loan_amount_var = tk.StringVar()
    annual_income_var = tk.StringVar()
    capital_var = tk.StringVar()
    credit_score_var = tk.StringVar()

    entry1 = tk.Entry(input_frame, textvariable=loan_amount_var)
    entry2 = tk.Entry(input_frame, textvariable=annual_income_var)
    entry3 = tk.Entry(input_frame, textvariable=capital_var)
    entry4 = tk.Entry(input_frame, textvariable=credit_score_var)

    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry3.grid(row=2, column=1)
    entry4.grid(row=3, column=1)

    # Buttons
    tk.Button(root, text="Load Bank Constraints", command=load_bank_constraints).pack(pady=5)
    tk.Button(root, text="Check Mortgage Eligibility", command=check_mortgage_eligibility).pack(pady=5)

    # Eligibility Results Display
    eligibility_result_label = tk.Label(root, text="", justify="left", wraplength=500, fg="blue")
    eligibility_result_label.pack(pady=10)

    root.mainloop()
