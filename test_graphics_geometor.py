from graphics_geometor import Graphics_Geometor
from test_geometor import except_assert

def test_originize_point():
    geo = Graphics_Geometor()

    #Pos, pos
    geo.set_origin((5,5))

    #Test that func checks input
    except_assert(geo.originize_point, (6))

    assert geo.originize_point((6,6)) == (1,-1)
    assert geo.originize_point((-5,6)) == (-10,-1)
    assert geo.originize_point((-5,-5)) == (-10,10)


def test_is_in_angle():

    geo = Graphics_Geometor()
    geo.set_origin((5,5))

#   Start simple is point 3,1 is included in the angle 0, 45
#   but 1,3 isnt
    assert geo.is_in_angle((8, 4), (0, 45))
    assert not geo.is_in_angle((7, 2), (0, 45))

#   If you are on the line, then its a fair ball
    assert geo.is_in_angle((8, 5), (0, 45))

#   What about angles not starting at 0
    assert geo.is_in_angle((6, 2), (45, 90))
    assert not geo.is_in_angle((8, 4), (45, 90))

#   If the angles are made in the reverse order it always starts with first
#   This angle would be greater than 180 deg
    assert not geo.is_in_angle((6, 2), (90, 45))
    assert geo.is_in_angle((8, 4), (90, 45))
