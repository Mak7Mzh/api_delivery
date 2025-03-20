from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select, update

from cfg import DATABASE_URL
from models import ReqCreate

class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL)
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_new_req(self, req_data: ReqCreate):
        """ Создание заявки на доставку """
        try:
            async with self.Session() as session:
                req_info = req_data.model_dump()

                data = requestss(**req_info)
                session.add(data)

                await session.commit()
                return data.id
        except Exception as e:
            print(f"ААЩИБИКА(create_new_req): {e}\n")
            return None

    async def get_req(self, id_req: int):
        """ Получение информации о заявке """
        try:
            async with self.Session() as session:
                query = select(requestss).where(requestss.id == id_req)
                req_page = await session.execute(query)
                return req_page.scalar()
        except Exception as e:
            print(f"ААЩИБИКА(get_req): {e}\n")
            return None

    async def cancel_req(self, id_req: int):
        """ Отмена заявки при условии, что товар не передан в доставку """
        try:
            async with self.Session() as session:
                status_req = await self.get_status_req(id_req)
                if status_req != "created":
                    if status_req == "cancelled": return "tovar_alredy_v_govne"
                    elif status_req is None: return None
                    else: return "tovar_v_govne"
                else:
                    query = update(requestss).where(requestss.id == id_req).values(status="cancelled")
                    await session.execute(query)
                    await session.commit()
                    return "good"
        except Exception as e:
            print(f"ААЩИБИКА(cancel_req): {e}\n")
            return None

    async def get_status_req(self, id_req: int):
        """ Получение статуса заявки """
        try:
            async with self.Session() as session:
                query = select(requestss.status).where(requestss.id == id_req)
                status_req = await session.execute(query)
                return status_req.scalar()
        except Exception as e:
            print(f"ААЩИБИКА(get_status_req): {e}\n")
            return None

    async def get_all_statusIndex(self): # не готово
        try:
            async with self.Session() as session:
                query = select(status_indexing)
                return None
        except Exception as e:
            print(f"ААЩИБИКА(get_all_statusIndex): {e}\n")
            return None




database = Database()
Base = declarative_base()

class status_indexing(Base):
    """ Таблица со всеми статусами заказов по индексу """
    __tablename__ = "app_status"

    index = Column(Integer, primary_key=True, index=True)
    status_hash = Column(String, nullable=False)
    status_text = Column(String, nullable=True)


class requestss(Base):
    """ Таблица со всеми заявками """
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="created")

    sender_name = Column(String, nullable=True)
    sender_phone = Column(Integer, nullable=True)
    sender_address = Column(String, nullable=True)

    recipient_name = Column(String, nullable=True)
    recipient_phone = Column(Integer, nullable=True)
    recipient_address = Column(String, nullable=True)
