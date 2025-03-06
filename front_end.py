import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import back_end
import time

def show_splash():
    splash = tk.Tk()
    splash.title("Welcome")
    splash.geometry("400x200")
    splash.configure(bg="white")

    label = tk.Label(splash, text="💰🏠", font=("Arial", 50), fg="darkgreen", bg="white")
    label.pack(expand=True)

    welcome_text = tk.Label(splash, text="Welcome to our Mortgage Calculator", font=("Arial", 12), bg="white")
    welcome_text.place(x=-200, y=150)

    def slide_text():
        for i in range(-200, 200, 2):
            welcome_text.place(x=i, y=150)
            splash.update()
            time.sleep(0.03)

    slide_text()
    time.sleep(1)
    splash.destroy()

show_splash()

root = tk.Tk()
root.title("Mortgage Calculator")
root.geometry("750x650")

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)
tree = ttk.Treeview(tree_frame, columns=(
"Bank Name", "Base Interest Rate", "Max Loan to Income", "Min Credit Score", "Down Payment (%)"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack()

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

def load_bank_constraints():
    try:
        df = back_end.read_constraints_from_excel()

        if df.empty:
            messagebox.showwarning("No Data", "No bank constraints found. Ensure constraints_data.xlsx exists.")
            return

        for i in tree.get_children():
            tree.delete(i)

        for _, row in df.iterrows():
            tree.insert("", "end", values=row.tolist())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load constraints: {e}")

def check_mortgage_eligibility():
    try:
        loan_amount = float(loan_amount_var.get())
        annual_income = float(annual_income_var.get())
        capital = float(capital_var.get())
        credit_score = int(credit_score_var.get())

        result_text = back_end.analyze_eligibility(loan_amount, annual_income, capital, credit_score)

        eligibility_result_text.config(state=tk.NORMAL)
        eligibility_result_text.delete("1.0", tk.END)
        eligibility_result_text.insert(tk.END, result_text if result_text else "No data available.")
        eligibility_result_text.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

tk.Button(root, text="Load Bank Constraints", command=load_bank_constraints).pack(pady=5)
tk.Button(root, text="Check Mortgage Eligibility", command=check_mortgage_eligibility).pack(pady=5)

eligibility_result_text = tk.Text(root, height=15, width=85, wrap=tk.WORD, state=tk.DISABLED)
eligibility_result_text.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()