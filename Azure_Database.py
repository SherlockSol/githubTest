import pyodbc
import time
import requests

# Connection details
server = 'myfreesqldbserversage.database.windows.net'  # Replace with your actual server name
database = 'myFreeDB'  # Replace with your actual database name
username = 'bricksage'  # Replace with your actual username
password = 'Indomitable928!'  # Replace with your actual password
driver = '{ODBC Driver 18 for SQL Server}'


def check_azure_status():
    try:
        response = requests.get('https://status.azure.com/en-us/status')
        if response.status_code == 200:
            return "Azure status page accessible."
        return "Warning: Unable to access Azure status page."
    except requests.RequestException as e:
        return f"Error accessing Azure status page: {e}"


def connect_to_database():
    try:
        connection = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
        print("Connection successful")
        return connection
    except pyodbc.Error as ex:
        print("Connection failed:", ex)
        time.sleep(5)  # Short wait before retrying
        return None


# Checking Azure service status
azure_status = check_azure_status()
print(azure_status)

# Retry logic
max_retries = 5
retry_delay = 10  # in seconds

for attempt in range(max_retries):
    connection = connect_to_database()
    if connection:
        break
    else:
        print(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1} of {max_retries})")
        time.sleep(retry_delay)

if not connection:
    print("All connection attempts failed. Please check your database status and network settings.")
else:
    cursor = connection.cursor()

    # SQL command to create a table
    sql_create_table = '''
    CREATE TABLE Employees (
        EmployeeID int NOT NULL PRIMARY KEY,
        LastName nvarchar(50) NOT NULL,
        FirstName nvarchar(50) NOT NULL,
        BirthDate date,
        HireDate date,
        Address nvarchar(100),
        City nvarchar(50),
        State nvarchar(50),
        PostalCode nvarchar(10)
    );
    '''

    # Execute the SQL command
    cursor.execute(sql_create_table)
    #dfdfdf

    # Commit and close
    connection.commit()
    cursor.close()
    connection.close()
