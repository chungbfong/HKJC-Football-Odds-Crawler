import urllib
import re
import time
from bs4 import BeautifulSoup
import timeit


scoreline= ["0100","0000","0001","0200","0101","0002","0201","0202","0102","0300","0303","0003","0301","0103","0302","0203","0400","0004","0401","0104","0402","0204","0500","0005","0501","0105","0502","0205","-1-H","-1-D","-1-A"]

#return match count
def live_scraping_loop ():
    print("live")
    match_count = 0

    r = urllib.urlopen('http://bet.hkjc.com/football/index.aspx?lang=en').read()
    soup = BeautifulSoup(r,'html.parser')
    current_live_match_id = []


    #append live-in match id into array
    for a in soup.findAll('a',  text = 'Match in progress, accepting bets now'):
        current_link = str(filter(str.isdigit,str(a.get('href'))))
        if current_link in current_live_match_id :
            break
        current_live_match_id.append(current_link)

    for a in soup.findAll('a',  text = 'Accept In Play Betting Only'):
        current_link = str(filter(str.isdigit,str(a.get('href'))))
        if current_link in current_live_match_id :
            break
        current_live_match_id.append(current_link)


    #scraping
    for a in current_live_match_id:
        flag = 0

        r = urllib.urlopen('http://bet.hkjc.com/football/odds/odds_inplay_all.aspx?lang=EN&tmatchid=' + a).read()
        soup = BeautifulSoup(r, 'html.parser')
        if (soup.find("td", class_="codds")):
            had = []
            next_goal_array = []
            goal_array = [[],[],[]]
            corner_array = [[],[]]
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
            next_goal_array.append(str(soup.find("span", id= str(a+"_NTS_H")).text))
            next_goal_array.append(str(soup.find("span", id=str(a + "_NTS_N")).text))
            next_goal_array.append(str(soup.find("span", id=str(a + "_NTS_A")).text))

            #corner
            if(soup.find(class_ ='spTotalCorner')):
                current_corner = str(soup.find("span", class_ ='spTotalCorner').text)
                if (soup.find('span', id=str(a + '_CHL_LINE_1'))):
                    corner_array[0].append(str(soup.find(id=str(a+'_CHL_LINE')).text))
                    corner_array[0].append(str(soup.find(id=str(a + '_CHL_H')).text))
                    corner_array[0].append(str(soup.find(id=str(a + '_CHL_L')).text))
                if(soup.find('span', id=str(a+'_CHL_LINE_1'))):
                    corner_array[1].append(str(soup.find( id=str(a+'_CHL_LINE_1')).text))
                    corner_array[1].append(str(soup.find(id=str(a + '_CHL_H_1')).text))
                    corner_array[1].append(str(soup.find(id=str(a + '_CHL_L_1')).text))

            #goal
            for i in range(0,3):
                if i ==0 : ii = ""
                else: ii = str(i)
                if(soup.find('span', id=str(a + '_HIL_LINE'+ii))):
                    goal_array[i].append(str(soup.find('span', id=str(a + '_HIL_LINE'+ii)).text))
                    goal_array[i].append(str(soup.find('span', id=str(a + '_HIL_H'+ii)).text))
                    goal_array[i].append(str(soup.find('span', id=str(a + '_HIL_L'+ii)).text))

            # Full Time Correct Score
            for i in range(0, 31):
                ft_score.append(str(soup.find('span', id=str(a + '_CRS_' + scoreline[i])).text))


            print(league)
            print(home)
            print(away)
            print(a)
            print(score)
            print(had)
            print(next_goal_array)
            print(current_corner)
            print(corner_array)
            print(goal_array)
            print(ft_score)

            match_count = match_count + 1

        else:
            flag = flag + 1
            if flag == 3:
                break


    return match_count
