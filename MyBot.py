# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random
import json

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
FIRST_TURN = 1
HEALTH = 0
PREV_HEALTH = 0

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"
def stance_to_int(player, stance):
    if stance == "Rock":
        return player.rock
    elif stance == "Paper":
        return player.paper
    elif stance == "Scissors":
        return player.scissors
# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()
    #with open('mapworld.json') as f:
        #data = json.load(f)
    if FIRST_TURN:
        HEALTH = me.health
        PREV_HEALTH = me.health
        
    else: 
        PREV_HEALTH = HEALTH
        HEALTH = me.health

    if FIRST_TURN:
        destination_node = 10
        chosen_stance = get_winning_stance(game.get_opponent().stance)
        if game.has_monster(destination_node):
            chosen_stance = "Rock"
    else:
        if me.location == me.destination: # check if we have moved this turn or if its turn 1
            # get all living monsters closest to me
            if game.has_monster(me.location) and game.get_monster(me.location).dead == False:
                destination_node = me.location
                chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
            else:
                monsters = game.get_all_monsters()
                index = -1
                mini = 1000
                shortest = 10
                for ind,m in enumerate(monsters):
                    if len(game.shortest_paths(me.location, m.location)[0]) <= shortest:
                        shortest = len(game.shortest_paths(me.location, m.location)[0])
                        if m.dead == True and m.respawn_counter > me.movement_counter - me.speed + shortest * (7 - me.speed):
                            continue
                        stance = get_winning_stance(m.stance)
                        damage_dealt = m.attack * (m.health / 1.0 * stance_to_int(me, stance))
                        if damage_dealt < mini:
                            mini = damage_dealt
                            index = ind
                monster_to_move_to = monsters[index]

                # get the set of shortest paths to that monster
                paths = game.shortest_paths(me.location, monster_to_move_to.location)
                destination_node = paths[random.randint(0, len(paths)-1)][0]
                if game.has_monster(destination_node) and me.movement_counter - me.speed == 1:
                    chosen_stance = get_winning_stance(game.get_monster(destination_node).stance)
                else: chosen_stance = get_winning_stance(game.get_opponent().stance)

        else:
            destination_node = me.destination
            chosen_stance = me.stance
            if PREV_HEALTH > HEALTH:
                chosen_stance = get_winning_stance(game.get_opponent().stance)

        if game.has_monster(me.location):
            # if there's a monster at my location, choose the stance that damages that monster
            chosen_stance = get_winning_stance(game.get_monster(me.location).stance)

        else:
            chosen_stance = stances[random.randint(0, 2)]
        # submit your decision for the turn (This function should be called exactly once per turn)
    FIRST_TURN = 0
    game.submit_decision(destination_node, chosen_stance)

