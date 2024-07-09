#Author: Joey
#Description: Terminal Valorant Tracker
#07/08/24

import time
import requests
import pandas as pd
import urllib.parse
import cloudscraper
from art import *
from tqdm import tqdm
from tabulate import tabulate
from bs4 import BeautifulSoup

name = tprint("Terminal Tracker")
print("\n")
tprint("                     Valorant")
user =  str(input("Enter Username > ")).strip()

def main():
    #Assign user_input to Username
    username = user_input()

    def connection():
        global soup
        scraper = cloudscraper.create_scraper(browser='chrome', delay=10)
        response = scraper.get(username)

        #Add delay
        time.sleep(15)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

    connection()
    def Rank(tag):
        #Return "span" tags with class "stat_value"
        return tag.name == "span" and tag.has_attr("class") and "stat__value" in tag.get("class")

    def Data(tag):
        #Return "span" tags with class "value"
        return tag.name == "span" and tag.has_attr("class") and "value" in tag.get("class")

    data = soup.find_all(Data)
    t = 0
    while t <= 3:
        if type(data) is list:
            rank = soup.find(Rank).text
        elif type(data) != list:
            #Restart connection
            t += 1
            connection()
            for _ in tqdm(range(t), desc="Loading..."):
                pass
            check = isinstance(data, list)
            if check:
                rank = soup.find(Rank).text
        else:
            print("Restart the program!")

    #First Line
    damage_round = soup.find_all(Data)[3].text
    headshot = soup.find_all(Data)[5].text
    win_percentage = soup.find_all(Data)[6].text
    kd = soup.find_all(Data)[4].text
    wins = soup.find_all(Data)[7].text

    #Second Line
    kast = soup.find_all(Data)[8].text
    DD_round = soup.find_all(Data)[9].text
    kills = soup.find_all(Data)[10].text
    deaths = soup.find_all(Data)[11].text
    acs = soup.find_all(Data)[13].text

    #Third Line
    first_blood = soup.find_all(Data)[16].text
    kad = soup.find_all(Data)[14].text
    ace = soup.find_all(Data)[18].text

    #Add Collected Data to dictionary
    dict = {'DMG/Round':[f'{damage_round}'],
            'K/D Ratio': [f'{kd}'],
            ' Win %': [f'{win_percentage}'],
            'Headshot':[f'{headshot}']}

    dict2 = {'KAST':[f'{kast}'],
            'DDΔ/Round':[f'{DD_round}'],
            'Kills': [f'{kills}'],
            'Deaths': [f'{deaths}'],
            'ACS':[f'{acs}']}

    dict3 = {'Current Rank':[f'{rank}'],
            'K/A/D': [f'{kad}'],
            'Ace': [f'{ace}'],
            'First Bloods': [f'{first_blood}']}

    df = pd.DataFrame(dict)
    df2 = pd.DataFrame(dict2)
    df3 = pd.DataFrame(dict3)

    #Displaying the Data
    print(name)
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print(tabulate(df2, headers = 'keys', tablefmt = 'psql'))
    print(tabulate(df3, headers = 'keys', tablefmt = 'psql'))

#Take User Input and Encode
def user_input():
    encode_user = urllib.parse.quote(user)
    link = f"https://tracker.gg/valorant/profile/riot/{encode_user}/overview"
    print(link)
    return link

main()
