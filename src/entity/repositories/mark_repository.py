from entity.models import Mark
from abc import ABC, abstractmethod

class MarkRepository(ABC):
    @abstractmethod
    async def add(self, mark: Mark):
        pass
    
    @abstractmethod
    async def update(self, mark: Mark):
        pass
    
    @abstractmethod
    async def delete(self, mark: Mark):
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Mark:
        pass

    @abstractmethod
    async def get_all(self) -> list[Mark]:
        pass
        


        