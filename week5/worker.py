import os
import redis
import time
import logging
import sys


logging.basicConfig(
	level=logging.INFO,
	stream=sys.stdout,
	format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger(__name__)


r = redis.Redis(
	host=os.getenv("REDIS_HOST", "redis"),
	port=int(os.getenv("REDIS_PORT", "6379")),
	db=0
)

log.info("Worker started, waiting for jobs...")

#dung BRPOP voi timeout de khong spam log/CPU
while True:
	try:
		item = r.brpop("jobs", timeout=5) #block toi da 5s
		if item:
			_list, payload = item
			log.info(f"Processing job: {payload.decode()}")
			time.sleep(2)
			log.info("Done")
		else:
			log.info("No job yet...")
	except Exception as e:
		log.exception(f"Worker error: {e}")
		time.sleep(1)
