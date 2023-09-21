# Spotideets

Spotideets is a web application that provides detailed statistics about Spotify listening habits, such as top tracks, genres, and artists over various time periods.

## Features

- Retrieve album information via the Spotify Web API using the `/v1/albums/{album_id}` endpoint.
- Create and manage albums, tracks, artists, and genres in the database.
- Establish relationships between albums, tracks, artists, and genres.
- Display top tracks, genres, and artists based on user preferences.
- Authenticate users using Spotify authentication.

## Technologies Used

- Python
- Django
- Django REST Framework
- Spotipy (Python library for the Spotify Web API)
- PostgreSQL (as the database)
- Redis (for caching)
- Gunicorn (as the WSGI server)
- Docker (for containerization)

## Installation

1. Clone the repository: `git clone https://github.com/your_username/spotideets.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Configuration

1. Create a Spotify Developer account and set up a new application.
2. Configure the following environment variables:
   - `SPOTIFY_CLIENT_ID`: Your Spotify application's client ID.
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify application's client secret.
   - [DATABASE_URL](file:///Users/stemitom/PycharmProjects/spotideets/spotideets/settings.py#97%2C24-97%2C24): The URL of your PostgreSQL database.
   - `REDIS_URL`: The URL of your Redis server.
   - [SECRET_KEY](file:///Users/stemitom/PycharmProjects/spotideets/spotideets/settings.py#26%2C1-26%2C1): A secret key for Django's cryptographic functions.

## Usage

1. Access the application at `http://localhost:8000`.
2. Log in with your Spotify account.
3. Explore the various features and statistics provided by Spotideets.

## Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for more information.