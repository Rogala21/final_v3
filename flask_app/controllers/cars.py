from flask import render_template, redirect, request, session
from flask_app.__init__ import app
from flask_app.models.cars import car
from flask_app.models.login_register import user


@app.route ('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', cars = car.get_all_cars(), user = user.get_by_id(session['user_id']))

@app.route ('/dashboard/new/car')
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_car.html', user = user.get_by_id(session['user_id']))

@app.route ('/dashboard/edit/car/<id>')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('edit_car.html', user = user.get_by_id(session['user_id']), car = car.get_car(id))

@app.route ('/dashboard/new/car/process', methods=["POST"])
def new_car_prcoess():
    if not car.check_stats_car(request.form):
        return redirect('/dashboard/new/car')
    car.new_car(request.form)
    return redirect('/dashboard')

@app.route ('/dashboard/edit/car/process', methods=["POST"])
def edit_prcoess():
    if not car.check_stats_car(request.form):
        return redirect('/dashboard/edit/car/'+str(request.form['id']))
    car.edit_car(request.form)
    return redirect('/dashboard')

@app.route('/dashboard/delete/<id>/process')
def delete_show_process(id):
    car.delete_car_for_sell(id)
    car.delete_car(id)
    return redirect("/dashboard")

@app.route('/dashboard/car/<id>')
def car_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("car.html", car = car.get_car(id))

@app.route('/buy/<id>')
def buy_car(id):
    data = {
        "car_id": id,
        "user_id": session['user_id']
    }
    car.buy_car(data)
    return redirect('/dashboard')

@app.route('/sell/<id>')
def sell_car(id):
    data = {
        "car_id": id,
        "user_id": session['user_id']
    }
    car.sell_car(data)
    return redirect('/dashboard')

@app.route('/user')
def see_my_cars():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("all_purchased_cars.html", cars = car.get_my_cars(session['user_id']), user = user.get_by_id(session['user_id']))