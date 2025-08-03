import tkinter as tk
from tkinter import ttk, messagebox
import os
import qrcode
from fpdf import FPDF
from database import load_clients, insert_client, update_client_db, delete_client_db, get_client_by_id

# -------------------- QR CODE --------------------
def generate_qr(client_id):
    client = get_client_by_id(client_id)
    if not client:
        return None
    url = f"client_login://{client_id}?pin={client.get('pin', '0000')}"
    img = qrcode.make(url)
    path = f"assets/qrcodes/{client_id}.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path

# -------------------- PDF GENERATION --------------------
def generate_pdf(client):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 15, txt="Real Estate Client Record", ln=True, align="C")
    pdf.ln(5)

    qr_path = generate_qr(client["id"])
    if qr_path:
        pdf.image(qr_path, x=150, y=35, w=40)

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(200, 10, txt="CNIC : _________________________", ln=True)
    pdf.cell(200, 10, txt="Heirship : ____________________", ln=True)
    pdf.ln(5)

    remaining = int(client["total_price"]) - int(client["paid_amount"])
    client_lines = [
        f"Client ID: {client['id']}",
        f"Name: {client['name']}",
        f"Father Name: {client['father_name']}",
        f"Plot No: {client['plot_no']}",
        f"Block: {client['block']}",
        f"Location: {client['location']}",
        f"Total Price: PKR {client['total_price']:,}",
        f"Paid Amount: PKR {client['paid_amount']:,}",
        f"Remaining Balance: PKR {remaining:,}",
        f"Last Payment Date: {client['last_payment_date']}"
    ]

    for line in client_lines:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.ln(20)
    pdf.cell(100, 10, txt="Owner Signature: ____________________", ln=False)
    pdf.cell(90, 10, txt="Approval Stamp: ____________________", ln=True)

    os.makedirs("pdf_outputs", exist_ok=True)
    pdf.output(f"pdf_outputs/{client['id']}_record.pdf", "F")


