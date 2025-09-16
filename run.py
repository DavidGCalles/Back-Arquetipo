from app import create_app
from os import urandom, environ
from app.services.db import DBManager
from config import LOGGER
# InfluxDB service
from app.services.nosql.influxdb_service import InfluxDBService

def initialize_databases():
    """Initializes the databases."""
    # Initialize the database
    db_manager = DBManager()
    db_manager.initialize_database('sqlite')

    # Initialize InfluxDB
    try:
        influx_service = InfluxDBService()
        # Example of writing data
        # influx_service.write_data(
        #     measurement="measurement_name",
        #     tags={"tag_key": "tag_value"},
        #     fields={"field_key": "field_value"}
        # )
        # Example of querying data
        # query = 'from(bucket:"your_influx_bucket") |> range(start: -1h)'
        # tables = influx_service.query_data(query)
        # for table in tables:
        #     for record in table.records:
        #         print(record)
        # influx_service.close()
    except ValueError as e:
        LOGGER.error(f"Failed to initialize InfluxDB: {e}")

app = create_app()
app.secret_key = urandom(24)
initialize_databases()

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port , debug= True)
