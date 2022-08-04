#!/usr/bin/python
import psycopg2
from config import config
import time


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