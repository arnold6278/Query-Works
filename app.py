import tkinter
import customtkinter
import pyodbc
import pandas as pd
from tkinter import filedialog, messagebox, Toplevel
from database import connect_to_database, execute_query
from visualization import VisualizationWindow

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Define a bold font style
        self.bold_font = ("Arial", 12, "bold")

        # Configure window
        self.title("QUERYWORKS")
        self.geometry(f"{1200}x700")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Sidebar
        self.grid_columnconfigure(1, weight=3)  # Main content area
        self.grid_columnconfigure(2, weight=3)  # Display frame
        self.grid_columnconfigure(3, weight=0)  # Buttons
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Create sidebar frame with widgets
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

        # Create main entry and buttons
        self.entry = customtkinter.CTkEntry(self, placeholder_text="SQL Query")
        self.entry.grid(row=0, column=1, columnspan=2, padx=(20, 10), pady=(0, 0), sticky="nsew")

        self.connect_button = customtkinter.CTkButton(master=self, text="Connect To Database", command=self.toggle_connection, fg_color="cornflower blue", text_color="white", font=self.bold_font)
        self.connect_button.grid(row=3, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.execute_button = customtkinter.CTkButton(master=self, fg_color="cornflower blue", border_width=0, text_color=("white", "#DCE4EE"), text="Execute Query", command=self.execute_sql_query, font=self.bold_font)
        self.execute_button.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # Add Save File button
        self.save_button = customtkinter.CTkButton(master=self, fg_color="cornflower blue", border_width=0, text_color=("white", "#DCE4EE"), text="Save File", command=self.save_file, font=self.bold_font)
        self.save_button.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # Add Data Visualization button
        self.visualize_button = customtkinter.CTkButton(master=self, fg_color="cornflower blue", border_width=0, text_color=("white", "#DCE4EE"), text="Data Visualization", command=self.open_visualization_window, font=self.bold_font)
        self.visualize_button.grid(row=0, column=3, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # Create textbox (Display frame)
        self.textbox_frame = customtkinter.CTkFrame(self)
        self.textbox_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(30, 0), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self.textbox_frame, width=500)
        self.textbox.pack(expand=True, fill="both")

        # Create connectivity status label
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
        self.query_results = pd.DataFrame()  # Store query results for export
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

        if not all([self.server_name, self.database, self.username, self.password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            self.connection = connect_to_database(self.server_name, self.database, self.username, self.password)
            self.connected = True
            self.status_label.configure(text="Connected", text_color="green")
            self.log("Connected to database.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log("Connection failed: " + str(e))

    def disconnect_from_database(self):
        if self.connection:
            self.connection.close()
            self.connected = False
            self.status_label.configure(text="Not Connected", text_color="red")
            self.log("Disconnected from database.")

    def execute_sql_query(self):
        if not self.connected:
            messagebox.showerror("Error", "Not connected to a database.")
            return

        query = self.entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a query.")
            return

        try:
            self.query_results = execute_query(self.connection, query)
            self.textbox.configure(state="normal")
            self.textbox.delete("1.0", tkinter.END)
            self.textbox.insert("1.0", self.query_results.to_string(index=False))
            self.textbox.configure(state="disabled")
            self.log("Query executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log("Query execution failed: " + str(e))

    def log(self, message):
        self.access_log.append(f"{datetime.now()}: {message}")
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tkinter.END)
        self.log_textbox.insert("1.0", "\n".join(self.access_log))
        self.log_textbox.configure(state="disabled")

    def save_file(self):
        if self.query_results.empty:
            messagebox.showerror("Error", "No data to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        self.query_results.to_csv(file_path, index=False)
        messagebox.showinfo("Info", "File saved successfully.")

    def change_appearance_mode_event(self, new_mode):
        customtkinter.set_appearance_mode(new_mode)

    def change_scaling_event(self, new_scaling):
        customtkinter.set_widget_scaling(float(new_scaling[:-1]) / 100)

    def open_visualization_window(self):
        if self.query_results.empty:
            messagebox.showerror("Error", "No data available for visualization.")
            return

        VisualizationWindow(self.query_results)

if __name__ == "__main__":
    app = App()
    app.mainloop()
