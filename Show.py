import requests
from seating import SeatingPlan, Seat, GVSeatingPlan


class Show:
    EXCLUSION_LIST = ["*", "(Eng Sub) "]

    def __init__(self, theatre_chain, show_date, start_time, hall, show_url, movie_name=None, theatre_name=None, has_subtitles=None, subtitles_language=None,
                 timezone=None, rating=None, seating=None):
        self.movie_name = self.normalize(movie_name)
        self.theatre = theatre_name
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

        if "(D-Box)" in self.movie_name:
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
        if self.theatre_chain is None:
          return False
        if self.theatre_chain == "GV":
            return "Gold Class" in self.theatre or "Deluxe" in self.theatre


class GVShow(Show):
    # Seat Status:
    # L - seat available
    # B - seat booked
    # T - seat blocked

    # Seat Types:
    # W - wheelchair bearth
    # N - normal seat
    GV_SEATING_PLAN_URL = "https://www.gv.com.sg/.gv-api/seatplan"

    def __init__(self, theatre_chain, cinema_id, film_code, show_date, start_time, hall, show_url, movie_name=None, theatre_name=None, has_subtitles=None, subtitles_language=None, timezone=None, rating=None):
        self.cinema_id = cinema_id
        self.film_code = film_code
        Show.__init__(self, theatre_chain, cinema_id, film_code, show_date, start_time, hall, show_url, movie_name, theatre_name, has_subtitles, subtitles_language,
                      timezone, rating)
        self.seating_plan = self.generate_seating_plan(
            self.cinema_id, self.film_code, self.hall, self.show_date, self.start_time)

    @staticmethod
    def generate_show_from_url(show_url):
        # https://www.gv.com.sg/GVSeatSelection#/cinemaId/80/filmCode/6811/showDate/04-08-2022/showTime/2205/hallNumber/1
        cinema_id = show_url.split("/cinemaId/")[1].split("/")[0]
        film_code = show_url.split("/filmCode/")[1].split("/")[0]
        show_date = show_url.split("/showDate/")[1].split("/")[0]
        start_time = show_url.split("/showTime/")[1].split("/")[0]
        hall = show_url.split("/hallNumber/")[1].split("/")[0]
        new_gv_show = GVShow("GV", cinema_id, film_code, show_date, start_time, hall, show_url)
        new_gv_show.seating_plan = new_gv_show.generate_seating_plan()
        return new_gv_show

    def generate_seating_plan(self):
        json_data = {
            'cinemaId': self.cinema_id,
            'filmCode': self.film_code,
            'showDate': self.show_date,
            'showTime': self.start_time,
            'hallNumber': self.hall,
        }
        seating_data = requests.post(
            self.GV_SEATING_PLAN_URL, json=json_data).json()['data']
        seating_plan = GVSeatingPlan([])
        for row in seating_data:
            seating_plan.seat_matrix.append([])
            for col in row:
                seat_status = self.get_gv_seat_status(col['status'])
                seat_type = self.get_gv_seat_type(col['type'])
                seating_plan.seat_matrix[seating_plan.row_count(
                ) - 1].append(Seat(col['rowNumber'], col['colNumber'], seat_status, seat_type))
