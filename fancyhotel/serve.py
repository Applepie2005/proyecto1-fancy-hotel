import os

from flask import Flask, render_template
from flask_restful import Api
import api_v2 as restapi



app = Flask(__name__)
app.secret_key = os.environ.get("FANCYHOTEL_SECRET_KEY", "dev-secret-key")
app.debug = True
api = Api(app)


@app.route('/')
def index():
	return render_template("index.html")

api.add_resource(restapi.LoginResource, '/api/login')
api.add_resource(restapi.LogoutResource, '/api/logout')
api.add_resource(restapi.NewUserRegistrationResource, '/api/register')
api.add_resource(restapi.SearchRoomsResource, '/api/searchRoom')
api.add_resource(restapi.CreateReservationResource, '/api/reservation/create')
api.add_resource(restapi.UpdateReservationResource, '/api/reservation')
api.add_resource(restapi.ReservationResource, '/api/reservation/<string:reservation_id>') #includes update_reservation
api.add_resource(restapi.UpdateReservationConfirmResource, '/api/reservation/<string:reservation_id>/availability')
api.add_resource(restapi.CreditCardResource, '/api/payment')
api.add_resource(restapi.ReviewResource, '/api/review')
api.add_resource(restapi.CancelReservationResource, '/api/reservation/<string:reservation_id>/cancel')
api.add_resource(restapi.CalendarAvailabilityResource, '/api/availability/calendar')
api.add_resource(restapi.ReservationReportResource, '/api/reports/reservation')
api.add_resource(restapi.PopularRoomReportResource, '/api/reports/popularRoom')
api.add_resource(restapi.RevenueReportResource, '/api/reports/revenue')
api.add_resource(restapi.DemandForecastResource, '/api/reports/demandForecast')
api.add_resource(restapi.PriceRuleResource, '/api/price-rules')
api.add_resource(restapi.ConfirmationOutboxResource, '/api/confirmations')
api.add_resource(restapi.GetReservationByCardNumberResource, '/api/reservation/cardNumber')


if __name__ == '__main__':
	host = os.environ.get("FANCYHOTEL_HOST", "127.0.0.1")
	port = int(os.environ.get("FANCYHOTEL_PORT", "5001"))
	debug = os.environ.get("FANCYHOTEL_DEBUG", "1").lower() in ("1", "true", "yes")
	use_reloader = os.environ.get("FANCYHOTEL_RELOAD", "").lower() in ("1", "true", "yes")
	print("\n>>> Abre en el navegador: http://127.0.0.1:{}\n".format(port))
	app.run(host, port, debug=debug, use_reloader=use_reloader)


