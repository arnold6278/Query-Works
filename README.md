
Here’s a README.md template for your project that explains how to use it, along with an overview of the functionality:

# QueryWorks

QueryWorks is a desktop application built using Python and Tkinter for executing SQL queries, visualizing data, and exporting query results. It provides an intuitive interface to interact with SQL Server databases, execute queries, and manage results in multiple formats including CSV and PDF reports. The app also includes functionality for data visualization like scatter plots, histograms, and pie charts.

## Features

- **Connect to SQL Server**: Input server credentials and connect to a database.
- **Execute SQL Queries**: Execute any valid SQL query and display the results within the application.
- **Data Export**: Save query results as CSV files.
- **Data Visualization**: Generate visual plots (scatter, histogram, pie charts) from query results.
- **Save Reports**: Save generated data analysis reports as PDF files.
- **User Interface Customization**: Change appearance mode (Light/Dark/System) and UI scaling for better usability.

## Requirements

- Python 3.x
- `tkinter` for GUI
- `customtkinter` for custom widgets
- `pyodbc` for SQL Server database connectivity
- `pandas` for data manipulation
- `matplotlib` and `seaborn` for data visualization
- `reportlab` for generating PDF reports

### Install Dependencies

You can install the required dependencies via `pip`:

```bash
pip install tkinter customtkinter pyodbc pandas matplotlib seaborn reportlab

USAGE
1. Connect to the Database
Enter the Server Name, Database Name, Username, and Password in the fields provided in the sidebar.
Click Connect To Database to establish the connection. The status will update to Connected upon successful connection.
2. Execute SQL Query
Type your SQL query into the main text entry box.
Click Execute Query to run the query. Results will be displayed in the textbox area below.
3. Save Query Results
After executing a query, you can save the results to a CSV file by clicking the Save File button.
Choose a location to save the file, and the query results will be exported in CSV format.
4. Data Visualization
Click the Data Visualization button to open a new window for data visualization.
Choose from scatter, histogram, or pie plot types.
Select appropriate columns for the X and Y axes.
Click Generate Plot to create the visualization.
You can also generate an analysis report, which can be viewed in a new window or saved as a PDF.
5. Customize Appearance
Use the Appearance Mode dropdown in the sidebar to choose between Light, Dark, or System appearance modes.
Use the UI Scaling dropdown to adjust the UI scaling percentage.
