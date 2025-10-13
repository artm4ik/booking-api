from database import SessionLocal, engine
from models import Base, User, UserRole
from auth import get_password_hash


def create_simple_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(User).filter(User.email == "admin@example.com").first()
        if existing:
            db.delete(existing)

        admin = User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print("Admin created: admin@example.com / admin123")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_simple_admin()