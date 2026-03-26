import uuid

from ..models import Base, User, Product, Ticket, Order
from ..config.database import engine, session

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_data():
    create_users()
    create_products()
    create_tickets()
    create_orders()
    session.commit()

def create_users():
    user = User(
        username='Admin',
        password='1',
        points=100
    )
    user2 = User(
        username='Alex',
        password='2',
        points=10
    )
    user3 = User(
        username='3',
        password='3',
        points=100
    )
    session.add_all([user, user2, user3])

def create_products():
    session.add_all(
        [
            Product(name="apple", cost=20, count=100),
            Product(name="banana", cost=30, count=100),
            Product(name="orange", cost=40, count=100),
            Product(name="mango", cost=50, count=100),
            Product(name="strawberry", cost=60, count=100),
            Product(name="peach", cost=70, count=100),
            Product(name="grape", cost=80, count=100)
        ]
    )

def create_tickets():
    session.add_all([Ticket(uuid=str(uuid.uuid4())) for _ in range(50)])

def create_orders():
    session.add_all(
        [
            Order(user_id=3, product_id=1, count=5),
            Order(user_id=3, product_id=2, count=7),
            Order(user_id=3, product_id=3, count=2)
        ]
    )