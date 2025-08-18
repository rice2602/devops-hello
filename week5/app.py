import os
from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

PG_DB = os.getenv("PGDATABASE", "mydb")
PG_USER = os.getenv("PGUSER", "user")
PG_PASS = os.getenv("PGPASSWORD", "pass")
PG_HOST = os.getenv("PGHOST", "db")
PG_PORT = os.getenv("PGPORT", "5432")

@app.route('/')
def hello():
	count = r.incr('hits')
	return f'Hello from Docker Compose! You have visited {count} times.'

@app.route('/pg')
def pg_counter():
	conn = psycopg2.connect(
		dbname=PG_DB,
		user=PG_USER,
		password=PG_PASS,
		host=PG_HOST,
		port=PG_PORT
	)

	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
	cur.execute("SELECT count FROM visits;")
	row = cur.fetchone()
	if row is None:
		cur.execute("INSERT INTO visits (count) VALUES (1);")
		count = 1
	else:
		count = row[0] + 1
		cur.execute("UPDATE visits SET count = %s;", (count,))
	conn.commit()
	cur.close()
	conn.close()
	
	return f"PostgreSQL visits: {count}"

@app.route('/job')
def create_job():
	r.rpush("jobs", "do-something")
	return "Job added!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
