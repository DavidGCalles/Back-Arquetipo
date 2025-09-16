"""This module provides a service for interacting with InfluxDB."""
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config import Config, LOGGER

class InfluxDBService:
    """A service for interacting with InfluxDB."""

    def __init__(self):
        """Initializes the InfluxDB service."""
        self.config = Config.DATABASE_CONFIGURATIONS.get("influxdb", {})
        if not self.config:
            raise ValueError("InfluxDB configuration not found.")

        self.client = InfluxDBClient(
            url=self.config["INFLUX_URL"],
            token=self.config["INFLUX_TOKEN"],
            org=self.config["INFLUX_ORG"]
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_data(self, measurement, tags, fields, bucket=None):
        """
        Writes a single data point to InfluxDB.
        Args:
            measurement (str): The name of the measurement.
            tags (dict): A dictionary of tags.
            fields (dict): A dictionary of fields.
            bucket (str, optional): The name of the bucket. Defaults to the one in the config.
        """
        bucket = bucket or self.config.get("INFLUX_BUCKET")
        if not bucket:
            raise ValueError("InfluxDB bucket not specified.")

        point = Point(measurement)
        for key, value in tags.items():
            point.tag(key, value)
        for key, value in fields.items():
            point.field(key, value)

        try:
            self.write_api.write(bucket=bucket, record=point)
            LOGGER.info("Successfully wrote data to InfluxDB.")
        except Exception as e:
            LOGGER.error(f"Failed to write data to InfluxDB: {e}")
            raise

    def query_data(self, query, bucket=None):
        """
        Queries data from InfluxDB.
        Args:
            query (str): The Flux query to execute.
            bucket (str, optional): The name of the bucket. Defaults to the one in the config.
        Returns:
            list: A list of tables, where each table is a list of records.
        """
        bucket = bucket or self.config.get("INFLUX_BUCKET")
        if not bucket:
            raise ValueError("InfluxDB bucket not specified.")

        try:
            tables = self.query_api.query(query, org=self.config["INFLUX_ORG"])
            LOGGER.info("Successfully queried data from InfluxDB.")
            return tables
        except Exception as e:
            LOGGER.error(f"Failed to query data from InfluxDB: {e}")
            raise

    def close(self):
        """Closes the InfluxDB client."""
        self.client.close()
