from . import TrackingConstants
from .. import noggin_constants as Constants
from ..util import MyMath as MyMath
from .. import StiffnessModes
from math import fabs, degrees
import HeadMoves
from objects import Location, RobotLocation, RelRobotLocation

class HeadTrackingHelper(object):
    def __init__(self, tracker):
        self.tracker = tracker

    def executeHeadMove(self, headMove):
        """performs a sweetmove"""
        # Note: Do not call every frame!
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.SCRIPTED_HEAD_COMMAND

        for position in headMove:
            if len(position) == 4:
                move = command.scripted_command.add_command()

                # Set most recent command
                move.time = position[1]
                if position[2] == 1:
                    move.interpolation = move.InterpolationType.LINEAR
                else:
                    move.interpolation = move.InterpolationType.SMOOTH

                # Only set the head angles
                move.angles.head_yaw   = position[0][0]
                move.angles.head_pitch = position[0][1]

                # Set all stiffnesses, since this command specifies them all
                move.stiffness.head_yaw =         position[3][0]
                move.stiffness.head_pitch =       position[3][1]

                move.stiffness.l_shoulder_pitch = position[3][2]
                move.stiffness.l_shoulder_roll =  position[3][3]
                move.stiffness.l_elbow_yaw =      position[3][4]
                move.stiffness.l_elbow_roll =     position[3][5]

                move.stiffness.r_shoulder_pitch = position[3][18]
                move.stiffness.r_shoulder_roll =  position[3][19]
                move.stiffness.r_elbow_yaw =      position[3][20]
                move.stiffness.r_elbow_roll =     position[3][21]

                move.stiffness.l_hip_yaw_pitch =  position[3][6]
                move.stiffness.l_hip_roll =       position[3][7]
                move.stiffness.l_hip_pitch =      position[3][8]
                move.stiffness.l_knee_pitch =     position[3][9]
                move.stiffness.l_ankle_pitch =    position[3][10]
                move.stiffness.l_ankle_roll =     position[3][11]

                move.stiffness.r_hip_yaw_pitch =  position[3][12]
                move.stiffness.r_hip_roll =       position[3][13]
                move.stiffness.r_hip_pitch =      position[3][14]
                move.stiffness.r_knee_pitch =     position[3][15]
                move.stiffness.r_ankle_pitch =    position[3][16]
                move.stiffness.r_ankle_roll =     position[3][17]

            else:
                self.tracker.printf("What kind of sweet ass-Move is this?")

        command.timestamp = int(self.tracker.brain.time * 1000)
        # Returns the last HJC in the HeadMove for keeping track of
        # when a move is done
        return move

    def startingPan(self, headMove):
        """Calculates the first part of a fixed pitch pan to get there quickly."""
        if len(headMove) < 2:
            # Not a normal pan: there's only 1 headMove.
            # Don't do a starting move.
            return

        headMoveYaw = headMove[1][0][0]
        headMovePitch = headMove[1][0][1]

        #TODO do this math in C++
        curYaw = degrees(self.tracker.brain.interface.joints.head_yaw)
        degreesPerSecond = 80 #fast, but hopefully won't destabilize the walk much
        yawDiff = MyMath.fabs(curYaw - headMoveYaw)
        totalTime = yawDiff/degreesPerSecond

        newHeadMove = ( ((headMoveYaw,headMovePitch), totalTime, 1,
                         StiffnessModes.LOW_HEAD_STIFFNESSES), )

        self.executeHeadMove(newHeadMove)

    # Should be generalized.
    def convertKickPan(self, headMove, invert):
        """
        Converts the first step of the kick pan to have the same speed
        as the second step, regardless of starting yaw.
        ASSERT: 2 step headMove.
        """
        headMoveYaw = headMove[0][0][0]
        headMovePitch = headMove[0][0][1]

        curYaw = degrees(self.tracker.brain.interface.joints.head_yaw)
        degreesPerSecond = (headMoveYaw*2)/headMove[0][1] # double the yaw b/c pans are symmetric
        yawDiff = MyMath.fabs(curYaw-headMoveYaw)
        totalTime = yawDiff/degreesPerSecond

        if invert is True:
            newHeadMove = ( ((-1*headMoveYaw,headMovePitch),
                             totalTime, headMove[0][2], headMove[0][3]),
                            ((-1*headMove[1][0][0],headMove[1][0][1]),
                             headMove[1][1], headMove[1][2], headMove[1][3]) )
        else:
            newHeadMove = ( ((headMoveYaw,headMovePitch),
                             totalTime, 1, headMove[0][3]),
                            headMove[1] )

        return newHeadMove

    def trackObject(self):
        """
        Method to actually perform the tracking.
        Should only be called explicitly from state
        methods in TrackingStates.py
        """
        # Note: safe to call every frame.

        target = self.tracker.target
        changeX, changeY = 0.0, 0.0

        # If we cannot see the target, abort.
        if not (target # target is null
                or (target.rel_x == 0.0 and target.rel_y == 0.0) # target is under us (info error)
                or (target.vis.frames_off > 0 and target.vis.frames_off < 3)): # off frame, but under thresh
# TODO: use a constant above
            return

        # If we haven't seen the target, look towards loc model.
        if target.vis.frames_off > 3:
