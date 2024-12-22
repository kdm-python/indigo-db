# Database

from loguru import logger
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError


from .models import Base


POSTGRES_URL = "postgresql://postgres:blackmore@localhost:5432/indigo"
MYSQL_URL = "mysql+pymysql://root:blackmore@172.17.0.3:3306/indigo"
SQLITE_URL = "sqlite:///indigo.db"


def connect_to_db(url: str = MYSQL_URL) -> Engine:  # type: ignore
    """Create and return a SQLAlchemy engine instance.

    Args:
        url (str): Database connection URL. Defaults to DB_URL.

    Returns:
        Engine: SQLAlchemy Engine instance

    Raises:
        SQLAlchemyError: If connection fails
    """
    try:
        engine = create_engine(url, echo=True)
        with engine.connect() as conn:  # Connection test
            conn.execute(text("SELECT 1"))
        logger.info(f"Successfully connected to database at: {url}")
        return engine
    except SQLAlchemyError as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        engine = create_engine(url)
        logger.info(f"engine created: {engine}")
    except Exception as e:
        logger.error(e)
        raise


def create_tables_if_not_exist(engine: Engine) -> None:
    """Create all tables defined in Base.metadata if they don't exist.

    Args:
        engine (Engine): SQLAlchemy Engine instance

    Raises:
        SQLAlchemyError: If table creation fails
    """
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise


def init_db() -> Engine:
    """Initialize the database: connect and create tables.

    Returns:
        Engine: SQLAlchemy Engine instance
    """
    engine = connect_to_db()
    create_tables_if_not_exist(engine)
    return engine


if __name__ == "__main__":
    # Optionally run as script
    init_db()
