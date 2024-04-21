from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'uberbooking'
}

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(**mysql_config)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, fields):
        # Create table query
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})"
        # Execute query
        self.cursor.execute(query)

    def close(self):
        # Commit changes and close cursor/connection
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

# Define table fields
cabs_fields = """
    cab_id VARCHAR(36) PRIMARY KEY,
    driver_id VARCHAR(36),
    type ENUM('sedan', 'SUV'),
    registration_number VARCHAR(255),
    ratings FLOAT,
    created_at TIMESTAMP
"""

customers_fields = """
    customer_id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255),
    created_at TIMESTAMP
"""

drivers_fields = """
    driver_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    dob DATE,
    created_at TIMESTAMP
"""

trips_fields = """
    trip_id VARCHAR(36) PRIMARY KEY,
    cab_id VARCHAR(36),
    customer_id VARCHAR(36),
    driver_id VARCHAR(36),
    created_at TIMESTAMP,
    status ENUM('created', 'ongoing', 'completed'),
    source POINT,
    destination POINT
"""

payments_fields = """
    payment_id VARCHAR(36) PRIMARY KEY,
    trip_id VARCHAR(36),
    method ENUM('credit_card', 'cash'),
    amount FLOAT,
    created_at TIMESTAMP
"""

# Create tables using Database class
db = Database()
db.create_table('cabs', cabs_fields)
db.create_table('customers', customers_fields)
db.create_table('drivers', drivers_fields)
db.create_table('trips', trips_fields)
db.create_table('payments', payments_fields)

# Close database connection
db.close()

