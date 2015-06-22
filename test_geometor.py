from geometor import Geometor


def test_geometor_included_by_angle():

    geo = Geometor()

#   Start simple is point 3,1 is included in the angle 0, 45
#   but 1,3 isnt
    assert geo.is_in_angle((3, 1), (0, 45))
    assert not geo.is_in_angle((1, 3), (0, 45))

#   If you are on the line, then its a fair ball
    assert geo.is_in_angle((3, 0), (0, 45))

#   What about angles not starting at 0
    assert geo.is_in_angle((1, 3), (45, 90))
    assert not geo.is_in_angle((3, 1), (45, 90))

#   If the angles are made in the reverse order it always starts with first
#   This angle would be greater than 180 deg
    assert not geo.is_in_angle((1, 3), (90, 45))
    assert geo.is_in_angle((3, 1), (90, 45))

#   also, negative points
    assert geo.is_in_angle((-1, 3), (90, 135))
    assert not geo.is_in_angle((-3, 1), (90, 135))
