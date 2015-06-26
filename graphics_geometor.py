from geometor import Geometor

class Graphics_Geometor(Geometor):
    def originize_point(self, point):
        """Converts graphics representation to standard
        and then calculates point relative to origin

        Arguments:
            point: length 2 tuple to convert

        Returns point relative to origin """


        self._tuple_is_usable(point)

#       Make points relative to origin
        x_r_point = point[0] - self.origin[0]

        #In graphics, the object is REVERSED
        y_r_point =  self.origin[1] - point[1]
        r_point = (x_r_point, y_r_point)
        return r_point

