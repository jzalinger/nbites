import HeadMoves
import noggin_constants
import VisionField_proto

MAX_PAN_SPEED = 2.0
DEFAULT_HEAD_PITCH = 20.0

DEFAULT_PAN_RATE = 80.0 # degrees per second

TRACKER_FRAMES_ON_TRACK_THRESH = 3
TRACKER_FRAMES_OFF_LOC_THRESH = 3
TRACKER_FRAMES_OFF_REFIND_THRESH = 10

CORNER_CHECK_TIME = 10

KICK_DICT = {"L_Side"           : HeadMoves.FIXED_PITCH_LOOK_RIGHT,
             "R_Side"           : HeadMoves.FIXED_PITCH_LOOK_LEFT,
             "L_Short_Side"     : HeadMoves.FIXED_PITCH_LOOK_RIGHT,
             "R_Short_Side"     : HeadMoves.FIXED_PITCH_LOOK_LEFT,
             "L_Straight"       : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Straight"       : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "L_Short_Straight" : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Short_Straight" : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "L_Quick_Straight" : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Quick_Straight" : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "L_Big_Straight"   : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Big_Straight"   : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "L_Long_Back"      : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Long_Back"      : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "L_Short_Back"     : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT,
             "R_Short_Back"     : HeadMoves.FIXED_PITCH_LOOK_STRAIGHT}
# TODO: Test and improve these pans.

ALL_LANDMARK_CORNERS = (noggin_constants.LANDMARK_MY_CORNER_LEFT_L,
                        noggin_constants.LANDMARK_MY_CORNER_RIGHT_L,
                        noggin_constants.LANDMARK_MY_GOAL_LEFT_L,
                        noggin_constants.LANDMARK_MY_GOAL_RIGHT_L,
                        noggin_constants.LANDMARK_MY_GOAL_LEFT_T,
                        noggin_constants.LANDMARK_MY_GOAL_RIGHT_T,
                        noggin_constants.LANDMARK_CENTER_LEFT_T,
                        noggin_constants.LANDMARK_CENTER_RIGHT_T,
                        noggin_constants.LANDMARK_OPP_CORNER_LEFT_L,
                        noggin_constants.LANDMARK_OPP_CORNER_RIGHT_L,
                        noggin_constants.LANDMARK_OPP_GOAL_LEFT_L,
                        noggin_constants.LANDMARK_OPP_GOAL_RIGHT_L,
                        noggin_constants.LANDMARK_OPP_GOAL_LEFT_T,
                        noggin_constants.LANDMARK_OPP_GOAL_RIGHT_T)

shape = VisionField_proto.messages.VisualCorner
SHAPE_RANK = {shape.UNKNOWN:              0, #0
              shape.INNER_L:              1,
              shape.OUTER_L:              1,
              shape.T:                    1,
              shape.CIRCLE:               1,
              shape.GOAL_L:               3 ,#5
              shape.CORNER_L:             2,
              shape.LEFT_GOAL_L:          3,
              shape.RIGHT_GOAL_L:         3,
              shape.RIGHT_GOAL_CORNER:    2,
              shape.LEFT_GOAL_CORNER:     2, #10
              shape.GOAL_T:               3,
              shape.SIDE_T:               3,
              shape.LEFT_GOAL_T:          3,
              shape.RIGHT_GOAL_T:         3,
              shape.YELLOW_GOAL_BOTTOM:   2, #15
              shape.YELLOW_GOAL_TOP:      2,
              shape.BLUE_GOAL_BOTTOM:     2,
              shape.BLUE_GOAL_TOP:        2,
              shape.LEFT_GOAL_YELLOW_L:   4,
              shape.LEFT_GOAL_BLUE_L:     4, #20
              shape.RIGHT_GOAL_YELLOW_L:  4,
              shape.RIGHT_GOAL_BLUE_L:    4,
              shape.RIGHT_GOAL_YELLOW_T:  4,
              shape.LEFT_GOAL_YELLOW_T:   4,
              shape.RIGHT_GOAL_BLUE_T:    4, #25
              shape.LEFT_GOAL_BLUE_T:     4,
              shape.CENTER_T_TOP:         3,
              shape.CENTER_T_BOTTOM:      3,
              shape.CENTER_CIRCLE_TOP:    2,
              shape.CENTER_CIRCLE_BOTTOM: 2} #30
