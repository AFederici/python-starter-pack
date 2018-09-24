# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random
import json
#import math
#import numpy as np

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
FIRST_TURN = 1
HEALTH = 0
PREV_HEALTH = 0
prevThrows = ["Rock", "Rock"]
throwsPred = [[[0,0,0] for i in range(3)] for i in range(3)]
HealthUrgencySet = {
    0: [0],
    1: [1, 6, 10],
    2: [2, 3, 5, 7, 9, 11, 16],
    3: [4, 8, 12, 15, 17],
    4: [13, 14, 18, 22]
}

def get_death_effects(monster): # monster is monster.death_effects
    if monster.speed > 0: return (monster.speed, "Speed")
    if monster.health > 0: return (monster.health, "Health")
    if monster.scissors > 0: return (monster.scissors, "Scissors")
    if monster.rock > 0: return (monster.rock, "Rock")
    if monster.paper > 0: return (monster.paper, "Paper")

def get_worst_stat_list():
    if me.paper <= me.rock and me.paper <= me.scissors: return "Paper"
    if me.scissors <= me.rock and me.scissors <= me.paper: return "Scissors"
    if me.rock <= me.paper and me.rock <= me.scissors: return "Rock"
    

def closest_killable():
    resp = game.get_monster(0).respawn_counter
    if resp == 0: resp = 40
    healthSetMax = (resp)//(7-me.speed)
    game.log("healthset" + str(healthSetMax))
    maxValue = min(healthSetMax, 4)
    checkingSet = set()
    for i in range(maxValue+1):
        checkingSet = checkingSet | set(HealthUrgencySet[i])
    game.log("len: " + str(len(list(checkingSet))))
    #for j in list(checkingSet):
    #    game.log("checkingset: " str(j))
    adjacentNodes = game.get_adjacent_nodes(me.location)
    #game.log("hi")
    should_check_nodes = [i for i in adjacentNodes if i in checkingSet]
    #for i in should_check_nodes:
        #game.log("should check: " + str(i))
    next_destination = killable(should_check_nodes, 1, healthSetMax)
    game.log("next dest: " + str(next_destination))
    if next_destination not in game.get_adjacent_nodes(me.location):
        return game.shortest_paths(me.location, next_destination)[0][0]
    return next_destination

