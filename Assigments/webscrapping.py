from bs4 import BeautifulSoup
import requests
import csv

date = input("please enter a date in the format MM/DD/YYYY: ")
website = requests.get(f"https://koora24.live/?date={date}")

About_match = []

def main(website):
    src = website.content
    soup = BeautifulSoup(src, 'lxml')
    championships = soup.find_all('div', {'class': 'AF_matches_Row'})
    for championship in championships:
        getting_match_info(championship)

    keys = About_match[0].keys()

    with open('Football.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_write = csv.DictWriter(output_file, keys)
        dict_write.writeheader()
        dict_write.writerows(About_match)
        print("File Created")

def getting_match_info(championship):
    championship_title=championship.find('span',{'class':'cup'}).text.strip()
    all_matches = championship.find_all('div', class_='AF_Match')
    for match in all_matches:
        team1 = match.find('div', {'class': 'AF_TeamName'}).text.strip()
        team2 = match.find('div', {'class': 'AF_Team AF_STeam'}).find('div', {'class': 'AF_TeamName'}).text.strip()
        match_score = match.find('div', {'class': 'AF_EventResult'}).find_all('span', {'class': 'result'})
        score = f"{match_score[0].text.strip()} - {match_score[1].text.strip()}"
        match_t = match.find('div', {'class': 'AF_Data'}).find('div', {'class': 'AF_EvTime'}).text.strip()
        About_match.append({'Title Name': championship_title, 'Team A': team1, 'Team B': team2, 'Match Score': score, 'Time': match_t})

main(website)

