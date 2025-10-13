from database import SessionLocal, engine
from models import Base, User, UserRole
from auth import get_password_hash


def create_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Создаем админа
        admin = User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)

        # Создаем обычного пользователя
        user = User(
            email="user@example.com",
            name="Regular User",
            hashed_password=get_password_hash("user123"),
            role=UserRole.USER
        )
        db.add(user)

        db.commit()
        print("Users created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_users()