import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create session from Python to the DB
session = Session(engine)

# Set up Flask and landing page
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii weather API!<br/>"
        f"Usage:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# /api/v1.0/precipitation
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Date 12 months ago
    last_twelve_months = dt.date.today() - relativedelta(months=12)
    p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= last_twelve_months).group_by(Measurement.date).all()
    return jsonify(p_results)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    s_results = session.query(Station.station, Station.name).all()
    return jsonify(s_results)


# /api/v1.0/tobs
# Return a JSON list of Temperature Observations (tobs) for the previous year



# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.



if __name__ == "__main__":
    app.run(debug=True)