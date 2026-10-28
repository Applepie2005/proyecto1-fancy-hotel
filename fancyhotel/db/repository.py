import calendar
import os
from datetime import date, datetime, timedelta
from uuid import uuid4

import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash


LOCATIONS = ["Atlanta", "Charlotte", "Savannah", "Orlando", "Miami"]
ROOM_TYPES = [
    ("Single", 90.0, 1, 25.0),
    ("Double", 135.0, 2, 30.0),
    ("Suite", 220.0, 4, 45.0),
]


class MysqlManager(object):
    def __init__(self):
        self.config = {
            "host": os.environ.get("FANCYHOTEL_DB_HOST", "127.0.0.1"),
            "port": int(os.environ.get("FANCYHOTEL_DB_PORT", "3306")),
            "user": os.environ.get("FANCYHOTEL_DB_USER", "root"),
            "password": os.environ.get("FANCYHOTEL_DB_PASSWORD", "password"),
        }
        self.database = os.environ.get("FANCYHOTEL_DB_NAME", "Fancy_Hotel")
        self._create_database()
        self.connection = self._connect(database=self.database)
        self.init_db()

    def _connect(self, database=None):
        kwargs = dict(self.config)
        if database:
            kwargs["database"] = database
        return mysql.connector.connect(**kwargs)

    def _create_database(self):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8mb4".format(self.database))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def init_db(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Customer (
                    username CHAR(5) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(40) NOT NULL,
                    email VARCHAR(120) NOT NULL,
                    PRIMARY KEY (username),
                    UNIQUE(email)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Manager (
                    username CHAR(5) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    PRIMARY KEY (username)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Credit_Card (
                    card_number CHAR(16) NOT NULL,
                    name VARCHAR(80) NOT NULL,
                    cvv_hash VARCHAR(255) NOT NULL,
                    expiration_date DATE NOT NULL,
                    username CHAR(5) NOT NULL,
                    PRIMARY KEY (card_number),
                    FOREIGN KEY (username) REFERENCES Customer(username)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Room (
                    location VARCHAR(20) NOT NULL,
                    room_number INT NOT NULL,
                    type VARCHAR(20) NOT NULL,
                    room_cost FLOAT NOT NULL,
                    capacity INT NOT NULL,
                    extra_bed_price FLOAT DEFAULT NULL,
                    PRIMARY KEY (location, room_number)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Reservation (
                    reservation_id INT NOT NULL AUTO_INCREMENT,
                    checkin_date DATE NOT NULL,
                    checkout_date DATE NOT NULL,
                    total_cost FLOAT NOT NULL DEFAULT 0,
                    username CHAR(5) NOT NULL,
                    card_number CHAR(16) DEFAULT NULL,
                    cancelled_or_not CHAR(1) NOT NULL DEFAULT '0',
                    confirmation_code VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (reservation_id),
                    FOREIGN KEY (username) REFERENCES Customer(username),
                    FOREIGN KEY (card_number) REFERENCES Credit_Card(card_number) ON DELETE SET NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Reserves_Extra_Bed (
                    location VARCHAR(20) NOT NULL,
                    room_number INT NOT NULL,
                    reservation_id INT NOT NULL,
                    extra_bed_or_not CHAR(1) DEFAULT '0',
                    PRIMARY KEY (location, room_number, reservation_id),
                    FOREIGN KEY (location, room_number) REFERENCES Room(location, room_number),
                    FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Review (
                    review_id INT NOT NULL AUTO_INCREMENT,
                    location VARCHAR(20) NOT NULL,
                    comment VARCHAR(1000) DEFAULT NULL,
                    rating VARCHAR(20) NOT NULL,
                    username CHAR(5) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (review_id),
                    FOREIGN KEY (username) REFERENCES Customer(username)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Price_Rule (
                    rule_id INT NOT NULL AUTO_INCREMENT,
                    location VARCHAR(20) NOT NULL,
                    room_type VARCHAR(20) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    adjustment_percent FLOAT NOT NULL,
                    created_by CHAR(5) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (rule_id),
                    FOREIGN KEY (created_by) REFERENCES Manager(username)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Confirmation_Outbox (
                    outbox_id INT NOT NULL AUTO_INCREMENT,
                    reservation_id INT NOT NULL,
                    recipient_email VARCHAR(120) NOT NULL,
                    subject VARCHAR(120) NOT NULL,
                    body VARCHAR(1000) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (outbox_id),
                    FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id)
                )
                """
            )
            self.connection.commit()
            self.seed_data()
        finally:
            cursor.close()

    def seed_data(self):
        cursor = self.connection.cursor()
        try:
            customers = [
                ("C0001", "password", "Ana", "Cliente", "ana@example.com"),
                ("C0002", "password", "Luis", "Viajero", "luis@example.com"),
            ]
            for username, password, first, last, email in customers:
                cursor.execute(
                    """
                    INSERT IGNORE INTO Customer (username, password_hash, first_name, last_name, email)
                    VALUES (%(username)s, %(password_hash)s, %(first_name)s, %(last_name)s, %(email)s)
                    """,
                    {
                        "username": username,
                        "password_hash": generate_password_hash(password),
                        "first_name": first,
                        "last_name": last,
                        "email": email,
                    },
                )
            cursor.execute(
                """
                INSERT IGNORE INTO Manager (username, password_hash)
                VALUES ('M0001', %(password_hash)s)
                """,
                {"password_hash": generate_password_hash("password")},
            )
            room_number = 100
            for location in LOCATIONS:
                for room_type, cost, capacity, extra_bed_price in ROOM_TYPES:
                    for offset in range(1, 3):
                        room_number += 1
                        cursor.execute(
                            """
                            INSERT IGNORE INTO Room (location, room_number, type, room_cost, capacity, extra_bed_price)
                            VALUES (%(location)s, %(room_number)s, %(type)s, %(room_cost)s, %(capacity)s, %(extra_bed_price)s)
                            """,
                            {
                                "location": location,
                                "room_number": room_number,
                                "type": room_type,
                                "room_cost": cost + (offset - 1) * 10,
                                "capacity": capacity,
                                "extra_bed_price": extra_bed_price,
                            },
                        )
            self.connection.commit()
            self._seed_reservations()
        finally:
            cursor.close()

    def _seed_reservations(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM Reservation")
            if cursor.fetchone()["total"] > 0:
                return
            cursor.execute("SELECT * FROM Room WHERE location = 'Atlanta' ORDER BY room_number LIMIT 4")
            rooms = cursor.fetchall()
            card_number = "4111111111111111"
            cursor.execute(
                """
                INSERT IGNORE INTO Credit_Card (card_number, name, cvv_hash, expiration_date, username)
                VALUES (%(card_number)s, 'Ana Cliente', %(cvv_hash)s, %(expiration_date)s, 'C0001')
                """,
                {
                    "card_number": card_number,
                    "cvv_hash": generate_password_hash("123"),
                    "expiration_date": date.today().replace(year=date.today().year + 2),
                },
            )
            ranges = [
                (date.today() - timedelta(days=90), date.today() - timedelta(days=87), rooms[0]),
                (date.today() - timedelta(days=60), date.today() - timedelta(days=56), rooms[1]),
                (date.today() - timedelta(days=30), date.today() - timedelta(days=26), rooms[2]),
                (date.today() + timedelta(days=7), date.today() + timedelta(days=10), rooms[3]),
            ]
            for checkin, checkout, room in ranges:
                nights = (checkout - checkin).days
                total = nights * float(room["room_cost"])
                cursor.execute(
                    """
                    INSERT INTO Reservation (checkin_date, checkout_date, total_cost, username, card_number, confirmation_code)
                    VALUES (%(checkin)s, %(checkout)s, %(total)s, 'C0001', %(card_number)s, %(code)s)
                    """,
                    {
                        "checkin": checkin,
                        "checkout": checkout,
                        "total": total,
                        "card_number": card_number,
                        "code": self._confirmation_code(),
                    },
                )
                reservation_id = cursor.lastrowid
                cursor.execute(
                    """
                    INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id, extra_bed_or_not)
                    VALUES (%(location)s, %(room_number)s, %(reservation_id)s, '0')
                    """,
                    {
                        "location": room["location"],
                        "room_number": room["room_number"],
                        "reservation_id": reservation_id,
                    },
                )
            self.connection.commit()
        finally:
            cursor.close()

    def _confirmation_code(self):
        return "FH-" + uuid4().hex[:8].upper()

    def _verify_hash(self, password, stored_hash):
        return check_password_hash(stored_hash, password)

    def _room_cost_expression(self):
        return """
            ROUND(room.room_cost * (1 + COALESCE((
                SELECT pr.adjustment_percent
                FROM Price_Rule pr
                WHERE pr.location = room.location
                    AND pr.room_type = room.type
                    AND pr.start_date <= %(checkinDate)s
                    AND pr.end_date >= %(checkinDate)s
                ORDER BY pr.created_at DESC
                LIMIT 1
            ), 0) / 100), 2)
        """

    def user_exists(self, username):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT username FROM Customer WHERE username = %(username)s", {"username": username})
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def email_exists(self, email):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT email FROM Customer WHERE email = %(email)s", {"email": email})
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def register_user(self, username, email, password, first_name, last_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Customer (username, email, password_hash, first_name, last_name)
                VALUES (%(username)s, %(email)s, %(password_hash)s, %(first_name)s, %(last_name)s)
                """,
                {
                    "username": username,
                    "email": email,
                    "password_hash": generate_password_hash(password),
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            self.connection.commit()
        finally:
            cursor.close()

    def login(self, username, password):
        role = "manager" if username.upper().startswith("M") else "customer"
        table = "Manager" if role == "manager" else "Customer"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT username, password_hash FROM {} WHERE username = %(username)s".format(table),
                {"username": username},
            )
            row = cursor.fetchone()
            if row and self._verify_hash(password, row["password_hash"]):
                return {"username": username, "role": role}
            return None
        finally:
            cursor.close()

    def _card_by_last4(self, username, last4):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT card_number, expiration_date
                FROM Credit_Card
                WHERE username = %(username)s AND RIGHT(card_number, 4) = %(last4)s
                ORDER BY expiration_date DESC
                LIMIT 1
                """,
                {"username": username, "last4": last4},
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def search_rooms(self, location, checkin_date, checkout_date, room_type=None, max_price=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            filters = ["room.location = %(location)s"]
            params = {
                "location": location,
                "checkinDate": checkin_date,
                "checkoutDate": checkout_date,
            }
            if room_type:
                filters.append("room.type = %(room_type)s")
                params["room_type"] = room_type
            price_expr = self._room_cost_expression()
            if max_price:
                filters.append(price_expr + " <= %(max_price)s")
                params["max_price"] = float(max_price)
            sql = """
                SELECT room.location, room.room_number, room.type, room.room_cost, room.capacity,
                       room.extra_bed_price, {price_expr} AS effective_cost
                FROM Room room
                WHERE {filters}
                    AND NOT EXISTS (
                        SELECT 1
                        FROM Reserves_Extra_Bed bed
                        JOIN Reservation res ON res.reservation_id = bed.reservation_id
                        WHERE bed.location = room.location
                            AND bed.room_number = room.room_number
                            AND res.cancelled_or_not = '0'
                            AND res.checkin_date < %(checkoutDate)s
                            AND res.checkout_date > %(checkinDate)s
                    )
                ORDER BY room.room_cost, room.room_number
            """.format(price_expr=price_expr, filters=" AND ".join(filters))
            cursor.execute(sql, params)
            rooms = [
                {
                    "location": row["location"],
                    "room_number": row["room_number"],
                    "room_type": row["type"],
                    "cost": float(row["effective_cost"]),
                    "base_cost": float(row["room_cost"]),
                    "capacity": row["capacity"],
                    "extra_bed_price": float(row["extra_bed_price"] or 0),
                }
                for row in cursor.fetchall()
            ]
            return {"response": rooms, "result": len(rooms) > 0}
        finally:
            cursor.close()

    def is_room_free(self, room_number, location, checkin_date, checkout_date, exclude_reservation=0):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT 1
                FROM Reserves_Extra_Bed bed
                JOIN Reservation res ON res.reservation_id = bed.reservation_id
                WHERE bed.room_number = %(room_number)s
                    AND bed.location = %(location)s
                    AND res.cancelled_or_not = '0'
                    AND res.reservation_id != %(exclude_reservation)s
                    AND res.checkin_date < %(checkoutDate)s
                    AND res.checkout_date > %(checkinDate)s
                LIMIT 1
                """,
                {
                    "room_number": room_number,
                    "location": location,
                    "checkinDate": checkin_date,
                    "checkoutDate": checkout_date,
                    "exclude_reservation": int(exclude_reservation or 0),
                },
            )
            return cursor.fetchone() is None
        finally:
            cursor.close()

    def insert_reservation(self, username, checkin_date, checkout_date, card_last4, rooms, total_cost=None):
        card = self._card_by_last4(username, card_last4)
        if not card:
            return -1, "Saved card was not found", False, None
        if str(card["expiration_date"]) < checkout_date:
            return -1, "This card expires before checkout", False, None

        checkin = datetime.strptime(checkin_date, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        nights = (checkout - checkin).days
        if nights <= 0:
            return -1, "Checkout must be after check-in", False, None

        calculated_total = 0
        for room in rooms:
            if not self.is_room_free(room["room_number"], room["location"], checkin_date, checkout_date):
                return -1, "Room {} is not available".format(room["room_number"]), False, None
            calculated_total += float(room["cost"])
            if str(room.get("extra_bed_or_not", "0")) == "1":
                calculated_total += float(room.get("extra_bed_price", 0) or 0)
        calculated_total *= nights

        code = self._confirmation_code()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Reservation (username, checkin_date, checkout_date, card_number, total_cost, confirmation_code)
                VALUES (%(username)s, %(checkin_date)s, %(checkout_date)s, %(card_number)s, %(total_cost)s, %(code)s)
                """,
                {
                    "username": username,
                    "checkin_date": checkin_date,
                    "checkout_date": checkout_date,
                    "card_number": card["card_number"],
                    "total_cost": calculated_total,
                    "code": code,
                },
            )
            reservation_id = cursor.lastrowid
            for room in rooms:
                cursor.execute(
                    """
                    INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id, extra_bed_or_not)
                    VALUES (%(location)s, %(room_number)s, %(reservation_id)s, %(extra_bed_or_not)s)
                    """,
                    {
                        "location": room["location"],
                        "room_number": room["room_number"],
                        "reservation_id": reservation_id,
                        "extra_bed_or_not": str(room.get("extra_bed_or_not", "0")),
                    },
                )
            self._insert_confirmation(cursor, reservation_id, username, code)
            self.connection.commit()
            return reservation_id, "Successfully created reservation", True, code
        finally:
            cursor.close()

    def _insert_confirmation(self, cursor, reservation_id, username, code):
        cursor.execute("SELECT email FROM Customer WHERE username = %(username)s", {"username": username})
        email = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT INTO Confirmation_Outbox (reservation_id, recipient_email, subject, body)
            VALUES (%(reservation_id)s, %(email)s, %(subject)s, %(body)s)
            """,
            {
                "reservation_id": reservation_id,
                "email": email,
                "subject": "Fancy Hotel reservation {}".format(code),
                "body": "Your reservation was created. Confirmation code: {}".format(code),
            },
        )

    def get_rooms_for_reservation(self, username, reservation_id):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT room.location, room.room_number, room.type, room.room_cost, room.capacity,
                       room.extra_bed_price, bed.extra_bed_or_not
                FROM Room room
                JOIN Reserves_Extra_Bed bed ON room.location = bed.location AND room.room_number = bed.room_number
                JOIN Reservation res ON res.reservation_id = bed.reservation_id
                WHERE res.reservation_id = %(reservation_id)s AND res.username = %(username)s
                """,
                {"reservation_id": reservation_id, "username": username},
            )
            return [
                {
                    "location": row["location"],
                    "room_number": row["room_number"],
                    "room_type": row["type"],
                    "cost": float(row["room_cost"]),
                    "capacity": row["capacity"],
                    "extra_bed_price": float(row["extra_bed_price"] or 0),
                    "extra_bed_or_not": row["extra_bed_or_not"],
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()

    def get_reservation(self, username, reservation_id, include_cancelled=False):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cancelled_filter = "" if include_cancelled else "AND cancelled_or_not = '0'"
            cursor.execute(
                """
                SELECT reservation_id, checkin_date, checkout_date, total_cost, username,
                       RIGHT(card_number, 4) AS card_last4, cancelled_or_not, confirmation_code
                FROM Reservation
                WHERE reservation_id = %(reservation_id)s AND username = %(username)s {cancelled_filter}
                """.format(cancelled_filter=cancelled_filter),
                {"reservation_id": reservation_id, "username": username},
            )
            row = cursor.fetchone()
            if not row:
                return {}
            return {
                "reservation_id": row["reservation_id"],
                "checkin_date": str(row["checkin_date"]),
                "checkout_date": str(row["checkout_date"]),
                "total_cost": float(row["total_cost"]),
                "username": row["username"],
                "card_last4": row["card_last4"],
                "cancelled_or_not": row["cancelled_or_not"],
                "confirmation_code": row["confirmation_code"],
                "rooms": self.get_rooms_for_reservation(username, reservation_id),
            }
        finally:
            cursor.close()

    def update_reservation(self, username, reservation_id, checkin_date, checkout_date, total_cost):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE Reservation
                SET checkin_date = %(checkin_date)s, checkout_date = %(checkout_date)s, total_cost = %(total_cost)s
                WHERE reservation_id = %(reservation_id)s AND username = %(username)s AND cancelled_or_not = '0'
                """,
                {
                    "reservation_id": reservation_id,
                    "checkin_date": checkin_date,
                    "checkout_date": checkout_date,
                    "username": username,
                    "total_cost": total_cost,
                },
            )
            self.connection.commit()
            return ("Reservation updated", cursor.rowcount > 0)
        finally:
            cursor.close()

    def calculate_reservation_cost(self, username, reservation_id, checkin_date, checkout_date):
        checkin = datetime.strptime(checkin_date, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        nights = (checkout - checkin).days
        if nights <= 0:
            return None, "Checkout must be after check-in"
        rooms = self.get_rooms_for_reservation(username, reservation_id)
        total = 0
        for room in rooms:
            if not self.is_room_free(room["room_number"], room["location"], checkin_date, checkout_date, reservation_id):
                return None, "Some rooms are not free during the specified dates"
            total += float(room["cost"])
            if str(room["extra_bed_or_not"]) == "1":
                total += float(room["extra_bed_price"])
        return total * nights, ""

    def cancel_reservation(self, username, reservation_id):
        reservation = self.get_reservation(username, reservation_id, False)
        if not reservation:
            return "This reservation does not exist", False
        checkin = datetime.strptime(reservation["checkin_date"], "%Y-%m-%d").date()
        days_until_checkin = (checkin - date.today()).days
        if days_until_checkin <= 1:
            cancellation_cost = reservation["total_cost"]
        elif days_until_checkin < 4:
            cancellation_cost = reservation["total_cost"] * 0.20
        else:
            cancellation_cost = 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE Reservation
                SET cancelled_or_not = '1', total_cost = %(total_cost)s
                WHERE reservation_id = %(reservation_id)s AND username = %(username)s AND cancelled_or_not = '0'
                """,
                {"reservation_id": reservation_id, "username": username, "total_cost": cancellation_cost},
            )
            self.connection.commit()
            return "", cursor.rowcount > 0
        finally:
            cursor.close()

    def add_credit_card(self, username, card_number, cvv, expiration_date, card_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Credit_Card (card_number, name, cvv_hash, expiration_date, username)
                VALUES (%(card_number)s, %(name)s, %(cvv_hash)s, %(expiration_date)s, %(username)s)
                """,
                {
                    "card_number": card_number,
                    "name": card_name,
                    "cvv_hash": generate_password_hash(cvv),
                    "expiration_date": expiration_date,
                    "username": username,
                },
            )
            self.connection.commit()
            return "Credit card successfully created", True
        except mysql.connector.IntegrityError:
            return "This credit card already exists", False
        finally:
            cursor.close()

    def get_credit_cards(self, username):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT name, RIGHT(card_number, 4) AS last4, expiration_date, username
                FROM Credit_Card
                WHERE username = %(username)s
                ORDER BY expiration_date DESC
                """,
                {"username": username},
            )
            return [
                {
                    "name": row["name"],
                    "last4": row["last4"],
                    "masked_number": "************" + row["last4"],
                    "expiration_date": str(row["expiration_date"]),
                    "username": row["username"],
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()

    def delete_credit_card(self, username, card_last4):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM Credit_Card
                WHERE username = %(username)s AND RIGHT(card_number, 4) = %(last4)s
                """,
                {"username": username, "last4": card_last4[-4:]},
            )
            self.connection.commit()
            return ("Credit card deleted", cursor.rowcount > 0)
        finally:
            cursor.close()

    def get_reservation_by_card_number(self, username, card_last4):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT reservation_id, checkin_date, checkout_date, total_cost, username,
                       RIGHT(card_number, 4) AS card_last4, cancelled_or_not
                FROM Reservation
                WHERE username = %(username)s AND RIGHT(card_number, 4) = %(last4)s
                """,
                {"username": username, "last4": card_last4[-4:]},
            )
            return [
                {
                    "reservation_id": row["reservation_id"],
                    "checkin_date": str(row["checkin_date"]),
                    "checkout_date": str(row["checkout_date"]),
                    "total_cost": float(row["total_cost"]),
                    "username": row["username"],
                    "card_last4": row["card_last4"],
                    "cancelled_or_not": row["cancelled_or_not"],
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()

    def has_completed_stay(self, username, location):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT 1
                FROM Reservation res
                JOIN Reserves_Extra_Bed bed ON bed.reservation_id = res.reservation_id
                WHERE res.username = %(username)s
                    AND bed.location = %(location)s
                    AND res.cancelled_or_not = '0'
                    AND res.checkout_date < CURDATE()
                LIMIT 1
                """,
                {"username": username, "location": location},
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def add_review(self, username, location, comment, rating):
        if not self.has_completed_stay(username, location):
            return "Only customers with a completed stay can review this location", False
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Review (location, comment, rating, username)
                VALUES (%(location)s, %(comment)s, %(rating)s, %(username)s)
                """,
                {"location": location, "comment": comment, "rating": rating, "username": username},
            )
            self.connection.commit()
            return "Review created", True
        finally:
            cursor.close()

    def get_reviews(self, location):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT review_id, location, comment, rating, username, created_at
                FROM Review
                WHERE location = %(location)s
                ORDER BY created_at DESC
                """,
                {"location": location},
            )
            return [
                {
                    "review_id": row["review_id"],
                    "location": row["location"],
                    "comment": row["comment"],
                    "rating": row["rating"],
                    "username": row["username"],
                    "created_at": str(row["created_at"]),
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()

    def reservation_report(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT MONTH(checkin_date) AS month, bed.location, COUNT(*) AS total
                FROM Reservation res
                JOIN Reserves_Extra_Bed bed ON res.reservation_id = bed.reservation_id
                WHERE res.cancelled_or_not = '0'
                GROUP BY MONTH(checkin_date), bed.location
                ORDER BY month, bed.location
                """
            )
            return self._nested_month_report(cursor.fetchall(), "total")
        finally:
            cursor.close()

    def room_report(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT month, location, type, total
                FROM (
                    SELECT MONTH(res.checkin_date) AS month, room.location, room.type, COUNT(*) AS total,
                           ROW_NUMBER() OVER (PARTITION BY MONTH(res.checkin_date), room.location ORDER BY COUNT(*) DESC) AS rn
                    FROM Room room
                    JOIN Reserves_Extra_Bed bed ON room.location = bed.location AND room.room_number = bed.room_number
                    JOIN Reservation res ON res.reservation_id = bed.reservation_id
                    WHERE res.cancelled_or_not = '0'
                    GROUP BY MONTH(res.checkin_date), room.location, room.type
                ) ranked
                WHERE rn = 1
                ORDER BY month, location
                """
            )
            report = {}
            for row in cursor.fetchall():
                month = str(row["month"])
                report.setdefault(month, {}).setdefault(row["location"], []).append(
                    {"type": row["type"], "count": row["total"]}
                )
            return report
        finally:
            cursor.close()

    def revenue_report(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT MONTH(res.checkin_date) AS month, bed.location, SUM(res.total_cost) AS total
                FROM Reservation res
                JOIN Reserves_Extra_Bed bed ON res.reservation_id = bed.reservation_id
                WHERE res.cancelled_or_not = '0'
                GROUP BY MONTH(res.checkin_date), bed.location
                ORDER BY month, bed.location
                """
            )
            return self._nested_month_report(cursor.fetchall(), "total")
        finally:
            cursor.close()

    def _nested_month_report(self, rows, value_name):
        report = {}
        for row in rows:
            month = str(row["month"])
            report.setdefault(month, {})[row["location"]] = float(row[value_name])
        return report

    def calendar_availability(self, location, month):
        year, month_number = [int(part) for part in month.split("-")]
        _, days_in_month = calendar.monthrange(year, month_number)
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM Room WHERE location = %(location)s", {"location": location})
            total_rooms = cursor.fetchone()["total"]
            days = []
            for day in range(1, days_in_month + 1):
                current = date(year, month_number, day)
                next_day = current + timedelta(days=1)
                cursor.execute(
                    """
                    SELECT COUNT(DISTINCT bed.room_number) AS booked
                    FROM Reserves_Extra_Bed bed
                    JOIN Reservation res ON res.reservation_id = bed.reservation_id
                    WHERE bed.location = %(location)s
                        AND res.cancelled_or_not = '0'
                        AND res.checkin_date < %(next_day)s
                        AND res.checkout_date > %(current)s
                    """,
                    {"location": location, "current": current, "next_day": next_day},
                )
                booked = cursor.fetchone()["booked"]
                if booked == 0:
                    status = "available"
                elif booked >= total_rooms:
                    status = "full"
                else:
                    status = "partial"
                days.append({"date": str(current), "booked": booked, "total": total_rooms, "status": status})
            return {"location": location, "month": month, "days": days}
        finally:
            cursor.close()

    def demand_forecast(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT location, COUNT(*) AS room_count
                FROM Room
                GROUP BY location
                """
            )
            room_counts = {row["location"]: row["room_count"] for row in cursor.fetchall()}
            cursor.execute(
                """
                SELECT bed.location, YEAR(res.checkin_date) AS year, MONTH(res.checkin_date) AS month,
                       SUM(DATEDIFF(res.checkout_date, res.checkin_date)) AS booked_nights
                FROM Reservation res
                JOIN Reserves_Extra_Bed bed ON bed.reservation_id = res.reservation_id
                WHERE res.cancelled_or_not = '0'
                GROUP BY bed.location, YEAR(res.checkin_date), MONTH(res.checkin_date)
                """
            )
            historical = cursor.fetchall()
            by_location = {}
            for row in historical:
                month_days = calendar.monthrange(row["year"], row["month"])[1]
                capacity = room_counts.get(row["location"], 1) * month_days
                occupancy = round((float(row["booked_nights"] or 0) / capacity) * 100, 2)
                by_location.setdefault(row["location"], []).append(
                    {"year": row["year"], "month": row["month"], "occupancy": occupancy}
                )
            today = date.today().replace(day=1)
            forecast = []
            for location in LOCATIONS:
                values = by_location.get(location, [])
                fallback = round(sum(v["occupancy"] for v in values[-3:]) / max(len(values[-3:]), 1), 2)
                for offset in range(1, 4):
                    future_month = today + timedelta(days=35 * offset)
                    future_month = future_month.replace(day=1)
                    same_month = [v["occupancy"] for v in values if v["month"] == future_month.month]
                    predicted = round(sum(same_month) / len(same_month), 2) if same_month else fallback
                    suggestion = "+15%" if predicted >= 80 else "+8%" if predicted >= 60 else "0%"
                    forecast.append(
                        {
                            "location": location,
                            "month": future_month.strftime("%Y-%m"),
                            "predicted_occupancy": predicted,
                            "price_suggestion": suggestion,
                        }
                    )
            return {"historical": by_location, "forecast": forecast}
        finally:
            cursor.close()

    def add_price_rule(self, location, room_type, start_date, end_date, adjustment_percent, created_by):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Price_Rule (location, room_type, start_date, end_date, adjustment_percent, created_by)
                VALUES (%(location)s, %(room_type)s, %(start_date)s, %(end_date)s, %(adjustment_percent)s, %(created_by)s)
                """,
                {
                    "location": location,
                    "room_type": room_type,
                    "start_date": start_date,
                    "end_date": end_date,
                    "adjustment_percent": adjustment_percent,
                    "created_by": created_by,
                },
            )
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def price_rules(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT rule_id, location, room_type, start_date, end_date, adjustment_percent, created_by, created_at
                FROM Price_Rule
                ORDER BY created_at DESC
                """
            )
            return [
                {
                    "rule_id": row["rule_id"],
                    "location": row["location"],
                    "room_type": row["room_type"],
                    "start_date": str(row["start_date"]),
                    "end_date": str(row["end_date"]),
                    "adjustment_percent": float(row["adjustment_percent"]),
                    "created_by": row["created_by"],
                    "created_at": str(row["created_at"]),
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()

    def confirmations(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT outbox_id, reservation_id, recipient_email, subject, body, created_at
                FROM Confirmation_Outbox
                ORDER BY created_at DESC
                LIMIT 20
                """
            )
            return [
                {
                    "outbox_id": row["outbox_id"],
                    "reservation_id": row["reservation_id"],
                    "recipient_email": row["recipient_email"],
                    "subject": row["subject"],
                    "body": row["body"],
                    "created_at": str(row["created_at"]),
                }
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()
