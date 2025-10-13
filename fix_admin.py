from database import SessionLocal, engine
from models import Base, User, UserRole
from auth import get_password_hash


def fix_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        db.query(User).delete()

        admin = User(
            email="admin@test.com",
            name="Admin User",
            hashed_password=get_password_hash("admin"),
            role=UserRole.ADMIN
        )
        db.add(admin)

        user = User(
            email="user@test.com",
            name="Regular User",
            hashed_password=get_password_hash("user"),
            role=UserRole.USER
        )
        db.add(user)

        db.commit()
        print("Users created:")
        print("Admin: admin@test.com / admin")
        print("User: user@test.com / user")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_admin()