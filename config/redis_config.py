import redis

# Redis connection configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

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
