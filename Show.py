import requests
from helper import authenticate_session, confirm_seat_selection, get_seat_str, make_land_request, set_base_headers
from seating import SeatingPlan, Seat, GVSeatingPlan
import urllib.parse
requests.adapters.DEFAULT_RETRIES = 3


class Show:
    EXCLUSION_LIST = ["*", "(Eng Sub) "]

    def __init__(self, theatre_chain, show_date, start_time, hall, show_url, movie_name=None, theatre_name=None, has_subtitles=None, subtitles_language=None,
                 timezone=None, rating=None, seating=None):
        self.movie_name = self.normalize(movie_name)
        self.theatre_name = theatre_name
        self.theatre_chain = theatre_chain
        self.has_subtitles = has_subtitles
        self.subtitles_language = subtitles_language
        self.show_date = show_date
        self.timezone = timezone
        self.start_time = start_time
        self.premium = self.is_premium()
        self.rating = rating
        self.hall = hall
        self.show_url = show_url
        self.seating = seating

        if self.movie_name and "(D-Box)" in self.movie_name:
            self.d_box = True
            self.movie = self.movie.replace("(D-Box) ", "")
        else:
            self.d_box = False

    def normalize(self, movie_name):
        if not movie_name:
            return None
        for exclusion in self.EXCLUSION_LIST:
            movie_name = movie_name.replace(exclusion, "")
        return movie_name

    def is_premium(self):
        if self.theatre_name is None:
            return False
        if self.theatre_chain == "GV":
            return "Gold Class" in self.theatre_name or "Deluxe" in self.theatre_name


class GVShow(Show):
    # Seat Status:
    # L - seat available
    # B - seat booked
    # T - seat blocked

    # Seat Types:
    # W - wheelchair bearth
    # N - normal seat

    def __init__(self, theatre_chain, cinema_id, film_code, show_date, start_time, hall, show_url, movie_name=None, theatre_name=None, has_subtitles=None, subtitles_language=None, timezone=None, rating=None):
        self.cinema_id = cinema_id
        self.film_code = film_code
        Show.__init__(self, theatre_chain, show_date, start_time, hall, show_url, movie_name, theatre_name, has_subtitles, subtitles_language,
                      timezone, rating)
        self.generate_seating_plan()

    @staticmethod
    def from_url(show_url):
        # https://www.gv.com.sg/GVSeatSelection#/cinemaId/80/filmCode/6811/showDate/04-08-2022/showTime/2205/hallNumber/1
        cinema_id = show_url.split("/cinemaId/")[1].split("/")[0]
        film_code = show_url.split("/filmCode/")[1].split("/")[0]
        show_date = show_url.split("/showDate/")[1].split("/")[0]
        start_time = show_url.split("/showTime/")[1].split("/")[0]
        hall = show_url.split("/hallNumber/")[1].split("/")[0]
        new_gv_show = GVShow("GV", cinema_id, film_code,
                             show_date, start_time, hall, show_url)
        return new_gv_show

    def generate_seating_plan(self):
        headers = {
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
        json_data = {
            'cinemaId': self.cinema_id,
            'filmCode': self.film_code,
            'showDate': self.show_date,
            'showTime': self.start_time,
            'hallNumber': self.hall,
        }
        session = requests.Session()
        session.headers = headers
        authenticate_session(session)
        seating_request = session.post(
            GVSeatingPlan.GV_SEATING_PLAN_URL, json=json_data)
        seating_data = seating_request.json()['data']
        seating_plan = GVSeatingPlan([])
        if not seating_data:
            self.seating_plan = seating_plan
            return
        seating_plan.seat_matrix = [[]] * len(seating_data)
        for row in range(len(seating_data)):
            seating_plan.seat_matrix[row] = [None] * len(seating_data[row])
        for row in range(len(seating_data)):
            for col in range(len(seating_data[row])):
                #print(seating_data[row][col])
                seat_status = seating_plan.get_gv_seat_status(seating_data[row][col]['status'])
                seat_type = seating_plan.get_gv_seat_type(seating_data[row][col]['type'])
                if seating_data[row][col]['rowId'] is None:
                    continue
                real_row = ord(seating_data[row][col]['rowId']) - ord('A') + 1
                real_col = int(seating_data[row][col]['columnId'])
                seating_plan.set_seat(real_row, real_col, Seat(real_row, real_col, seat_status, seat_type))
        self.seating_plan = seating_plan

    def block_seats(self, seats):
        seat_str = get_seat_str(seats, self.seating_plan)
        if not seat_str:
            return None
        session = requests.Session()
        # authenticate and generate JSESSIONID
        authenticate_session(session)
        # obtain ticket ID
        set_base_headers(session)
        ticket_url = "https://www.gv.com.sg/.gv-api/getticketprice"
        ticket_data = {"cinemaId": self.cinema_id, "filmCode": self.film_code, "showDate": self.show_date,
                       "showTime": self.start_time, "hallNumber": self.hall, "sectionId": "1", "seatType": "N", "sms": False}
        ticket_request = session.post(ticket_url, json=ticket_data)
        ticket_id = ticket_request.json()['data']['tickets'][0]['priceId']
        # create payment session
        payment_url = "https://www.gv.com.sg/.gv-api/getpaymentmodes"
        payment_data = {"priceId": ticket_id}
        payment_request = session.post(payment_url, json=payment_data)
        # confirm seats
        seats_data = confirm_seat_selection(session, seat_str)
        # land request
        land_response = make_land_request(session, seats_data)
        if land_response.status_code == 200 and 'error' not in land_response.url:
            return session.cookies
        return None

    def unblock_seats(self, seats, cookies):
        session = requests.Session()
        set_base_headers(session)
        session.cookies = cookies
        seat_str = get_seat_str(seats, self.seating_plan)
        if not seat_str:
            return None
        seats_data = confirm_seat_selection(session, seat_str)
        land_response = make_land_request(session, seats_data)
        if land_response.status_code == 200 and 'error' in land_response.url:
            return session.cookies
        return None
