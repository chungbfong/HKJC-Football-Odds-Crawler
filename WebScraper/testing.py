import urllib
import re
import time
from datetime import datetime as dt
import datetime
from pytz import timezone
from bs4 import BeautifulSoup
from pymongo import MongoClient
import schedule
import pprint
import timeit

connection = MongoClient("ds213209.mlab.com", 13209)
db = connection["hkjcodds"]
db.authenticate("chungbhk", "marco121596")
live_match_time = []


def main():
    for match in db.Match.find({"isLive":True,"matchtime":{"$gt":time.time()}}):
        a = match["matchtime"]
        if a not in live_match_time:
            live_match_time.append(a)
    print("Live Match Time Incoming:")
    print(live_match_time)
    print("")


if __name__ == "__main__":
    main()