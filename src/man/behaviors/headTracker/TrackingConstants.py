import HeadMoves

MAX_PAN_SPEED = 2.0
DEFAULT_HEAD_PITCH = 20.0

TRACKER_FRAMES_ON_TRACK_THRESH = 3
TRACKER_FRAMES_OFF_LOC_THRESH = 3
TRACKER_FRAMES_OFF_REFIND_THRESH = 10

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
