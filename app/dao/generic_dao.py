"""This DAO represents the minimum entity to be used as DAO. Can be used as base class or totally rewritten."""
from app.services.db import DBManager
from config import LOGGER

class BaseDAO:
    """
    Base Data Access Object class for handling database operations.

    Attributes:
        table (str): The name of the database table this DAO is associated with.
        connection: The database connection object.
    """
    def __init__(self):
        """
        Initializes the BaseDAO with a specific table name and database connection.
        """
        self.table = "item"
        self.placeholder = "?" if "sqlite" in DBManager().db_type else "%s"
        self.db_manager = DBManager()
        self.connection = None
    def generic_get_all(self):
        """
        Fetches all records from the database table.

        Returns:
            list: A list of tuples representing each record fetched from the table.
        """
        self.connection = self.db_manager.get_db_connection()
        query = f"SELECT * FROM {self.table}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        finally:
            cursor.close()
            self.connection.close()
        return data
   
    def generic_get_by_field(self, field:str, value, like:bool=False):
        """
        Fetches a record from the database based on a specific field value.
        It has the option to use a LIKE clause for partial matching.
        
        Parameters:
        - field (str): The field to search for in the database table.
        - value (str|int): The value to match in the specified field.
        - like (bool): Whether to use a LIKE clause for partial matching (default is False).
        
        Returns:
        - tuple: A tuple representing the record fetched from the table.
        """
        self.connection = self.db_manager.get_db_connection()
        operator = "LIKE" if like else "="
        query = f"SELECT * FROM {self.table} WHERE {field} {operator} {self.placeholder}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (value,))
            data = cursor.fetchone()
        finally:
            cursor.close()
            self.connection.close()
        return data

    def generic_search(self, search_data: dict, like: bool = False):
        """
        Searches for records in the database based on the search_data dictionary.
        It has the option to use a LIKE clause for partial matching.

        Parameters:
        - search_data (dict): A dictionary containing the fields to search for and their values.
        - like (bool): Whether to use a LIKE clause for partial matching (default is False).

        Returns:
        - list: A list of tuples representing the records fetched from the table.
        """
        self.connection =self.db_manager.get_db_connection()
        
        # Build the conditions for the query
        conditions = []
        for key, value in search_data.items():
            if like and ('name' in key or 'description' in key):
                # For 'name' or 'description', use LIKE with '%' around the value
                conditions.append(f"{key} LIKE {self.placeholder}")
                search_data[key] = f"%{value}%"  # Add '%' around the value for LIKE
            else:
                # For other fields, use '='
                conditions.append(f"{key} = {self.placeholder}")
        
        # Join the conditions with 'AND'
        conditions_str = " AND ".join(conditions)
        
        # Build the full query
        query = f"SELECT * FROM {self.table} WHERE {conditions_str}"
        
        LOGGER.debug(query)  # Log the query for debugging
        
        # Execute the query
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(search_data.values()))  # Pass the updated search_data
            data = cursor.fetchall()
        finally:
            cursor.close()
            self.connection.close()
        
        return data


    def generic_insert(self, insert_data: dict, ignore_flag: bool = False):
        """
        Inserts a new record into the database table.

        Args:
            insert_data (dict): A dictionary containing column-value pairs to be inserted.

        Returns:
            int: The auto-generated ID of the newly inserted record.
        """

        # Extract keys and values from insert_data
        self.connection = self.db_manager.get_db_connection()
        keys = ", ".join(insert_data.keys())
        placeholders = ", ".join([self.placeholder] * len(insert_data))  # Use the appropriate placeholder

        # Construct the SQL query with placeholders
        query = f"INSERT{' OR IGNORE' if ignore_flag else ''} INTO {self.table} ({keys}) VALUES ({placeholders});"

        # Convert insert_data values to a tuple for the execute method
        values = tuple(insert_data.values())

        # Create cursor, execute the query, and commit the changes
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)  # Execute with values tuple to safely pass data
            self.connection.commit()
            new_id = cursor.lastrowid  # Retrieves the last inserted ID
        except Exception as e:
            LOGGER.error("Error inserting data: %s", e)
            new_id = None
        finally:
            cursor.close()
            self.connection.close()

        return new_id  # Return the autogenerated ID

    def generic_update(self, pk:str, update_data:dict, immutable_keys:list = None):
        """
        Update a record in the database with new data provided in the update_data dictionary.

        This method dynamically constructs and executes an SQL UPDATE statement to modify a record
        in the database. It identifies the record to update using the primary key provided and updates
        the specified fields with new values.

        Parameters:
        - pk (str): The key in the update_data dictionary that holds the primary key of the record.
        - update_data (dict): A dictionary containing the fields to update with their new values. 
                            The dictionary must contain the primary key as one of its keys.

        Returns:
        - int: The number of rows affected by the update operation.

        Raises:
        - KeyError: If the primary key is not found in the update_data dictionary."""
        if not update_data:
            return 0
        if immutable_keys and self.check_for_immutable_keys(update_data, immutable_keys) not in [None, pk]:
            raise ValueError(f"Immutable keys cannot be modified: {immutable_keys}")
        self.connection = self.db_manager.get_db_connection()
        primary_key = update_data.pop(pk)
        keys = ", ".join([f"{key} = {self.placeholder}" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(primary_key)  # Append the primary key to values to use in the WHERE clause
        sql = f"UPDATE {self.table} SET {keys} WHERE {pk} = {self.placeholder}"
        LOGGER.debug(sql)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            rowcount = cursor.rowcount
        finally:
            cursor.close()
            self.connection.close()

        return rowcount  # Return the number of rows affected

    def generic_replace(self, replace_data:dict):
        """
        Replaces a record in the database with new data provided in the replace_data dictionary.

        This method constructs and executes an SQL REPLACE statement to replace a record in the database
        with new data. It identifies the record to replace using the primary key provided and replaces
        all fields with the new values provided.

        Parameters:
        - pk (str): The key in the replace_data dictionary that holds the primary key of the record.
        - replace_data (dict): A dictionary containing the fields to replace with their new values. 
                            The dictionary must contain the primary key as one of its keys.

        Returns:
        - int: The number of rows affected by the replace operation.

        Raises:
        - KeyError: If the primary key is not found in the replace_data dictionary.
        """
        self.connection = self.db_manager.get_db_connection()
        keys = ", ".join(replace_data.keys())
        placeholders = ", ".join([self.placeholder] * len(replace_data.keys()))
        values = list(replace_data.values())
        sql = f"REPLACE INTO {self.table} ({keys}) VALUES ({placeholders})"
        LOGGER.debug(sql)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            rowcount = cursor.rowcount
        finally:
            cursor.close()
            self.connection.close()
        return rowcount

    def generic_delete(self, pk:str, id_to_delete):
        """
        Deletes a record from the database based on the primary key and its value.

        This method constructs and executes a SQL DELETE statement to remove a record 
        from the specified table. It uses the primary key and its value to identify 
        the record to be deleted. It's important to handle this method with care to 
        avoid accidental data loss.

        Parameters:
        - pk (str): The name of the primary key column in the table.
        - id_to_delete (Union[str, int]): The value of the primary key for the record to be deleted.

        Returns:
        - bool: True if the deletion was executed successfully, False otherwise.

        Example:
        - generic_delete('user_id', 101)
        This would attempt to delete from the table where the 'user_id' column equals 101.

        Raises:
        - Exception: If the SQL execution fails or if there are issues with the database connection.
        """
        success = False
        try:
            self.connection = self.db_manager.get_db_connection()
            query = f"DELETE FROM {self.table} WHERE {pk} = {self.placeholder}"
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, (id_to_delete,))
                self.connection.commit()
                success = True
            finally:
                cursor.close()
                self.connection.close()
        except Exception as e:
            LOGGER.error("Error deleting record: %s", e)
            success = False
        return success

    def delete_all(self):
        self.connection = self.db_manager.get_db_connection()
        self.connection.execute(f"DELETE FROM {self.table};")
        self.connection.commit()
        self.connection.close()
    
    def check_for_immutable_keys(self, data: dict, immutable_keys: list):
        """
        Checks if any of the immutable keys are present in the data dictionary.

        Parameters:
        - data (dict): The dictionary to check for immutable keys.
        - immutable_keys (list): A list of keys that should not be modified.

        Returns:
        - str: The immutable key found in the data, or None if no immutable keys are present.
        """
        for key in immutable_keys:
            if key in data:
                return key
        return None