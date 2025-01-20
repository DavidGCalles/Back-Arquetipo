CREATE TABLE IF NOT EXISTS gpio_pins (
            pin_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mode TEXT CHECK(mode IN ('INPUT', 'OUTPUT')), 
            state TEXT CHECK(state IN ('HIGH', 'LOW')) DEFAULT NULL,
            pull TEXT CHECK(pull IN ('PULL_UP', 'PULL_DOWN', 'NONE')) DEFAULT 'NONE',
            protocol TEXT CHECK(protocol IN ('I2C', 'SPI', 'UART', 'GPIO', 'ONEWIRE')) DEFAULT 'GPIO',
            object_type TEXT CHECK(object_type IN ('SENSOR', 'ACTUATOR', 'OTHER')) DEFAULT 'OTHER'
        );