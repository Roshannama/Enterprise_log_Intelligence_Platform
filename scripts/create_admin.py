from app.auth.service import create_user
from app.db.database import SessionLocal


def main():
    db = SessionLocal()
    try:
        user = create_user(
            db=db,
            username="admin",
            email="admin@localhost.com",
            full_name="System Administrator",
            password="admin123",
            role="admin",
            department="IT",
        )
        print("Admin created successfully.")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")
    except Exception as exc:
        db.rollback()
        print(f"Could not create admin: {exc}")
    finally:
        db.close()


if __name__ == "__main__":

    main()
