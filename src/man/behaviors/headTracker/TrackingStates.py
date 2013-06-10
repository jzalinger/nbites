from . import TrackingConstants as constants
import HeadMoves
from objects import RelLocation
import noggin_constants as NogginConstants
from ..playbook import PBConstants
from ..players import GoalieConstants
import BallModel_proto as BallModel

DEBUG = False

def tracking(tracker):
    """
    While the target is visible, track it via vision values.
    If the target is lost, switches to fullPan.
    """
    # If the target is not in vision, trackObject will track via loc.
    tracker.helper.trackObject()

    if not tracker.target.on and tracker.counter > 15:
        if DEBUG : tracker.printf("Missing object this frame",'cyan')
        if (tracker.target.frames_off >
            constants.TRACKER_FRAMES_OFF_REFIND_THRESH):
            return tracker.goLater('fullPan')

    return tracker.stay()

def trackingFieldObject(tracker):
    tracker.helper.trackStationaryObject()
    if not tracker.target.on and tracker.counter > 15:
        if (tracker.target.frames_off >
            constants.TRACKER_FRAMES_OFF_REFIND_THRESH):
            return tracker.goLater('fullPan')

    return tracker.stay()

# Not currently used, but would be good functionality to have in the future.
def lookAtTarget(tracker):
    """Look to the relative coords of the stored target, using localization."""
    #tracker.helper.lookAtTarget(tracker.target)
    return tracker.stay()

# Enters the corner state cycle
def checkCorner(tracker):
    """
    Look to nearest corner for localization, then return to tracking the ball.
    """
    if not tracker.helper.isActive():
        return tracker.goLater('waitThenTrack')

    if tracker.counter == 1:
        tracker.helper.lookToNearestCornerWithinDist(200)

    return tracker.stay()

# Part of the corner state cycle
def waitThenTrack(tracker):
    if tracker.counter > constants.CORNER_CHECK_TIME:
        return tracker.goLater('returnPanAndTrack')

    return tracker.stay()

# Part of the corner state cycle
def returnPanAndTrack(tracker):
    if tracker.counter == 1:
        tracker.target = tracker.brain.ball.vis
        tracker.helper.executeHeadMove(tracker.helper.lookToAngle(tracker.storedYaw))
        return tracker.stay()
    elif not tracker.helper.isActive() or tracker.target.frames_on > constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        return tracker.goLater(tracker.postCornerState)

def lookStraightThenTrack(tracker):
    """
    Perform a 'look straight' head move.
    Once ball is seen enough, track it.

    Usually, this is used to lock the robot's
    head forward while it spins and searches
    for the ball.
    """
    if tracker.firstFrame():
        # Send the motion request message to stop
        request = tracker.brain.interface.motionRequest
        request.stop_head = True
        request.timestamp = int(tracker.brain.time * 1000)
        # Perform the head move to look straight ahead
        tracker.helper.executeHeadMove(HeadMoves.FIXED_PITCH_LOOK_STRAIGHT)
        # Make sure target is set right
        tracker.target = tracker.brain.ball.vis

    if tracker.target.frames_on > constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        tracker.trackBall()

    return tracker.stay()

def fullPan(tracker):
    """
    Repeatedly executes the headMove FIXED_PITCH_PAN.
    Once the ball is located, switches to tracking.
    """
    if tracker.firstFrame():
        # Send the motion request message to stop
        request = tracker.brain.interface.motionRequest
        request.stop_head = True
        request.timestamp = int(tracker.brain.time * 1000)
        # Smartly start the pan
        tracker.helper.startingPan(HeadMoves.FIXED_PITCH_PAN)

    if not tracker.helper.isActive():
        # Repeat the pan
        tracker.helper.executeHeadMove(HeadMoves.FIXED_PITCH_PAN)

    if not isinstance(tracker.target, BallModel.messages.FilteredBall):
        if tracker.target.on:
            return tracker.goLater('trackingFieldObject')

    if (isinstance(tracker.target, BallModel.messages.FilteredBall) and
        target.frames_on > constants.TRACKER_FRAMES_ON_TRACK_THRESH):
        return tracker.goLater('tracking')

    return tracker.stay()

def afterKickScan(tracker):
    """
    Looks in the direction the ball was kicked in.
    If the ball is seen, go to state 'ballTracking'.
    """
    if tracker.firstFrame():
        tracker.performHeadMove(constants.KICK_DICT[tracker.kickName])

    return tracker.stay()
