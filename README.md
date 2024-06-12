
# ShiverGiver

ShiverGiver is a web application built with FastAPI that integrates with Redis for caching, Neo4j for graph database functionality, and MongoDB for document storage. This application provides efficient data management and caching mechanisms for user data, tokens, and appointments.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.8+
- Redis
- Neo4j
- MongoDB

## Packages Used

```ini
fastapi>=0.68.0,<0.69.0
uvicorn>=0.15.0,<0.16.0
redis
neo4j
pymongo
python-decouple
PyJWT 
pydantic 
passlib 
jose 
email_validator 
bcrypt 
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/shivergiver.git
cd shivergiver
```

### Install Dependencies

Create a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory of your project to manage your environment variables. Here is an example configuration:

```ini
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGO_URL=mongodb://localhost:27017
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

Replace the placeholder values with your actual configuration details.

## Running the Application

To start the FastAPI server, run the following command:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Usage
In swagger UI after the login you reaciece a token that you can add to the authorisation header which will get you authenticated and you can use all the protected routes as well

### API Documentation

FastAPI automatically generates interactive API documentation. You can access it by visiting:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Key Endpoints

- `POST /register`: Register a new user.
- `POST /login`: Authenticate a user and receive a token.
- `GET /users/profile`: Get the current user's profile (authentication required).
- `GET /users/getAllUser`: Get all user's profile (authentication required).
- `POST /appointments`: Create a new appointment (authentication required).
- `GET /appointments`: Retrieve all appointments (authentication required).
- `GET /appointments/{appointment_id}`: Retrieve a particular appointments (authentication required).
- `PUT /appointments/{appointment_id}`: update records for a particular appointments (authentication required).
- `DELETE /appointments/{appointment_id}`: deletes a particular appointments (authentication required).
- `POST /albums`: Create a new album (authentication required).
- `GET /albums`: Retrieve all albums (authentication required).
- `GET /albums/{albums_id}`: Retrieve a particular album (authentication required).
- `PUT /albums/{albums_id}`: update records for a particular album (authentication required).
- `DELETE /albums/{albums_id}`: deletes a particular album (authentication required).


##### neo4j routes

- `GET /neo4j`: creates the nodes for artist, album and the tracks and add the relation (authentication required).
- `GET /neo4j/genre`: creates the nodes for genre and add its relation to artists(authentication required).

## Development

Ensure you have all the necessary testing dependencies installed.


## Acknowledgements

Thanks to the contributors and open-source community for their valuable work and support.

## future plans
##### We are planning to implement the following features:

Artist Collaboration Suggestions: Use Neo4j relationships to suggest artists with similar genres for potential collaborations.

User Recommendations: Provide users with recommendations based on the artists they listen to or the albums they like.

---