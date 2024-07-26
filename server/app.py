#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurants_dict = [restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants]
        
        return restaurants_dict, 200

api.add_resource(Restaurants, "/restaurants")


class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            return restaurant_dict, 200
        else:
            return {"error": "Restaurant not found"}, 404
        
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant is None:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
        
api.add_resource(RestaurantById, "/restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizzas_dict = [pizza.to_dict() for pizza in pizzas]

        response = make_response(
            pizzas_dict,
            200,
         )
        
        return response
    
api.add_resource(Pizzas, "/pizzas")

class RestaurantPizzas(Resource):
    def post(self):
        try:
            data = request.get_json()

            new_restaurant_pizza = RestaurantPizza(
                restaurant_id=data["restaurant_id"],
                pizza_id=data["pizza_id"],
                price=data["price"]
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            
            response_dict = new_restaurant_pizza.to_dict()

            response = make_response(
                response_dict,
                201,
            )

            return response
        except Exception:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400

api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
