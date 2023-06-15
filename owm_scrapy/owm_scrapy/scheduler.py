import os
import time
import schedule


schedule.every(10).minutes.do(lambda: os.system('scrapy crawl openweathermap'))

while True:
    schedule.run_pending()
    time.sleep(1)
