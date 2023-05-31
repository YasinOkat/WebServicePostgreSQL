# WebServicePostgreSQL

# Car Tracking App Server

This is the server-side code for a car tracking application built with Flask. The server provides API endpoints for user authentication, car management, and tracking car rentals.

# Features

   1. User Authentication: Allows users to log in and verifies their credentials against a PostgreSQL database.
   2. Car Management: Provides endpoints to fetch the list of available cars, insert new car data, and delete car records.
   3. Car Rental: Supports the insertion of rental information into the database, including the user's name, car plate number, destination, and purpose of the trip.

# Prerequisites

Before running the server, make sure you have the following dependencies installed:

    Python 3
    Flask
    psycopg2 (for PostgreSQL database connectivity)

# Getting Started

To run the server on your local machine, follow these steps:

   1. Clone the repository: 
      ```bash
      git clone https://github.com/your-username/car-tracking-server.git
      
   2. Install the required dependencies.
   3. Set up your PostgreSQL database and update the db_connection_string variable in app.py with your database credentials.
   4. Start the server: 
      ```bash
      python app.py
   6. The server should now be running on http://localhost:5000.

# API Endpoints

The server provides the following API endpoints:

    GET /: Home endpoint to verify that the server is running.
    POST /login: User login endpoint. Requires the kullaniciadi (username) and sifre (password) as JSON payload. Returns a JSON response indicating the success of the login attempt.
    GET /getArabalar: Fetches the list of available cars from the database. Returns a JSON response containing the list of cars.
    POST /arabaBirak: Handles the return of a rented car. Requires the kilometre (mileage) and plaka (car plate number) as JSON payload. Updates the car's mileage and marks it as returned in the database.
    POST /insertData: Inserts rental information into the database. Requires the plaka (car plate number), ad (user's name), hedef (destination), and amac (purpose) as JSON payload.
    POST /deleteData: Deletes a car record from the database. Requires the plaka (car plate number) as JSON payload.
    GET /getKullanilanArabalar: Fetches the list of rented cars from the database. Returns a JSON response containing the list of rented cars.

# Database Configuration

Make sure to configure the db_connection_string variable in app.py with the appropriate PostgreSQL database connection string. This includes the database name, username, password, and host information.
# Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.
# License

This project is licensed under the GNU General Public License (GPL). See the [LICENSE](LICENSE) file for more information.
