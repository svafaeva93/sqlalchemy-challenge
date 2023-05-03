# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Date

from datetime import datetime, timedelta

from flask import Flask,jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#1. List all the available routes.

@app.route("/")
def home():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Below are the Available Routes for Hawaii's Weather Data:<br/>"
        f"Precipitation in the last 12 months - <a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"List of Weather Stations - <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"Temeperature Observations from the Most Active Station - <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>" 
        f"Enter a start date (yyyy-mm-dd) to obtain the minimum, maximum, and average temperatures for all dates after the specified date:/api/v1.0/<start><br>"
        f"Enter both a start and end date (yyyy-mm-dd) to obtain the minimum, maximum, and average temperatures for that date range: /api/v1.0/<start>/<end><br>"
    )

#2. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
 # Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    one_year_ago = '2016-08-23'
    recent_date = '2017-08-23'

    precipitation = session.query(Measurement.date, Measurement.prcp).\
         filter(Measurement.date.between(one_year_ago, recent_date)).all()
    
    session.close()

    output = []
    for date, prcp in precipitation:
        precipitation = {}
        precipitation["date"]=date
        precipitation["prcp"]=prcp
        output.append(precipitation)

    return jsonify(output)
#3. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    active_stations = session.query(Measurement.station, func.count(Measurement.station))\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.station).desc())
    session.close()

    result = []
    for station, count in active_stations:
        active_stations={}
        active_stations["station"]=station
        active_stations["count"]=count
        result.append(active_stations)
      
    return jsonify(result)

#4.Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    most_active_id = session.query(Measurement.station, func.count(Measurement.station))\
                            .group_by(Measurement.station)\
                            .order_by(func.count(Measurement.station).desc())\
                            .first()[0]
    
    one_year_ago = '2016-08-23'
    recent_date = '2017-08-23'

    # Query temperature observations for the previous year for the most-active station
    date_tobs_results = session.query(Measurement.date, Measurement.tobs)\
                            .filter(Measurement.station == most_active_id)\
                            .filter(Measurement.date.between(one_year_ago,recent_date))\
                            .all()
    
    session.close()

    query_values = []
    for date, tobs in date_tobs_results:
            dates_tobs = {}
            dates_tobs["date"] = date
            dates_tobs["tobs"] = tobs
            query_values.append(dates_tobs)
            
    return jsonify(query_values) 


#5. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>") 
def start_date(start):
    session = Session(engine) 

    # Create query for min, avg, and max tobs where query date is greater than or equal to the start date 
    
    start_date_query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close() 

    start_date_values =[]
    for min, avg, max in start_date_query:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["average"] = avg
        start_date_dict["max"] = max
        start_date_values.append(start_date_dict)
    
    return jsonify(start_date_values)

@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    session = Session(engine)

    # Create query for min, avg, and max tobs with a query date that's greater than or equal to the start date and less than or equal to end date

    start_end_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
  
    start_end_date_values = []
    for min, avg, max in start_end_date_query:
        start_end_date_dict = {}
        start_end_date_dict["min_temp"] = min
        start_end_date_dict["avg_temp"] = avg
        start_end_date_dict["max_temp"] = max
        start_end_date_values.append(start_end_date_dict) 
    

    return jsonify(start_end_date_values)
   
if __name__ == '__main__':
    app.run(debug=True) 