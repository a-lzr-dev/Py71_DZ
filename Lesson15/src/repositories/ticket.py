from sqlalchemy import select

from . import BaseRepository
from ..config.database import session
from ..models import Ticket, User


class Tickets(BaseRepository):

    @staticmethod
    def get_ticket(uuid: str) -> Ticket:
        # получение тикета по номеру
        query = select(Ticket).where(Ticket.uuid == uuid)
        return session.execute(query).first()

    @staticmethod
    def valid_ticket(ticket: Ticket) -> bool:
        # проверка актуальности тикета
        return ticket and ticket.available

    @staticmethod
    def change_ticket(ticket: Ticket, user: User) -> int:
        # обмен тикета
        ticket.available = False
        ticket.user = user
        user.points += 20
        session.commit()
        return user.points