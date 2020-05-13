import sqlalchemy
import datetime as dt
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.Measurement
Station = Base.classes.Station
session = Session(engine)
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precip_data():
    last_year = dt.date(2020,5,13) - dt.timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()
    precip_dict = {date: prcp for date, prcp in precip}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def find_stations():
    data_query = session.query(Station.station).all()
    station_list = list(np.ravel(data_query))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def monthly_temps():
    last_year = dt.date(2020,5,13) - dt.timedelta(days=365)
    data_query = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_year).all()

    temp_list = list(np.ravel(data_query))
    return jsonify(temp_list)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def temp_analysis(start=None, end=None):
    select_func = [func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        query_results = session.query(*select_func).\
            filter(Measurement.date >= start).all()
        temp = list(np.ravel(query_results))
        return jsonify(temp)

    query_results = session.query(*select_func).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temp_list = list(np.ravel(query_results))
    return jsonify(temp_list)


if __name__ == '__main__':
    app.run()

