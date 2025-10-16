# Booking API - Сервис бронирования отелей и авиабилетов

## Описание
Backend-приложение для бронирования отелей и авиабилетов с системой авторизации, ролевой моделью и полным CRUD функционалом.

## Функциональность
- 🔐 JWT авторизация и регистрация
- 🏨 Бронирование номеров в отелях
- ✈️ Поиск и бронирование авиабилетов
- 👥 Ролевая модель (user/admin)
- 🔍 Фильтрация и сортировка
- 📚 Полная документация API

## Технологии
- Python 3.8+
- FastAPI
- SQLAlchemy
- SQLite
- JWT аутентификация

## Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/artm4ik/booking-api.git
cd booking-api
Создайте виртуальное окружение:

bash
python3 -m venv venv
source venv/bin/activate
Установите зависимости:

bash
pip install -r requirements.txt
Создайте тестовые данные:

bash
python fix_admin.py
Запустите сервер:

bash
python3 main.py
Откройте документацию:
http://localhost:8000/docs

Тестовые пользователи
Админ: admin@test.com / admin

Пользователь: user@test.com / user

Основные API Endpoints
Пользователи
POST /users/register - Регистрация

POST /users/login - Вход в систему

GET /users/me - Профиль пользователя

PUT /users/me - Обновление профиля

Отели
GET /hotels/ - Поиск отелей (фильтры: city, stars)

POST /hotels/ - Создание отеля (только админ)

GET /hotels/{id}/rooms - Номера отеля (фильтры: room_type, price, max_people)

Бронирования
POST /bookings/ - Бронирование номера

GET /bookings/my - Мои бронирования

DELETE /bookings/{id} - Отмена бронирования

Авиабилеты
GET /flights/ - Поиск рейсов

POST /flights/search - Расширенный поиск рейсов

POST /flights/{id}/book - Бронирование билета

GET /flights/my-tickets - Мои билеты

Фильтрация и сортировка
Отели:
По городу: GET /hotels/?city=Moscow

По звездам: GET /hotels/?stars=5

Сортировка по звездам (по убыванию)

Номера:
По типу: GET /hotels/1/rooms?room_type=premium

По цене: GET /hotels/1/rooms?max_price=10000

По количеству людей: GET /hotels/1/rooms?min_people=2

Сортировка по цене (по возрастанию)

Особенности реализации
JWT токены с сроком действия 30 минут

Проверка доступности номеров при бронировании

Автоматический расчет количества дней проживания

Специальные категории для авиабилетов ("самый быстрый", "самый дешевый")

Полная валидация данных

Обработка ошибок с понятными сообщениями
