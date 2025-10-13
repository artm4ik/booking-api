from database import SessionLocal
from models import User, Hotel, Room, Flight
from auth import get_password_hash
from datetime import datetime, timedelta


def create_test_data():
    db = SessionLocal()

    try:
        admin = User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)

        user = User(
            email="user@example.com",
            name="Regular User",
            hashed_password=get_password_hash("user123"),
            role="user"
        )
        db.add(user)

        hotels_data = [
            {"name": "Grand Hotel", "city": "Moscow", "stars": 5},
            {"name": "Comfort Inn", "city": "Moscow", "stars": 3},
            {"name": "Seaside Resort", "city": "Sochi", "stars": 4},
        ]

        hotels = []
        for hotel_data in hotels_data:
            hotel = Hotel(**hotel_data)
            db.add(hotel)
            hotels.append(hotel)

        db.commit()

        rooms_data = [
            {"hotel_id": hotels[0].id, "room_type": "premium", "price": 15000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[0].id, "room_type": "standard", "price": 8000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[1].id, "room_type": "standard", "price": 5000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[2].id, "room_type": "large", "price": 12000, "rooms_count": 2, "max_people": 4},
        ]

        for room_data in rooms_data:
            room = Room(**room_data)
            db.add(room)

        flights_data = [
            {"departure_city": "Moscow", "arrival_city": "Sochi", "departure_time": datetime.now() + timedelta(days=1),
             "arrival_time": datetime.now() + timedelta(days=1, hours=3), "price": 8000, "total_seats": 180,
             "available_seats": 150},
            {"departure_city": "Moscow", "arrival_city": "Sochi", "departure_time": datetime.now() + timedelta(days=2),
             "arrival_time": datetime.now() + timedelta(days=2, hours=4), "price": 6000, "total_seats": 180,
             "available_seats": 180},
            {"departure_city": "Moscow", "arrival_city": "Saint Petersburg",
             "departure_time": datetime.now() + timedelta(days=1),
             "arrival_time": datetime.now() + timedelta(days=1, hours=1), "price": 4000, "total_seats": 120,
             "available_seats": 100},
        ]

        for flight_data in flights_data:
            flight = Flight(**flight_data)
            db.add(flight)

        test_user = User(
            email="test@example.com",
            name="Test User",
            hashed_password=get_password_hash("test123"),
            role="user"
        )
        db.add(test_user)

        db.commit()
        print("Тестовые данные созданы успешно!")

    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()