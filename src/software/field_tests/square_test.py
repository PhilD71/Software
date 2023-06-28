import pytest

import math
import software.python_bindings as tbots
import sys
from proto.ssl_gc_common_pb2 import Team
from proto.import_all_protos import *
from software.field_tests.field_test_fixture import *

from software.simulated_tests.simulated_test_fixture import *
from software.logger.logger import createLogger
from software.simulated_tests.robot_enters_region import RobotEventuallyEntersRegion
from proto.message_translation.tbots_protobuf import create_world_state

logger = createLogger(__name__)

def test_one_robots_square(field_test_runner):
    id1 = 5
    id2 = 6

    world = field_test_runner.world_buffer.get(block=True, timeout=WORLD_BUFFER_TIMEOUT)
    print("Here are the robots:")
    print([robot.current_state.global_position for robot in world.friendly_team.team_robots])

    tactic_0 = MoveTactic(
        destination=Point(x_meters=-2.3, y_meters=0.5),
        final_speed=0.0,
        dribbler_mode=DribblerMode.OFF,
        final_orientation=Angle(radians=-math.pi/2),
        ball_collision_type=BallCollisionType.AVOID,
        auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=0.0),
        max_allowed_speed_mode=MaxAllowedSpeedMode.PHYSICAL_LIMIT,
        target_spin_rev_per_s=0.0
    )
    tactic_1 = MoveTactic(
        destination=Point(x_meters=-2.3, y_meters=-0.75),
        final_speed=0.0,
        dribbler_mode=DribblerMode.OFF,
        final_orientation=Angle(radians=-math.pi/2),
        ball_collision_type=BallCollisionType.AVOID,
        auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=0.0),
        max_allowed_speed_mode=MaxAllowedSpeedMode.PHYSICAL_LIMIT,
        target_spin_rev_per_s=0.0
    )
    tactic_2 = MoveTactic(
        destination=Point(x_meters=-3.6, y_meters=-0.75),
        final_speed=0.0,
        dribbler_mode=DribblerMode.OFF,
        final_orientation=Angle(radians=-math.pi/2),
        ball_collision_type=BallCollisionType.AVOID,
        auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=0.0),
        max_allowed_speed_mode=MaxAllowedSpeedMode.PHYSICAL_LIMIT,
        target_spin_rev_per_s=0.0
    )
    tactic_3 = MoveTactic(
        destination=Point(x_meters=-3.6, y_meters=0.5),
        final_speed=0.0,
        dribbler_mode=DribblerMode.OFF,
        final_orientation=Angle(radians=-math.pi/2),
        ball_collision_type=BallCollisionType.AVOID,
        auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=0.0),
        max_allowed_speed_mode=MaxAllowedSpeedMode.PHYSICAL_LIMIT,
        target_spin_rev_per_s=0.0
    )
    # tactics = [tactic_0, tactic_1, tactic_2, tactic_3]
    tactics = [(tactic_0, tactic_2), (tactic_1, tactic_3), (tactic_2, tactic_0), (tactic_3, tactic_1)]

    for tactic in tactics:

        # print(f"Robot {id1} Going to {tactic[0].destination} and Robot {id2} going to {tactic[1].destination}")
        params = AssignedTacticPlayControlParams()
        params.assigned_tactics[id1].move.CopyFrom(tactic[0])
        params.assigned_tactics[id2].move.CopyFrom(tactic[1])

        field_test_runner.set_tactics(params, True)
        field_test_runner.run_test(
            always_validation_sequence_set=[[]],
            eventually_validation_sequence_set=[[]],
            test_timeout_s=4,
        )


    # Send a stop tactic after the test finishes
    stop_tactic = StopTactic()
    params = AssignedTacticPlayControlParams()
    params.assigned_tactics[id1].stop.CopyFrom(stop_tactic)

if __name__ == "__main__":
    # Run the test, -s disables all capturing at -vv increases verbosity
    sys.exit(pytest.main([__file__, "-svv"]))
