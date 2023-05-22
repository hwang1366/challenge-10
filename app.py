# Import the dependencies.
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

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
# Define what to do when a user hits the index route.
@app.route("/")
def welcome():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

#Define what to do when a user hits the precipitation route.
@app.route("/api/v1.0/precipitation")
def precipitation():

    recent_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)

    year_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago, Measurement.prcp != None).\
        order_by(Measurement.date).all()
    
    dates_precip = []
    
    for dateprecip in year_prcp:
        dateprecip_dict = {}
        dateprecip_dict["date"] = dateprecip.date
        dateprecip_dict["prcp"] = dateprecip.prcp
        dates_precip.append(dateprecip_dict)
    
    return jsonify(dict(year_prcp))

#Define what to do when a user hits the stations route.
@app.route("/api/v1.0/stations")
def stations():


    session.query(Measurement.station).distinct().count()
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
                               group_by(Measurement.station).\
                               order_by(func.count(Measurement.station).desc()).all()

    act_stations = []
    
    for act_stat in active_stations: 
        stations_dict = {}
        stations_dict["station"] = act_stat.station
        act_stations.append(stations_dict)

    return jsonify(dict(active_stations))

#Define what to do when a user hits the tobs route.
@app.route("/api/v1.0/tobs")
def tobs():
    
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    year_temp = session.query(Measurement.tobs).\
      filter(Measurement.date >= year_ago, Measurement.station == 'USC00519281').\
      order_by(Measurement.tobs).all()

    year_temps = []
    for y_temps in year_temp
        yrtemp_dict = {}
        yrtemp_dict["tobs"] = y_temps.tobs
        year_temps.append(yrtemp_dict)

    return jsonify(year_temp)

#Define what to do when a user hits the <start> route.
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    #TMIN, TAVG, and TMAX for a list of dates.
    
    #Args:
        #start_date (string): A date string in the format %Y-%m-%d
        #end_date (string): A date string in the format %Y-%m-%d
    #Returns:
        #TMIN, TAVE, and TMAX
    
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    temp_start = {}
    temp_start["min_Temp"] = results[0][0]
    temp_start["avg_Temp"] = results[0][1]
    temp_start["max_Temp"] = results[0][2]
    
    return jsonify(temp_start)

#Define what to do when a user hits the <start>/<end> route.
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temp_start_end = {}
    temp_start_end["min_Temp"] = results[0][0]
    temp_start_end["avg_Temp"] = results[0][1]
    temp_start_end["max_Temp"] = results[0][2]

    return jsonify(temp_start_end)


if __name__ == '__main__':
    app.run(debug=True)





