import tkinter as tk
# from client_login import launch_login
from admin_panel import launch_admin_panel



# Call show_admin_login() when "Admin" button is clicked
def main():
    root = tk.Tk()
    root.title("🏠 Real Estate - Secure Client System")
    root.geometry("400x550")
    root.configure(bg="#f5f5f5")

    # ------------ Header ------------
    header = tk.Label(
        root,
        text="🏠 Secure Client Record System",
        font=("Helvetica", 16, "bold"),
        bg="#003366",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    # ------------ Logo (Optional) ------------
    try:
        logo_img = tk.PhotoImage(file="assets/logo.png")  # optional image
        tk.Label(root, image=logo_img, bg="#f5f5f5").pack(pady=(30, 10))
    except:
        pass  # No image? Skip logo display

    # ------------ Welcome Text ------------
    tk.Label(
        root,
        text="Welcome to the Real Estate Client Portal",
        font=("Arial", 11, "italic"),
        bg="#f5f5f5",
        fg="#333"
    ).pack(pady=(10, 30))

    # # ------------ Buttons ------------
    # tk.Button(
    #     root, text="📷 Client Login", command=launch_login,
    #     font=("Arial", 12, "bold"), bg="#0066cc", fg="white",
    #     width=25, height=2, relief="raised", bd=3
    # ).pack(pady=20)

    tk.Button(
        root, text="🛠 Admin Panel", command=launch_admin_panel,
        font=("Arial", 12, "bold"), bg="#009933", fg="white",
        width=25, height=2, relief="raised", bd=3
    ).pack()

    # ------------ Footer ------------
    tk.Label(
        root,
        text="© 2025 EstateSecure Systems",
        font=("Arial", 9), bg="#f5f5f5", fg="#999"
    ).pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
