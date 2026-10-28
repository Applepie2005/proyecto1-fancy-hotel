import re
from datetime import datetime

from flask import session
from flask_restful import Resource, reqparse, request

import db


class QueryRequestParser(reqparse.RequestParser):
    """Query-string args only; avoids Flask-RESTful parsing JSON on GET."""

    def add_argument(self, *args, **kwargs):
        if "location" not in kwargs:
            kwargs["location"] = "args"
        return super(QueryRequestParser, self).add_argument(*args, **kwargs)


class JsonBodyRequestParser(reqparse.RequestParser):
    """JSON body only for POST/PUT from the Angular client."""

    def add_argument(self, *args, **kwargs):
        if "location" not in kwargs:
            kwargs["location"] = "json"
        return super(JsonBodyRequestParser, self).add_argument(*args, **kwargs)


def _role():
    return session.get("role")


def _require_manager():
    if _role() != "manager":
        return {"message": "Manager role required", "result": False}, 403
    return None


def _date_delta(check_in, check_out):
    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")
    return (end - start).days


_CUSTOMER_USERNAME = re.compile(r"^C[A-Z0-9]{4}$")
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class NewUserRegistrationResource(Resource):
    def post(self):
        body = request.get_json(silent=True)
        if not body:
            return {"error": "Datos de registro inválidos. Recarga la página e intenta de nuevo.", "result": False}, 400

        username = (body.get("username") or "").strip().upper()
        email = (body.get("email") or "").strip()
        password = body.get("password") or ""
        first_name = (body.get("firstName") or "").strip()
        last_name = (body.get("lastName") or "").strip()

        if not username or not email or not password or not first_name or not last_name:
            return {"error": "Completa usuario, nombre, apellido, correo y contraseña.", "result": False}, 400
        if not _CUSTOMER_USERNAME.match(username):
            return {
                "error": "El usuario debe ser C seguido de 4 letras o números (ejemplo: C1234).",
                "result": False,
            }, 400
        if not _EMAIL.match(email):
            return {"error": "Correo electrónico inválido.", "result": False}, 400
        if len(password) < 6:
            return {"error": "La contraseña debe tener al menos 6 caracteres.", "result": False}, 400
        if db.mysqldb.user_exists(username):
            return {"error": "Ese nombre de usuario ya está registrado. Elige otro (ej. C5678).", "result": False}, 400
        if db.mysqldb.email_exists(email):
            return {"error": "Ese correo ya está registrado. Usa otro correo.", "result": False}, 400

        db.mysqldb.register_user(username, email, password, first_name, last_name)
        return {"message": "Usuario creado correctamente", "result": True}


class LoginResource(Resource):
    def __init__(self):
        self.reqparse = JsonBodyRequestParser()
        self.reqparse.add_argument("username", type=str, required=True)
        self.reqparse.add_argument("password", type=str, required=True)

    def post(self):
        args = self.reqparse.parse_args()
        login = db.mysqldb.login(args["username"].upper(), args["password"])
        if not login:
            return {"error": "Login information invalid", "result": False}, 401
        session["username"] = login["username"]
        session["role"] = login["role"]
        return {"message": "You logged in!", "result": True, "username": login["username"], "role": login["role"]}


class LogoutResource(Resource):
    def post(self):
        session.clear()
        return {"message": "Logged out", "result": True}


class SearchRoomsResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("location", type=str, required=True)
        self.reqparse.add_argument("checkIn", type=str, required=True)
        self.reqparse.add_argument("checkOut", type=str, required=True)
        self.reqparse.add_argument("roomType", type=str, required=False)
        self.reqparse.add_argument("maxPrice", type=float, required=False)

    def get(self):
        args = self.reqparse.parse_args()
        return db.mysqldb.search_rooms(
            args["location"], args["checkIn"], args["checkOut"], args.get("roomType"), args.get("maxPrice")
        )


class CreateReservationResource(Resource):
    def post(self):
        body = request.get_json(force=True)
        nights = _date_delta(body["checkIn"], body["checkOut"])
        if nights <= 0:
            return {"message": "Checkout must be after check-in", "result": False}, 400
        reservation_id, message, result, code = db.mysqldb.insert_reservation(
            body["username"],
            body["checkIn"],
            body["checkOut"],
            body.get("card_last4") or body.get("card_number", "")[-4:],
            body["rooms"],
        )
        status = 200 if result else 400
        return {"id": reservation_id, "message": message, "result": result, "confirmation_code": code}, status


class UpdateReservationResource(Resource):
    def __init__(self):
        self.reqparse = JsonBodyRequestParser()
        self.reqparse.add_argument("reservation_id", type=str, required=True)
        self.reqparse.add_argument("checkIn", type=str, required=True)
        self.reqparse.add_argument("checkOut", type=str, required=True)
        self.reqparse.add_argument("username", type=str, required=True)

    def put(self):
        args = self.reqparse.parse_args()
        return self._update(args["username"], args["reservation_id"], args["checkIn"], args["checkOut"])

    def _update(self, username, reservation_id, check_in, check_out):
        total_cost, error = db.mysqldb.calculate_reservation_cost(username, reservation_id, check_in, check_out)
        if error:
            return {"message": error, "result": False}, 400
        message, status = db.mysqldb.update_reservation(username, reservation_id, check_in, check_out, total_cost)
        return ({"message": message, "result": status, "total_cost": total_cost}, 200 if status else 400)