# TODO: use a constant above
            self.lookToPoint(target)
# TODO: safeguard above call from errors due to calling every frame
# TODO: use loc information and helper.lookAtTarget instead??
            return

        # Assert: target is visible.

        # Find the target's angular distance from yaw center.
        changeX = target.vis.angle_x_deg
        # ignore changeY: pitch is fixed

        curYaw   = degrees(self.tracker.brain.interface.joints.head_yaw)
        maxChange = 13.0

        # Warning- no gain is applied currently!
        safeChangeX = MyMath.clip(changeX, -maxChange, maxChange)
        # ignore safeChangeY: pitch is fixed

        newYaw = curYaw + safeChangeX
        # ignore newPitch: pitch is fixed

        maxSpeed = 2.0 # TODO: use a constant

        # Set motion message fields
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.POS_HEAD_COMMAND

        command.pos_command.head_yaw = newYaw
        command.pos_command.head_pitch = 20.0 # TODO: MAKE A CONSTANT FOR THIS
        command.pos_command.max_speed_yaw = maxSpeed
        command.pos_command.max_speed_pitch = maxSpeed

        command.timestamp = int(self.tracker.brain.time * 1000)

    def trackStationaryObject(self):
        # Note: safe to call every frame.
        target = self.tracker.target
        changeX, changeY = 0.0, 0.0

        # If we cannot see the target, abort.
        if (not target # target is null
            or (target.frames_off > 0)):
            return

        # Find the target's angular distance from yaw center.
        changeX = target.angle_x_deg
        curYaw  = degrees(self.tracker.brain.interface.joints.head_yaw)

        #WOW this is ugly
        maxChange = 13.0
        maxSpeed = 2.0

        # Warning- no gain is applied currently!
        safeChangeX = MyMath.clip(changeX, -maxChange, maxChange)
        newYaw = curYaw + safeChangeX

        # Set motion message fields
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.POS_HEAD_COMMAND

        command.pos_command.head_yaw = newYaw
        command.pos_command.head_pitch = 20.0 # TODO: MAKE A CONSTANT FOR THIS
        command.pos_command.max_speed_yaw = maxSpeed
        command.pos_command.max_speed_pitch = maxSpeed

        command.timestamp = int(self.tracker.brain.time * 1000)

    def lookAtTarget(self, rel_x, rel_y):
        '''
        Given relative coordinates, sends a command that will calculate
        and set the necessary angles to look at those coordinates.
        '''
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.COORD_HEAD_COMMAND

        command.coord_command.rel_x = rel_x
        command.coord_command.rel_y = rel_y
        command.timestamp = int(self.tracker.brain.time * 1000)

    def lookToPoint(self, target):
        """
        If the relative y is positive, look left. Otherwise, look right.
        """
        if hasattr(target, "height"):
            height = target.height
        else:
            height = 0

        if target.rel_y > 0:
            self.executeHeadMove(HeadMoves.FIXED_PITCH_LOOK_LEFT)
        else:
            self.executeHeadMove(HeadMoves.FIXED_PITCH_LOOK_RIGHT)

    def lookToAngle(self, yaw):
        """
        Returns a headmove that will make the robot
        look to the given yaw at an appropriate (fixed) pitch.

        Note: Use as parameter for tracker.performHeadMove()
        """
        if yaw > 55 or yaw < -55:
            pitch = 11.0
        else:
            pitch = 17.0

        return (((yaw, pitch),
                 2.0, 1, StiffnessModes.LOW_HEAD_STIFFNESSES),)
        # TODO: use constants above

    # @method: minimizes delta yaw. not safe to call every frame.
    def lookToNearestCornerWithinDist(self, distance):
        self.cornerDistanceThreshold = distance
        allCorners = map(self.cornerToRelRobotLocation, Constants.ALL_LANDMARK_CORNERS)
        closeCorners = filter(self.closerThanDist, allCorners)
        cornerYaws = map(self.yawDiffToLookAtCorner, closeCorners)
        sortedYaws = sorted(cornerYaws, key=fabs)

        self.executeHeadMove(self.lookToAngle(sortedYaws[0]))

    # @method: helper for filtering in self.getAllCornersWithinDist
    # @param corner: must be a location
    def closerThanDist(self, corner):
        return self.brain.loc.distTo(corner) < self.cornerDistanceThreshold

    # @param corner: tuple consisting of x, y, ID
    def cornerToRelRobotLocation(self, corner):
        myLoc = self.brain.loc
        target = RobotLocation(corner[0],corner[1],0)
        return myLoc.getRelRobotLocationOf(target)

    # @param corner: must be a relRobotLocation
    def yawDiffToLookAtCorner(self, corner):
        bearing = self.brain.loc.getRelativeBearing(corner)
        curYaw  = degrees(self.tracker.brain.interface.joints.head_yaw)

        yawDiff = bearing - curYaw

        if fabs(bearing) > 119.5: # hardware joint limit
            return -1
        else:
            return yawDiff

    # Basic output for troubleshooting
    def printHeadAngles(self):
        print ("Cur yaw: "   + str(self.tracker.brain.interface.joints.head_yaw) +
               "Cur pitch: " + str(self.tracker.brain.interface.joints.head_pitch))
