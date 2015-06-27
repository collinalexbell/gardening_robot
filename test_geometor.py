from geometor import Geometor
import math


def test_geometor_is_in_angle():

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
#   also, negative points assert geo.is_in_angle((-1, 3), (90, 135))
    assert not geo.is_in_angle((-3, 1), (90, 135))

    assert geo.is_in_angle((1,0), (-20, 20))
    assert not geo.is_in_angle((1,0), (20, -20))

def except_assert(func, params):
    try:
        func(*params)
        assert False
    except:
        assert True

def test_tuple_is_usable():
    geo = Geometor()

    #Test if origin is not a tuple
    except_assert(geo._tuple_is_usable, ('s'))
    except_assert(geo._tuple_is_usable, (5))

    #Test if origin is not a tuple of numbers
    except_assert(geo._tuple_is_usable, ((4,'s')))
    except_assert(geo._tuple_is_usable, (('s',4)))
    except_assert(geo._tuple_is_usable, ((True,False)))

    #Test if origin is not len 2
    except_assert(geo._tuple_is_usable, ((4,5,6)))


def test_set_orgin():
    geo = Geometor()
#   Test if it checks input for correctness
    except_assert(geo.set_origin, ('s'))

    #Test if origin gets set if params are right
    geo.set_origin((2,3))
    assert geo.get_origin() == (2,3)

def test_geometor_get_origin_based_points():
    geo = Geometor()

    #Pos, pos
    geo.set_origin((5,5))

    #Test that func checks input
    except_assert(geo.originize_point, (6))

    assert geo.originize_point((6,6)) == (1,1)
    assert geo.originize_point((-5,6)) == (-10,1)
    assert geo.originize_point((-5,-5)) == (-10,-10)

def test_get_distance():
    geo = Geometor()

    #Lests start off easy
    assert geo.get_distance((0,0),(1,0)) == 1

    assert geo.get_distance((0,0),(1,1)) == math.sqrt(2)

    assert geo.get_distance((1,1),(4,5)) == 5

    assert geo.get_distance((4,5),(1,1)) == 5



