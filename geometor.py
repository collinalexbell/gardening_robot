import math


class Geometor:
    def __init__(self):
        self.origin = (0, 0)

    def is_in_angle(self, point, angle_range):
        """Returns True if point is in angle relative to origin"""
#       Make points relative to origin
        x_r_point = point[0] - self.origin[0]
        y_r_point = point[1] - self.origin[1]
        r_point = (x_r_point, y_r_point)

#       Get angle to relative to origin
        if r_point[0] == 0 and r_point[1] == 0:
            return True
#       Anytime x = 0, then there will be a divide by 0 error, handle it
        if r_point[0] == 0:
            if r_point[1] > 0:
                angle = 90
            else:
                angle = 270
        else:
            angle = math.degrees(math.atan(r_point[1]/r_point[0]))

#       Convert angle if x is negative since atan is pi to -pi
        if r_point[0] < 0:
            angle += 180

#       Test if that angle is between the range
        if((angle_range[0] - angle_range[1]) < 0):
            print("In first if")
            if angle >= angle_range[0] and angle <= angle_range[1]:
                return True
            else:
                return False
        else:
            if angle >= angle_range[0] or angle <= angle_range[1]:
                return True
            else:
                return False
