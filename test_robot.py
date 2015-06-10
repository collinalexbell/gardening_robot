from robot import Robot

def test_convert_turn_output_to_cardinal_direction():
    robot = Robot( 5, 5, 'world')
    robot.turn('right')


    assert robot.convert_turn_output_to_cardinal_direction('right') == 'down'
    assert robot.convert_turn_output_to_cardinal_direction('left') == 'up'

    robot.turn('left')
    assert robot.convert_turn_output_to_cardinal_direction('right') == 'up'
    assert robot.convert_turn_output_to_cardinal_direction('left') == 'down'

    robot.turn('down')
    assert robot.convert_turn_output_to_cardinal_direction('right') == 'left'
    assert robot.convert_turn_output_to_cardinal_direction('left') == 'right'

    robot.turn('up')
    assert robot.convert_turn_output_to_cardinal_direction('right') == 'right'
    assert robot.convert_turn_output_to_cardinal_direction('left') == 'left'