# -------------------- ADMIN PANEL --------------------
def launch_admin_panel():
    win = tk.Toplevel()
    win.title("\U0001F3E0 Real Estate Admin Panel")
    win.geometry("600x750")
    win.configure(bg="#f5f5f5")

    tk.Label(win, text="\U0001F6E0 Admin Panel", font=("Helvetica", 16, "bold"), bg="#003366", fg="white", pady=10).pack(fill="x")
    tk.Label(win, text="Manage client records efficiently", font=("Arial", 11, "italic"), bg="#f5f5f5", fg="#333").pack(pady=(10, 20))

    def clear_form():
        for e in entries.values():
            e.delete(0, tk.END)

    def add_client():
        try:
            client = {k: entries[k].get().strip() for k in fields}
            if not all(client.values()):
                status_label.config(text="\u26A0\uFE0F Fill all fields", fg="red")
                return
            client["total_price"] = int(client["total_price"].replace(",", ""))
            client["paid_amount"] = int(client["paid_amount"].replace(",", ""))

            if client["paid_amount"] > client["total_price"]:
                status_label.config(text="\u274C Paid > Total", fg="red")
                return

            insert_client(client)
            generate_pdf(client)
            status_label.config(text="\u2705 Client Added", fg="green")
            clear_form()
        except Exception as e:
            status_label.config(text=f"\u274C Error: {str(e)}", fg="red")

    def search_client():
        client_id = entries["id"].get().strip()
        client = get_client_by_id(client_id)
        if client:
            for key in fields:
                if key != "id":
                    entries[key].delete(0, tk.END)
                    entries[key].insert(0, str(client.get(key, "")))
            status_label.config(text="\u2705 Client Found. Now edit & Update.", fg="green")
        else:
            status_label.config(text="\u274C Client not found", fg="red")

    def update_client():
        try:
            client = {k: entries[k].get().strip() for k in fields}
            client["total_price"] = int(client["total_price"].replace(",", ""))
            client["paid_amount"] = int(client["paid_amount"].replace(",", ""))
            update_client_db(client)
            generate_pdf(client)
            status_label.config(text="\u2705 Client Updated", fg="green")
        except Exception as e:
            status_label.config(text=f"\u274C Error: {str(e)}", fg="red")

    def delete_client():
        client_id = entries["id"].get().strip()
        if not client_id:
            status_label.config(text="\u26A0\uFE0F Client ID required", fg="red")
            return

        # 🔎 Check if the client exists in the database
        client = get_client_by_id(client_id)
        if not client:
            messagebox.showerror("Client Not Found", f"❌ No client found with ID: {client_id}")
            status_label.config(text="❌ Client not found", fg="red")
            return

        # 🪪 Admin PIN entry popup
        def confirm_delete():
            admin_pin = admin_pin_entry.get().strip()
            

            if not admin_pin :
                messagebox.showwarning("Missing", "Please enter both Admin PIN and Client PIN.")
                return

            if admin_pin == "4321":  # ✅ Replace this with your actual admin PIN or fetch from DB
                delete_client_db(client_id , client["pin"])
                status_label.config(text="\u2705 Client Deleted", fg="green")
                clear_form()
                popup.destroy()
            else:
                messagebox.showerror("Access Denied", "❌ Invalid Admin PIN")

        # 🔐 Create popup window
        popup = tk.Toplevel()
        popup.title("Confirm Deletion")
        popup.geometry("300x230")
        popup.configure(bg="#f5f5f5")
        popup.grab_set()

        tk.Label(popup, text="🔐 Admin Verification", font=("Arial", 13, "bold"),
                bg="#003366", fg="white", pady=10).pack(fill="x")

        tk.Label(popup, text="Enter Admin PIN:", font=("Arial", 11), bg="#f5f5f5").pack(pady=(15, 5))
        admin_pin_entry = tk.Entry(popup, show="*", font=("Arial", 11), justify="center")
        admin_pin_entry.pack()

        

        tk.Button(popup, text="🗑️ Delete Now", bg="#dc3545", fg="white", font=("Arial", 12),
                command=confirm_delete).pack(pady=20)





    def view_clients():
        viewer = tk.Toplevel(win)
        viewer.title("Client List")
        viewer.geometry("600x400")
        viewer.configure(bg="#f5f5f5")

        columns = ["ID", "Name", "Plot", "Block", "Paid", "Total", "Date"]
        tree = ttk.Treeview(viewer, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        for c in load_clients():
            tree.insert("", "end", values=(
                c.get("id"), c.get("name"), c.get("plot_no"), c.get("block"),
                f"{int(c.get('paid_amount')):,}", f"{int(c.get('total_price')):,}",
                c.get("last_payment_date")
            ))

    menu_frame = tk.Frame(win, bg="#f5f5f5")
    menu_frame.pack(pady=30)

    tk.Button(menu_frame, text="\u2795 Add Client Record", font=("Arial", 13), bg="#28a745", fg="white", command=lambda: show_form("Add"), width=30).pack(pady=5)
    tk.Button(menu_frame, text="\u270D Update Client Record", font=("Arial", 13), bg="#007bff", fg="white", command=lambda: show_form("Update"), width=30).pack(pady=5)
    tk.Button(menu_frame, text="\U0001F5D1 Delete Client Record", font=("Arial", 13), bg="#dc3545", fg="white", command=lambda: show_form("Delete"), width=30).pack(pady=5)
    tk.Button(menu_frame, text="\U0001F4CB View All Clients", font=("Arial", 13), bg="#6c757d", fg="white", command=view_clients, width=30).pack(pady=5)

    form_frame = tk.Frame(win, bg="#f5f5f5")

    fields = {
        "id": "Client ID",
        "name": "Full Name",
        "father_name": "Father Name",
        "plot_no": "Plot Number",
        "block": "Block",
        "location": "Location",
        "total_price": "Total Price",
        "paid_amount": "Paid Amount",
        "last_payment_date": "Last Payment Date",
        "pin": "4-Digit PIN"
    }

    entries = {}
    for key, label in fields.items():
        frame = tk.Frame(form_frame, bg="#f5f5f5")
        frame.pack(anchor="w", fill="x", padx=20)
        tk.Label(frame, text=label + ":", font=("Arial", 10, "bold"), bg="#f5f5f5").pack(anchor="w")
        ent = tk.Entry(frame, font=("Arial", 10))
        ent.pack(fill="x", pady=2)
        entries[key] = ent

    status_label = tk.Label(form_frame, text="", font=("Arial", 10), bg="#f5f5f5")
    status_label.pack(pady=10)

    add_btn = tk.Button(form_frame, text="\u2795 Add Client", bg="#28a745", fg="white", font=("Arial", 12), command=add_client)
    search_btn = tk.Button(form_frame, text="\U0001F50D Search Client", bg="#ffc107", fg="black", font=("Arial", 12), command=search_client)
    update_btn = tk.Button(form_frame, text="\u270D Update Client", bg="#007bff", fg="white", font=("Arial", 12), command=update_client)
    delete_btn = tk.Button(form_frame, text="\U0001F5D1 Confirm Delete", bg="#dc3545", fg="white", font=("Arial", 12), command=delete_client)

    def show_form(action):
        menu_frame.pack_forget()
        form_frame.pack(fill="both", expand=True)
        clear_form()
        status_label.config(text=f"\U0001F504 Ready to {action} client", fg="#333")

        for b in [add_btn, update_btn, search_btn, delete_btn]:
            b.pack_forget()

        for key in fields:
            entries[key].master.pack_forget()

        if action == "Delete":
            for key in ["id", "pin"]:
                entries[key].master.pack(anchor="w", fill="x", padx=20)
            delete_btn.pack()
        else:
            for key in fields:
                entries[key].master.pack(anchor="w", fill="x", padx=20)
            if action == "Add":
                add_btn.pack()
            elif action == "Update":
                search_btn.pack()
                update_btn.pack()
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    launch_admin_panel()
    root.mainloop()


