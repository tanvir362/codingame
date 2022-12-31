import sys
import math


def calculate_target(x1, y1, x2, y2, angle):
    m = (y2-y1) / (x2-x1)
    d = math.hypot(x2-x1, y2-y1)
    r = d * math.tan(math.radians(abs(angle)))
    print('Target distance', r, file=sys.stderr, flush=True)
    r*=5

    z = ((r*r) / (1 + (1 / (m*m))))**0.5

    xt1, xt2 = x2 + z, x2 - z
    yt1, yt2 = (x2 - xt1)/2 + y2, (x2 - xt2)/2 + y2

    if angle>=0:
        return (round(xt1), round(yt1))

    else:
        return (round(xt2), round(yt2))



check_points = {}

cp = 1
completed_a_lap = False
# game loop
boost_applied = False
turn_count = 0
xp, yp = 0, 0 # just initialize no use of initial value
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # if not check_points.get((next_checkpoint_x, next_checkpoint_y)):
    #     check_points[(next_checkpoint_x, next_checkpoint_y)] = cp
    #     cp += 1

    # print('previous ang', next_checkpoint_angle, file=sys.stderr, flush=True)
    # if turn_count == 0:
    #     next_checkpoint_angle = 0
    # else:
    cp_angle = math.atan2(next_checkpoint_y-y, next_checkpoint_x-x)
    # pd_angle = math.atan2(y-yp, x-xp)

    next_checkpoint_angle = math.degrees(cp_angle) + next_checkpoint_angle

    print(f"dist:{next_checkpoint_dist},ang:{next_checkpoint_angle}",file=sys.stderr, flush=True)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100) or "BOOST"
    # i.e.: "x y thrust"
    # dist = round(math.hypot(next_checkpoint_x-x, next_checkpoint_y-y))
    

    # if (abs(next_checkpoint_angle)>=40 and next_checkpoint_dist<1500) or abs(next_checkpoint_angle)>=80:
        
    #     if math.hypot(opponent_x-x, opponent_y-y)<805:
    #         th = 'SHIELD'
    #     else:
    #         th = 0

    #     target_x, target_y = next_checkpoint_x, next_checkpoint_y
    
    
    # else:
    #     if (not boost_applied) and next_checkpoint_dist>3000:
    #         th = 'BOOST'
    #         boost_applied = True
    #     else:
    #         if abs(next_checkpoint_angle)>=50 and math.hypot(opponent_x-x, opponent_y-y)<805:
    #             th = 'SHIELD'
    #         else:
    #             th = 100

    #     target_x, target_y = calculate_target(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle)


    if abs(next_checkpoint_angle) >= 80:
        # target_x, target_y = next_checkpoint_x, next_checkpoint_y
        th = 0
    else:
        # target_x, target_y = calculate_target(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle)
        th = 100

    if (not boost_applied) and next_checkpoint_dist>4000:
        print('Applying BOOST..', file=sys.stderr, flush=True)
        th = 'BOOST'
        boost_applied = True

    elif math.hypot(opponent_x-x, opponent_y-y)<805:
        print('Applying SHIELD..', file=sys.stderr, flush=True)
        th = 'SHIELD'

    elif next_checkpoint_dist<800:
        th = 0


    print(th, file=sys.stderr, flush=True)
    
    print(next_checkpoint_x, next_checkpoint_y, th)

    xp, yp = x, y
    turn_count += 1
