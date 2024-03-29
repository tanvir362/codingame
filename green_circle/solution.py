import sys
import math
import json

# Complete the hackathon before your opponent by following the principles of Green IT

skills  = [
    'TRAINING',
    'CODING',
    'DAILY_ROUTINE',
    'TASK_PRIORITIZATION',
    'ARCHITECTURE_STUDY',
    'CONTINUOUS_INTEGRATION',
    'CODE_REVIEW',
    'REFACTORING'
]

applications = {}
my_skills = {}
my_location = -1
my_release_count = 0


# game loop
while True:
    print('------turn start------',file=sys.stderr, flush=True)
    game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    print('phase', game_phase, file=sys.stderr, flush=True)

    applications_count = int(input())
    for i in range(applications_count):
        inputs = input().split()
        object_type = inputs[0]
        _id = int(inputs[1])
        training_needed = int(inputs[2])  # number of TRAINING skills needed to release this application
        coding_needed = int(inputs[3])  # number of CODING skills needed to release this application
        daily_routine_needed = int(inputs[4])  # number of DAILY_ROUTINE skills needed to release this application
        task_prioritization_needed = int(inputs[5])  # number of TASK_PRIORITIZATION skills needed to release this application
        architecture_study_needed = int(inputs[6])  # number of ARCHITECTURE_STUDY skills needed to release this application
        continuous_delivery_needed = int(inputs[7])  # number of CONTINUOUS_DELIVERY skills needed to release this application
        code_review_needed = int(inputs[8])  # number of CODE_REVIEW skills needed to release this application
        refactoring_needed = int(inputs[9])  # number of REFACTORING skills needed to release this application

        applications[_id] = {
            "needs": {skills[indx-2]: int(inputs[indx]) for indx in range(2,10) if int(inputs[indx]) > 0 },
            "requirements": [*map(int, inputs[2:10])]
        }
    
    print(json.dumps(applications, indent=2),file=sys.stderr, flush=True)
    
    for i in range(2):
        # player_location: id of the zone in which the player is located
        # player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
        # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
        player_location, player_score, player_permanent_daily_routine_cards, player_permanent_architecture_study_cards = [int(j) for j in input().split()]
        if i==0:
            print('me',player_location, player_score, file=sys.stderr, flush=True)
            my_location = player_location
            my_release_count = player_score

        else:
            print('opponent',player_location, player_score, file=sys.stderr, flush=True)
    
    card_locations_count = int(input())
    print('at every card location', file=sys.stderr, flush=True)
    for i in range(card_locations_count):
        inputs = input().split()
        cards_location = inputs[0]  # the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS (AUTOMATED and OPPONENT_AUTOMATED will appear in later leagues)
        training_cards_count = int(inputs[1])
        coding_cards_count = int(inputs[2])
        daily_routine_cards_count = int(inputs[3])
        task_prioritization_cards_count = int(inputs[4])
        architecture_study_cards_count = int(inputs[5])
        continuous_delivery_cards_count = int(inputs[6])
        code_review_cards_count = int(inputs[7])
        refactoring_cards_count = int(inputs[8])
        bonus_cards_count = int(inputs[9])
        technical_debt_cards_count = int(inputs[10])
        print('inputs', inputs, file=sys.stderr, flush=True)

    possible_moves_count = int(input())
    ac = "RANDOM"
    for i in range(possible_moves_count):
        possible_move = input()
        print('possible move', possible_move, file=sys.stderr, flush=True)

        

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT; In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING;
    if game_phase == 'MOVE':
        if my_location > 0:
            print('MOVE', my_location-1, my_location-1)
        else:
            print('MOVE', 7, 7)

    elif game_phase == 'RELEASE':
        print('RANDOM', 'Release')
    print('------turn end------',file=sys.stderr, flush=True)
