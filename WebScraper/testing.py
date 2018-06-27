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


def main():
    r = urllib.urlopen("http://bet.hkjc.com/football/odds/odds_allodds.aspx?lang=EN&tmatchid=127438").read()
    soup = BeautifulSoup(r, 'html.parser')
    print(str(soup.find('span', id=str("127438"+ '_HHA_HG')).find('label', class_='lblGoal').text))
    print(str(soup.find('span', id=str("127438" + '_HHA_AG')).find('label', class_='lblGoal').text))
if __name__ == "__main__":
    main()