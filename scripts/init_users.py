from app.db.database import Base, engine
from app.db.models.user import User


def main():
    print("Creating missing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables are ready.")


if __name__ == "__main__":

    main()
