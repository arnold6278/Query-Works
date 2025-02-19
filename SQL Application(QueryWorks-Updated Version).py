import tkinter
import customtkinter
import pyodbc
import csv
from tkinter import font
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog, messagebox, Toplevel;

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
            connection_string = f"DRIVER={{SQL Server}};SERVER={self.server_name};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(connection_string)
            self.connected = True
            self.status_label.configure(text="Connected", text_color="green")
            self.log_access("Database connection established.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.configure(text="Not Connected", text_color="red")
            self.connected = False

    def disconnect_from_database(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.connected = False
            self.status_label.configure(text="Not Connected", text_color="red")
            self.log_access("Database connection closed.")

    def execute_sql_query(self):
        if not self.connected:
            messagebox.showerror("Error", "Not connected to a database.")
            return

        query = self.entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a SQL query.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            self.query_results = pd.DataFrame.from_records(rows, columns=columns)  # Convert rows to DataFrame
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", self.query_results.to_string())
            self.log_access("Query executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.query_results.empty:
            messagebox.showerror("Error", "No data to save.")
            return

        filetypes = [("CSV Files", "*.csv"), ("PDF Files", "*.pdf")]
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)
        if not file:
            return

        if file.endswith(".csv"):
            self.query_results.to_csv(file, index=False)
        elif file.endswith(".pdf"):
            self.save_as_pdf(file)
        else:
            messagebox.showerror("Error", "Unsupported file format.")

    def save_as_pdf(self, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        text_object = c.beginText(40, height - 40)
        text_object.setFont("Helvetica", 12)

        for row in self.query_results.to_dict(orient='records'):
            line = ', '.join(f"{key}: {value}" for key, value in row.items())
            text_object.textLine(line)
        
        c.drawText(text_object)
        c.showPage()
        c.save()

    def open_visualization_window(self):
        if self.query_results.empty:
            messagebox.showerror("Error", "No data available for visualization.")
            return

        VisualizationWindow(self.query_results)

    def change_appearance_mode_event(self, mode):
        customtkinter.set_appearance_mode(mode)

    def change_scaling_event(self, scaling):
        customtkinter.set_widget_scaling(float(scaling.strip('%')) / 100)

    def log_access(self, message):
        self.access_log.append(f"{datetime.now()}: {message}")
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        for log_entry in self.access_log:
            self.log_textbox.insert("end", log_entry + "\n")
        self.log_textbox.configure(state="disabled")


class VisualizationWindow(Toplevel):
    def __init__(self, data):
        super().__init__()

        self.title("Data Visualization")
        self.geometry("800x600")
        self.data = pd.DataFrame(data)

        # Create visualization options
        self.plot_type_var = tkinter.StringVar(value="scatter")
        self.x_column_var = tkinter.StringVar(value=self.data.columns[0] if not self.data.empty else "")
        self.y_column_var = tkinter.StringVar(value=self.data.columns[1] if len(self.data.columns) > 1 else "")

        self.create_widgets()

    def create_widgets(self):
        # Plot type selection
        plot_type_frame = customtkinter.CTkFrame(self)
        plot_type_frame.pack(fill="x", padx=10, pady=10)

        plot_type_label = customtkinter.CTkLabel(plot_type_frame, text="Select Plot Type:", font=("Arial", 12, "bold"))
        plot_type_label.pack(side="left")

        plot_type_menu = customtkinter.CTkOptionMenu(plot_type_frame, variable=self.plot_type_var, values=["scatter", "histogram", "pie"])
        plot_type_menu.pack(side="left", padx=10)

        plot_button = customtkinter.CTkButton(plot_type_frame, text="Generate Plot", command=self.generate_plot)
        plot_button.pack(side="left")

        # X and Y column selection
        column_frame = customtkinter.CTkFrame(self)
        column_frame.pack(fill="x", padx=10, pady=10)

        x_column_label = customtkinter.CTkLabel(column_frame, text="Select X Column:", font=("Arial", 12, "bold"))
        x_column_label.pack(side="left")

        self.x_column_menu = customtkinter.CTkOptionMenu(column_frame, variable=self.x_column_var, values=list(self.data.columns))
        self.x_column_menu.pack(side="left", padx=10)

        y_column_label = customtkinter.CTkLabel(column_frame, text="Select Y Column:", font=("Arial", 12, "bold"))
        y_column_label.pack(side="left")

        self.y_column_menu = customtkinter.CTkOptionMenu(column_frame, variable=self.y_column_var, values=list(self.data.columns))
        self.y_column_menu.pack(side="left", padx=10)

        # Plot display area
        self.plot_frame = customtkinter.CTkFrame(self)
        self.plot_frame.pack(expand=True, fill="both")

    def generate_plot(self):
        plot_type = self.plot_type_var.get()
        x_column = self.x_column_var.get()
        y_column = self.y_column_var.get()

        if x_column not in self.data.columns:
            messagebox.showerror("Error", "Selected X column not found in data.")
            return

        if plot_type in ["scatter", "histogram"] and y_column not in self.data.columns:
            messagebox.showerror("Error", "Selected Y column not found in data.")
            return

        plt.figure(figsize=(8, 6))
        if plot_type == "scatter":
            if y_column:
                plt.scatter(self.data[x_column], self.data[y_column])
            else:
                messagebox.showerror("Error", "Scatter plot requires both X and Y columns.")
                return
        elif plot_type == "histogram":
            plt.hist(self.data[x_column], bins=30)
        elif plot_type == "pie":
            if y_column:
                self.data[y_column].value_counts().plot(kind='pie', autopct='%1.1f%%')
            else:
                messagebox.showerror("Error", "Pie chart requires a column with categorical data.")
                return
        else:
            messagebox.showerror("Error", "Invalid plot type.")
            return

        plt.title(f"{plot_type.capitalize()} Plot")
        plt.xlabel(x_column)
        if plot_type in ["scatter", "histogram"]:
            plt.ylabel(y_column)
        plt.xticks(rotation=90)  # Rotate x-axis labels for readability
        plt.show()

if __name__ == "__main__":
    app = App()
    app.mainloop()
