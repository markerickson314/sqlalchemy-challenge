import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup

app = Flask(__name__)

# flask routes

@app.route("/")
def home():
    return (
        "Home Page<br/>"
        "Available routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date <br/>"
        "/api/v1.0/start_date/end_date<br/>"
        "<br/>"
        "start_date and end_date format as '2016-09-23'"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime(Measurement.date) >= "2016-08-23").all()
    session.close()

    data = {}
    for date, prcp in results:
        data[date] = prcp

    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station)
    session.close()

    data = []
    for station in results:
        data.append(station)
        
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(func.strftime(Measurement.date) >= "2016-08-18")
    session.close()

    data = {}
    for date, tobs in results:
        data[date] = tobs

    return jsonify(data)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), \
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def end(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), \
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    session.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)