class ReservationResource(Resource):
    def __init__(self):
        self.reqparse = JsonBodyRequestParser()
        self.reqparse.add_argument("checkIn", type=str, required=True)
        self.reqparse.add_argument("checkOut", type=str, required=True)
        self.reqparse.add_argument("username", type=str, required=True)
        self.getreqparse = QueryRequestParser()
        self.getreqparse.add_argument("username", type=str, required=True)

    def get(self, reservation_id):
        args = self.getreqparse.parse_args()
        reservation = db.mysqldb.get_reservation(args["username"], reservation_id, False)
        if reservation:
            return {"data": reservation, "result": True}
        return {"error": "No reservation found", "result": False}, 404

    def put(self, reservation_id):
        args = self.reqparse.parse_args()
        total_cost, error = db.mysqldb.calculate_reservation_cost(
            args["username"], reservation_id, args["checkIn"], args["checkOut"]
        )
        if error:
            return {"message": error, "result": False}, 400
        message, status = db.mysqldb.update_reservation(
            args["username"], reservation_id, args["checkIn"], args["checkOut"], total_cost
        )
        return ({"message": message, "result": status, "total_cost": total_cost}, 200 if status else 400)


class UpdateReservationConfirmResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("checkIn", type=str, required=True)
        self.reqparse.add_argument("checkOut", type=str, required=True)
        self.reqparse.add_argument("username", type=str, required=True)

    def get(self, reservation_id):
        args = self.reqparse.parse_args()
        total_cost, error = db.mysqldb.calculate_reservation_cost(
            args["username"], reservation_id, args["checkIn"], args["checkOut"]
        )
        if error:
            return {"message": error, "result": False}, 400
        rooms = db.mysqldb.get_rooms_for_reservation(args["username"], reservation_id)
        return {"message": "Rooms are available", "result": True, "rooms": rooms, "total_cost": total_cost}


class CancelReservationResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("username", type=str, required=True)

    def get(self, reservation_id):
        args = self.reqparse.parse_args()
        message, status = db.mysqldb.cancel_reservation(args["username"], reservation_id)
        return ({"message": "Cancelled reservation" if status else message, "result": status}, 200 if status else 400)


class CreditCardResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("username", type=str, required=True)
        self.delete_reqparse = QueryRequestParser()
        self.delete_reqparse.add_argument("username", type=str, required=True)
        self.delete_reqparse.add_argument("card_number", type=str, required=True)
        self.create_reqparse = reqparse.RequestParser()
        self.create_reqparse.add_argument("username", type=str, required=True, location="json")
        self.create_reqparse.add_argument("card_number", type=str, required=True, location="json")
        self.create_reqparse.add_argument("name", type=str, required=True, location="json")
        self.create_reqparse.add_argument("cvv", type=str, required=True, location="json")
        self.create_reqparse.add_argument("expiration_date", type=str, required=True, location="json")

    def get(self):
        args = self.reqparse.parse_args()
        return db.mysqldb.get_credit_cards(args["username"])

    def post(self):
        args = self.create_reqparse.parse_args()
        message, status = db.mysqldb.add_credit_card(
            args["username"], args["card_number"], args["cvv"], args["expiration_date"], args["name"]
        )
        return ({"message": message, "result": status}, 200 if status else 400)

    def delete(self):
        args = self.delete_reqparse.parse_args()
        reservations = db.mysqldb.get_reservation_by_card_number(args["username"], args["card_number"])
        today = datetime.now()
        for reservation in reservations:
            if (datetime.strptime(reservation["checkout_date"], "%Y-%m-%d") - today).days > 0:
                return {"message": "This card is used in a future reservation!", "result": False}, 400
        message, status = db.mysqldb.delete_credit_card(args["username"], args["card_number"])
        return ({"message": message, "result": status}, 200 if status else 400)


class ReviewResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("location", type=str, required=True)
        self.create_reqparse = reqparse.RequestParser()
        self.create_reqparse.add_argument("username", type=str, required=True, location="json")
        self.create_reqparse.add_argument("comment", type=str, required=True, location="json")
        self.create_reqparse.add_argument("rating", type=str, required=True, location="json")
        self.create_reqparse.add_argument("location", type=str, required=True, location="json")

    def get(self):
        args = self.reqparse.parse_args()
        return db.mysqldb.get_reviews(args["location"])

    def post(self):
        args = self.create_reqparse.parse_args()
        message, status = db.mysqldb.add_review(args["username"], args["location"], args["comment"], args["rating"])
        return ({"message": message, "result": status}, 200 if status else 400)


class CalendarAvailabilityResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("location", type=str, required=True)
        self.reqparse.add_argument("month", type=str, required=True)

    def get(self):
        args = self.reqparse.parse_args()
        return db.mysqldb.calendar_availability(args["location"], args["month"])


class _ManagerReport(Resource):
    def _blocked(self):
        blocked = _require_manager()
        return blocked


class ReservationReportResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.reservation_report()


class PopularRoomReportResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.room_report()


class RevenueReportResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.revenue_report()


class DemandForecastResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.demand_forecast()


class PriceRuleResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.price_rules()

    def post(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        body = request.get_json(force=True)
        rule_id = db.mysqldb.add_price_rule(
            body["location"],
            body["room_type"],
            body["start_date"],
            body["end_date"],
            float(body["adjustment_percent"]),
            session["username"],
        )
        return {"rule_id": rule_id, "message": "Price rule created", "result": True}


class ConfirmationOutboxResource(_ManagerReport):
    def get(self):
        blocked = self._blocked()
        if blocked:
            return blocked
        return db.mysqldb.confirmations()


class GetReservationByCardNumberResource(Resource):
    def __init__(self):
        self.reqparse = QueryRequestParser()
        self.reqparse.add_argument("username", type=str, required=True)
        self.reqparse.add_argument("card_number", type=str, required=True)

    def get(self):
        args = self.reqparse.parse_args()
        return db.mysqldb.get_reservation_by_card_number(args["username"], args["card_number"])
