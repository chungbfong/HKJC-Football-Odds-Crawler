import urllib
import re
import time
from bs4 import BeautifulSoup
import timeit
import pymongo
import scraping_loop as sl
import live_scraping_loop as lsl
import schedule

start_time = timeit.default_timer()


count =  lsl.live_scraping_loop()+ sl.scraping_loop()


print(count)

#running time county
elapsed = timeit.default_timer() - start_time
print(count)
print(elapsed)
print(elapsed/count)




