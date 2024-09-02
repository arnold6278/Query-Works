import tkinter
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
import customtkinter
import pyodbc
import csv
from tkinter import font
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Define a bold font style
        self.bold_font = ("Arial", 12, "bold")

        # configure window
        self.title("QUERYWORKS")
        self.geometry(f"{1200}x700")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Sidebar
        self.grid_columnconfigure(1, weight=3)  # Main content area
        self.grid_columnconfigure(2, weight=3)  # Display frame
        self.grid_columnconfigure(3, weight=0)  # Buttons
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=self.bold_font)
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=self.bold_font)
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Server details frame
        self.server_frame = customtkinter.CTkFrame(self)
        self.server_frame.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")
        self.server_frame.grid_columnconfigure(4, weight=1)

        self.servername_label = customtkinter.CTkLabel(self.server_frame, text="Server Name:", font=self.bold_font)
        self.servername_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.servername_entry = customtkinter.CTkEntry(self.server_frame)
        self.servername_entry.grid(row=0, column=4, padx=10, pady=10, sticky="we")

        self.database_label = customtkinter.CTkLabel(self.server_frame, text="Database:", font=self.bold_font)
        self.database_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.database_entry = customtkinter.CTkEntry(self.server_frame)
        self.database_entry.grid(row=1, column=4, padx=10, pady=10, sticky="we")

        self.username_label = customtkinter.CTkLabel(self.server_frame, text="Username:", font=self.bold_font)
        self.username_label.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        self.username_entry = customtkinter.CTkEntry(self.server_frame)
        self.username_entry.grid(row=2, column=4, padx=10, pady=10, sticky="we")

        self.password_label = customtkinter.CTkLabel(self.server_frame, text="Password:", font=self.bold_font)
        self.password_label.grid(row=3, column=3, padx=10, pady=10, sticky="w")
        self.password_entry = customtkinter.CTkEntry(self.server_frame, show="*")
        self.password_entry.grid(row=3, column=4, padx=10, pady=10, sticky="we")

        # create main entry and buttons
        self.entry = customtkinter.CTkEntry(self, placeholder_text="SQL Query")
        self.entry.grid(row=0, column=1, columnspan=2, padx=(20, 10), pady=(0, 0), sticky="nsew")

        self.connect_button = customtkinter.CTkButton(master=self, text="Connect To Database", command=self.toggle_connection, fg_color="cornflower blue", text_color="white", font=self.bold_font)
        self.connect_button.grid(row=0, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.execute_button = customtkinter.CTkButton(master=self, fg_color="cornflower blue", border_width=1, text_color=("white", "#DCE4EE"), text="Execute Query", command=self.execute_sql_query, font=self.bold_font)
        self.execute_button.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # Add Save File button
        self.save_button = customtkinter.CTkButton(master=self, fg_color="cornflower blue", border_width=1, text_color=("white", "#DCE4EE"), text="Save File", command=self.save_file, font=self.bold_font)
        self.save_button.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # create textbox (Display frame)
        self.textbox_frame = customtkinter.CTkFrame(self)
        self.textbox_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(30, 0), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self.textbox_frame, width=500)
        self.textbox.pack(expand=True, fill="both")

        # create connectivity status label
        self.status_label = customtkinter.CTkLabel(self, text="Not Connected", text_color="red", font=self.bold_font)
        self.status_label.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="w")

        # Adjust layout to fill the space
        self.log_frame = customtkinter.CTkFrame(self)
        self.log_frame.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(10, 20), sticky="nsew")
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=0)
        self.log_frame.grid_columnconfigure(0, weight=1)

        self.log_textbox = customtkinter.CTkTextbox(self.log_frame, state="disabled", wrap="word")
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Database connection settings
        self.server_name = ""
        self.database = ""
        self.username = ""
        self.password = ""
        self.connection = None
        self.query_results = []  # Store query results for export
        self.connected = False  # Track connection status
        self.access_log = []  # Store access logs

    def toggle_connection(self):
        if self.connected:
            self.disconnect_from_database()
        else:
            self.connect_to_database()

    def connect_to_database(self):
        self.server_name = self.servername_entry.get().strip()
        self.database = self.database_entry.get().strip()
        self.username = self.username_entry.get().strip()
        self.password = self.password_entry.get().strip()

        # Check if any field is empty
        if not self.server_name or not self.database or not self.username or not self.password:
            tkinter.messagebox.showerror("Input Error", "Please fill in all the connection details.")
            return

        try:
            # Establish a connection to the database
            self.connection = pyodbc.connect(
                f"Driver={{SQL Server}};"
                f"Server={self.server_name};"
                f"Database={self.database};"
                f"uid={self.username};pwd={self.password};"
            )
            self.status_label.configure(text="Connected", text_color="green")
            self.connect_button.configure(text="Disconnect")
            self.connected = True
            self.log_access(f"Connected to the database: Server={self.server_name}, Database={self.database}")
        except pyodbc.Error as e:
            self.status_label.configure(text=f"Connection Failed: {e}", text_color="red")
            self.connection = None
            tkinter.messagebox.showerror("Connection Error", f"Failed to connect to the database:\n{e}")

    def disconnect_from_database(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            self.status_label.configure(text="Disconnected", text_color="red")
            self.connect_button.configure(text="Connect to Database")
            self.connected = False

            # Clear server details but not the query entry
            self.servername_entry.delete(0, tkinter.END)
            self.username_entry.delete(0, tkinter.END)
            self.database_entry.delete(0, tkinter.END)
            self.password_entry.delete(0, tkinter.END)
            
            # Clear the textboxes
            self.clear_textbox()
            
            self.log_access("Disconnected from the database")

    def clear_textbox(self):
        # Clear the query results textbox
        self.textbox.delete("1.0", tkinter.END)
        # Clear the log textbox
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tkinter.END)
        self.log_textbox.configure(state="disabled")

    def execute_sql_query(self):
        if not self.connected:
            tkinter.messagebox.showerror("Not Connected", "You must connect to the database first.")
            return

        query = self.entry.get().strip()
        if not query.upper().startswith("SELECT"):
            tkinter.messagebox.showerror("Invalid Query", "Only SELECT queries are allowed.")
            return

        try:
            # Clear previous results and logs
            self.clear_textbox()

            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.query_results = [columns] + rows
            self.textbox.delete("1.0", tkinter.END)

            # Display server and database information
            header = f"Server Name: {self.server_name}\nDatabase: {self.database}\n\n"
            self.textbox.insert(tkinter.END, header)
            
            # Display query results
            for row in rows:
                self.textbox.insert(tkinter.END, str(row) + "\n")

            cursor.close()
            self.log_access(f"Executed query: {query} - Success")
        except pyodbc.Error as e:
            error_message = f"Error executing SQL query: {e}"
            tkinter.messagebox.showerror("Query Execution Error", error_message)
            self.log_access(f"Executed query: {query} - Failed: {error_message}")

    def save_file(self):
        if not self.query_results:
            tkinter.messagebox.showwarning("No Data", "There is no data to save.")
            return

        file_type = tkinter.simpledialog.askstring("File Type", "Enter file type (CSV or PDF):").strip().lower()
        if file_type not in ["csv", "pdf"]:
            tkinter.messagebox.showerror("Invalid File Type", "Please enter 'CSV' or 'PDF'.")
            return

        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=f".{file_type}", filetypes=[(f"{file_type.upper()} files", f"*.{file_type}"), ("All files", "*.*")])
        if not file_path:
            return

        try:
            if file_type == "csv":
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.query_results)
                tkinter.messagebox.showinfo("Success", f"Data saved to {file_path}")
                self.log_access(f"Data saved to {file_path}")
            elif file_type == "pdf":
                c = canvas.Canvas(file_path, pagesize=letter)
                width, height = letter
                x = 40
                y = height - 40
                line_height = 20

                for row in self.query_results:
                    text = " | ".join(str(cell) for cell in row)
                    c.drawString(x, y, text)
                    y -= line_height
                    if y < 40:
                        c.showPage()
                        y = height - 40

                c.save()
                tkinter.messagebox.showinfo("Success", f"Data saved to {file_path}")
                self.log_access(f"Data saved to {file_path}")
        except Exception as e:
            tkinter.messagebox.showerror("Save Error", f"Error saving file:\n{e}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def log_access(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.access_log.append(f"{timestamp}: {action}")
        self.update_access_log_display()

    def update_access_log_display(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tkinter.END)
        for entry in self.access_log:
            self.log_textbox.insert(tkinter.END, entry + "\n")
        self.log_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()

