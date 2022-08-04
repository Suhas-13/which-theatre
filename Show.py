import requests


class Show:
    EXCLUSION_LIST = ["*", "(Eng Sub) "]

    def __init__(self, movie, theatre, theatre_chain, has_subtitles, subtitles_language, show_date, timezone, start_time, rating, hall, show_url, seating=None):
        self.movie = self.normalize(movie)
        self.theatre = theatre
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

        if "(D-Box)" in self.movie:
            self.d_box = True
            self.movie = self.movie.replace("(D-Box) ", "")
        else:
            self.d_box = False

    def normalize(self, movie_name):
        for exclusion in self.EXCLUSION_LIST:
            movie_name = movie_name.replace(exclusion, "")
        return movie_name

    def is_premium(self):
        if self.theatre_chain == "GV":
            return "Gold Class" in self.theatre or "Deluxe" in self.theatre


class GVShow(Show):
    GV_SEATING_PLAN_URL = "https://www.gv.com.sg/.gv-api/seatplan"

    def __init__(self, movie, theatre, theatre_chain, has_subtitles, subtitles_language, show_date, timezone, start_time, rating, hall, show_url, cinema_id, film_code):
        self.cinema_id = cinema_id
        self.film_code = film_code
        Show.__init__(self, movie, theatre, theatre_chain, has_subtitles, subtitles_language,
                      show_date, timezone, start_time, rating, hall, show_url, seating=None)
        self.seating_plan = self.generate_seating_plan(
            self.cinema_id, self.film_code, self.hall, self.show_date, self.start_time)

    def generate_seating_plan(self, cinema_id, film_code, hall_number, show_date, show_time):
        json_data = {
            'cinemaId': cinema_id,
            'filmCode': film_code,
            'showDate': show_date,
            'showTime': show_time,
            'hallNumber': hall_number,
        }
        seating_plan = requests.post(self.GV_SEATING_PLAN_URL, json=json_data).json()

