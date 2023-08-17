import redis
from apscheduler.schedulers.blocking import BlockingScheduler

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Define a function to read a value from a key
def read_value():
    value = r.get('some_key')
    print(value)

# Create a scheduler
sched = BlockingScheduler()

# Schedule the function to run every minute
sched.add_job(read_value, 'interval', minutes=1)

# Start the scheduler
sched.start()
