## Requirements definition

The idea is that we want a web application that will allow a user to search and get a thumbnail of an image
that has been retrieved from Unsplash. In particular our web application should expose a REST API
endpoint that will allow a user to specify a search term of the desired photo to be found at Unsplash.
Optional arguments, can be the preferred orientation of the photo or the color based on which photos will
be filtered out. Only one photo should be picked ( randomly ) and then create the appropriate thumbnail.
After thumbnail generation is finished, the request user should be given a unique link that can be used to
view the thumbnail.

Constraints
- Don’t use any thumbnail functionality already offered by Unsplash.

Implementation should be in Python. A free account at Unsplash is required in order to use it’s API.
Deliverables
- A single compressed file containing the .git repository
- We should be able to verify the functionality using docker-compose

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) must be installed on your system.

### Environment Setup

1. Copy the `.env.example` file to `.env` and make sure to replace `my_api_key` with your actual Unsplash API access key:

```sh
UNSPLASH_ACCESS_KEY=your_actual_api_key
```

Save the `.env` file with your API key.

## Running the Application

The **Thumbnail API** can be easily run using Docker Compose.

1. Open your terminal and navigate to the project directory.

2. Build and start the application using the following command:

```sh
docker-compose up -d
```
This command will build the Docker containers and start the application in detached mode.

## API Documentation
You may access the API documentation under http://localhost:8000/api/docs/. The documentation provides details about each endpoint, including the supported HTTP methods, input parameters, response formats, and example requests/responses

## API Endpoints

**POST /image/random/**: Search for a random image based on specified criteria and receive image metadata in the response.

**GET /image/thumbnail/{unique_link}**: Retrieve and serve image thumbnails using a unique link provided by the /image/random/ endpoint.

## Running Tests
To run the tests with pytest, you need to attach to the Docker container. Run the following command:

```sh
docker-compose exec service pytest
```
This command will execute the tests inside the running Docker container.

## Code

- `config.py`: Manages application settings and configurations.
- `crud.py`: Defines functions for Creating database records.
- `database.py`: Handles the database connection, session management, and SQLAlchemy setup.
- `main.py`: Serves as the main entry point for the FastAPI application and includes routing definitions for the API endpoints.
- `models.py`: Contains the database models and SQLAlchemy schema.
- `schemas.py`: Defines Pydantic models for request and response data validation.
- `services.py`: Provides utility functions and services used in the application.