from abc import ABC, abstractmethod

class APIClient(ABC):
    @abstractmethod
    def search(self, query):
        """Search the API using a query string.

        Args:
            query (str): The query string for searching.

        Raises:
            NotImplementedError: This method must be overridden by a subclass.
        """
        pass  # Using pass instead of raising NotImplementedError

    @abstractmethod
    def retrieve_item(self, item_id):
        """Retrieve a specific item from the API using its unique item ID.

        Args:
            item_id (str): The unique identifier of the item to retrieve.

        Raises:
            NotImplementedError: This method must be overridden by a subclass.
        """
        pass  # Using pass instead of raising NotImplementedError

    @abstractmethod
    def get_metadata(self, item_id):
        """Get metadata for a specific item from the API using its unique item ID.

        Args:
            item_id (str): The unique identifier of the item to retrieve metadata for.

        Raises:
            NotImplementedError: This method must be overridden by a subclass.
        """
        pass  # Using pass instead of raising NotImplementedError
