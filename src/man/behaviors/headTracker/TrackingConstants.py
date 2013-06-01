import HeadMoves
import noggin_constants

MAX_PAN_SPEED = 2.0
DEFAULT_HEAD_PITCH = 20.0

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

# TODO: Test and improve these pans.
