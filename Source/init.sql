 CREATE TABLE IF NOT EXISTS flight_data (
    id SERIAL PRIMARY KEY,
    flight_date DATE NOT NULL,
    airline_code VARCHAR(50) NOT NULL,
    source_airport VARCHAR(10) NOT NULL,
    destination_airport VARCHAR(10) NOT NULL,
    departure_time INTEGER NOT NULL,
    departure_delay INTEGER NOT NULL,
    arrival_time INTEGER NOT NULL,
    arrival_delay INTEGER NOT NULL,
    airtime INTEGER NOT NULL,
    distance INTEGER NOT NULL);
