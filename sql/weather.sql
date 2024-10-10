-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Locations table
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    latitude NUMERIC(10,8) NOT NULL,
    longitude NUMERIC(11,8) NOT NULL,
    timezone_id VARCHAR(50),
    localtime_epoch BIGINT,
    local_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Weather data table
CREATE TABLE weather_data (
    weather_id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL,
    last_updated_epoch BIGINT,
    last_updated TIMESTAMP WITH TIME ZONE,
    temp_c NUMERIC(5,2),
    temp_f NUMERIC(5,2),
    is_day BOOLEAN,
    condition_text VARCHAR(100),
    condition_icon VARCHAR(255),
    condition_code INTEGER,
    wind_mph NUMERIC(5,2),
    wind_kph NUMERIC(5,2),
    wind_degree INTEGER,
    wind_dir VARCHAR(3),
    pressure_mb NUMERIC(6,1),
    pressure_in NUMERIC(5,2),
    precip_mm NUMERIC(5,2),
    precip_in NUMERIC(5,2),
    humidity INTEGER,
    cloud INTEGER,
    feelslike_c NUMERIC(5,2),
    feelslike_f NUMERIC(5,2),
    windchill_c NUMERIC(5,2),
    windchill_f NUMERIC(5,2),
    heatindex_c NUMERIC(5,2),
    heatindex_f NUMERIC(5,2),
    dewpoint_c NUMERIC(5,2),
    dewpoint_f NUMERIC(5,2),
    vis_km NUMERIC(5,1),
    vis_miles NUMERIC(5,1),
    uv NUMERIC(3,1),
    gust_mph NUMERIC(5,2),
    gust_kph NUMERIC(5,2),
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);
