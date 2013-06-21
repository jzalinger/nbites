from . import TrackingConstants
import noggin_constants as Constants
from ..util import MyMath as MyMath
from .. import StiffnessModes
from math import fabs, degrees
import HeadMoves
from objects import Location, RobotLocation, RelLocation, RelRobotLocation

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

        destination = (headMoveYaw, headMovePitch)
        self.executeHeadMove(self.makeHeadMoveWithSpeed(destination))

    def makeHeadMoveWithSpeed(self, destination, speed = TrackingConstants.DEFAULT_PAN_RATE):
        """
        Given the destination yaw and pitch and a speed (in degrees per second),
        calculates the difference from current joint angles and returns
        a tuple for executeHeadMove with the correct time.
        """
        headMoveYaw = destination[0]
        headMovePitch = destination[1]

        # We should probably move this math to C++ if possible.
        curYaw = degrees(self.tracker.brain.interface.joints.head_yaw)
        curPitch = degrees(self.tracker.brain.interface.joints.head_pitch)

        yawDiff = MyMath.fabs(curYaw - headMoveYaw)
        pitchDiff = MyMath.fabs(curPitch - headMovePitch)

        totalTime = max(yawDiff, pitchDiff) / speed

        headMove = ( (destination, totalTime, 1, StiffnessModes.LOW_HEAD_STIFFNESSES), )
        return headMove

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

        # Safety check on the target
        if not self.validateTarget(self.tracker.target):
            print "Trying to track an invalid target."
            return

        target = self.tracker.target
        changeX, changeY = 0.0, 0.0

        # If we cannot see the target, abort.
        if not target.on:
            # If we haven't seen the target, look towards loc model.
            if target.frames_off > TrackingConstants.TRACKER_FRAMES_OFF_LOC_THRESH:
                self.lookToPoint(target)
