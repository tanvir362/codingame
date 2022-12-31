import sys
import math

from functools import lru_cache

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

@lru_cache(maxsize=100000000)
def turn(groups):
    print(f'---turn---{t+1}',file=sys.stderr, flush=True)
    boarded = 0

    group_loaded = 0
    while boarded<l and group_loaded<n:
        seat_reamaining = l-boarded

        if groups[0]<=seat_reamaining:
            boarded += groups[0]
            print(groups[0], 'boarding.. from', groups, file=sys.stderr, flush=True)
            groups = groups[1:]+(groups[0],)

            group_loaded += 1

        else:
            break
            

    print('trun end:', groups, file=sys.stderr, flush=True)

    return (boarded, groups)



l, c, n = [int(i) for i in input().split()]

groups = tuple(int(input()) for i in range(n))

total = 0
for t in range(c):
    turn_earning, groups = turn(groups)
    total += turn_earning

print(total)
