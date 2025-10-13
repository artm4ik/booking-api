from database import SessionLocal
from models import User, UserRole
from auth import get_password_hash


def create_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@test.com").first()
        if existing:
            db.delete(existing)
            db.commit()

        hashed_password = get_password_hash("admin123")
        admin = User(
            email="admin@test.com",
            name="Admin User",
            hashed_password=hashed_password,
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print("Admin user created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()