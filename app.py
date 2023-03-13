import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f"Stations:/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None,end=None):
    data=[func.min(Measurement.tobs),
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)]

    if not end:
        temps=session.query(*data).filter(Measurement.date>=start).all()
        session.close()
        temps=list(np.ravel(temps))
        return jsonify(temps)

    temps=session.query(*data).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()
    temps=list(np.ravel(temps))

    return jsonify(temps)



if __name__=="__main__":
    app.run()