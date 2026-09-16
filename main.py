import pygame
import numpy as np
import random

# Configuration

WIDTH = 800
HEIGHT = 800

BOWL_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
BOWL_RADIUS = 300

# Start with 1 ball, then 2. Many at once is the bonus.
NUM_PARTICLES = 2
PARTICLE_RADIUS = 12
PARTICLE_SPEED = 150.0

# Pixels per second squared, not m/s^2. Note that +y points DOWN on screen.
GRAVITY = 900.0

# How much speed survives a bounce. 1.0 loses nothing, below 1.0 is weaker.
WALL_RESTITUTION = 1.0
RESTITUTION = 1.0

FPS = 60

positions = []
velocities = []

for i in range(NUM_PARTICLES):

    # A random spot inside the bowl, with the whole ball fitting.
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0, BOWL_RADIUS - PARTICLE_RADIUS)

    positions.append(BOWL_CENTER + distance * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

    # A random direction, at roughly PARTICLE_SPEED.
    # Swap for np.array([0.0, 0.0]) to drop the ball from rest.
    angle = random.uniform(0, 2 * np.pi)

    velocities.append(PARTICLE_SPEED * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

# Pygame setup

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

clock = pygame.time.Clock()

running = True

# Main loop

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Seconds since the last frame. This is your timestep.
    dt = clock.tick(FPS) / 1000.0

    ###########################################################################
    # TODO: Make every ball fall, and bounce it off the wall of the bowl.     #
    # 1. INTEGRATION & WALL COLLISIONS FOR EVERY BALL
    for i in range(NUM_PARTICLES):
        # Semi-implicit Euler integration: Update velocity first, then position
        # Gravity accelerates downward (+y in Pygame coordinate system)
        velocities[i] += np.array([0.0, GRAVITY]) * dt
        positions[i] += velocities[i] * dt

        # Calculate offset from center of bowl
        disp_from_center = positions[i] - BOWL_CENTER
        dist_from_center = np.linalg.norm(disp_from_center)

        # Check wall collision: Ball escapes when center distance exceeds max allowed radius
        max_dist = BOWL_RADIUS - PARTICLE_RADIUS
        if dist_from_center > max_dist and dist_from_center > 0:
            # Unit normal pointing inward toward bowl center
            n_hat = -disp_from_center / dist_from_center

            # Velocity component along normal
            v_n = np.dot(velocities[i], n_hat)

            # Reflect velocity if moving outward (v_n < 0 means moving away from center)
            if v_n < 0:
                velocities[i] -= (1.0 + WALL_RESTITUTION) * v_n * n_hat

            # Position correction: Separate overlap to prevent wall sticking/tunneling
            overlap = dist_from_center - max_dist
            positions[i] += n_hat * overlap                                                                      #
    # Two things happen here, in an order that matters.                       #
    #                                                                         #
    # First, it falls. Gravity is an acceleration, so ask yourself what it    #
    # changes directly: the position, or the velocity? And once that has      #
    # changed, what does the ball's new position depend on?                   #
    #                                                                         #
    # Second, it has to stay in the bowl. Work out how you would even         #
    # tell that it has escaped, given that you know where the centre of       #
    # the bowl is, how wide the bowl is, and how wide the ball is.            #
    # Careful: the ball is drawn with a radius of its own, so its edge        #
    # reaches the wall before its centre would.                               #
    #                                                                         #
    # Once you know it has escaped, two things need fixing. Where should      #
    # the ball actually be, and what should its velocity become? For the      #
    # velocity, only the part heading into the wall should change. The        #
    # part sliding along the wall carries on untouched. WALL_RESTITUTION      #
    # decides how much of the incoming speed comes back out.                  #
    ###########################################################################
    
    # CODE STARTS HERE.

    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    ###########################################################################
    # TODO: Make the balls bounce off each other. 
    # 2. PAIRWISE BALL-TO-BALL COLLISIONS
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            disp = positions[i] - positions[j]
            dist = np.linalg.norm(disp)

            # Detect contact: Center-to-center distance is less than combined radii (2 * PARTICLE_RADIUS)
            min_dist = 2 * PARTICLE_RADIUS
            if dist < min_dist and dist > 0:
                # Normal unit vector pointing from ball j to ball i
                n_hat = disp / dist

                # Relative velocity (how fast closing gap is)
                v_rel = velocities[i] - velocities[j]
                v_n = np.dot(v_rel, n_hat)

                # Only resolve if balls are approaching each other (v_n < 0)
                if v_n < 0:
                    impulse = 0.5 * (1.0 + RESTITUTION) * v_n * n_hat
                    velocities[i] -= impulse
                    velocities[j] += impulse

                # Position separation: Push balls apart equally by half the overlap depth
                overlap = min_dist - dist
                positions[i] += 0.5 * overlap * n_hat
                positions[j] -= 0.5 * overlap * n_hat
                                                                       #
    # Start with the condition. Given two balls, what has to be true          #
    # about where they are for them to be touching? Every ball has the        #
    # same radius, which makes this simpler than it sounds.                   #
    #                                                                         #
    # Then the response. A collision changes velocities, not positions.       #
    # Which direction does the change act along, and how would you get        #
    # that direction from the two positions you have? Only the motion         #
    # along that direction matters, the rest is unaffected.                   #
    #                                                                         #
    # One trap worth thinking about: two balls that are overlapping but       #
    # already moving apart should be left alone. If you bounce them again     #
    # they will get stuck together. How would you tell "approaching"          #
    # from "separating"?                                                      #
    #                                                                         #
    # Finally, this has to happen for every pair of balls, not just one.      #
    ###########################################################################

    # CODE STARTS HERE.

    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    # Render

    screen.fill((20, 20, 25))

    pygame.draw.circle(
        screen,
        (180, 180, 180),
        BOWL_CENTER.astype(int),
        BOWL_RADIUS,
        width=3
    )

    for position in positions:
        pygame.draw.circle(
            screen,
            (220, 220, 220),
            position.astype(int),
            PARTICLE_RADIUS
        )

    pygame.display.flip()

pygame.quit()
