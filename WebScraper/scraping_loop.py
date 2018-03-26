import urllib
import re
import time
from bs4 import BeautifulSoup

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
            asianhad_array = [[], []]
            goal_array = [[], [], []]
            firsthalfgoal_array = [[], [], []]
            corner_array = [[], [], []]
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
                if d in match_no_temp:
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
                asianhad_array[0].append(str(soup.find('span', id=str(a+'_HDC_HG')).find('label', class_='lblGoal').text))
                asianhad_array[0].append(str(soup.find('span', id=str(a+'_HDC_H')).text))

                #asian handicap away
                asianhad_array[1].append(str(soup.find('span', id=str(a+'_HDC_AG')).find('label', class_='lblGoal').text))
                asianhad_array[1].append(str(soup.find('span', id=str(a+'_HDC_A')).text))


            #goal array insertion
            if (soup.find('span' ,id=str(a+'_HIL_LINE'))):
                 goal = str(soup.find('span' ,id=str(a+'_HIL_LINE')).text)
                 highgodds = str(soup.find('span', id=str(a+'_HIL_H')).text)
                 lowgodds = str(soup.find('span', id=str(a+'_HIL_L')).text)
                 goal_array[0].extend((goal,highgodds,lowgodds))

            if (soup.find('span' ,id=str(a+'_HIL_LINE_1'))):
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_1')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_1')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_1')).text)
                goal_array[1].extend((goal, highgodds, lowgodds))

            if (soup.find('span' ,id=str(a+'_HIL_LINE_2'))):
                goal = str(soup.find('span' ,id=str(a+'_HIL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_HIL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_HIL_L_2')).text)
                goal_array[2].extend((goal, highgodds, lowgodds))



            #first half goal array insertion
            if (soup.find('span' ,id=str(a+'_FHL_LINE'))):
                 goal = str(soup.find('span' ,id=str(a+'_FHL_LINE')).text)
                 highgodds = str(soup.find('span', id=str(a+'_FHL_H')).text)
                 lowgodds = str(soup.find('span', id=str(a+'_FHL_L')).text)
                 firsthalfgoal_array[0].extend((goal,highgodds,lowgodds))

            if (soup.find('span' ,id=str(a+'_FHL_LINE_1'))):
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_1')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_1')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_1')).text)
                firsthalfgoal_array[1].extend((goal, highgodds, lowgodds))

            if (soup.find('span' ,id=str(a+'_HIL_LINE_2'))):
                goal = str(soup.find('span' ,id=str(a+'_FHL_LINE_2')).text)
                highgodds = str(soup.find('span', id=str(a+'_FHL_H_2')).text)
                lowgodds = str(soup.find('span', id=str(a+'_FHL_L_2')).text)
                firsthalfgoal_array[2].extend((goal, highgodds, lowgodds))




            #corner array insertion
            if(soup.find('span', id=str(a+'_CHL_LINE'))):
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L')).text)
                corner_array[0].extend((cornerline,highcodds,lowcodds))

            if(soup.find('span', id=str(a+'_CHL_LINE_1'))):
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE_1')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H_1')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L_1')).text)
                corner_array[1].extend((cornerline, highcodds, lowcodds))

            if(soup.find('span', id=str(a+'_CHL_LINE_2'))):
                cornerline = str(soup.find('span', id=str(a+'_CHL_LINE_2')).text)
                highcodds = str(soup.find('span', id=str(a+'_CHL_H_2')).text)
                lowcodds= str(soup.find('span', id=str(a+'_CHL_L_2')).text)
                corner_array[2].extend((cornerline, highcodds, lowcodds))

            #total goal add
            for i in range(0,7):
                ttg.append(str(soup.find('span', id=str(a+'_TTG_'+str(i))).text))
            ttg.append(str(soup.find('span', id=str(a + '_TTG_-7')).text))

            #Full Time Correct Score
            for i in range(0,31):
                ft_score.append(str(soup.find('span', id=str(a+'_CRS_'+scoreline[i])).text))

            #Half Time Correct Score
            for i in range(0,31):
                ht_score.append(str(soup.find('span', id=str(a+'_FCS_'+scoreline[i])).text))

            #print out all scraping data in a match
            print(league)
            print(home)
            print(away)
            print("matchtime:" + matchtime)
            print("scrapetime:"+ scrapetime)
            print("matchid:"+a)
            print(match_day , match_no)
            print(isLive)
            print(livechannel)
            print(had)
            print(hha)
            print(fha)
            print(asianhad_array)
            print(firsthalfgoal_array)
            print(goal_array)
            print(corner_array)
            print(ttg)
            print(ft_score)
            print(ht_score)
            match_count = match_count + 1

    return match_count