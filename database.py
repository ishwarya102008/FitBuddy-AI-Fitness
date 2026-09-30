from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    username = Column(String)
    age = Column(Integer)
    weight = Column(String)
    goal = Column(String)
    intensity = Column(String)
    original_plan = Column(Text)
    updated_plan = Column(Text)


Base.metadata.create_all(bind=engine)


def save_user(user_id, username, age, weight, goal, intensity):
    db = SessionLocal()

    user = User(
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db.add(user)
    db.commit()

    db.close()


def save_plan(user_id, plan):
    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:
        user.original_plan = plan
        db.commit()

    db.close()


def get_user(user_id):
    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    db.close()

    return user


def update_plan(user_id, plan):
    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:
        user.updated_plan = plan
        db.commit()

    db.close()


def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    return users