def killable(nodesToCheck, distance, healthSetMax, enemy=False):
    bestValue = -1
    bestSpot = -1
    #game.log("i ran")
    for location in nodesToCheck:
        if location == 0 and healthSetMax - distance == 1:
            return 0
        #game.log("location" + str(location))
        #game.log("killable loop: " + str(location))
        if len(game.shortest_paths(0, location)[0]) < (healthSetMax - distance):
            if game.has_monster(location):
                #game.log("has monster")
                if not game.get_monster(location).dead:
                    ##game.log(" not dead")
                    #game.log("arg 1  : " + str(game.get_monster(location).health))
                    #game.log("stance to int: " + str(stance_to_int(me,get_winning_stance(game.get_monster(location).stance))))
                    #game.log("speed" + str(7 - me.speed))
                    if game.get_monster(location).health < stance_to_int(me,get_winning_stance(game.get_monster(location).stance)) * (7 - me.speed): ##
                        #game.log("last")
                        death_eff = get_death_effects(game.get_monster(location).death_effects)
                        reward = death_eff[0] * 1.0
                        temp_attack = game.get_monster(location).attack
                        if temp_attack == 0: temp_attack = 1
                        total_dam = ((game.get_monster(location).health // stance_to_int(me,get_winning_stance(game.get_monster(location).stance))) +1 ) * temp_attack
                        score = 1.0 * reward / total_dam
                        #game.log("schore" + str(score))
                        if score > bestValue: 
                            game.log("trige")
                            bestValue = score
                            bestSpot = location
                        if score == bestValue and get_worst_stat_list() == death_eff[1]:
                            game.log("trige")
                            bestValue = score
                            bestSpot = location
                #else:
                #    if game.get_monster(location).respawn_counter < distance * (7-me.speed):
                #        if game.get_monster(location).health < stance_to_int(get_winning_stance(game.get_monster(location).stance)) * (7-speed):

    if bestValue == -1:
        newNodesToCheck_temp = [game.get_adjacent_nodes(i) for i in nodesToCheck]
        newNodesToCheck = list(set(sum(newNodesToCheck_temp, [])))
        healthSetMax -= 1
        maxValue = min(healthSetMax, 4)
        checkingSet = set()
        for i in range(maxValue+1):
            checkingSet = checkingSet | set(HealthUrgencySet[i])
        should_check_nodes = [i for i in newNodesToCheck if i in checkingSet]
        if distance == 2: return should_check_nodes[0]
        for i in should_check_nodes: 
            game.log("should check" + str(i))
        next_destination = killable(should_check_nodes, 2, healthSetMax)
    return bestSpot

def getStance(location):
    if me.location == location:

        if game.has_monster(me.location):
            monster = game.get_monster(me.location)
            if not (monster.dead):
                return get_winning_stance(monster.stance)
            #else:
                #if location == 0:
                #    return "Scissors"
            #    elif me.location == enemy.location or me.location in game.get_adjacent_nodes(enemy.location):
            #        return rpsCounter()
            #    else:
            #        return stances[random.randint(0, 2)]
        #else:
        #    if me.location == enemy.location or me.location in game.get_adjacent_nodes(enemy.location):
        #        return rpsCounter()
        #    else:
        #        return stances[random.randint(0, 2)]

        #if me.location == enemy.location or me.location in game.get_adjacent_nodes(enemy.location):
        #    return rpsCounter()
        #else:
        #    return stances[random.randint(0, 2)]
    else:

        if game.has_monster(location):
            monster = game.get_monster(location)
            if not (monster.dead): # if monster is alive
                if (location == enemy.location or location in game.get_adjacent_nodes(enemy.location)): # if monster is not dead and enemy is at monster or nearby
                    if stance_to_int(enemy, get_winning_stance(monster.stance)) > monster.attack: # if enemyy does more damage with their attack
                        return get_winning_stance(get_winning_stance(monster.stance)) # intentionally go weak against monster to either beat or tie opponent
                return get_winning_stance(monster.stance)

    if location == enemy.location or location in game.get_adjacent_nodes(enemy.location):
        return rpsCounter()
    else:
        return stances[random.randint(0, 2)]

def rpsCounter():
    currentThrow = enemy.stance
    #chang this
    throwsPred[stance_to_index(prevThrows[0])][stance_to_index(prevThrows[1])][stance_to_index(currentThrow)] += 1
    prevThrows.pop()
    prevThrows.insert(0,currentThrow)
    predSum = sum(throwsPred[stance_to_index(prevThrows[0])][stance_to_index(prevThrows[1])])
    if predSum == 0:
        return stances[random.randint(0, 2)]
    else:
        temp = [i / predSum for i in throwsPred[stance_to_index(prevThrows[0])][stance_to_index(prevThrows[1])]]
        temp_max_ind = temp.index(max(temp))
        return stances[(temp_max_ind+1)%3]


def stance_to_index(stance):
    if stance == "Rock":
        return 0
    elif stance == "Paper":
        return 1
    elif stance == "Scissors":
        return 2

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
    enemy = game.get_opponent()
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




    #destination_node = paths[0][0]
    #check for this??

    # get more health if we are low
    #if (me.health < len(game.shortest_paths(me.location, 0)[0]) * 15):
    #    destination_node = game.shortest_paths(me.location, 0)[0][0]

    else:
        if me.location == me.destination: # check if we have moved this turn or if its turn 1
            # get all living monsters closest to me

            if game.has_monster(me.location) and game.get_monster(me.location).dead == False:
                destination_node = me.location
                chosen_stance = getStance(me.location)
            else:
                if me.health < 60:
                    destination_node = game.shortest_paths(me.location, 0)[0][0]
                    chosen_stance = getStance(destination_node)
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
                            damage_dealt = m.attack * (m.health / (1.0 * stance_to_int(me, stance)))
                            if damage_dealt < mini:
                                mini = damage_dealt
                                index = ind
                    monster_to_move_to = monsters[index]

                    # get the set of shortest paths to that monster
                    paths = game.shortest_paths(me.location, monster_to_move_to.location)
                    destination_node = paths[random.randint(0, len(paths)-1)][0]
                    #if game.has_monster(destination_node) and me.movement_counter - me.speed == 1:
                    #    chosen_stance = getStance(destination_node)
                    #else: chosen_stance = get_winning_stance(game.get_opponent().stance)
                    chosen_stance = getStance(destination_node)

        else:
            destination_node = me.destination
            chosen_stance = me.stance
            if PREV_HEALTH > HEALTH:
                chosen_stance = getStance(destination_node)

        #f game.has_monster(me.location):
            # if there's a monster at my location, choose the stance that damages that monster
        #    chosen_stance = getStance(me.location)

        #else:
        #    chosen_stance = stances[random.randint(0, 2)]
        # submit your decision for the turn (This function should be called exactly once per turn)
    FIRST_TURN = 0
    game.submit_decision(destination_node, chosen_stance)

