from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite databáza (lokálny súbor)
DATABASE_URL = "sqlite:///./expenses.db"

# spojenie s databázou
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# session = „pracovné okno“ do DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# základ pre modely (tabuľky)
Base = declarative_base()