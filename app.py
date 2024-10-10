from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:change-me@localhost:5432/weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Fetch API key from environment variable
# you will need to register for a free account here -> https://www.weatherapi.com

API_KEY = os.environ.get('WEATHERAPI_KEY')
API_URL = 'http://api.weatherapi.com/v1/current.json'

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    tz_id = db.Column(db.String(100))
    localtime_epoch = db.Column(db.Integer)
    localtime = db.Column(db.DateTime)

class CurrentWeather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    last_updated_epoch = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)
    temp_c = db.Column(db.Float)
    temp_f = db.Column(db.Float)
    is_day = db.Column(db.Boolean)
    condition_text = db.Column(db.String(100))
    condition_icon = db.Column(db.String(200))
    condition_code = db.Column(db.Integer)
    wind_mph = db.Column(db.Float)
    wind_kph = db.Column(db.Float)
    wind_degree = db.Column(db.Integer)
    wind_dir = db.Column(db.String(10))
    pressure_mb = db.Column(db.Float)
    pressure_in = db.Column(db.Float)
    precip_mm = db.Column(db.Float)
    precip_in = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    cloud = db.Column(db.Integer)
    feelslike_c = db.Column(db.Float)
    feelslike_f = db.Column(db.Float)
    vis_km = db.Column(db.Float)
    vis_miles = db.Column(db.Float)
    uv = db.Column(db.Float)
    gust_mph = db.Column(db.Float)
    gust_kph = db.Column(db.Float)

    location = db.relationship('Location', backref=db.backref('current_weather', lazy=True))

def fetch_and_store_weather(city):
    params = {
        'key': API_KEY,
        'q': city,
        'aqi': 'no'
    }
    
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Store location data
        location_data = data['location']
        location = Location(
            name=location_data['name'],
            region=location_data['region'],
            country=location_data['country'],
            lat=location_data['lat'],
            lon=location_data['lon'],
            tz_id=location_data['tz_id'],
            localtime_epoch=location_data['localtime_epoch'],
            localtime=datetime.fromisoformat(location_data['localtime'])
        )
        db.session.add(location)
        db.session.flush()
        
        # Store current weather data
        current_data = data['current']
        current_weather = CurrentWeather(
            location_id=location.id,
            last_updated_epoch=current_data['last_updated_epoch'],
            last_updated=datetime.fromisoformat(current_data['last_updated']),
            temp_c=current_data['temp_c'],
            temp_f=current_data['temp_f'],
            is_day=current_data['is_day'] == 1,
            condition_text=current_data['condition']['text'],
            condition_icon=current_data['condition']['icon'],
            condition_code=current_data['condition']['code'],
            wind_mph=current_data['wind_mph'],
            wind_kph=current_data['wind_kph'],
            wind_degree=current_data['wind_degree'],
            wind_dir=current_data['wind_dir'],
            pressure_mb=current_data['pressure_mb'],
            pressure_in=current_data['pressure_in'],
            precip_mm=current_data['precip_mm'],
            precip_in=current_data['precip_in'],
            humidity=current_data['humidity'],
            cloud=current_data['cloud'],
            feelslike_c=current_data['feelslike_c'],
            feelslike_f=current_data['feelslike_f'],
            vis_km=current_data['vis_km'],
            vis_miles=current_data['vis_miles'],
            uv=current_data['uv'],
            gust_mph=current_data['gust_mph'],
            gust_kph=current_data['gust_kph']
        )
        db.session.add(current_weather)
        db.session.commit()
        
        return location, current_weather
    else:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        location, current_weather = fetch_and_store_weather(city)
        if location and current_weather:
            return render_template('weather.html', location=location, weather=current_weather)
        else:
            return render_template('index.html', error="Unable to fetch weather data for the specified city.")
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    location, current_weather = fetch_and_store_weather(city)
    if location and current_weather:
        return jsonify({
            'location': {
                'name': location.name,
                'region': location.region,
                'country': location.country,
                'lat': location.lat,
                'lon': location.lon
            },
            'current': {
                'temp_c': current_weather.temp_c,
                'condition': current_weather.condition_text,
                'icon': current_weather.condition_icon
            }
        })
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

