from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class DataStorage(ABC):
    @abstractmethod
    async def save_data(self, data: Dict[str, Any]) -> bool:
        """Save data to storage.

        Args:
            data (Dict[str, Any]): Data to save.

        Returns:
            bool: True if save was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def retrieve_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve data from storage based on a query.

        Args:
            query (Optional[Dict[str, Any]]): Query parameters.

        Returns:
            List[Dict[str, Any]]: List of retrieved data entries.
        """
        pass
