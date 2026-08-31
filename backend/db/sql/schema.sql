--Enums
CREATE TYPE work_order_priority AS ENUM('Low', 'Medium', 'Critical');

CREATE TYPE work_order_status AS ENUM('Pending', 'In-Progress', 'Completed', 'Failed');

CREATE TYPE equipment_status AS ENUM('Available', 'In-Use', 'Maintenance', 'Offline');


--Tables
CREATE TABLE hospitals(
--serial is data type whcih increments automatically 
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_region VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    supervisor_id INTEGER NOT NULL
);

CREATE TABLE technicians (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    facility_id INTEGER NOT NULL REFERENCES hospitals(id)
);

CREATE TABLE equipment(
    id SERIAL PRIMARY KEY,
    serial_number VARCHAR(100) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
--name status of enum type equipment status
    status equipment_status NOT NULL,
    charge_level NUMERIC(5,2) NOT NULL CHECK ( charge_level BETWEEN 0 AND 100),
    facility_id INTEGER NOT NULL REFERENCES hospitals(id)
);

CREATE TABLE work_orders(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    priority work_order_priority NOT NULL,
    status work_order_status NOT NULL,
    equipment_id INTEGER NOT NULL REFERENCES equipment(id),
    technician_id INTEGER NOT NULL REFERENCES technican(id)
);

CREATE TABLE service_reports(
    id SERIAL PRIMARY KEY,
    work_order_id INTEGER NOT NULL REFERENCES work_orders(id),
    file_url TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


