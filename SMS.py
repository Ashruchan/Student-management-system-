import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# === CONFIG ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === GLOBAL STATE ===
DB_NAME = "sms"
DB_USER = "root"
DB_HOST = "localhost"
DB_PASSWORD = None  # Will be set by GUI prompt

# === GUI Root ===
app = ctk.CTk()
app.title("Student Management System")
app.geometry("1000x650")
app.configure(bg="#fff07c")  # Yellow background

# === FONT STYLES ===
TITLE_FONT = ("Segoe UI", 26, "bold")
LABEL_FONT = ("Segoe UI", 16)
BUTTON_FONT = ("Segoe UI", 15, "bold")
ENTRY_FONT = ("Segoe UI", 14)

# === DB Connection ===
def connect_to_mysql():
    global DB_PASSWORD
    while True:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            if conn.is_connected():
                return conn
        except Error as e:
            DB_PASSWORD = prompt_password("Enter MySQL Root Password")
            if not DB_PASSWORD:
                app.destroy()
                exit()

def prompt_password(title):
    dialog = ctk.CTkInputDialog(title=title, text="MySQL Root Password:")
    return dialog.get_input()

def initialize_database():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cursor.close()
    conn.close()

    create_tables()

def create_tables():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            dob DATE,
            gender VARCHAR(20),
            email VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            enrollment_date DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            amount DECIMAL(10,2),
            payment_date DATE,
            payment_method VARCHAR(50),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def execute_query(query, params=()):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_data(query, params=()):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# === UI COMPONENTS ===

main_frame = ctk.CTkFrame(app, fg_color="#fff07c")
main_frame.pack(expand=True, fill="both", padx=30, pady=30)

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def main_menu():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Student Management System", font=TITLE_FONT, text_color="black").pack(pady=25)

    buttons = [
        ("Add Student", add_student_form),
        ("View Students", view_students),
        ("Add Payment", add_payment_form),
        ("Check Payments", check_payments),
        ("Delete Student", delete_student_form),
    ]

    for text, command in buttons:
        ctk.CTkButton(main_frame, text=text, font=BUTTON_FONT, command=command, height=40, width=240, fg_color="white", text_color="black").pack(pady=10)

def add_student_form():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Add New Student", font=TITLE_FONT, text_color="black").pack(pady=10)

    fields = ["First Name", "Last Name", "Date of Birth (YYYY-MM-DD)", "Gender", "Email", "Phone", "Address", "Enrollment Date"]
    entries = []

    for field in fields:
        ctk.CTkLabel(main_frame, text=field, font=LABEL_FONT, text_color="black").pack()
        entry = ctk.CTkEntry(main_frame, font=ENTRY_FONT, width=400)
        entry.pack(pady=4)
        entries.append(entry)

    def save():
        values = [e.get() for e in entries]
        query = """
            INSERT INTO students
            (first_name, last_name, dob, gender, email, phone, address, enrollment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, values)
        messagebox.showinfo("Success", "Student added successfully!")
        main_menu()

    ctk.CTkButton(main_frame, text="Submit", command=save, font=BUTTON_FONT, fg_color="white", text_color="black").pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=main_menu, font=BUTTON_FONT, fg_color="white", text_color="black").pack()

def view_students():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Student Records", font=TITLE_FONT, text_color="black").pack(pady=10)

    data = fetch_data("SELECT * FROM students")

    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=900, height=450)
    scroll_frame.pack()

    headers = ["ID", "First Name", "Last Name", "DOB", "Gender", "Email", "Phone", "Address", "Enroll Date"]
    for j, header in enumerate(headers):
        ctk.CTkLabel(scroll_frame, text=header, font=("Segoe UI", 14, "bold"), width=120, text_color="black").grid(row=0, column=j)

    for i, row in enumerate(data, start=1):
        for j, val in enumerate(row):
            ctk.CTkLabel(scroll_frame, text=str(val), font=("Segoe UI", 12), width=120, text_color="black").grid(row=i, column=j)

    ctk.CTkButton(main_frame, text="Back", command=main_menu, font=BUTTON_FONT, fg_color="white", text_color="black").pack(pady=10)

def delete_student_form():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Delete Student", font=TITLE_FONT, text_color="black").pack(pady=10)

    ctk.CTkLabel(main_frame, text="Enter Student ID:", font=LABEL_FONT, text_color="black").pack()
    student_id_entry = ctk.CTkEntry(main_frame, font=ENTRY_FONT)
    student_id_entry.pack(pady=5)

    def delete():
        sid = student_id_entry.get()
        execute_query("DELETE FROM students WHERE student_id=%s", (sid,))
        messagebox.showinfo("Deleted", f"Student ID {sid} deleted.")
        main_menu()

    ctk.CTkButton(main_frame, text="Delete", command=delete, font=BUTTON_FONT, fg_color="white", text_color="black").pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=main_menu, font=BUTTON_FONT, fg_color="white", text_color="black").pack()

def add_payment_form():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Add Payment", font=TITLE_FONT, text_color="black").pack(pady=10)

    fields = ["Student ID", "Amount", "Payment Date (YYYY-MM-DD)", "Payment Method"]
    entries = []

    for field in fields:
        ctk.CTkLabel(main_frame, text=field, font=LABEL_FONT, text_color="black").pack()
        entry = ctk.CTkEntry(main_frame, font=ENTRY_FONT, width=400)
        entry.pack(pady=4)
        entries.append(entry)

    def save_payment():
        values = [e.get() for e in entries]
        query = """
            INSERT INTO payments (student_id, amount, payment_date, payment_method)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query, values)
        messagebox.showinfo("Success", "Payment recorded.")
        main_menu()

    ctk.CTkButton(main_frame, text="Submit", command=save_payment, font=BUTTON_FONT, fg_color="white", text_color="black").pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=main_menu, font=BUTTON_FONT, fg_color="white", text_color="black").pack()

def check_payments():
    clear_frame()
    ctk.CTkLabel(main_frame, text="Check Payment Status", font=TITLE_FONT, text_color="black").pack(pady=10)

    ctk.CTkLabel(main_frame, text="Enter Student ID:", font=LABEL_FONT, text_color="black").pack()
    entry = ctk.CTkEntry(main_frame, font=ENTRY_FONT)
    entry.pack(pady=4)

    def check():
        sid = entry.get()
        payments = fetch_data("SELECT amount, payment_date, payment_method FROM payments WHERE student_id=%s", (sid,))
        if not payments:
            messagebox.showinfo("No Payments", "No payments found.")
        else:
            result = "\n".join([f"₹{p[0]} on {p[1]} via {p[2]}" for p in payments])
            messagebox.showinfo("Payments", result)

    ctk.CTkButton(main_frame, text="Check", command=check, font=BUTTON_FONT, fg_color="white", text_color="black").pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=main_menu, font=BUTTON_FONT, fg_color="white", text_color="black").pack()

# === MAIN ===
if __name__ == '__main__':
    initialize_database()
    main_menu()
    app.mainloop()
