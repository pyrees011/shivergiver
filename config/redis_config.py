import redis
from decouple import config

# Redis connection configuration
REDIS_HOST= config("REDIS_HOST")
REDIS_PORT= config("REDIS_PORT")
REDIS_DB= config("REDIS_DB")

try:
    # Create a new connection
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    # Test the connection
    redis_conn.ping()
    print("Pinged your deployment. You successfully connected to Redis!")
# except redis.ConnectionError as e:
#     print(f"Could not connect to Redis: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
