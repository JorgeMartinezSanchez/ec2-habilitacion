import datetime
from uuid import UUID
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.types import Date
from src.db.session_model import SessionModel
from src.db.registration_model import RegistrationModel
from src.models.session_filters import SessionFilters

class SessionRepository:
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def get_sessions(self, filters: SessionFilters) -> tuple[int, list]:
        base_query = self._build_filtered_query(filters)
        
        # Agregar conteo de registros confirmados
        # Usamos una subconsulta para contar los registros confirmados por sesión
        confirmed_count_subquery = (
            select(
                RegistrationModel.session_id,
                func.count().label("confirmed_count")
            )
            .where(RegistrationModel.status == "confirmed")
            .group_by(RegistrationModel.session_id)
            .subquery()
        )

        total_count = await self.database_session.scalar(
            select(func.count()).select_from(base_query.subquery())
        )

        # Modificar la consulta principal para incluir el conteo
        query = (
            select(
                SessionModel,
                func.coalesce(confirmed_count_subquery.c.confirmed_count, 0).label("registered")
            )
            .select_from(SessionModel)
            .outerjoin(
                confirmed_count_subquery,
                SessionModel.id == confirmed_count_subquery.c.session_id
            )
            .options(selectinload(SessionModel.track))
        )
        
        # Aplicar los filtros
        if filters.search_query:
            search_pattern = f"%{filters.search_query}%"
            query = query.where(
                SessionModel.title.ilike(search_pattern) | SessionModel.abstract.ilike(search_pattern)
            )

        if filters.track_id:
            query = query.where(SessionModel.track_id == filters.track_id)
            
        if filters.day:
            local_date = cast(func.timezone(filters.timezone, SessionModel.starts_at), Date)
            query = query.where(local_date == datetime.date.fromisoformat(filters.day))
        
        query = query.order_by(SessionModel.starts_at)\
                     .limit(filters.page_size)\
                     .offset((filters.page - 1) * filters.page_size)

        results = (await self.database_session.execute(query)).all()
        
        # Convertir los resultados a una lista de objetos SessionModel con el campo registered
        sessions_with_registered = []
        for session_model, registered in results:
            # Asignar el atributo registered al objeto session_model
            session_model.registered = registered
            sessions_with_registered.append(session_model)

        return total_count, sessions_with_registered

    async def get_session_by_id(self, session_id: UUID):
        # Similar al método anterior pero para una sola sesión
        confirmed_count_subquery = (
            select(
                RegistrationModel.session_id,
                func.count().label("confirmed_count")
            )
            .where(RegistrationModel.status == "confirmed")
            .group_by(RegistrationModel.session_id)
            .subquery()
        )

        query = (
            select(
                SessionModel,
                func.coalesce(confirmed_count_subquery.c.confirmed_count, 0).label("registered")
            )
            .select_from(SessionModel)
            .outerjoin(
                confirmed_count_subquery,
                SessionModel.id == confirmed_count_subquery.c.session_id
            )
            .where(SessionModel.id == session_id)
            .options(selectinload(SessionModel.track))
        )

        result = (await self.database_session.execute(query)).first()
        
        if result:
            session_model, registered = result
            session_model.registered = registered
            return session_model
        
        return None

    async def search_sessions(self, search_query: str) -> list[SessionModel]:
        search_pattern = f"%{search_query}%"
        
        confirmed_count_subquery = (
            select(
                RegistrationModel.session_id,
                func.count().label("confirmed_count")
            )
            .where(RegistrationModel.status == "confirmed")
            .group_by(RegistrationModel.session_id)
            .subquery()
        )

        query = (
            select(
                SessionModel,
                func.coalesce(confirmed_count_subquery.c.confirmed_count, 0).label("registered")
            )
            .select_from(SessionModel)
            .outerjoin(
                confirmed_count_subquery,
                SessionModel.id == confirmed_count_subquery.c.session_id
            )
            .where(SessionModel.title.ilike(search_pattern) | SessionModel.abstract.ilike(search_pattern))
            .options(selectinload(SessionModel.track))
            .order_by(SessionModel.starts_at)
            .limit(50)
        )

        results = (await self.database_session.execute(query)).all()
        
        sessions_with_registered = []
        for session_model, registered in results:
            session_model.registered = registered
            sessions_with_registered.append(session_model)

        return sessions_with_registered

    def _build_filtered_query(self, filters: SessionFilters):
        # Este método ya no se usa directamente para la consulta final
        # pero lo mantenemos por compatibilidad
        query = select(SessionModel)

        if filters.search_query:
            search_pattern = f"%{filters.search_query}%"
            query = query.where(
                SessionModel.title.ilike(search_pattern) | SessionModel.abstract.ilike(search_pattern)
            )

        if filters.track_id:
            query = query.where(SessionModel.track_id == filters.track_id)
            
        if filters.day:
            local_date = cast(func.timezone(filters.timezone, SessionModel.starts_at), Date)
            query = query.where(local_date == datetime.date.fromisoformat(filters.day))
        
        return query