# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import mysql.connector
# from client_record import show_client_record

# # ---------------- DATABASE CONNECTION ----------------
# def get_client_by_id(client_id):
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="abc123",
#         database="qr_secure_db"
#     )
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
#     client = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return client

# # ---------------- LOGIN LAUNCH ----------------
# def launch_login():
#     root = tk.Toplevel()
#     root.title("\U0001F3E0 Client QR Login")
#     root.geometry("400x250")
#     root.configure(bg="#f5f5f5")

#     tk.Label(
#         root,
#         text="\U0001F50D QR Code Login Simulation",
#         font=("Helvetica", 14, "bold"),
#         bg="#003366",
#         fg="white",
#         pady=10
#     ).pack(fill="x")

#     tk.Label(
#         root,
#         text="Enter your Client ID to simulate QR scan:",
#         font=("Arial", 11),
#         bg="#f5f5f5",
#         pady=10
#     ).pack()

#     id_entry = tk.Entry(root, font=("Arial", 11), width=30, relief="groove", bd=2)
#     id_entry.pack(pady=10)

#     status = tk.Label(root, text="", font=("Arial", 10), bg="#f5f5f5", fg="red")
#     status.pack()

#     def submit_id():
#         client_id = id_entry.get().strip()
#         if not client_id:
#             status.config(text="\u26A0\uFE0F Please enter a Client ID")
#             return

#         try:
#             client = get_client_by_id(client_id)
#             if client:
#                 ask_pin(root, client)
#             else:
#                 status.config(text="\u274C Client not found.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Database error: {str(e)}")

#     tk.Button(
#         root, text="\u2705 Submit", command=submit_id,
#         font=("Arial", 11, "bold"), bg="#0066cc", fg="white",
#         padx=10, pady=5, relief="raised"
#     ).pack(pady=10)

#     tk.Label(
#         root, text="Secure Access Only", font=("Arial", 9, "italic"),
#         bg="#f5f5f5", fg="#666"
#     ).pack(pady=10)

# # ---------------- PIN ENTRY WINDOW ----------------
# def ask_pin(parent, client):
#     pin_window = tk.Toplevel(parent)
#     pin_window.title("\U0001F510 Secure PIN Verification")
#     pin_window.geometry("350x220")
#     pin_window.configure(bg="#f5f5f5")
#     pin_window.resizable(False, False)

#     tk.Label(
#         pin_window,
#         text="\U0001F512 Enter Your 4-Digit PIN",
#         font=("Helvetica", 14, "bold"),
#         bg="#003366",
#         fg="white",
#         pady=10
#     ).pack(fill="x")

#     tk.Label(
#         pin_window,
#         text=f"Welcome, {client['name']} \U0001F44B",
#         font=("Arial", 11),
#         bg="#f5f5f5",
#         pady=15
#     ).pack()

#     pin_entry = tk.Entry(
#         pin_window,
#         font=("Arial", 12),
#         show="*",
#         justify="center",
#         width=10,
#         bd=2,
#         relief="groove"
#     )
#     pin_entry.pack(pady=5)

#     status = tk.Label(pin_window, text="", font=("Arial", 9), bg="#f5f5f5", fg="red")
#     status.pack(pady=(5, 0))

#     def validate_pin():
#         entered = pin_entry.get()
#         if entered == client["pin"]:
#             pin_window.destroy()
#             parent.destroy()
#             show_client_record(client)
#         else:
#             status.config(text="\u274C Incorrect PIN. Please try again.")

#     tk.Button(
#         pin_window,
#         text="\u2714 Verify",
#         font=("Arial", 11, "bold"),
#         bg="#009933",
#         fg="white",
#         width=15,
#         command=validate_pin
#     ).pack(pady=15)

#     pin_entry.focus()
