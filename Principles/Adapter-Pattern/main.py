"""
Problem Statement:
In data engineering, applications often need to interact with various data sources,
each with its own unique interface for data operations. Managing these diverse data
sources directly in the application can lead to complex, hard-to-maintain code, especially
when adding new data sources or changing existing ones. The goal is to simplify data
access across different data stores (like MySQL, MongoDB, and Amazon S3) by providing a
unified interface that abstracts away the specifics of each data source. This approach
enhances flexibility, reduces code complexity, and makes the system more maintainable.

Solution:
Implement the Adapter pattern to create a unified data access layer. This pattern allows
the application to interact with different data sources through a common interface,
regardless of their underlying APIs. Adapters are created for each data source (MySQL,
MongoDB, S3), translating the unified interface's calls into data source-specific operations.
This design simplifies integrating and managing multiple data sources within data
engineering projects.
"""

import mysql.connector
from pymongo import MongoClient
import boto3


# Define a common interface for all adapters to ensure they can be used interchangeably
class DataStoreAdapter:
    """Unified interface for data access across different data stores."""

    def read_data(self, identifier):
        """Method to read data from the data store.

        Args:
            identifier: An identifier to locate data in the store.

        Returns:
            Data fetched from the data store.
        """
        raise NotImplementedError

    def write_data(self, identifier, data):
        """Method to write data to the data store.

        Args:
            identifier: An identifier to store data under.
            data: The data to be stored.
        """
        raise NotImplementedError


# Adapter for MySQL
class MySQLAdapter(DataStoreAdapter):
    """Adapter for interacting with MySQL database."""

    def __init__(self, connection_details):
        """Initialize the MySQL connection.

        Args:
            connection_details: A dictionary with connection details (user, password, database).
        """
        self.connection = mysql.connector.connect(**connection_details)
        self.cursor = self.connection.cursor()

    def read_data(self, table_name):
        """Read data from a MySQL table.

        Args:
            table_name: Name of the MySQL table to read from.

        Returns:
            All rows fetched from the table.
        """
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def write_data(self, table_name, data):
        """Insert data into a MySQL table.

        Args:
            table_name: Name of the table to insert data into.
            data: Data to insert (assumed to be a tuple of values).
        """
        self.cursor.execute(f"INSERT INTO {table_name} VALUES (%s, %s, %s)", data)
        self.connection.commit()


# Adapter for MongoDB
class MongoDBAdapter(DataStoreAdapter):
    """Adapter for interacting with MongoDB."""

    def __init__(self, connection_uri, db_name):
        """Initialize the MongoDB client.

        Args:
            connection_uri: URI for connecting to MongoDB.
            db_name: The name of the database to use.
        """
        self.client = MongoClient(connection_uri)
        self.db = self.client[db_name]

    def read_data(self, collection_name):
        """Read data from a MongoDB collection.

        Args:
            collection_name: The name of the collection to read from.

        Returns:
            A list of documents found in the collection.
        """
        collection = self.db[collection_name]
        return list(collection.find({}))

    def write_data(self, collection_name, data):
        """Write data to a MongoDB collection.

        Args:
            collection_name: The name of the collection to write to.
            data: The document to insert.
        """
        collection = self.db[collection_name]
        collection.insert_one(data)


# Adapter for Amazon S3
class S3Adapter(DataStoreAdapter):
    """Adapter for interacting with Amazon S3."""

    def __init__(self, bucket_name):
        """Initialize the S3 resource.

        Args:
            bucket_name: The name of the S3 bucket to use.
        """
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def read_data(self, file_name):
        """Read data from a file stored in an S3 bucket.

        Args:
            file_name: The name of the file to read.

        Returns:
            The content of the file as a string.
        """
        obj = self.bucket.Object(file_name)
        return obj.get()['Body'].read().decode('utf-8')

    def write_data(self, file_name, data):
        """Write data to a file in an S3 bucket.

        Args:
            file_name: The name of the file to write.
            data: The content to write to the file.
        """
        obj = self.bucket.Object(file_name)
        obj.put(Body=data.encode('utf-8'))


# Example usage
# Note: Replace placeholders with actual connection details and bucket names
if __name__ == "__main__":
    # Setup and use adapters here
    mysql_adapter = MySQLAdapter({'host': 'localhost', 'user': 'user', 'password': 'password', 'database': 'dbname'})
    mongodb_adapter = MongoDBAdapter('mongodb://localhost:27017/', 'dbname')
    s3_adapter = S3Adapter('mybucket')

    # Example of reading data from each source
    print(mysql_adapter.read_data('mytable'))
    print(mongodb_adapter.read_data('mycollection'))
    print(s3_adapter.read_data('myfile.txt'))
