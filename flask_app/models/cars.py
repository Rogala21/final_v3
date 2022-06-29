from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers.cars import session
from flask import flash 


db = "car_dealz_db"

class car: 
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.seller_id = data['seller_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller = data['seller']
        self.status = 'Not Sold'

    @classmethod
    def new_car(cls, data):
        query = "INSERT INTO car_dealz_db.cars (price, model, make, year, description, seller_id, seller) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(seller_id)s, %(seller)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def edit_car(cls, data):
        query = "UPDATE car_dealz_db.cars SET price = %(price)s, model = %(model)s, make = %(make)s, description = %(description)s, seller_id = %(seller_id)s WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM car_dealz_db.cars LEFT JOIN car_dealz_db.cars_for_sell ON cars.id = car_id LEFT JOIN car_dealz_db.users ON user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        cars = []
        for i in results:
            car = cls(i)
            if i['car_id'] != None:
                car.status = "Sold"
            cars.append(car)
        return cars

    @classmethod
    def get_car(cls, id):
        query = "SELECT * FROM car_dealz_db.cars JOIN car_dealz_db.users ON seller_id = users.id LEFT JOIN car_dealz_db.cars_for_sell ON users.id = user_id AND cars.id = car_id WHERE cars.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        car = cls(results[0])
        if results[0]["user_id"] != None:
            car.status = "Sold"
        return car

    @classmethod
    def delete_car_for_sell(cls, id):
        query = "DELETE FROM car_dealz_db.cars_for_sell WHERE car_id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return results

    @classmethod
    def delete_car(cls, id):
        query = "DELETE FROM car_dealz_db.cars WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return results

    @classmethod
    def buy_car(cls, data):
        query = "INSERT INTO car_dealz_db.cars_for_sell (car_id, user_id) VALUES (%(car_id)s,%(user_id)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def sell_car(cls, data):
        query = "DELETE FROM car_dealz_db.cars_for_sell WHERE car_id = %(car_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_my_cars(cls, id):
        query = "SELECT * FROM car_dealz_db.cars JOIN car_dealz_db.cars_for_sell ON cars.id = car_id WHERE user_id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        cars = []
        for car in cars:
            cars.append(cls(car))
        return results

    @staticmethod
    def check_stats_car(car):
        is_valid = True 
        if int(car['price']) < 1:
            flash(u"Price Needs to be higher")
            is_valid = False
        if len(car['year']) < 1:
            flash(u"Enter a year")
            is_valid = False
        if len(car['description']) < 10:
            flash(u"Needs a longer description")
            is_valid = False
        return is_valid