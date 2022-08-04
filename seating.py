class SeatingPlan:
    # 0 - seat not available
    # 1 - seat taken
    # 2 - seat available
    def __init__(self, seat_matrix):
        self.seat_matrix = seat_matrix

    def is_seat_available(self, row, col):
        return self.seat_matrix[row][col].status == 2

class Seat:
    def __init__(self, row, col, status):
        self.row = row
        self.col = col
        self.status = status