# TODO: safeguard above call from errors due to calling every frame
# TODO: use loc information and helper.lookAtTarget instead??
            return

        # Assert: target is visible.

        # Find the target's angular distance from yaw center.
        changeX = target.angle_x_deg
        # ignore changeY: pitch is fixed

        curYaw   = degrees(self.tracker.brain.interface.joints.head_yaw)
        maxChange = 13.0

        # Warning- no gain is applied currently!
        safeChangeX = MyMath.clip(changeX, -maxChange, maxChange)
        # ignore safeChangeY: pitch is fixed

        newYaw = curYaw + safeChangeX
        # ignore newPitch: pitch is fixed

        maxSpeed = TrackingConstants.MAX_PAN_SPEED

        # Set motion message fields
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.POS_HEAD_COMMAND

        command.pos_command.head_yaw = newYaw
        command.pos_command.head_pitch = TrackingConstants.DEFAULT_HEAD_PITCH
        command.pos_command.max_speed_yaw = maxSpeed
        command.pos_command.max_speed_pitch = maxSpeed

        command.timestamp = int(self.tracker.brain.time * 1000)

    # Generalize this method, states, API,  with method trackObject
    def trackStationaryObject(self):
        # Note: safe to call every frame.

        # Safety check on the target
        if not self.validateTarget(self.tracker.target):
            print "Trying to track an invalid target."
            return

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
        maxSpeed = TrackingConstants.MAX_PAN_SPEED

        # Warning- no gain is applied currently!
        safeChangeX = MyMath.clip(changeX, -maxChange, maxChange)
        newYaw = curYaw + safeChangeX

        # Set motion message fields
        command = self.tracker.brain.interface.headMotionCommand
        command.type = command.CommandType.POS_HEAD_COMMAND

        command.pos_command.head_yaw = newYaw
        command.pos_command.head_pitch = TrackingConstants.DEFAULT_HEAD_PITCH
        command.pos_command.max_speed_yaw = maxSpeed
        command.pos_command.max_speed_pitch = maxSpeed

        command.timestamp = int(self.tracker.brain.time * 1000)

    # URGENT TODO: make robust when target doesn't have a rel_y attribute
    def lookToPoint(self, target):
        """
        If the relative y is positive, look left. Otherwise, look right.
        """
        if target.rel_y > 0:
            self.executeHeadMove(HeadMoves.FIXED_PITCH_LOOK_LEFT)
        else:
            self.executeHeadMove(HeadMoves.FIXED_PITCH_LOOK_RIGHT)

    def lookToAngle(self, yaw, speed = TrackingConstants.DEFAULT_PAN_RATE):
        """
        Returns a headmove that will make the robot
        look to the given yaw at an appropriate (fixed) pitch.

        Note: Use as parameter for tracker.executeHeadMove()
        """
        # Clip yaw for safety
        clippedYaw = MyMath.clip(yaw, -119.5, 119.5) # hardware joint limit

        if fabs(clippedYaw) > 55:
            pitch = 11.0
        else:
            pitch = 17.0

        return self.makeHeadMoveWithSpeed((clippedYaw,pitch), speed)

    # @param cornerList: tuples consisting of x, y, ID
    def cornersToLocations(self, cornerList):
        locationList = []

        # Build a Location object out of every corner tuple
        for corner in cornerList:
            locationList.append(Location(corner[0],corner[1]))

        return locationList

    # @param corner: must be a Location or an x,y,ID tuple
    def lookToCorner(self, corner):
        myLoc = self.tracker.brain.loc

        if not isinstance(corner, Location):
            yaw = myLoc.getRelativeBearing(Location(corner[0], corner[1]))
        else:
            yaw = myLoc.getRelativeBearing(corner)

        self.executeHeadMove(self.lookToAngle(yaw))

        #print "DEBUG:"
        #print "corner's location: " + str(corner.x) + ", " + str(corner.y)
        #print "yaw: " + str(yaw)

    def findVisualCornerForLoc(self):
        """
        Given where we are currently looking, determine the visual
        corner with the most potential to be useful for loc and
        return it (for tracking method).
        """
        visionField = self.tracker.brain.interface.visionField
        visualCorners = []
        visualCornerRanking = []

        for corner in range(visionField.visual_corner_size()):
            visualCorners.append(visionField.visual_corner(corner))
            visualCornerRanking.append(TrackingConstants.SHAPE_RANK[visualCorners[-1].corner_type])

        # safety check for empty list
        if len(visualCorners) == 0:
            return None

        return visualCorners[visualCornerRanking.index(max(visualCornerRanking))].visual_detection

    def lookToLocation(self, location, speed):
        """
        Given a Location or RelLocation, look to the correct yaw.
        Pass the given speed through to lookToAngle.
        """
        if isinstance(location, Location):
            bearing = self.bearingToLocation(location)
        elif isinstance(location, RelLocation):
            bearing = self.bearingToRelLocation(location)
        else:
            print "Passed an invalid location to HeadTrackingHelper."
            return

        # Check if the given speed is usable
        if speed == -1:
            self.executeHeadMove(self.lookToAngle(bearing))
        else:
            self.executeHeadMove(self.lookToAngle(bearing, speed))

    def bearingToLocation(self, location):
        """
        Given a global Location, determine the bearing from our current loc.
        """
        myLoc = self.tracker.brain.loc
        bearing = myLoc.getRelativeBearing(location)
        return bearing

    def bearingToRelLocation(self, relLocation):
        """
        Given a relative location, determine the bearing.
        """
        return = relLocation.bearing()

    def convertLandmarkTupleToLocation(self, landmark):
        return Location(landmark[0], landmark[1])

    # Basic output for troubleshooting
    def printHeadAngles(self):
        print ("Cur yaw: "   + str(self.tracker.brain.interface.joints.head_yaw) +
               "Cur pitch: " + str(self.tracker.brain.interface.joints.head_pitch))

    # Regardless of state, is the head moving?
    def isActive(self):
        return self.tracker.brain.motion.head_is_active

    def validateTarget(self, newTarget):
        """
        Checks if the given newTarget has the needed attributes
        to be used as a target for trackObject.
        """
        return (hasattr(newTarget, on) and
                hasattr(newTarget, frames_off) and
                hasattr(newTarget, frames_on) and
                hasattr(newTarget, angle_x_deg))

    def validateLocation(self, location):
        """
        Check if the parameter is a Location, RelLocation, or one of their children.
        """
        return (isinstance(location, Location) or
                isinstance(location, RelLoction))

    def greenField(self):
        """
        Returns true if there are no visual objects in sight.
        """
        visField = self.tracker.brain.interface.VisionField

        if visField.goal_post_l.visual_detection.on:
            return False
        if visField.goal_post_r.visual_detection.on:
            return False
        for corner in range(visField.visual_corner_size):
            if visField.visual_corner(corner).visual_detection.on:
                return False
        for line in range(visField.visual_line_size):
            if visField.visual_line(line).visual_detection.on:
                return False
        if visField.visual_cross.visual_detection.on:
            return False

        return True
