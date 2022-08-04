class SeatingPlan:
    # 0 - seat not available
    # 1 - seat taken
    # 2 - seat temporarily blocked
    # 3 - seat available

    def __init__(self, seat_matrix):
        self.seat_matrix = seat_matrix

    def row_count(self):
        return len(self.seat_matrix)

    def is_seat_available(self, row, col):
        return self.seat_matrix[row][col].status == 2

class GVSeatingPlan(SeatingPlan):
    AVAILABLE_STATUSES = ['L']
    TEMP_UNAVAILABLE_STATUSES = ['T']
    UNAVAILABLE_STATUSES = ['B']

    ACCESSIBLE_TYPE = ['W']
    NORMAL_TYPE = ['N']

    def __init__(self, seat_matrix):
        SeatingPlan(seat_matrix)

    def get_gv_seat_status(self, status):
        if status in self.AVAILABLE_STATUSES:
            return 2
        elif status in self.TEMP_UNAVAILABLE_STATUSES:
            return 1
        elif status in self.UNAVAILABLE_STATUSES:
            return 0

    def get_gv_seat_type(self, seat_type):
        if seat_type in self.ACCESSIBLE_TYPE:
            return 0
        elif seat_type in self.NORMAL_TYPE:
            return 1



class Seat:
    def __init__(self, row, col, status, seat_type):
        self.row = row
        self.col = col
        self.status = status
        self.seat_type = seat_type



