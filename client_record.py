import tkinter as tk

def show_client_record(client):
    win = tk.Toplevel()
    win.title("🏡 Client Record")
    win.geometry("500x500")
    win.configure(bg="#f5f5f5")

    # ---------- Header ----------
    tk.Label(
        win,
        text="🏡 Real Estate Client Record",
        font=("Helvetica", 18, "bold"),
        bg="#003366",
        fg="white",
        pady=15
    ).pack(fill="x")

    # ---------- Record Frame ----------
    frame = tk.Frame(win, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # ---------- Client Data ----------
    remaining = int(client["total_price"]) - int(client["paid_amount"])

    rows = [
        ("Client Name", client["name"]),
        ("Plot Number", client["plot_no"]),
        ("Block", client["block"]),
        ("Location", client["location"]),
        ("Total Price", f"PKR {client['total_price']:,}"),
        ("Paid Amount", f"PKR {client['paid_amount']:,}"),
        ("Remaining Balance", f"PKR {remaining:,}"),
        ("Last Payment Date", client["last_payment_date"])
    ]

    for label, value in rows:
        row = tk.Frame(frame, bg="#ffffff")
        row.pack(fill="x", pady=6)

        tk.Label(row, text=label + ":", width=18, anchor="w",
                 font=("Arial", 11, "bold"), bg="#ffffff").pack(side="left")

        tk.Label(row, text=value, anchor="w", font=("Arial", 11),
                 bg="#ffffff", fg="#333").pack(side="left", fill="x", expand=True)

    # ---------- Footer ----------
    tk.Label(
        win,
        text="🔒 Secure Access • Client Confidential",
        font=("Arial", 9, "italic"),
        bg="#f5f5f5",
        fg="#888"
    ).pack(pady=(10, 15))
