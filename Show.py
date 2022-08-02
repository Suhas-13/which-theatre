class Show:
  def __init__(self, movie, theatre, theatre_chain, has_subtitles, subtitles_language, show_date, timezone, start_time, rating, hall):
    self.movie = movie
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

  def is_premium(self):
    if self.theatre_chain == "GV":
      return "Gold Class" in self.theatre
