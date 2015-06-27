import math


class Geometor:
    """Class used to do geometric manipulations"""

    def __init__(self):
        self.origin = (0, 0)

    def _tuple_is_usable(self, origin):
        """Tests the tuple for errors

            Returns: True if no error or throws Exception if error

            Arguments: tup - a tuple to be tested
        """
        e_msg = 'param: Origin was not a len 2 tuple of numbers'
        try:
            obj_l_is_2 = len(origin) == 2
            obj_is_tup = type(origin) == type((0,0))
            el1_is_int = type(origin[0]) == type(0)
            el2_is_int = type(origin[1]) == type(0)

            if obj_l_is_2 and obj_is_tup and el1_is_int and el2_is_int:
                return True
            else:
                raise Exception(e_msg)
        except:
            raise Exception(e_msg)



    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        """Sets origin for angle analysis

        Arguments:
            origin:must be a tuple

        Returns:
            1 if origin was set
            "Throws exception otherwise"""


        self._tuple_is_usable(origin)

        self.origin =  origin
        return 1

    def is_in_angle(self, point, angle_range):
        """Tests if point is in area cut by angle at self.origin

        Arguments:
            point: a point in standard mathematical format
            angle_range: a tuple of 2 angles that define the cut

        Returns:
            True if point is in angle cut
            False if point is not in angle cut"""

        r_point = self.originize_point(point)

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
            #print("In first if")
            if angle >= angle_range[0] and angle <= angle_range[1]:
                return True
            else:
                return False
        else:
            if angle >= angle_range[0] or angle <= angle_range[1]:
                return True
            else:
                return False

    def originize_point(self, point):
        """Gets point relative to origin

        Arguments:
            point: length 2 tuple to convert

        Returns point relative to origin """


        self._tuple_is_usable(point)

#       Make points relative to origin
        x_r_point = point[0] - self.origin[0]
        y_r_point = point[1] - self.origin[1]
        r_point = (x_r_point, y_r_point)
        return r_point

    def get_distance(self, point1, point2):
        x_dist = abs(point1[0] - point2[0])
        y_dist = abs(point1[1] - point2[1])

        x2 = math.pow(x_dist,2)
        y2 = math.pow(y_dist,2)

        dist = math.sqrt(x2 + y2)
        return dist




