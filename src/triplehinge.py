# coding=utf-8

"""
Build a  planar 3-R robot.

This module builds a planar 3-r robot, identical to the one buildt in the
matlab- arboris t06_ConstructionRobot.m tutorial.

When ran as a script, the module shows the robot in motion.
"""


import arboris as arb
import numpy as np

def transport_mass_matrix(mass,H):
    """Transport (express) the mass matrix into another frame."""
    Ad = arb.Hg.adjoint(arb.Hg.inv(H))
    return np.dot(
        Ad.transpose(),
        np.dot(mass, Ad))
        
def mass_parallelepiped(m,lengths):
    """The mass matrix of an homogeneous parallelepiped."""
    (a, b, c) = lengths
    return np.diag((
        m/12*(b**2+c**2 ), 
        m/12*(a**2+c**2), 
        m/12*(a**2+b**2),
        m, m, m))

def triplehinge():
    """Build a  planar 3-R robot."""

    arm_length=0.5
    arm_mass=1
    forearm_length=0.4
    forearm_mass=0.8
    hand_length=0.2
    hand_mass=0.2

    # Create a world
    w = arb.World()
    
    # the world already has a ground body
    ground = w.bodies[0]

    # create other bodies
    arm = arb.Body(
        name='Arm',
        mass=transport_mass_matrix(
            mass_parallelepiped(
                arm_mass, 
                (arm_length/10,arm_length,arm_length/10)),
            arb.Hg.transl((0,arm_length/2,0))))
    forearm = arb.Body(
        name='ForeArm',
        mass=transport_mass_matrix(
            mass_parallelepiped(
                forearm_mass, 
                (forearm_length/10,forearm_length,forearm_length/10)),
                arb.Hg.transl((0,forearm_length/2,0))))
    hand = arb.Body(
        name='Hand',
        mass=transport_mass_matrix(
            mass_parallelepiped(
                hand_mass, 
                (hand_length/10,hand_length,hand_length/10)),
                arb.Hg.transl((0,hand_length/2,0))))


    # create a joint between the ground and the arm
    shoulder = arb.HingeJoint(
        name = 'Shoulder',
        leftframe = ground.frames[0],
        rightframe = arm.frames[0],
        gpos = .5)
    # add the new joint to the world (this will also add arm to w.bodies)
    w.addjoint(shoulder)
    
    # add a frame to the arm, where the forearm will be anchored
    f = arm.newframe(
        arb.Hg.transl((0,arm_length,0)),
        'ElbowLeftFrame')
    # create a joint between the arm and the forearm
    elbow = arb.HingeJoint(
        name = 'Elbow',
        leftframe = f,
        rightframe = forearm.frames[0],
        gpos = -.5)
    w.addjoint(elbow)


    # add a frame to the forearm, where the hand will be anchored
    f = forearm.newframe(
        arb.Hg.transl((0,forearm_length,0)),
        'WristLeftFrame')
    # create a joint between the forearm and the hand
    wrist = arb.HingeJoint(
        name = 'Wrist',
        leftframe = f,
        rightframe = hand.frames[0],
        gpos = -.5)
    w.addjoint(wrist)
    return w

if __name__ == "__main__":

    w = triplehinge()
    
    #compute dynamic model
    w.dynamic()

    import visu
    import visual
    visu.scale=0.3
    vw = visu.World(world=w,scale=0.1)
    for t in range(100):
        visual.rate(10)
        print t
        w.joints[1].gpos=t/20.
        w.geometric()
        vw.update()

