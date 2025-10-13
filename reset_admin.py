from database import SessionLocal
from models import User
from auth import get_password_hash


def reset_admin():
    db = SessionLocal()
    try:
        old_admin = db.query(User).filter(User.email == "admin@test.com").first()
        if old_admin:
            db.delete(old_admin)
            db.commit()
            print("Old admin deleted")

        hashed_password = get_password_hash("admin123")
        admin = User(
            email="admin@test.com",
            name="Admin User",
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("New admin created with proper password hash")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    reset_admin()