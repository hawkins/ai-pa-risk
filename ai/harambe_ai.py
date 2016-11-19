from __future__ import print_function

from risktools import *


# This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""

    continent_scores = {"N. America": 0, "S. America": 3, "Africa": 0, "Europe": 0, "Asia": 0, "Australia": 3}
    border_territories = [0, 2, 8, 9, 10, 16, 17, 19, 21, 24, 25, 26, 27, 28, 30, 37, 38]


    # Get the possible actions in this state
    actions = getAllowedActions(state)

    # To keep track of the best actions we find
    scored_actions = []

    # Evaluate each action
    for action in actions:
        action_value = 0.0

        if state.turn_type == "PreAssign":
            continent = get_target_continent(action, state)
            action_value += continent_scores[continent.name]
            if action.to_territory in border_territories:
                action_value += 1

        elif state.turn_type == "PrePlace":
            continent = get_target_continent(action, state)
            action_value += continent_scores[continent.name]
            if action.to_territory in border_territories:
                action_value += 1

        elif state.turn_type == "Place":
            for neighbor in get_neighbors(state.board, action.to_territory):
                if state.owners[neighbor] != state.owners[get_territory(state.board, action.to_territory)]:
                    action_value += 0.5

        elif state.turn_type == "TurnInCards":
            pass

        elif state.turn_type == "Attack":
            # Simulate the action, get all possible successors
            successors, probabilities = simulateAction(state, action)
            for successor, probability in zip(successors, probabilities):
                # Each successor contributes its heuristic value * its probability to this action's value
                action_value += getReinforcementNum(successor, state.current_player)

        elif state.turn_type == "Occupy":
            pass

        elif state.turn_type == "Fortify":
            pass

        else:
            print("NOT A VALID STATE")

        scored_actions.append((action_value, action))

    # Return the best action
    return max(scored_actions)[1]


def get_territory(board, territory):
    if type(territory) is int:
        return territory
    else:
        return board.territory_to_id[territory]

def get_neighbors(board, territory):
    return board.territories[get_territory(board, territory)].neighbors


def get_target_continent(action, state):
    return state.board.continents[get_continent_from_territory_ID(get_territory(state.board, action.to_territory))]

def get_continent_from_territory_ID(territoryID):
    if territoryID <= 8:
        return "N. America"
    elif 8 < territoryID <= 12:
        return "S. America"
    elif 12 < territoryID <= 18:
        return "Africa"
    elif 18 < territoryID <= 25:
        return "Europe"
    elif 25 < territoryID <= 37:
        return "Asia"
    else:
        return "Australia"

def is_border_territory(board, territoryID):
    # TODO
    # Get neighboring territories
    # Detect if any are in other continent
    pass

# Stuff below this is just to interface with Risk.pyw GUI version
# DO NOT MODIFY

def aiWrapper(function_name, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    print('AI Wrapper created state. . . ')
    game_state.print_state()
    action = getAction(game_state)
    return translateAction(game_state, action)


def Assignment(player):
    # Need to Return the name of the chosen territory
    return aiWrapper('Assignment')


def Placement(player):
    # Need to return the name of the chosen territory
    return aiWrapper('Placement')


def Attack(player):
    # Need to return the name of the attacking territory, then the name of the defender territory
    return aiWrapper('Attack')


def Occupation(player, t1, t2):
    # Need to return the number of armies moving into new territory
    occupying = [t1.name, t2.name]
    aiWrapper('Occupation', occupying)


def Fortification(player):
    return aiWrapper('Fortification')
