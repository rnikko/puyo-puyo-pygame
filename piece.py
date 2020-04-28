from random import choice


SUB_POS = [(0, -2), (-2, 0), (0, 2), (2, 0)]
TXT_COLOR = ["R",  "G",  "B",  "P",  "Y"]
RGB_COLOR = [
    (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 0, 255),
    (255, 255, 0)
]


class Piece:
    def __init__(self):
        self.mp_c = choice(TXT_COLOR)
        self.sp_c = choice(TXT_COLOR)

        self._angle = 0

        self._mp_y = 3
        self._mp_x = 6

        self.sp_y = 1
        self.sp_x = 6

        self.prev_angle = self._angle
        self.prev_mp_y = self._mp_y
        self.prev_mp_x = self._mp_x
        self.prev_sp_y = self.sp_y
        self.prev_sp_x = self.sp_x

    def __str__(self):
        shape = [
            "",
            f"Piece Shape   .{self.sp_c}.",
            f"              .{self.mp_c}.",
            f"              ...",
            "",
            f"            Angle : {self.angle}",
            "",
            f"Main Puyo Pos - Y : {self.mp_y}",
            f"              - X : {self.mp_x}",
            "",
            f"Sub  Puyo Pos - Y : {self.sp_y}",
            f"              - X : {self.sp_x}",
            ""
        ]
        return "\n".join(shape)

    def calc_xy(self):
        self.prev_sp_x = self.sp_x
        self.prev_sp_y = self.sp_y
        self.sp_x = self._mp_x + SUB_POS[self._angle][0]
        self.sp_y = self._mp_y + SUB_POS[self._angle][1]

    def undo(self):
        self._mp_x = self.prev_mp_x
        self._mp_y = self.prev_mp_y
        self.sp_x = self.prev_sp_x
        self.sp_y = self.prev_sp_y
        self._angle = self.prev_angle

    def set_prev(self):
        self.prev_mp_x = self._mp_x
        self.prev_mp_y = self._mp_y
        self.prev_angle = self._angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_val):
        self.set_prev()
        self._angle = new_val
        self.calc_xy()

    @property
    def mp_y(self):
        return self._mp_y

    @mp_y.setter
    def mp_y(self, new_val):
        self.set_prev()
        self._mp_y = new_val
        self.calc_xy()

    @property
    def mp_x(self):
        return self._mp_x

    @mp_x.setter
    def mp_x(self, new_val):
        self.set_prev()
        self._mp_x = new_val
        self.calc_xy()
