class SeatingPlan:
    # -1 - seat not available
    # 0 - seat taken
    # 1 - seat temporarily blocked
    # 2 - seat available

    def __init__(self, seat_matrix):
        self.seat_matrix = seat_matrix

    def row_count(self):
        return len(self.seat_matrix)

    def full_search(self, row, col):
        for row in self.seat_matrix:
            for col in row:
                if self.seat_matrix[row][col].row == row and self.seat_matrix[row][col].col == col:
                    return self.seat_matrix[row][col]
        return None

    def get_seat(self, row, col):
        if row < 0 or col < 0 or row > self.row_count() or col > len(self.seat_matrix[row - 1]):
            return self.full_search(row, col)
        elif self.seat_matrix[row - 1][col - 1].row == row and self.seat_matrix[row - 1][col - 1].col == col:
            return self.seat_matrix[row - 1][col - 1]
        else:
            return self.full_search(row, col)



class GVSeatingPlan(SeatingPlan):
    GV_SEATING_PLAN_URL = "https://www.gv.com.sg/.gv-api2/seatplan"

    AVAILABLE_STATUSES = ['L']
    TEMP_UNAVAILABLE_STATUSES = ['T']
    UNAVAILABLE_STATUSES = ['B']

    ACCESSIBLE_TYPE = ['W']
    NORMAL_TYPE = ['N']

    def __init__(self, seat_matrix):
        SeatingPlan.__init__(self, seat_matrix)

    def get_gv_seat_status(self, status):
        if status in self.AVAILABLE_STATUSES:
            return 2
        elif status in self.TEMP_UNAVAILABLE_STATUSES:
            return 1
        elif status in self.UNAVAILABLE_STATUSES:
            return 0
        else:
            return -1

    def get_gv_seat_type(self, seat_type):
        if seat_type in self.ACCESSIBLE_TYPE:
            return 0
        elif seat_type in self.NORMAL_TYPE:
            return 1
        else:
            return -1

    @staticmethod
    def create_seat_by_id(seat_id):
        row = ord(seat_id.split(":")[0]) - ord('A') + 1
        col = int(seat_id.split(":")[1])
        return Seat(row, col)



class Seat:
    def __init__(self, row, col, status = None, seat_type = None):
        self.row = row
        self.col = col
        self.status = status
        self.seat_type = seat_type

    def is_available(self):
        return self.status == 2


