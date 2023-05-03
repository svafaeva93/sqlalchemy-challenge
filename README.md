## SQLAlchemy-Challenge

Instructions

As part of trip planning for a long holiday vacation in Honolulu, Hawaii, climate analysis about the area was needed. The following sections outline the steps taken to accomplish this task.

Part 1: Analyze and Explore the Climate Data

This section required use of Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Tools such as SQLAlchemy ORM queries, Pandas, and Matplotlib were required. 

1. Used (climate_starter.ipynb and hawaii.sqlite) to complete climate analysis and data exploration.

2. Used the SQLAlchemy create_engine() function to connect to SQLite database.

3. Used the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.

4. Linked Python to the database by creating a SQLAlchemy session.

5. Performed a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

Precipitation Analysis

1. Found the most recent date in the dataset.
2. Using that date, retreived the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Select only the "date" and "prcp" values.
4. Loaded the query results into a Pandas DataFrame. 
5. Sorted the DataFrame values by "date".
6. Plotted the results by using matplotlib and Pandas 
7. Used Pandas to print the summary statistics for the precipitation data.

Station Analysis

1. Designed a query to calculate the total number of stations in the dataset.
2. Designed a query to find the most-active stations (that is, the stations that have the most rows). 
3. Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4. Designed a query to get the previous 12 months of temperature observation (TOBS) data. 
  - Filtered by the station that has the greatest number of observations.
  - Queried the previous 12 months of TOBS data for that station.
  - Plotted the results as a histogram with bins=12
 5. Closed Session.

Part 2: Design Climate App

1. Started at the homepage.
   
   List all the available routes.

2. /api/v1.0/precipitation

Converted the query results from precipitation analysis (i.e. retrieved only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
Returned the JSON representation of your dictionary.

3. /api/v1.0/stations

Returned a JSON list of stations from the dataset.

4./api/v1.0/tobs

Queried the dates and temperature observations of the most-active station for the previous year of data.
Returned a JSON list of temperature observations for the previous year.

5./api/v1.0/<start> and /api/v1.0/<start>/<end>

Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculated TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculated TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
