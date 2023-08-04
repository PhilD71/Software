import pytest

import software.python_bindings as tbots
import sys
import math
from proto.ssl_gc_common_pb2 import Team
from proto.import_all_protos import *
from software.field_tests.field_test_fixture import *

from software.simulated_tests.simulated_test_fixture import *
from software.logger.logger import createLogger
from software.simulated_tests.robot_enters_region import RobotEventuallyEntersRegion
from proto.message_translation.tbots_protobuf import create_world_state

logger = createLogger(__name__)


def test_pivot_kick(field_test_runner):

    id = 7

    world_state = WorldState()

    world_state.blue_robots[id].CopyFrom(
        RobotState(
            global_position=Point(
                x_meters=0,y_meters=-1
            ),
        )
    )

    world_state.ball_state.CopyFrom(
        BallState(
            global_position=Point(
                x_meters=0.5, y_meters=-2
            ),
            global_velocity=Vector(
                x_component_meters=0,y_component_meters=0
            ),
        )
    )

    # world = field_test_runner.world_buffer.get(block=True, timeout=WORLD_BUFFER_TIMEOUT)
    # print("Here are the robots:")
    # print(
    #     [
    #         robot.current_state.global_position
    #         for robot in world.friendly_team.team_robots
    #     ]
    # )

    params = AssignedTacticPlayControlParams()
    params.assigned_tactics[id].pivot_kick.CopyFrom(
        PivotKickTactic(
            kick_origin=Point(x_meters=-1.13, y_meters=0.75),
            kick_direction=Angle(radians=-math.pi / 2),
            auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=5.0),
        )
    )

    field_test_runner.set_worldState(world_state)
    field_test_runner.set_tactics(params, True)
    field_test_runner.run_test(
        always_validation_sequence_set=[[]],
        eventually_validation_sequence_set=[[]],
        test_timeout_s=15,
    )
    # Send a stop tactic after the test finishes
    stop_tactic = StopTactic()
    params = AssignedTacticPlayControlParams()
    params.assigned_tactics[id].stop.CopyFrom(stop_tactic)


if __name__ == "__main__":
    # Run the test, -s disables all capturing at -vv increases verbosity
    sys.exit(pytest.main([__file__, "-svv"]))
