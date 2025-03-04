import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import back_end


# Function to load bank constraints into the Treeview table
def load_bank_constraints():
    """ Load bank constraints and display them in the tree view """
    try:
        # Ensure the function exists in the back_end module
        if not hasattr(back_end, "read_constraints_from_excel"):
            raise AttributeError("Function 'read_constraints_from_excel' not found in back_end module.")

        df = back_end.read_constraints_from_excel()

        # Display a warning if no data is available
        if df.empty:
            messagebox.showwarning("No Data", "No bank constraints found. Ensure constraints_data.xlsx exists.")
            return

        # Clear existing entries in the Treeview
        for i in tree.get_children():
            tree.delete(i)

        # Insert bank constraints into the table
        for _, row in df.iterrows():
            tree.insert("", "end", values=row.tolist())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load constraints: {e}")


# Function to check mortgage eligibility based on user input
def check_mortgage_eligibility():
    """ Checks mortgage eligibility based on user input and displays details on GUI """
    try:
        # Retrieve values entered by the user
        loan_amount = float(loan_amount_var.get())
        annual_income = float(annual_income_var.get())
        capital = float(capital_var.get())
        credit_score = int(credit_score_var.get())

        # Get eligibility results from the back-end function
        result_text = back_end.analyze_eligibility(loan_amount, annual_income, capital, credit_score)

        # Display results in the text box
        eligibility_result_text.config(state=tk.NORMAL)  # Enable editing
        eligibility_result_text.delete("1.0", tk.END)  # Clear previous results
        eligibility_result_text.insert(tk.END, result_text if result_text else "No data available.")
        eligibility_result_text.config(state=tk.DISABLED)  # Disable editing
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")


# GUI Setup
root = tk.Tk()
root.title("Mortgage Calculator")  # Set window title
root.geometry("750x650")  # Set window size

# Treeview for displaying bank constraints
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)
tree = ttk.Treeview(tree_frame, columns=(
"Bank Name", "Base Interest Rate", "Max Loan to Income", "Min Credit Score", "Down Payment (%)"), show="headings")

# Set column headings and size
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack()

# Input Fields Section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
tk.Label(input_frame, text="Loan Amount (USD):").grid(row=0, column=0)
tk.Label(input_frame, text="Annual Income (USD):").grid(row=1, column=0)
tk.Label(input_frame, text="Capital (USD):").grid(row=2, column=0)
tk.Label(input_frame, text="Credit Score:").grid(row=3, column=0)

# Variables to store user input
loan_amount_var = tk.StringVar()
annual_income_var = tk.StringVar()
capital_var = tk.StringVar()
credit_score_var = tk.StringVar()

# Entry fields for user input
entry1 = tk.Entry(input_frame, textvariable=loan_amount_var)
entry2 = tk.Entry(input_frame, textvariable=annual_income_var)
entry3 = tk.Entry(input_frame, textvariable=capital_var)
entry4 = tk.Entry(input_frame, textvariable=credit_score_var)

# Position entry fields on the grid
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)
entry4.grid(row=3, column=1)

# Buttons to load bank constraints and check eligibility
tk.Button(root, text="Load Bank Constraints", command=load_bank_constraints).pack(pady=5)
tk.Button(root, text="Check Mortgage Eligibility", command=check_mortgage_eligibility).pack(pady=5)

# Textbox for displaying eligibility results
eligibility_result_text = tk.Text(root, height=15, width=85, wrap=tk.WORD, state=tk.DISABLED)
eligibility_result_text.pack(pady=10)

# Ensure GUI starts immediately
if __name__ == "__main__":
    root.mainloop()