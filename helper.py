#!/usr/bin/python
import psycopg2
from config import config
import time
import requests


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
    session.post(auth_url, headers = headers)

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


def block_gv_seats_until(block_length, booking_url, seats):
    pass