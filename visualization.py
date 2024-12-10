import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox, Toplevel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkTextbox

class VisualizationWindow(Toplevel):
    def __init__(self, data):
        super().__init__()

        self.title("Data Visualization")
        self.geometry("800x600")
        self.data = pd.DataFrame(data)
        self.report = ""  # Store the report content

        # Create visualization options
        self.plot_type_var = tk.StringVar(value="scatter")
        self.x_column_var = tk.StringVar(value=self.data.columns[0] if not self.data.empty else "")
        self.y_column_var = tk.StringVar(value=self.data.columns[1] if len(self.data.columns) > 1 else "")

        self.create_widgets()

    def create_widgets(self):
        # Plot type selection
        plot_type_frame = CTkFrame(self)
        plot_type_frame.pack(fill="x", padx=10, pady=10)

        plot_type_label = CTkLabel(plot_type_frame, text="Select Plot Type:", font=("Arial", 12, "bold"))
        plot_type_label.pack(side="left")

        plot_type_menu = CTkOptionMenu(plot_type_frame, variable=self.plot_type_var, values=["scatter", "histogram", "pie"])
        plot_type_menu.pack(side="left", padx=10)

        plot_button = CTkButton(plot_type_frame, text="Generate Plot", command=self.generate_plot)
        plot_button.pack(side="left")

        # X and Y column selection
        column_frame = CTkFrame(self)
        column_frame.pack(fill="x", padx=10, pady=10)

        x_column_label = CTkLabel(column_frame, text="Select X Column:", font=("Arial", 12, "bold"))
        x_column_label.pack(side="left")

        self.x_column_menu = CTkOptionMenu(column_frame, variable=self.x_column_var, values=list(self.data.columns))
        self.x_column_menu.pack(side="left", padx=10)

        y_column_label = CTkLabel(column_frame, text="Select Y Column:", font=("Arial", 12, "bold"))
        y_column_label.pack(side="left")

        self.y_column_menu = CTkOptionMenu(column_frame, variable=self.y_column_var, values=list(self.data.columns))
        self.y_column_menu.pack(side="left", padx=10)

        # Add View Report Button
        report_button = CTkButton(self, text="View Report", command=self.show_report_window)
        report_button.pack(pady=10)

        # Add Save Report as PDF Button
        save_report_button = CTkButton(self, text="Save Report as PDF", command=self.save_report_as_pdf)
        save_report_button.pack(pady=10)

        # Plot display area
        self.plot_frame = CTkFrame(self)
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

        # Generate analysis report
        self.generate_report(x_column, y_column)

    def generate_report(self, x_column, y_column):
        report = f"Data Analysis Report:\n\n"
        
        # Basic statistics
        report += f"Summary Statistics for '{x_column}':\n"
        report += f"{self.data[x_column].describe()}\n\n"
        
        if y_column and y_column in self.data.columns:
            report += f"Summary Statistics for '{y_column}':\n"
            report += f"{self.data[y_column].describe()}\n\n"
            report += f"Correlation between '{x_column}' and '{y_column}': {self.data[x_column].corr(self.data[y_column])}\n\n"

        self.report = report  # Store the report content for later use

    def show_report_window(self):
        if not self.report:
            messagebox.showerror("Error", "No report generated yet. Please generate a plot first.")
            return
        
        report_window = Toplevel(self)
        report_window.title("Analysis Report")
        report_window.geometry("400x300")
        
        report_textbox = CTkTextbox(report_window, state="normal", wrap="word")
        report_textbox.pack(expand=True, fill="both")
        report_textbox.insert("1.0", self.report)
        report_textbox.configure(state="disabled")

    def save_report_as_pdf(self):
        if not self.report:
            messagebox.showerror("Error", "No report generated yet. Please generate a plot first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        text_object = c.beginText(40, height - 40)
        text_object.setFont("Helvetica", 12)

        for line in self.report.split('\n'):
            text_object.textLine(line)
        
        c.drawText(text_object)
        c.showPage()
        c.save()
