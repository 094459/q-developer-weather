# Voting Application

This is a Flask-based voting application that allows users to get the weather given a city. It uses an external API which you will need to register for and create an API key for (https://www.weatherapi.com)

## Prerequisites

- Python 3.7 or higher
- PostgreSQL

## Installation

1. Clone the repository:
2. Create a virtual environment:

```
python -m venv venv
```


3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required dependencies:




## Database Setup

1. Ensure PostgreSQL is installed and running on your system.

2. Create a new PostgreSQL database for the application:

```
createdb weather
```


3. Update the database connection string in `app.py`:

```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/voting'
```
Replace username and password with your PostgreSQL credentials.



## Running the Application

Set the Flask application environment variables:

On Windows:

```
set FLASK_APP=app.py
set FLASK_ENV=development

```

On macOS and Linux:

```
export FLASK_APP=app.py
export FLASK_ENV=development

```

Run the Flask development server:

```
flaskk run
```

Open your web browser and navigate to http://127.0.0.1:5000 to access the application.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
