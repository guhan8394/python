import sqlite3

def create_db():
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            contact TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'available'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in DATE,
            check_out DATE,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_room(room_number, price):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO rooms (room_number, price, status) VALUES (?, ?, 'available')", (room_number, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_room_price(room_number, new_price):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET price = ? WHERE room_number = ?", (new_price, room_number))
    conn.commit()
    conn.close()

def get_available_rooms():
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_number, price FROM rooms WHERE status = 'available'")
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def get_booking_details():
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bookings.id, users.username, rooms.room_number, bookings.check_in, bookings.check_out
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN rooms ON bookings.room_id = rooms.id
    ''')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def add_user(username, contact, password):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, contact, password) VALUES (?, ?, ?)", (username, contact, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_credentials(username, password):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_booking(user_id, room_number):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM rooms WHERE room_number = ? AND status = 'available'", (room_number,))
    room = cursor.fetchone()
    if room:
        cursor.execute("INSERT INTO bookings (user_id, room_id, check_in) VALUES (?, ?, DATE('now'))", (user_id, room[0]))
        cursor.execute("UPDATE rooms SET status = 'booked' WHERE id = ?", (room[0],))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def cancel_booking(booking_id, user_id):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_id FROM bookings WHERE id = ? AND user_id = ?", (booking_id, user_id))
    booking = cursor.fetchone()
    if booking:
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        cursor.execute("UPDATE rooms SET status = 'available' WHERE id = ?", (booking[0],))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_user_bookings(user_id):
    conn = sqlite3.connect('hotel_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bookings.id, rooms.room_number, bookings.check_in, bookings.check_out
        FROM bookings
        JOIN rooms ON bookings.room_id = rooms.id
        WHERE bookings.user_id = ?
    ''', (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings
