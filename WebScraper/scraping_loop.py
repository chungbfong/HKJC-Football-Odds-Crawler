import urllib
import re
import time
import datetime
import pprint
from pymongo import MongoClient
from bs4 import BeautifulSoup

connection = MongoClient("ds213209.mlab.com",13209)
db = connection["hkjcodds"]
db.authenticate("chungbhk", "marco121596")


days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
scoreline= ["0100","0000","0001","0200","0101","0002","0201","0202","0102","0300","0303","0003","0301","0103","0302","0203","0400","0004","0401","0104","0402","0204","0500","0005","0501","0105","0502","0205","-1-H","-1-D","-1-A"]

def scraping_loop():
    links = []
    matchid_isLive = []
    match_count = 0


    #looking for vaild match id pages , ie. matches can be bet
    for count in range(0,6):
        x = str(count)
        site = urllib.urlopen('http://bet.hkjc.com/football/schedule/schedule.aspx?lang=EN&pageno='+x).read()
        checkpagesoup = BeautifulSoup(site,'html.parser')
        for a in checkpagesoup.find_all(title="All Odds"):
            if str(a.get('href')) in links:
                break
            links.append(str(a.get('href')))


    #main scraping loop
    for g in links:
        r = urllib.urlopen('http://bet.hkjc.com'+g).read()
        soup = BeautifulSoup(r,'html.parser')
        a = str(filter(str.isdigit,g))
        if(soup.find("td", class_="codds")):
            had = []
            fha = []
            hha = []
            asianhad_list = []
            goal_list = [] #
            firsthalfgoal_list = [] #
            corner_list = [] #
            team = []
            isLive = False
            ttg = []
            ft_score = []
            ht_score = []
            livechannel = None

            #iterating to find home and away
            hometemp = soup.find('td',class_="codds")
            temp= hometemp.find_next()
            awaytemp= temp.find_next()
            home= str(hometemp.text).replace("(Home)","")
            away=str(awaytemp.text).replace("(Away)","")

            #time
            matchtime = str(soup.find("span",id="ctl00_cm_ucddm_spesst").text)
            matchtime = re.sub('Expected Stop Selling Time:','',matchtime)
            scrapetime= str(time.ctime())

            #league
            league = soup.find(onerror="errImg(this);",class_= True, alt = True).get('title')

            #match number
            match_day = ''
            match_no_temp = soup.find('td', class_="cteaminfo ctext").text.encode('utf-8')
            for d in days:
                if d.encode() in match_no_temp:
                    match_day = d
                    break
            match_no = filter(str.isdigit,match_no_temp)

            #isLive

            if(soup.find('img', src="/football/info/images/clock_off.gif?CV=" )):
                isLive= True
                matchid_isLive.append(a)

            # live channel
            if(isLive == True):
                if (soup.find(onclick="javascript:goTVUrl();")):
                    livechannel = soup.find(onclick="javascript:goTVUrl();").find(onerror="errImg(this);").get('title')


            #home draw away
            had.append(str(soup.find("span", id= str(a+"_HAD_H")).text))
            had.append(str(soup.find('span', id=str(a+'_HAD_D')).text))
            had.append(str(soup.find('span', id= str(a+'_HAD_A')).text))

            #first half home draw away
            fha.append(str(soup.find("span", id= str(a+"_FHA_H")).text))
            fha.append(str(soup.find('span', id=str(a+'_FHA_D')).text))
            fha.append(str(soup.find('span', id= str(a+'_FHA_A')).text))

            #handicap  home draw away
            hha.append(str(soup.find("span", id= str(a+"_HHA_H")).text))
            hha.append(str(soup.find('span', id=str(a+'_HHA_D')).text))
            hha.append(str(soup.find('span', id= str(a+'_HHA_A')).text))

            #asian handicap insertion
            if (soup.find('span', id=str(a+'_HDC_HG'))):
                #asian handicap home
                asianhad_list.append(str(soup.find('span', id=str(a+'_HDC_HG')).find('label', class_='lblGoal').text))
                asianhad_list.append(str(soup.find('span', id=str(a+'_HDC_H')).text))

                #asian handicap away
                asianhad_list.append(str(soup.find('span', id=str(a+'_HDC_AG')).find('label', class_='lblGoal').text))
                asianhad_list.append(str(soup.find('span', id=str(a+'_HDC_A')).text))


            #goal list insertion
            if (soup.find('span' ,id=str(a+'_HIL_LINE'))):
                 temp = []
                 goal = str(soup.find('span' ,id=str(a+'_HIL_LINE')).text)
                 highgodds = str(soup.find('span', id=str(a+'_HIL_H')).text)
                 lowgodds = str(soup.find('span', id=str(a+'_HIL_L')).text)
                 temp.append(goal)
                 temp.append(highgodds)
                 temp.append(lowgodds)
                 goal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_HIL_LINE_1'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_1')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_1')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_1')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                goal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_HIL_LINE_2'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_2')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                goal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_HIL_LINE_3'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_2')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                goal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_HIL_LINE_4'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_2')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                goal_list.append(temp)


            #first half goal list insertion
            if (soup.find('span' ,id=str(a+'_FHL_LINE'))):
                 temp = []
                 goal = str(soup.find('span' ,id=str(a+'_FHL_LINE')).text)
                 highgodds = str(soup.find('span', id=str(a+'_FHL_H')).text)
                 lowgodds = str(soup.find('span', id=str(a+'_FHL_L')).text)
                 temp.append(goal)
                 temp.append(highgodds)
                 temp.append(lowgodds)
                 firsthalfgoal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_FHL_LINE_1'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_1')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_1')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_1')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                firsthalfgoal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_FHL_LINE_2'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_2')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                firsthalfgoal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_FHL_LINE_3'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_3')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_3')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_3')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                firsthalfgoal_list.append(temp)

            if (soup.find('span' ,id=str(a+'_FHL_LINE_4'))):
                temp = []
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_4')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_4')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_4')).text)
                temp.append(goal)
                temp.append(highgodds)
                temp.append(lowgodds)
                firsthalfgoal_list.append(temp)

            #corner list insertion
            if(soup.find('span', id=str(a+'_CHL_LINE'))):
                temp = []
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L')).text)
                temp.append(cornerline)
                temp.append(highcodds)
                temp.append(lowcodds)
                corner_list.append(temp)

            if(soup.find('span', id=str(a+'_CHL_LINE_1'))):
                temp = []
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE_1')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H_1')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L_1')).text)
                temp.append(cornerline)
                temp.append(highcodds)
                temp.append(lowcodds)
                corner_list.append(temp)

            if(soup.find('span', id=str(a+'_CHL_LINE_2'))):
                temp = []
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE_2')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H_2')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L_2')).text)
                temp.append(cornerline)
                temp.append(highcodds)
                temp.append(lowcodds)
                corner_list.append(temp)

            #total goal
            for i in range(0,7):
                ttg.append(str(soup.find('span', id=str(a+'_TTG_'+str(i))).text))
            ttg.append(str(soup.find('span', id=str(a + '_TTG_-7')).text))

            #Full Time Correct Score
            for i in range(0,31):
                ft_score.append(str(soup.find('span', id=str(a+'_CRS_'+scoreline[i])).text))

            #Half Time Correct Score
            for i in range(0,31):
                ht_score.append(str(soup.find('span', id=str(a+'_FCS_'+scoreline[i])).text))

            #change time
            td = datetime.datetime.strptime(str(datetime.datetime.now().year) + "/" + matchtime, "%Y/%d/%m %H:%M")

            match = {
            "_id":int(a),
            "league":league,
            "home": home,
            "away": away,
            "matchtime:" : int(time.mktime(td.timetuple())),
            "int_scrapetime:":int(time.time()),
            "matchid" :int(a),
            "matchday":match_day,
            "matchno":match_no,
            "isLive":isLive,
            "livechannel" : livechannel,
            "had" : [had],
            "had_time" : [int(time.time())],
            "hha" : [hha],
            "hha_time": [int(time.time())],
            "fha" : [fha],
            "fha_time" : [int(time.time())],
            "asianhad_list" :[asianhad_list],
            "asianhad_list_time": [int(time.time())],
            "firsthalfgoal_list":[firsthalfgoal_list],
            "firsthalfgoal_list_time": [int(time.time())],
            "goal_list":[goal_list],
            "goal_list_time": [int(time.time())],
            "corner_list":[corner_list],
            "corner_list_time": [int(time.time())],
            "ttg":[ttg],
            "ttg_time":[int(time.time())],
            "ft_score":[ft_score],
            "ft_score_time": [int(time.time())],
            "ht_score":[ht_score],
            "ht_score_time": [int(time.time())]
            }

            print(a)
            print(league)
            print(home)
            print(away)
            '''
            print(league)
            print(home)
            print(away)
            print(int(time.mktime(td.timetuple())))#matchtime
            print(int(time.time()))#scrapetime
            print(a)
            print("matchid:"+a)
            print(match_day , match_no)
            print(isLive)
            print(livechannel)
            print(had) #c
            print(hha)  #c
            print(fha)  #c
            print(asianhad_list)   #c
            print(firsthalfgoal_list)  #c
            print(goal_list)   #c
            print(corner_list) #c
            print(ttg)  #c
            print(ft_score) #c
            print(ht_score) #c
            '''
            #compare or insert
            if(db.Match.find({"_id":int(a)}).count()>0):
                print("FOUND")
                flag = False
                #had compare
                temp = db.Match.find_one({"_id":int(a)})["had"]
                if (temp[-1] != had):
                    db.Match.update({"_id":int(a)},{"$push":{"had":had}})
                    db.Match.update({"_id":int(a)},{"$push":{"had_time":int(time.time())}})
                    flag = True

                #hha compare
                temp = db.Match.find_one({"_id":int(a)})["hha"]
                if (temp[-1] != hha):
                    db.Match.update({"_id":int(a)},{"$push":{"hha":hha}})
                    db.Match.update({"_id":int(a)},{"$push":{"hha_time":int(time.time())}})
                    flag = True

                #fha compare
                temp = db.Match.find_one({"_id":int(a)})["fha"]
                if (temp[-1] != fha):
                    db.Match.update({"_id":int(a)},{"$push":{"fha":fha}})
                    db.Match.update({"_id":int(a)},{"$push":{"fha_time":int(time.time())}})
                    flag = True

                #asian handicap compare
                temp = db.Match.find_one({"_id":int(a)})["asianhad_list"]
                if (temp[-1] != asianhad_list):
                    db.Match.update({"_id":int(a)},{"$push":{"asianhad_list":asianhad_list}})
                    db.Match.update({"_id":int(a)},{"$push":{"asianhad_list_time":int(time.time())}})
                    flag = True

                #goal compare
                temp = db.Match.find_one({"_id":int(a)})["goal_list"]
                if (temp[-1] != goal_list):
                    db.Match.update({"_id":int(a)},{"$push":{"goal_list":goal_list}})
                    db.Match.update({"_id":int(a)},{"$push":{"goal_list_time":int(time.time())}})
                    flag = True

                #firsthalfgoal compare
                temp = db.Match.find_one({"_id":int(a)})["firsthalfgoal_list"]
                if (temp[-1] != firsthalfgoal_list):
                    db.Match.update({"_id":int(a)},{"$push":{"firsthalfgoal_list":firsthalfgoal_list}})
                    db.Match.update({"_id":int(a)},{"$push":{"firsthalfgoal_list_time":int(time.time())}})
                    flag = True

                #corner compare
                temp = db.Match.find_one({"_id":int(a)})["corner_list"]
                if (temp[-1] != corner_list):
                    db.Match.update({"_id":int(a)},{"$push":{"corner_list":corner_list}})
                    db.Match.update({"_id":int(a)},{"$push":{"corner_list_time":int(time.time())}})
                    flag = True

                #ttg compare
                temp = db.Match.find_one({"_id":int(a)})["ttg"]
                if (temp[-1] != ttg):
                    db.Match.update({"_id":int(a)},{"$push":{"ttg":ttg}})
                    db.Match.update({"_id":int(a)},{"$push":{"ttg_time":int(time.time())}})
                    flag = True

                #ft_score compare
                temp = db.Match.find_one({"_id":int(a)})["ft_score"]
                if (temp[-1] != ft_score):
                    db.Match.update({"_id":int(a)},{"$push":{"ft_score":ft_score}})
                    db.Match.update({"_id":int(a)},{"$push":{"ft_score_time":int(time.time())}})
                    flag = True

                if flag == True:
                    print("Odds Changed and Updated")

            else:
                db.Match.insert(match)


            match_count = match_count + 1
            '''
            if match_count == 3:
                for b in db.Match.find():
                    pprint.pprint(b)
                break
            '''
    return match_count



scraping_loop()
