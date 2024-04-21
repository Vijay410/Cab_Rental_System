import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def create_users_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """
        self.cursor.execute(create_table_sql)

    def create_vehicles_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_number VARCHAR(20),
                model VARCHAR(50),
                year INT
            )
        """
        self.cursor.execute(create_table_sql)

    def create_drivers_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS drivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                driver_license_number VARCHAR(20),
                vehicle_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        """
        self.cursor.execute(create_table_sql)

    def create_rides_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS rides (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                driver_id INT,
                vehicle_id INT,
                pickup_location VARCHAR(100),
                dropoff_location VARCHAR(100),
                ride_status VARCHAR(20),
                ride_started_at DATETIME,
                ride_completed_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (driver_id) REFERENCES drivers(id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        """
        self.cursor.execute(create_table_sql)

    def commit_changes(self):
        self.connection.commit()

if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", "root", "admin", "cabrental")
    db_manager.connect()
    db_manager.create_users_table()
    db_manager.create_vehicles_table()
    db_manager.create_drivers_table()
    db_manager.create_rides_table()
    db_manager.commit_changes()
    db_manager.close()
