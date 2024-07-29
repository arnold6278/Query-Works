import tkinter
import tkinter.messagebox
import tkinter.filedialog
import customtkinter
import pyodbc
import csv

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("QueryWorks")
        self.geometry(f"{1100}x580")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Server details frame
        self.server_frame = customtkinter.CTkFrame(self)
        self.server_frame.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")
        self.server_frame.grid_columnconfigure(4, weight=1)

        self.servername_label = customtkinter.CTkLabel(self.server_frame, text="Server Name:")
        self.servername_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.servername_entry = customtkinter.CTkEntry(self.server_frame)
        self.servername_entry.grid(row=0, column=4, padx=10, pady=10, sticky="we")

        self.database_label = customtkinter.CTkLabel(self.server_frame, text="Database:")
        self.database_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.database_entry = customtkinter.CTkEntry(self.server_frame)
        self.database_entry.grid(row=1, column=4, padx=10, pady=10, sticky="we")

        self.username_label = customtkinter.CTkLabel(self.server_frame, text="Username:")
        self.username_label.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        self.username_entry = customtkinter.CTkEntry(self.server_frame)
        self.username_entry.grid(row=2, column=4, padx=10, pady=10, sticky="we")

        self.password_label = customtkinter.CTkLabel(self.server_frame, text="Password:")
        self.password_label.grid(row=3, column=3, padx=10, pady=10, sticky="w")
        self.password_entry = customtkinter.CTkEntry(self.server_frame, show="*")
        self.password_entry.grid(row=3, column=4, padx=10, pady=10, sticky="we")

        # create main entry and buttons
        self.entry = customtkinter.CTkEntry(self, placeholder_text="SQL Query")
        self.entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.connect_button = customtkinter.CTkButton(master=self, text="Connect to Database", command=self.toggle_connection)
        self.connect_button.grid(row=0, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.execute_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Execute Query", command=self.execute_sql_query)
        self.execute_button.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # Add Save as CSV button
        self.save_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Save as CSV", command=self.save_as_csv)
        self.save_button.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(30, 0), sticky="nsew")

        # create connectivity status label
        self.status_label = customtkinter.CTkLabel(self, text="Not Connected", text_color="red")
        self.status_label.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="w")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Database connection settings
        self.server_name = ""
        self.database = ""
        self.username = ""
        self.password = ""
        self.connection = None
        self.query_results = []  # Store query results for CSV export
        self.connected = False  # Track connection status

    def toggle_connection(self):
        if self.connected:
            self.disconnect_from_database()
        else:
            self.connect_to_database()

    def connect_to_database(self):
        # Get the connection details from the entries
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

    def execute_sql_query(self):
        if not self.connected:
            tkinter.messagebox.showerror("Not Connected", "You must connect to the database first.")
            return

        query = self.entry.get().strip()
        if not query.upper().startswith("SELECT"):
            tkinter.messagebox.showerror("Invalid Query", "Only SELECT queries are allowed.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.query_results = [columns] + rows
            self.textbox.delete("1.0", tkinter.END)
            for row in rows:
                self.textbox.insert(tkinter.END, str(row) + "\n")
            cursor.close()
        except pyodbc.Error as e:
            tkinter.messagebox.showerror("Query Execution Error", f"Error executing SQL query:\n{e}")

    def save_as_csv(self):
        if not self.query_results:
            tkinter.messagebox.showwarning("No Data", "There is no data to save.")
            return

        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(self.query_results)
            tkinter.messagebox.showinfo("Success", f"Data saved to {file_path}")
        except Exception as e:
            tkinter.messagebox.showerror("Save Error", f"Error saving CSV file:\n{e}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
