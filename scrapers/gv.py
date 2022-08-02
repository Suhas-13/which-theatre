import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime, time
from Show import Show

BASE_URL = "https://www.gv.com.sg/GVBuyTickets#/"
CINEMA_URL = "https://www.gv.com.sg/.gv-api/cinemas?t=297_1659243048002"
TICKET_URL = "https://www.gv.com.sg/.gv-api/v2buytickets"
CINEMA_IDS= {}
CINEMA_NAMES = []
headers = {
    'authority': 'www.gv.com.sg',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en-SG;q=0.9,en;q=0.8',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://www.gv.com.sg',
    'referer': 'https://www.gv.com.sg/GVBuyTickets',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x_developer': 'ENOVAX',
}

def get_cinema_list(CINEMA_URL):
    cinemas = requests.post(CINEMA_URL, headers=headers)
    global CINEMA_IDS, CINEMA_NAMES
    cinema_list = cinemas.json()['data']
    for cin_list in cinema_list:
        CINEMA_IDS[cin_list['id']] = cin_list['name']
        CINEMA_NAMES.append(cin_list['name'])

def get_gv_showtimes(TICKET_URL):
    no_advance_opts = {
        'cinemaId': '',
        'filmCode': '',
        'date': '',
        'advanceSales': False,
    }
    advance_opts = {
        'cinemaId': '',
        'filmCode': '',
        'date': '',
        'advanceSales': True,
    }
    regular_shows = (requests.post('https://www.gv.com.sg/.gv-api/v2buytickets', headers=headers, json=no_advance_opts)).json()['data']['cinemas']
    advance_shows = (requests.post('https://www.gv.com.sg/.gv-api/v2buytickets', headers=headers, json=advance_opts)).json()['data']['cinemas']
    global CINEMA_IDS, CINEMA_NAMES
    if not CINEMA_IDS:
        get_cinema_list(CINEMA_URL)
    show_list = []
    for cinema in regular_shows + advance_shows:
        for movie in cinema['movies']:
            has_subtitles = len(movie['subTitles']) > 0
            subtitles = ','.join(movie['subTitles'])
            for timing in movie['times']:
                show_time = timing['time12'][0: len(timing['time12'] - 2)] + ' ' + timing['time12'][len(timing['time12'] - 2):]
                show = Show(movie['filmTitle'], CINEMA_IDS[cinema['id']], "GV", has_subtitles, subtitles,
                    timing['showDate'], "SGT", show_time,
                        movie['rating'], timing['hall'])
                show_list.append(show)
    return show_list

