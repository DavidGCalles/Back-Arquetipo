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

    def query(self, query, bucket=None):
        """
        Queries data from InfluxDB.
        Args:
            query (str): The Flux query to execute.
            bucket (str, optional): The name of the bucket.
        Returns:
            list: A list of query results, or None if an error occurs.
        """
        if not self.service:
            return None
        try:
            tables = self.service.query_data(query, bucket)
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
