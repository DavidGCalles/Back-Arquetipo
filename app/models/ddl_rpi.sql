CREATE TABLE IF NOT EXISTS gpio_pins (
            pin_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mode TEXT CHECK(mode IN ('INPUT', 'OUTPUT')), 
            state TEXT CHECK(state IN ('HIGH', 'LOW')) DEFAULT NULL,
            pull TEXT CHECK(pull IN ('PULL_UP', 'PULL_DOWN', 'NONE')) DEFAULT 'NONE',
            protocol TEXT CHECK(protocol IN ('I2C', 'SPI', 'UART', 'GPIO', 'ONEWIRE')) DEFAULT 'GPIO',
            object_type TEXT CHECK(object_type IN ('SENSOR', 'ACTUATOR', 'OTHER')) DEFAULT 'OTHER'
        );

CREATE TABLE IF NOT EXISTS devices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_id TEXT,
    name TEXT NOT NULL,
    device_type TEXT CHECK(device_type IN ('SENSOR', 'ACTUATOR')) DEFAULT 'OTHER',
    manufacturer TEXT,
    model TEXT,
    serial_number TEXT UNIQUE,
    purchase_date DATE,
    warranty_expiration DATE,
    location TEXT,
    status TEXT CHECK(status IN ('ACTIVE', 'INACTIVE', 'MAINTENANCE', 'RETIRED')) DEFAULT 'ACTIVE',
    pin_number INTEGER,
    range_min INTEGER,
    range_max INTEGER,
    measure_unit TEXT,
    last_used TIMESTAMP,
    value TEXT,
    FOREIGN KEY (pin_number) REFERENCES gpio_pins(pin_number)
);