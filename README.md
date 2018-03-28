# HKJC-Web-Scraper
- basic crawler of bet.hkjc.com/football for live and fixed football odds which should be used for data mining and analysis
  Only for educational use 

# Packages 
- BeautifulSoup

# Working Environment : 
- Python 2.7

# Standard Output
/*
Standard fixed football match odds printing output:


Australian Division 1               //League Name
Perth Glory                         //Home Team 
Sydney FC                           //Away Team
matchtime:29/03 18:30               //match time
scrapetime:Thu Mar 29 03:45:55 2018 //scrape time
matchid:124969                      //match id
('THU', '1')                        //match number
True                                //True = live betting, False = no live betting
T303-TVB myTV SUPER 303             //TV broadcast channel, return None if no tv broadcast channel
['3.30', '3.60', '1.85']            // Home , Draw , Away
['1.80', '3.70', '3.30']            // Handicapped Home Draw Away
['3.75', '2.25', '2.40']            // First Half Home Draw Away
//Asian Handicap 
[['0/+0.5', '2.12'], ['0/-0.5', '1.73']] 

//First Half Goal Line ['GoalLine','HighOdds','LowOdds']
[['1.5', '2.20', '1.59'], ['1/1.5', '1.90', '1.80'], ['1.5/2', '2.68', '1.41']]

//Full Time Goal Line  ['GoalLine','HighOdds','LowOdds']
[['2.5', '1.54', '2.30'], ['2.5/3', '1.68', '2.05'], ['3.5', '2.40', '1.50']]

//Corner  ['CornerLine','HighOdds','LowOdds']
[['10.5', '2.05', '1.68'], ['11.5', '2.55', '1.45'], ['13.5', '4.25', '1.18']]

//Total Goals ['0','1','2','3','4','5','6','7+']
['16.00', '6.20', '3.90', '3.75', '4.70', '7.25', '11.00', '15.00']

//Correct Score For First Half 
//["0100","0000","0001","0200","0101","0002","0201","0202","0102","0300","0303","0003","0301","0103","0302","0203","0400","0004","0401","0104","0402","0204","0500","0005","0501","0105","0502","0205","-1-H","-1-D","-1-A"]
['13.00', '16.00', '9.50', '19.00', '7.75', '10.50', '9.75', '11.00', '7.25', '40.00', '35.00', '16.00', '22.00', '12.50', '22.00', '17.00', '90.00', '30.00', '60.00', '26.00', '60.00', '35.00', '250.0', '70.00', '200.0', '60.00', '200.0', '80.00', '60.00', '150.0', '29.00']

//Correct Score For Full Time
//["0100","0000","0001","0200","0101","0002","0201","0202","0102","0300","0303","0003","0301","0103","0302","0203","0400","0004","0401","0104","0402","0204","0500","0005","0501","0105","0502","0205","-1-H","-1-D","-1-A"]
['5.60', '3.40', '4.15', '17.00', '6.25', '9.00', '17.00', '40.00', '13.00', '60.00', '400.0', '30.00', '60.00', '35.00', '150.0', '100.0', '300.0', '100.0', '300.0', '150.0', '600.0', '400.0', '900.0', '400.0', '900.0', '600.0', '1000', '900.0', '900.0', '3000', '600.0']




*/

