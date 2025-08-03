from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, List, Dict, Optional


ModelType = TypeVar("ModelType", bound=DeclarativeMeta) # Type variable for generic model types

class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: ModelType):
        """
        Initialize with a DB session and model class.
        
        :param db: AsyncSession object
        :param model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    async def create(self, data: dict) -> ModelType:
        """
        Create a new record in the database.
        
        :param data: The data to insert, as a dictionary.
        :return: The created model object.
        """
        obj = self.model(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get(self, id: int) -> Optional[ModelType]:
        """
        Fetch a record by ID.
        
        :param id: The primary key value.
        :return: The model object, or None if not found.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self, 
        filters: Optional[Dict[str, any]] = None, 
        limit: int = 10, 
        offset: int = 0, 
        order_by: str = 'id', 
        order_direction: str = 'ASC'
    ) -> List[ModelType]:
        """
        Fetch all records with optional filters, pagination, and sorting.
        
        :param filters: A dictionary of filters (field_name: value).
        :param limit: The maximum number of results to fetch.
        :param offset: The starting point for pagination.
        :param order_by: The field to order by.
        :param order_direction: The direction to order ('ASC' or 'DESC').
        :return: A list of model objects.
        """
        query = select(self.model)
        
        # filters
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)

        # sorting
        if order_by:
            order_func = getattr(self.model, order_by)
            if order_direction.upper() == 'DESC':
                query = query.order_by(order_func.desc())
            else:
                query = query.order_by(order_func.asc())

        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        """
        Update a record by ID.
        
        :param id: The ID of the record to update.
        :param data: The data to update, as a dictionary.
        :return: The updated model object, or None if not found.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        return None

    async def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        :param id: The ID of the record to delete.
        :return: True if the record was deleted, False if not found.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False

    async def count(self, filters: Optional[Dict[str, any]] = None) -> int:
        """
        Count records based on optional filters.
        
        :param filters: A dictionary of filters (field_name: value).
        :return: The count of records that match the filters.
        """
        query = select(func.count()).select_from(self.model)
        
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        
        result = await self.db.execute(query)
        return result.scalar()

    async def paginate_query(
        self,
        filters: Optional[Dict[str, any]] = None,
        page: int = 1,
        page_size: int = 10,
        order_by: str = 'id',
        order_direction: str = 'ASC'
    ) -> dict:
        """
        Perform a paginated query with optional filters and sorting.
        
        :param filters: The filters to apply (field_name: value).
        :param page: The page number (1-indexed).
        :param page_size: The number of items per page.
        :param order_by: The field to order by.
        :param order_direction: The direction ('ASC' or 'DESC').
        :return: A dictionary with keys 'results' (list) and 'pagination' (dict).
        """
        count = await self.count(filters)
        pagination = {
            "page": page,
            "size": page_size,
            "count": count,
            "next": page + 1 if count > page * page_size else None,
            "previous": page - 1 if page > 1 else None
        }

        results = await self.get_all(
            filters=filters,
            limit=page_size,
            offset=(page - 1) * page_size,
            order_by=order_by,
            order_direction=order_direction
        )

        return {"results": results, "pagination": pagination}
