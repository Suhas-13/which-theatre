from show import *
from seating import *
import time


class GVShowBlock:
    def __init__(self, show_url, seats, duration):
        self.show = GVShow.from_url(show_url)
        self.cookies = None
        self.blocking = False
        self.duration = duration
        self.seats = seats

    def start_blocking(self):
        if self.duration:
            target_time = time.time() + self.duration
        self.blocking = True
        while self.blocking:
            if self.duration and time.time() > target_time:
                break
            self.show.generate_seating_plan()
            cookies = self.show.block_seats(self.seats)
            if cookies:
                self.cookies = cookies
            time.sleep(30)

    def stop_blocking(self):
        self.blocking = False
        self.show.unblock_seats(self.seats, self.cookies)
