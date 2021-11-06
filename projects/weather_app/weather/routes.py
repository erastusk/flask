from flask import Flask, render_template, url_for, redirect,flash, request
from weather.forms import SignupForm, LoginForm, ContactUsForm, CityForm
import requests
from weather.models import User, City
from weather import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required






url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid=3c118b3f2bdd1585de7625953f54d47a"

resp = {
  "base": "stations", 
  "clouds": {
    "all": 20
  }, 
  "cod": 200, 
  "coord": {
    "lat": 27.9475, 
    "lon": -82.4584
  }, 
  "dt": 1635203064, 
  "id": 4174757, 
  "main": {
    "feels_like": 79.83, 
    "humidity": 90, 
    "pressure": 1011, 
    "temp": 79.83, 
    "temp_max": 82.2, 
    "temp_min": 77.72
  }, 
  "name": "Tampa", 
  "sys": {
    "country": "US", 
    "id": 2005199, 
    "sunrise": 1635161779, 
    "sunset": 1635202270, 
    "type": 2
  }, 
  "timezone": -14400, 
  "visibility": 10000, 
  "weather": [
    {
      "description": "few clouds", 
      "icon": "10d", 
      "id": 801, 
      "main": "Clouds"
    }
  ], 
  "wind": {
    "deg": 270, 
    "speed": 4.61
  }
}
default_city = {
        'city' : 'Tampa',
        'temperature' : resp['main']['temp'],
        'high' : resp['main']['temp_max'],
        'low' : resp['main']['temp_min'],
        'description' : resp['weather'][0]['description'],
        'icon' :resp['weather'][0]['icon'],
        'country': resp['sys']['country']
    }

@app.route("/", methods=['POST', 'GET'])
def home ():
  if current_user.is_authenticated:
        return redirect(url_for('profile'))
  if request.method == 'POST':        
    resp_owm =  requests.get(url.format(city_name=request.form['city'])).json()
    if resp_owm['cod'] == 200:
      #If city is not found cod key value type is a string, when found it's a int.
      weather = {
        'city' : resp_owm['name'],
        'temperature' : resp_owm['main']['temp'],
        'high' : resp_owm['main']['temp_max'],
        'low' : resp_owm['main']['temp_min'],
        'description' : resp_owm['weather'][0]['description'],
        'icon' :resp_owm['weather'][0]['icon'],
        'country_flag': resp_owm['sys']['country'].lower(),
        'country': resp_owm['sys']['country']}
      return render_template('home.html', weather=weather)
    else:
        flash('City Not Found!')
  return render_template('home.html', weather=default_city)
  
    

    
@app.route("/contact", methods=['POST', 'GET'])
def contact ():
    form = ContactUsForm()
    if form.validate_on_submit():  
        flash(f'Thank you {form.firstname.data}!', 'we will get back to you shortly')      
        return render_template ('contactus.html', form=form)    
    return render_template ('contactus.html', form=form)

@app.route("/signup", methods=['POST', 'GET'])
def signup ():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data} created!', 'success')
        return redirect(url_for('signin'))   
    return render_template ('signup.html', form=form)

@app.route("/signin", methods=['POST', 'GET'])
def login ():
    
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
          login_user(user)
          next_page = request.args.get('next')
          flash(f'Sign in for {form.email.data} successful!', 'success')
          return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
          flash('Login Unsuccessful. Please check email and password', 'danger')   
    return render_template ('signin.html', form=form)

def refresh_profile_cities():
  profile_db_cities = City.query.filter_by(user_id=current_user.id).all()
  return profile_db_cities

def get_weather (cities):
  profile_ui_cities =  []
  for city in cities:
    resp_owm =  requests.get(url.format(city_name=city.city)).json()
    city = {
    'city' : resp_owm['name'],
    'temperature' : resp_owm['main']['temp'],
    'high' : resp_owm['main']['temp_max'],
    'low' : resp_owm['main']['temp_min'],
    'description' : resp_owm['weather'][0]['description'],
    'icon' :resp_owm['weather'][0]['icon'],
    'country_flag': resp_owm['sys']['country'].lower(),
    'country': resp_owm['sys']['country']}
    profile_ui_cities.append(city)
  return profile_ui_cities        

@app.route("/profile", methods=['POST', 'GET'])
@login_required
def profile ():
  if request.method == 'POST':
    delete_city = City.query.filter_by(city=request.form['close_city'].lower(),user_id=current_user.id).delete()
    db.session.commit() 
    cities = refresh_profile_cities()
    if cities:
      weather_res_cities = get_weather(cities)
      return render_template ('profile.html', cities=weather_res_cities, email=current_user.email)
  else:
      cities = refresh_profile_cities()
      if cities:
        weather_res_cities = get_weather(cities)
        return render_template ('profile.html', cities=weather_res_cities, email=current_user.email)
  return render_template ('profile.html', cities=[default_city], email=current_user.email)      


@app.route("/add_city", methods=['POST', 'GET'])
@login_required

def profile_add_city ():
    if request.method == 'POST':  
        resp_owm =  requests.get(url.format(city_name=request.form['city'])).json()
        if resp_owm['cod'] == 200:
            city = City.query.filter_by(city=request.form['city'],user_id=current_user.id).first()
            if city:
                flash(f'City already exists!', 'success') 
            else:
                city = City(city=request.form['city'], user_id=current_user.id)
                db.session.add(city)
                db.session.commit() 
                flash(f"{request.form['city']} successfully Added!", 'success')
                return redirect(url_for('profile'))
        else:
          flash('City Not Found!')  
          return redirect(url_for('profile'))
    return redirect(url_for('profile'))                  

     

@app.route("/logout", methods=['POST', 'GET'])
def logout ():
    logout_user()
    return render_template('home.html', weather=default_city)   