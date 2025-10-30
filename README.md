# Student Management System

## Installation

1. Install the required dependencies:
   - `customtkinter`
   - `mysql.connector`

You can install them using pip:

```
pip install customtkinter mysql-connector-python
```

2. Ensure you have a MySQL server running on your local machine.

## Usage

1. Run the `SMS.py` script to start the Student Management System application.
2. The application will prompt you to enter the MySQL root password. Provide the correct password to connect to the database.
3. The main menu will be displayed, allowing you to perform the following actions:
   - Add a new student
   - View student records
   - Add a payment for a student
   - Check payment status for a student
   - Delete a student

## API

The application provides the following functions:

- `connect_to_mysql()`: Establishes a connection to the MySQL database.
- `prompt_password(title)`: Prompts the user to enter a password.
- `initialize_database()`: Creates the necessary database and tables.
- `create_tables()`: Creates the `students` and `payments` tables.
- `execute_query(query, params)`: Executes a SQL query with optional parameters.
- `fetch_data(query, params)`: Fetches data from the database based on a SQL query and parameters.

## Contributing

Contributions to the Student Management System project are welcome. If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the project's repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

The application does not include any automated tests. However, you can manually test the functionality by running the `SMS.py` script and interacting with the user interface.
