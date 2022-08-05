#!/usr/bin/python
import psycopg2
from config import config
import time
import requests
import urllib.parse


def authenticate_session(session):
    headers = {
        'Host': 'www.gv.com.sg',
        # 'Content-Length': '5',
        'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Ts': 'YP6NlzFd9JWqpNjBLcKJbg==',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'text/plain, */*; q=0.01',
        'Tx': 'vJduj9ZLuUo4HsCc8iPG3wygsavQ4oOAaAZeXf3c1ck=',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.gv.com.sg',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.gv.com.sg/GVSeatSelection',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en;q=0.9',
    }
    auth_url = "https://www.gv.com.sg/.gv-api-v2/isauthenticated"
    session.post(auth_url, headers=headers)


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def check_for_table(table_name):
    cur.execute(
        "select exists(select * from information_schema.tables where table_name=%s)", (table_name,))
    return cur.fetchone()[0]


def get_seat_str(seats, seating_plan):
    seat_list = []
    for seat in seats:
        seat_id = (chr(ord('A') + seat.row - 1) +
                   ":" + str(seat.col).zfill(2))
        seat_index = seating_plan.get_seat_index(seat.row, seat.col)
        if not seat_index:
            continue
        new_seat = seating_plan.get_seat(seat_index[0], seat_index[1])
        if new_seat and new_seat.is_available():
            seat_list.append(seat_id)
    if len(seat_list) == 0:
        return None
    seat_str = "|".join(seat_list) + '|'
    return seat_str


'''

cur = connect()
if not check_for_table("shows"):
    show_table = (
        """
        CREATE TABLE shows (
                movie VARCHAR(400) NOT NULL,
                theatre VARCHAR(400) NOT NULL,
                theatre_chain VARCHAR(200) NOT NULL,
                has_subtitles BOOLEAN NOT NULL,
                subtitles_language VARCHAR(100),
                date DATE NOT NULL,
                timezone VARCHAR(30),
                start_time time NOT NULL,
                premium BOOLEAN NOT NULL,
                rating VARCHAR(15),
                hall VARCHAR(10),
                bookingUrl VARCHAR(100)
        )
        """)
    cur.execute(show_table)

'''


def make_land_request(session, seats_data):
    land_url = "https://upayment.gv.com.sg/web/land"
    session.headers = {
        'Host': 'upayment.gv.com.sg',
        # 'Content-Length': '203',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.gv.com.sg',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.gv.com.sg/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en;q=0.9',
    }
    land_response = session.post(land_url, data=seats_data)
    return land_response


def confirm_seat_selection(session, seat_str):
    seats_data = {"seats": seat_str, "paymentModeId": 1, "appId": "",
                  "vcJson": "", "patronType": None, "declaredQty": None}
    seats_url = "https://www.gv.com.sg/.gv-api/confirmselection"
    seats_request = session.post(seats_url, json=seats_data)
    seats_data = "data=" + urllib.parse.quote(seats_request.json()['data'])
    return seats_data


def set_base_headers(session):
    session.headers = {
        'Host': 'www.gv.com.sg',
        'Sec-Ch-Ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'X_developer': 'ENOVAX',
        'Content-Type': 'application/json; charset=UTF-8',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.gv.com.sg',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.gv.com.sg/GVSeatSelection',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

