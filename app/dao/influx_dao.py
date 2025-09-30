"""This module provides a Data Access Object (DAO) for InfluxDB."""
from app.services.nosql.influxdb_service import InfluxDBService
from config import LOGGER

class InfluxDAO:
    """A DAO for interacting with InfluxDB."""

    def __init__(self):
        """Initializes the InfluxDAO."""
        try:
            self.service = InfluxDBService()
        except ValueError as e:
            LOGGER.error(f"Failed to initialize InfluxDBService in DAO: {e}")
            self.service = None

    def write(self, measurement, tags, fields, bucket=None):
        """
        Writes a single data point to InfluxDB.
        Args:
            measurement (str): The name of the measurement.
            tags (dict): A dictionary of tags.
            fields (dict): A dictionary of fields.
            bucket (str, optional): The name of the bucket.
        Returns:
            bool: True if write was successful, False otherwise.
        """
        if not self.service:
            return False
        try:
            self.service.write_data(measurement, tags, fields, bucket)
            return True
        except Exception as e:
            LOGGER.error(f"DAO Error writing to InfluxDB: {e}")
            return False
        finally:
            if self.service:
                self.service.close()

    def query(self, bucket, measurement, start_range, stop_range=None):
        """
        Queries data from InfluxDB with specific filters.
        Args:
            bucket (str): The name of the bucket.
            measurement (str): The measurement to query.
            start_range (str): The start of the time range.
            stop_range (str, optional): The end of the time range.
        Returns:
            list: A list of query results, or None if an error occurs.
        """
        if not self.service:
            return None
        
        try:
            # Construct the Flux query dynamically
            query = f'from(bucket:"{bucket}") |> range(start: {start_range}'
            if stop_range:
                query += f', stop: {stop_range}'
            query += f') |> filter(fn: (r) => r._measurement == "{measurement}")'

            tables = self.service.query_data(query)
            results = []
            for table in tables:
                for record in table.records:
                    results.append(record.values)
            return results
        except Exception as e:
            LOGGER.error(f"DAO Error querying InfluxDB: {e}")
            return None
        finally:
            if self.service:
                self.service.close()
