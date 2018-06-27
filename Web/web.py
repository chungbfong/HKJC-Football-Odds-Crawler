'''
match = {
    'had':[
            {   'time':time,
                'home';home,
                'draw':draw,
                'away':away
            }

          ]

    'hha':[
            {   'time':time,
                'home';home,
                'draw':draw,
                'away':away
            }

          ]

    'fha':[
            {   'time':time,
                'home_line':home_line,
                'home':home,
                'draw':draw,
                'away_line',:away_line,
                'away':away
            }

          ]

    'fg':{

            {
                'time':time,
                'home':home,
                'no_goal':no_goal,
                'away':away

            }


         }

    'asianhad':[

            {
             'time':time,
              'home_line' :  home_line,
              'home' : home,
              'away_line':away_line,
              'away' : away

            }


               ]

    'goal':[

        {

        'time':time,
        'data':[

         {
            'goal_line' = goal_line,
          'high' = 'high'
          'low' = 'low'
        ]


    ]




}

'''


import urllib
import re
import time
from datetime import datetime as dt
import datetime
from pytz import timezone
from bs4 import BeautifulSoup
from pymongo import MongoClient
import schedule
import timeit
live_match_time = []
ongoing_match = False
ongoing_match_end_time = 0
connection = MongoClient("ds213209.mlab.com", 13209)
db = connection["hkjcodds"]
db.authenticate("chungbhk", "marco121596")
scoreline= ["0100","0000","0001","0200","0101","0002","0201","0202","0102","0300","0303","0003","0301","0103","0302","0203","0400","0004","0401","0104","0402","0204","0500","0005","0501","0105","0502","0205","-1-H","-1-D","-1-A"]

#return match count
def live_scraping_loop ():
    try:
        print("live")
        match_count = 0

        r = urllib.urlopen('http://bet.hkjc.com/football/index.aspx?lang=en').read()
        soup = BeautifulSoup(r,'html.parser')
        current_live_match_id = []


        #append live-in match id into array
        for a in soup.findAll('a',  text = 'Match in progress, accepting bets now'):
            try:
                current_link = str(filter(str.isdigit,str(a.get('href'))))
                if current_link in current_live_match_id :
                    break
                current_live_match_id.append(current_link)
            except:
                print("Error Found!")
                pass

        for a in soup.findAll('a',  text = 'Accept In Play Betting Only'):
            try:
                current_link = str(filter(str.isdigit,str(a.get('href'))))
                if current_link in current_live_match_id :
                    break
                current_live_match_id.append(current_link)
            except:
                print("Error Found!")
                pass


        #scraping
        for a in current_live_match_id:
            #try:
                flag = 0
                r = urllib.urlopen('http://bet.hkjc.com/football/odds/odds_inplay_all.aspx?lang=EN&tmatchid=' + a).read()
                soup = BeautifulSoup(r, 'html.parser')
                if (soup.find("td", class_="codds")):
                    had = []
                    next_goal = []
                    goal_list = []
                    corner_list = []
                    ft_score = []
                    current_corner = 0
                    score = 0

                    hometemp = soup.find('td',class_="codds")
                    temp= hometemp.find_next()
                    awaytemp= temp.find_next()
                    home= str(hometemp.text).replace("(Home)","")
                    away=str(awaytemp.text).replace("(Away)","")
                    league = soup.find(onerror="errImg(this);", class_=True, alt=True).get('title')

                    score = str(soup.find("span", class_ = "nolnk span_vs").text)
                    #add home draw away odds
                    had.append(str(soup.find("span", id= str(a+"_HAD_H")).text))
                    had.append(str(soup.find('span', id=str(a+'_HAD_D')).text))
                    had.append(str(soup.find('span', id= str(a+'_HAD_A')).text))

                    #next Goal
                    next_goal.append(str(soup.find("span", id= str(a+"_NTS_H")).text))
                    next_goal.append(str(soup.find("span", id=str(a + "_NTS_N")).text))
                    next_goal.append(str(soup.find("span", id=str(a + "_NTS_A")).text))

                    #corner
                    if(soup.find(class_ ='spTotalCorner')):
                        current_corner = str(soup.find("span", class_ ='spTotalCorner').text)
                        if (soup.find('span', id=str(a + '_CHL_LINE'))):
                            temp = []
                            temp.append(str(soup.find(id=str(a+'_CHL_LINE')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_H')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_L')).text))
                            corner_list.append(temp)
                        if(soup.find('span', id=str(a+'_CHL_LINE_1'))):
                            temp = []
                            temp.append(str(soup.find( id=str(a+'_CHL_LINE_1')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_H_1')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_L_1')).text))
                            corner_list.append(temp)
                        if(soup.find('span', id=str(a+'_CHL_LINE_2'))):
                            temp = []
                            temp.append(str(soup.find( id=str(a+'_CHL_LINE_2')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_H_2')).text))
                            temp.append(str(soup.find(id=str(a + '_CHL_L_2')).text))
                            corner_list.append(temp)

                    #goal
                    for i in range(0,3):
                        if i ==0 : ii = ""
                        else: ii = str(i)
                        if(soup.find('span', id=str(a + '_HIL_LINE'+ii))):
                            temp = []
                            temp.append(str(soup.find('span', id=str(a + '_HIL_LINE'+ii)).text))
                            temp.append(str(soup.find('span', id=str(a + '_HIL_H'+ii)).text))
                            temp.append(str(soup.find('span', id=str(a + '_HIL_L'+ii)).text))
                            goal_list.append(temp)

                    # Full Time Correct Score
                    for i in range(0, 31):
                        ft_score.append(str(soup.find('span', id=str(a + '_CRS_' + scoreline[i])).text))

                    match = {
                        "_id": int(a),
                        "league": league,
                        "home": home,
                        "away": away,
                        "start_time": int(time.time()),
                        "halftime":[],
                        "score": [score],
                        "score_time":[int(time.time())],
                        "current_corner":[current_corner],
                        "curremt_corner_time":[int(time.time())],
                        "goal_list":[goal_list],
                        "goal_list_time":[int(time.time())],
                        "had":[had],
                        "had_time":[int(time.time())],
                        "next_goal":[next_goal],
                        "next_goal_time":[int(time.time())],
                        "corner_list":[corner_list],
                        "corner_list_time":[int(time.time())],
                        "ft_score":[ft_score],
                        "ft_score_time":[int(time.time())]
                    }
                    print(league)
                    print(home)
                    print(away)
                    print(a)
                    print(score)
                    print(had)
                    print(next_goal)
                    print(current_corner)
                    print(corner_list)
                    print(goal_list)
                    print(ft_score)
                    print("")

                    if (db.LiveMatch.find({"_id": int(a)}).count() > 0):
                        print("FOUND")
                        flag = False
                        temp = db.LiveMatch.find_one({"_id": int(a)})["score"]
                        #score compare
                        if (temp[-1] != score):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"score": score}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"score_time": int(time.time())}})
                            flag = True

                        temp = db.LiveMatch.find_one({"_id": int(a)})["current_corner"]
                        #current_corner compare
                        if (temp[-1] != current_corner):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"current_corner": current_corner}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"current_corner_time": int(time.time())}})
                            flag = True

                        # had compare
                        temp = db.LiveMatch.find_one({"_id": int(a)})["had"]
                        if (temp[-1] != had):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"had": had}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"had_time": int(time.time())}})
                            flag = True

                        # next_goal compare
                        temp = db.LiveMatch.find_one({"_id": int(a)})["next_goal"]
                        if (temp[-1] != next_goal):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"next_goal": next_goal}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"next_goal_time": int(time.time())}})
                            flag = True

                        # corner compare
                        temp = db.LiveMatch.find_one({"_id": int(a)})["corner_list"]
                        if (temp[-1] != corner_list):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"corner_list": corner_list}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"corner_list_time": int(time.time())}})
                            flag = True

                        # goal compare
                        temp = db.LiveMatch.find_one({"_id": int(a)})["goal_list"]
                        if (temp[-1] != goal_list):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"goal_list": goal_list}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"goal_list_time": int(time.time())}})
                            flag = True

                        # ft_score compare
                        temp = db.LiveMatch.find_one({"_id": int(a)})["ft_score"]
                        if (temp[-1] != ft_score):
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"ft_score": ft_score}})
                            db.LiveMatch.update({"_id": int(a)}, {"$push": {"ft_score_time": int(time.time())}})
                            flag = True

                    else:
                        db.LiveMatch.insert(match)

                    match_count = match_count + 1

                else:
                    flag = flag + 1
                    if flag == 3:
                        break
            #except Exception as e:
                #print("Error Found!")
                #print(e)
                #pass
        if(len(current_live_match_id)==0):
            ongoing_match = False
        else:
            ongoing_match= True
        return match_count

    except:
        pass

def main():
    try:
        schedule.every(1).minutes.do(live_scraping_loop)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        pass

main()
