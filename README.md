# CGM Data Insights: A Flask-Powered Web App for Continuous Glucose Monitoring Analysis

## Aims
- Continuously ingest data from an API, store it efficiently and visualise the results
- This project aims to improve skills such as database management, data engineering, web development, and application design, with an emphasis on modularity and computational efficiency

#### -- Project Status: [Complete]

---

## Project Objective

The main objective is to develop a seamless pipeline for real-time monitoring of blood glucose levels using data from Libre Freestyle sensors. The project emphasizes efficient data processing, storage, and visualization, providing insights into glucose levels over time. The use of psycopg2 for database interactions and connection pooling are key components in enhancing the system's performance.

## Data Source

The data is sourced directly from my Libre Freestyle sensor, utilizing its API to fetch real-time Continuous Glucose Monitoring (CGM) data.

## Technologies

* Python
* PostgreSQL
* Requests
* NumPy
* psycopg2
* SQLAlchemy
* Flask
* Pandas
* Plotly
* schedule
* atexit

## Methodologies

- **Data Fetching:** Utilizing the `requests` library to connect to the Libre Freestyle sensor API and fetch real-time CGM data.
- **Data Processing:** Applying basic transformations such as data type conversions to ensure data integrity and compatibility with the database.
- **Database Management:** Employing `psycopg2` for efficient data loading into a PostgreSQL database, utilizing connection pooling to optimize database interactions and reduce overhead.
- **Visualization:** Implementing a Flask application to visualize the blood glucose data using `Plotly`, providing real-time insights into glucose levels.
- **Continuous Operation:** Using `schedule` for periodic data fetching and `atexit` to ensure graceful shutdown of processes, the system operates continuously on a VM for uninterrupted data monitoring and analysis.

---

## Skills

### Database Management
- Managing database connections, executing transactions, and retrieving data
- Relational database operations and SQL
- Optimising data storage and retrieval processes, improving data commit efficiency

### API Integration and Data Ingestion
- Fetching data from external APIs, integrating third-party data sources into application
- Handling API authentication and managing data queries based on specific user contexts

### Data Processing and Analysis
- Preprocessing and transforming raw data for database insertion
- Handling of various data types and management of missing or inconsistent data
- Analysing and visualising data using Flask for presentation

### Modular Programming and Software Architecture
- Object-oriented programming, structuring functionality into Management classes like AuthenticationManagement

### Web Development and Visualisation
- Implementation of web-based interfaces using Flask for data visualisation
- Integration of data processing and visualisation into a web application, enhancing user interaction

### File Management and Persistence
- Managing data persistence using various formats (e.g., JSON, Parquet), enabling flexible data storage and access patterns.
- Management of data files, including saving, loading, and amending operations, to support the application's data lifecycle.

---

## Contacts

For more information or to discuss this project further, please reach out.

Email: delstonds@outlook.com
