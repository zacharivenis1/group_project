import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import back_end  # Import the backend module that contains functions to read and analyze bank constraints


def load_bank_constraints():
    """
    Load bank constraints from an Excel file using the back_end module,
    and display them in the Treeview widget.
    """
    try:
        # Read the bank constraints into a DataFrame.
        df = back_end.read_constraints_from_excel()
        # Warn the user if no data is found.
        if df.empty:
            messagebox.showwarning("No Data", "No bank constraints found. Ensure constraints_data.xlsx exists.")
            return

        # Clear any existing entries in the tree view.
        for i in tree.get_children():
            tree.delete(i)

        # Insert each row from the DataFrame into the tree view.
        for _, row in df.iterrows():
            tree.insert("", "end", values=row.tolist())
    except Exception as e:
        # Show an error message if something goes wrong while loading data.
        messagebox.showerror("Error", f"Failed to load constraints: {e}")


def check_mortgage_eligibility():
    """
    Retrieves user input from the GUI, checks mortgage eligibility using the
    back_end module, and displays the results in a Text widget.
    """
    try:
        # Convert the input strings to appropriate numerical types.
        loan_amount = float(loan_amount_var.get())
        annual_income = float(annual_income_var.get())
        capital = float(capital_var.get())
        credit_score = int(credit_score_var.get())

        # Analyze eligibility using the backend function.
        result_text = back_end.analyze_eligibility(loan_amount, annual_income, capital, credit_score)

        # Enable the Text widget, clear previous content, insert the new result, then disable editing.
        eligibility_result_text.config(state=tk.NORMAL)
        eligibility_result_text.delete("1.0", tk.END)
        eligibility_result_text.insert(tk.END, result_text if result_text else "No data available.")
        eligibility_result_text.config(state=tk.DISABLED)
    except ValueError:
        # Display an error message if conversion of user inputs fails.
        messagebox.showerror("Input Error", "Please enter valid numerical values.")


# --------------------- GUI Setup ---------------------
root = tk.Tk()  # Create the main application window.
root.title("Mortgage Calculator")  # Set the window title.
root.geometry("650x600")  # Set the window size.

# Create a frame for the Treeview widget that displays bank constraints.
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

# Define the Treeview widget with specific columns.
tree = ttk.Treeview(
    tree_frame,
    columns=("Bank Name", "Base Interest Rate", "Max Loan to Income", "Min Credit Score", "Down Payment (%)"),
    show="headings"
)

# Set up headings and column widths for the Treeview.
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack()  # Display the Treeview in the frame.

# Create a frame for input fields where users enter mortgage details.
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Add labels for each input field.
tk.Label(input_frame, text="Loan Amount (USD):").grid(row=0, column=0)
tk.Label(input_frame, text="Annual Income (USD):").grid(row=1, column=0)
tk.Label(input_frame, text="Capital (USD):").grid(row=2, column=0)
tk.Label(input_frame, text="Credit Score (300 - 850):").grid(row=3, column=0)

# Define StringVar variables to hold the user input values.
loan_amount_var = tk.StringVar()
annual_income_var = tk.StringVar()
capital_var = tk.StringVar()
credit_score_var = tk.StringVar()

# Create entry widgets for each input and place them in the grid.
entry1 = tk.Entry(input_frame, textvariable=loan_amount_var)
entry2 = tk.Entry(input_frame, textvariable=annual_income_var)
entry3 = tk.Entry(input_frame, textvariable=capital_var)
entry4 = tk.Entry(input_frame, textvariable=credit_score_var)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)
entry4.grid(row=3, column=1)

# Create buttons to trigger loading bank constraints and checking eligibility.
tk.Button(root, text="Load Bank Constraints", command=load_bank_constraints).pack(pady=5)
tk.Button(root, text="Check Mortgage Eligibility", command=check_mortgage_eligibility).pack(pady=5)

# Create a Text widget to display the eligibility results, with wrapping enabled for readability.
eligibility_result_text = tk.Text(root, height=12, width=75, wrap=tk.WORD, state=tk.DISABLED)
eligibility_result_text.pack(pady=10)

# Start the GUI event loop to make the window responsive.
if __name__ == "__main__":
    root.mainloop()

