from __future__ import print_function

from risktools import *


# This is the function implement to implement an AI. Then this AI will work with either the GUI or the play_risk_ai script.
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""

    # Continent priority score list
    continent_scores = {"N. America": 0, "S. America": 3, "Africa": 0, "Europe": 0, "Asia": 0, "Australia": 3}
    # Territory priority score list
    # Territories which border other continents have higher priority.
    border_territories = (0, 2, 8, 9, 10, 16, 17, 19, 21, 24, 25, 26, 27, 28, 30, 37, 38)


    # Get the possible actions in this state
    actions = getAllowedActions(state)

    # To keep track of the best actions we find
    scored_actions = []

    # Evaluate each action
    for action in actions:
        action_value = 0.0

        # In PreAssign, we want to find an available target continent with the highest continent score, then make the priority more granular by choosing a territory within that continent that borders another continent.
        # Prioritize territories within border_territories list.
        # Prioritize territories residing within continents that are close to being conquered by the enemy.
        if state.turn_type == "PreAssign":
            continent = get_target_continent(action, state)
            # Add continent priority score to action value
            action_value += continent_scores[continent.name]
            # If the territory is within the border_territories list.
            if get_territory(state.board, action.to_territory) in border_territories:
                action_value += 1
            # If n-1 territories in the target continent are owned by someone other than the AI...
            enemyOwnedTerritories, unownedTerritories = 0
            for territories in continent

            # Prioritize available territories within that continent


        # In PrePlace, we do the same as what is done in PreAssign above.
        elif state.turn_type == "PrePlace":
            continent = get_target_continent(action, state)
            action_value += continent_scores[continent.name]
            if get_territory(state.board, action.to_territory) in border_territories:
                action_value += 1

        # In Place, we want to be somewhat aggressive and place troops near enemy-owned territories.
        elif state.turn_type == "Place":
            for neighbor in get_neighbors(state.board, action.to_territory):
                if state.owners[neighbor] != state.owners[get_territory(state.board, action.to_territory)]:
                    action_value += 0.5

        # Performs the default TurnInCards action.
        elif state.turn_type == "TurnInCards":
            pass

        # Simulate attack actions and use heuristics to choose the action with the most desirable outcome.
        # Prioritize enemy territories in which fewer other territories within the same continent are owned by that enemy.
        elif state.turn_type == "Attack":
            # Simulate the action, get all possible successors
            successors, probabilities = simulateAction(state, action)
            for successor, probability in zip(successors, probabilities):
                # Each successor contributes its heuristic value * its probability to this action's value
                action_value += getReinforcementNum(successor, state.current_player)

        # Choose an action based on the amount of troops that action would take to execute.
        elif state.turn_type == "Occupy":
            action_value += action.troops

        # Fortify territories, prioritizing territories that border enemy territories.
        elif state.turn_type == "Fortify":
            if action.to_territory is None:
                action_value -= 1
            else:
                if not all(state.owners[n] == state.current_player for n in get_neighbors(state.board, action.to_territory)):
                    action_value += 1

        else:
            print("NOT A VALID STATE")

        scored_actions.append((action_value, action))

    # Return the best action
    return max(scored_actions)[1]

# Return the territory that an action would take place in
def get_territory(board, territory):
    if type(territory) is int:
        return territory
    else:
        return board.territory_to_id[territory]

# Return the neighbors of a given territory.
def get_neighbors(board, territory):
    return board.territories[get_territory(board, territory)].neighbors

# Return the continent that a state would occur in, given some action such as occupying, fortifying, attacking, etc.
def get_target_continent(action, state):
    return state.board.continents[get_continent_from_territory_ID(get_territory(state.board, action.to_territory))]

# Return the continent of a territory given the territory ID
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

# Return the number of territories within the same continent as the given territory ID, and the upper territory ID of that continent
# Can be used to iterate through territories in a continent
def get_shared_territories_count_and_IDs_from_territory_ID(territoryID):
    if territoryID <= 8:
        return 8, 8
    elif 8 < territoryID <= 12:
        return 4, 12
    elif 12 < territoryID <= 18:
        return 6, 18
    elif 18 < territoryID <= 25:
        return 7, 25
    elif 25 < territoryID <= 37:
        return 12, 37
    else:
        return 1, 38


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
