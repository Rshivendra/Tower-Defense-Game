#Student/Class: Rajmohan Shivendra/DS01
#Date: 07 August 2022

import random

import shelve

import sys

import math

game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat' : 0,                   # threat meter for difficulty
    'danger' : 1                    # danger level for difficulty
    }



# Monster/Defenders for Basic - Advance
#========================================
archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5,
          'upgrd_goal' : 3
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3,
        'upgrd_goal' : 5
        }

zombie = {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 3
        }

werewolf = {'shortform': 'WWOLF',
            'name':'Werewolf',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 4,
            'moves' : 2,
            'reward': 3}

#========================================

#filler spot =  {'name': 'Zombie', 'hp': 15, 'defender' : False, 'mons_lvl': (game_vars['danger'] - 1), 'bossMinion' : False}

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

# Monsters/defenders for Optional
#=========================================
skeletonking = {'shortform':'SKING',
                'name'   : 'Skeletonking',
                'maxHP'  : len(field),
                'moves'  : 0,
                'reward' : 'win'
                }


skeleton = {'shortform': 'SKELE',
            'name':'Skeleton',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 3,
            'moves' : 1,
            'reward': 4
            }

musketeer = {'shortform' : 'MUSKT',
          'name': 'Musketeer',
          'maxHP': 9,
          'min_damage': 5,
          'max_damage': 7,
          }

brick = {'shortform': 'BRICK',
        'name': 'Brick',
        'maxHP': 30,
        'min_damage': 0,
        'max_damage': 0
        }

wizard = {'shortform': 'WIZAR',
        'name': 'Wizard',
        'maxHP': 12,
        'min_damage': 5,
        'max_damage': 8,
        'price' : 25
        }
#=======================================


#                Variables for Game Options/Row&Col Selection
#==============================================================================

menuScreen = ['Desperate Defenders','Defend the city from undead monsters!']

menuOptions = ['Start new game', 'Load saved game','Quit']

row_alpha = {}

col_limit = ['1','2','3']

twr_list = ["Archer ({} gold)".format(archer.get('price')), "Wall ({} gold)".format(wall.get('price')),\
            "Wizard ({} gold)".format(wizard.get('price')) ,"Don't buy"]

twr_dict = {1 : archer, 2 : wall, 3 : wizard}

combat_list = ["Buy unit", "End turn", "Save game", "Quit"]

spaces = 5

threat_mtr_max = 10

mobs_list = [zombie,werewolf,skeleton]

boss_lvl = "no"

#==============================================================================


#                        Functions to Print Screens/Menus for Game
#=================================================================================================
def showMenuScreen(menuScreen):
    print(menuScreen[0])
    print("{}".format(len(menuScreen[0])*"-"))
    print(menuScreen[1])


def showMenuOptions(menuOptions):
    for i in range(len(menuOptions)):
        print("{}. {}".format(i+1,menuOptions[i]))

def showCombatMenu(combatMenuOptions):
        print("{}. {:10} {}. {}".format(1, combatMenuOptions[0],2,combatMenuOptions[1])) 
        print("{}. {:10} {}. {}".format(3, combatMenuOptions[2],4,combatMenuOptions[3]))

def showGameStats(game_vars):
        
    print("Turn {:1}      Threat = [{}]       Danger Level {}".\
          format(game_vars.get('turn'),(threat_mtr_max*" ") if game_vars.get('threat') == 0 else ((game_vars.get('threat')*"-")\
                                                                                          + (threat_mtr_max  - game_vars.get('threat')) * " "),\
                 game_vars.get('danger')))
    
    print("Gold = {:1}   Monsters killed = {}/{}".format(game_vars.get('gold'),\
                                                         game_vars.get('monsters_killed'),\
                                                         game_vars.get('monster_kill_target')))
  
def showTwrOptions(twr_list):
    for i in range(len(twr_list)):
        print("{}. {}".format(i+1, twr_list[i]))
    
#=================================================================================================



# Draw Field function:
#===========================================
# Draws the field for every turn of the game
# prints the rows, and columns of the field
# which prints the unit's health and name
# if there is a unit on that row/column
#===========================================
def draw_field(field):
    row_num = len(field)
    column_num = 0
    key_count = 0

    for limits in col_limit:
        print("{:>5}".format(limits), end=" "*(int(len(col_limit))-2))
    print()


    for row in range(row_num):

        column_num = len(field[key_count])

        print(" "+"+-----"*(column_num) +"+")
                    
        row_alpha[key_count] = chr(65+key_count)
        
        print("{}".format(row_alpha.get(key_count)),end="")
        
        for col in range(column_num):

            if field[row][col] != None:
                unit_name = field[row][col].get('name').lower()
                print("|"+"{:^5s}".format(eval(unit_name).get('shortform')),end = "")
                
            else:
                print("|"+"{:^5}".format(" "),end= "")
          
        key_count+=1
        
        print("|")
        print(" ",end = "")
                
        for col in range(column_num):
            
            if field[row][col] != None:
                unit_name = field[row][col].get('name').lower()
                
                if field[row][col].get('defender'):
                    print("|"+"{:2}/{:<2}".format(field[row][col].get('hp'),eval(unit_name).get('maxHP')),end = "")

                elif field[row][col].get('boss'):
                    print("|"+"{:2}/{:<2}".format(field[row][col].get('hp'),eval(unit_name).get('maxHP')),end = "")                    
                    
                else:
                    print("|"+"{:<2}/{:<2}".format(field[row][col].get('hp'),eval(unit_name).get('maxHP') + \
                                                   field[row][col].get('mons_lvl')),end = "")
                               
            else:
                print("|"+"{:^5}".format(" "),end="")
                
        print("|")


    print(" " + "+-----"*(column_num) + "+")
            
            
#-----------------------------------------------------
# place_unit()    
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    If in defender argument is False, monster placement function will activate
#    Else if defender argument is True, placement for defender placement will activate
#    If position is invalid, return back this function after printing a error msg
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name,defender):

    if defender == False:
        while True:
            if field[position][-1] != None:
                #print("Position is not empty")
                position = random.randint(0,(len(field)-1))
                continue
            else:
                #print("Position is empty")
                field[position][-1]= unit_name
                return True
    else:
        try:
            if position[0].isdigit():
                print("Invalid Input Please Try Again..")
                position = checker(twr_option,str)
                return place_unit(field, position, unit_name,defender)

            elif position[1].isalpha():
                print("Invalid Input Please Try Again..")
                position = checker(twr_option,str)
                return place_unit(field, position, unit_name,defender)

            else:
                pass

            row_ltr = position[0].upper()
            col_num = int(position[1]) - 1

            if len(position) > 2:
                print("Position is not on the field of play")
                position = checker(twr_option,str)
                return place_unit(field, position, unit_name,defender)
                
            elif col_num > len(col_limit)-1 or col_num < 0:
                print("Defender is placed past the first 3 columns")
                position = checker(twr_option,str)
                return place_unit(field, position, unit_name,defender)
                
            else:
                
                for key, value in row_alpha.items():
                    if value == row_ltr:
                            row = key
                    else:
                        pass
                                                    
                if field[row][col_num] != None:
                    print("Position is occupied")
                    position = checker(twr_option,str)
                    return place_unit(field, position, unit_name,defender)
                else:
                    field[row][col_num] = {'name' : unit_name['name'],
                                               'hp' : unit_name['maxHP'],
                                               'defender' : True,
                                               'current' : 0}
                    return True
                    # the spawning defender function is spawned with a dictionary
                    # it will spawn with name,hp,defender identifier and current
                    # current is used for upgrading of unit which can be interpretted as
                    # kill count
                
        except IndexError:
            print("Position is not on the field of play")
            position = checker(twr_option,str)
            return place_unit(field, position, unit_name,defender)

        except ValueError:
            print("Position is not on the field of play")
            position = checker(twr_option,str)
            return place_unit(field, position, unit_name,defender)

        except:
            print("Position is not on the field of play")
            position = checker(twr_option,str)
            return place_unit(field, position, unit_name,defender)
                    

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#    each time a monster is spawn the number of monsters on the field
#    will increase for every time the monster is spawned
#    after which monster will go to place_unit function to be placed
#---------------------------------------------------------------------

def spawn_monster(field, monster_list):
    
    row = random.randint(0,(len(field)-1))

    unit = {'name' : monster_list['name'],
                      'hp' : monster_list['maxHP'] + (game_vars['danger'] - 1),
                      'defender' : False,
                      'mons_lvl' : (game_vars['danger'] - 1),
                      'bossMinion' : False}
    
                      # the spawning of monster will be use of dictionary
                      # it will have name,hp,mons_lvl,bossMinionIdentifier
                      # mon_lvl is used for advance to know what level is the monster
                      # based on the danger level,
                      # bossMinion is used to identify if the mob is the boss's minion
                      # or not.
    
    game_vars['num_monsters'] = game_vars.get('num_monsters') + 1
    game_vars.update()
    
    place_unit(field, row, unit,unit.get('defender'))

#-----------------------------------------------------
# buyTwr()    
#
#   Allows for purchasing of tower
#   this function will check if the option is valid
#   else ask to reprompt option
#   if the amount of gold the user has is not sufficient
#   prompt an error msg saying the amount of gold required
#   has not been met
#   if the gold is enough, it will move on to place_unit()
#-----------------------------------------------------
def buyTwr(twr_option,twr_placing,field):
    if twr_option != len(twr_list):
        twr = twr_dict[twr_option]

        if game_vars.get('gold') >= twr.get('price'):
            
            game_vars['gold'] = game_vars.get('gold') - twr.get('price')
            game_vars.update()
            
            place_unit(field, twr_placing, twr,True)

        else:
            print("Uh oh! you are not able to purchase this tower..")
            twr_option = checker(twr_list,int)

            return buyTwr(twr_option,twr_placing,field)
    else:
        return False

#-----------------------------------------------------
# twrAttack()    
#
#  used for the attacking of the various defenders.
#
#     Archer: attacks in a straight line
#             weak against Skeletons
#
#     Wall: does no damage so this function will not be of use
#
#     Wizard: Attacks in a straight line but chance
#             to shift monster to a random lane back to the start
#
#     If Archer reaches 3 kills, evolve to musketeer
#     musketeer shoots in 2 other lanes except for its own
#
#     If wall survives for a few turns when theres a monster on the same lane
#     evolves to Brick with additional 5 health points.
#
#     if a monster reaches 0 multiple events happen:
#               1. the threat meter increases based on the reward
#               2. gold will be given based on the reward for killing monster
#               3. the number of monsters on the field will decrease by 1
#
#     this function will aslo be using to deduct the health of the boss
#     if a tower kills a boss minion it will deduct 1 health away from the boss
#     if it reaches 0 boss dies and user wins.
#-----------------------------------------------------        
def twrAttack(defender_name, field, row, column,mons,monsColumn):
    
    lane = row_alpha[row]
    defender_dict = defender_name.lower()
    defender_dict = eval(defender_dict)
    
    dmg = random.randint(defender_dict.get('min_damage'),defender_dict.get('max_damage'))

    if defender_dict.get('min_damage') == 0 and defender_dict.get('max_damage') == 0:

        if defender_name.lower() == 'wall':
            
            field[row][column]['current'] = field[row][column].get('current') + (random.randint(1,2))
            
            unitUpgrade(defender_name.lower(),field,row,column)
            
        else:
            pass
        
    else:
                
        for colCheck in range(len(field[0])):

            if monsColumn != colCheck:
                pass
            
            else:
                
                unitDmg(defender_name.lower(),field,mons,lane,field[row][colCheck],dmg)

                if field[row][colCheck]['hp'] > 0:

                    if defender_name.lower() == 'wizard':

                        chngChance = random.randint(0,2)

                        if chngChance == 1:
                        
                            row_switch = random.randint(0,(len(field)-1))

                            while True:
                                if row_switch == row:
                                    
                                    row_switch = random.randint(0,(len(field)-1))
                                    continue
                                
                                else:
                                    print("{} uses his magic to cast a tornado on {} in lane {}!".format(defender_name.lower(),mons['name'],lane))
                                    field[row][colCheck] = None
                                    place_unit(field, row_switch, mons,False)
                                    break

                        else:
                            pass

                    else:
                        pass
                                
                else:
                
                    if defender_name.lower() == 'archer':

                        field[row][column]['current'] = field[row][column].get('current') + 1
                    
                        unitUpgrade(defender_name.lower(),field,row,column)

                    else:
                        pass

                    
                    if field[row][colCheck]['bossMinion'] == False:

                        mons_name = eval(field[row][colCheck].get('name').lower())

                        delte = bossMinion(mons_name,field[row][colCheck],False,field)

                        field[row][colCheck] = delte


                    else:
                        
                        mons_name = eval(field[row][colCheck].get('name').lower())

                        delte = bossMinion(mons_name,field[row][colCheck],True,field)

                        field[row][colCheck] = delte
                        
                        for row in range(len(field)):
                            if field[row][-1] == None:
                                pass
                            
                            elif field[row][-1].get('boss') == True:
                                
                                field[row][-1]['hp'] = field[row][-1].get('hp') - 1
                            
                                if field[row][-1]['hp'] <= 0:
                    
                                    field[row][-1] = None
                                    print("The boss rests...")
                                    
                                    print("Congratulations you have won the game! :)")
                                    sys.exit()
                                
                            else:
                                continue
                            
                        
                        
#-----------------------------------------------------
# bossMinion()    
#
#   used for twrAttacking function
#   if the monster is a bossMinion,
#   gold,num_monsters will be increased
#
#   else, gold,num_monsters,threatMeter
#         monstersKilled will be increased
#         respectively
#-----------------------------------------------------
def bossMinion(mons_name,monsterCheck,minion_tf,field):

    if minion_tf == False:
    
        kil_reward = mons_name.get('reward') + monsterCheck.get('mons_lvl')

        game_vars['threat'] = game_vars.get('threat') + kil_reward
                            
        game_vars['gold'] = game_vars.get('gold') + kil_reward
        game_vars['num_monsters'] = game_vars.get('num_monsters') - 1
                            
        print("{} Dies!".format(monsterCheck.get('name')))

        game_vars['monsters_killed'] = game_vars.get('monsters_killed') + 1

        monsterCheck = None
                    
        return monsterCheck

        game_vars.update()
        
    else:
                
        kil_reward = mons_name.get('reward') + monsterCheck.get('mons_lvl')

        game_vars['gold'] = game_vars.get('gold') + kil_reward

        game_vars['num_monsters'] = game_vars.get('num_monsters') - 1

        print("{} minion Dies!".format(monsterCheck.get('name')))

        monsterCheck = None

        return monsterCheck
    
        game_vars.update()



#-----------------------------------------------------
# unitUpgrade()    
#
#   used in twrAttacking function
#   if archer or wall reaches a specifc killCount/TurnCount
#   they evolve into musketeer/brick respectively
#-----------------------------------------------------
def unitUpgrade(defender_name,field,row,column):

                        
    if defender_name == 'archer' and field[row][column]['current'] >= eval(defender_name).get('upgrd_goal'):

            
        field[row][column] = {'name' : musketeer['name'],
                              'hp' : musketeer['maxHP'],
                              'defender' : True,
                             }

        print("{} has been upgraded to {}".format(defender_name,field[row][column].get('name')))

    elif defender_name == 'wall' and field[row][column]['current'] >= eval(defender_name).get('upgrd_goal'):

          
        field[row][column] = {'name' : brick['name'],
                              'hp' : field[row][column]['hp']+5,
                              'defender' : True,
                              }

        print("{} has been upgraded to {}".format(defender_name,field[row][column].get('name')))

    else:
        pass   

    

#-----------------------------------------------------
# unitDmg()    
#
#   using in twrAttacking function
#   used to check if a specifc tower is attacking a
#   specific monster, is so, damage calculation will be
#   applied based on it
#   else normal damage calculations will be made
#-----------------------------------------------------
def unitDmg(defender_name,field,mons,lane,monsterCheck,dmg):
    
    hp = monsterCheck.get('hp')

    if monsterCheck.get('name').lower() == 'skeleton' and defender_name == 'archer':

        print("{} in lane {} shoots {} for {} damage!".format(defender_name,lane,mons.get('name'),dmg))
                    
        monsterCheck['hp'] = hp - (dmg/2)
        monsterCheck['hp'] = math.floor(monsterCheck['hp'])
                    
    else:
                    
        print("{} in lane {} shoots {} for {} damage!".format(defender_name,lane,mons.get('name'),dmg))
                    
        monsterCheck['hp'] = hp - dmg


#-----------------------------------------------------
# monster_advance()    
#
#   this function is for the moving of monsters on the field
#   monster will move step by step so if monster moves by 2 steps
#   the monster will move 1 step then another
#   there are 4 conditions when a monster advances
#      1. if next position is empty, monster is free to go
#      2. if next position is a defender damage will be made
#         and if defender's hp reaches 0 defender dies
#      3. if the next position has a monster moving will be stopped
#      4. if monster advances out of the field, then the user loses
#-----------------------------------------------------
def monster_advance(monster_name, field, row,column):
    steps_list = []
    lane = row_alpha[row]
    
    mons_dict = monster_name.lower()
    mons_dict = eval(mons_dict)
    
    step = mons_dict.get('moves')

    for i in range(1,step+1):
        i = 1
        steps_list.append(i)
            
    for movement in steps_list:
        column_next = column - movement
        if field[row][column_next] == None:
                
            if column_next < 0:
                print("A {} has reached the city! All is lost!".format(mons_dict.get('name')))
                print("You have lost the game. :(")
                sys.exit()
                break
            
            print("{} in lane {} advances!".format(monster_name,lane))
            field[row][column_next] = field[row][column]
            
            field[row][column] = None
            column = column_next
            # Moves if next space is empty

        
        elif field[row][column_next].get('defender') == True:
            
            hp = field[row][column_next].get('hp')
            dmg = random.randint(mons_dict.get('min_damage')+field[row][column].get('mons_lvl'),\
                                 mons_dict.get('max_damage')+field[row][column].get('mons_lvl'))
            
            field[row][column_next]['hp'] = hp - dmg
            print("{} in lane {} hits {} for {} damage!".format(mons_dict.get('name'),lane,field[row][column_next].get('name'),dmg))
            
            if field[row][column_next]['hp'] <= 0:
                
                print("{} Dies!".format(field[row][column_next].get('name')))
                field[row][column_next] = None
                # Attacks unit based on number of steps
   
        else:
            print("{} in lane {} is blocked from advancing".format(field[row][column].get('name'),lane))
            return False
            # Stop movement

#-----------------------------------------------------
# initialize_game()    
#
#   this function is used for when user presses new game
#   all game_vars will be set to the default value
#-----------------------------------------------------                             
def initialize_game(game_vars):
    game_vars['turn'] = game_vars.get('turn') + 1
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars.update()


#-----------------------------------------------------
# turnProgress()    
#
#   this function will help increase the turn count and gold by 1
#   for everytime this function is called
#-----------------------------------------------------
def turnProgress(game_vars):
    game_vars['turn'] = game_vars.get('turn') + 1
    game_vars['gold'] = game_vars.get('gold') + 1
    game_vars.update()

#-----------------------------------------------------
# checker()    
#
#   this function is used for input validation
#   if its an integer type then based on the lenght of the options from a list
#   it will display a error msg
#   if its a str input type, then it will check if its empty or not
#-----------------------------------------------------
def checker(item_list,typ_input):
    valueChecker = 0

    if typ_input == int:
        while True: 
            try:
                valueChecker = int(input("Your choice? "))

                if valueChecker > len(item_list) or valueChecker <= 0:
                    print("Please input an option from 1 - {}!".format(len(item_list)))
                else:
                    return valueChecker
                    break
                
            except ValueError:
                print("Value Error!, Please input numeric value!")
    else:
        while True:
            try:
                valueChecker = input("Place where? ")
                if not valueChecker:
                    raise ValueError('Input a valid positon E.g a1,b2,d3,etc')
                else:
                    return valueChecker
                    break
            except ValueError as e:
                print(e)
            
#-----------------------------------------------------
# bossMob()    
#
#   this function will spawn in the boss's
#   minions based on the hp of the boss
#-----------------------------------------------------
def bossMob(minion_mob,boss,field):
    hp = 0
    for spawnRate in range(boss.get('maxHP')+1):
        
        unit = {'name' : minion_mob['name'],
        'hp' : minion_mob['maxHP'] + (game_vars['danger'] - 1),
        'defender' : False,
        'mons_lvl' : (game_vars['danger'] - 1),
        'bossMinion' : True
               }
  
        game_vars['num_monsters'] = game_vars.get('num_monsters') + 1
        
        row_minion = random.randint(0,len(field)-1)

        if unit.get('defender') == True:
            pass
        
        else:
                if field[row_minion][-2] != None:
                    
                    row_minion = random.randint(0,(len(field)-1))
                    continue
                
                else:
                    
                    boss['maxHP'] = hp = hp + 1
                    field[row_minion][-2] = unit
                                   
        game_vars.update()
    
#-----------------------------------------------------
# clearMons()    
#
#   this function will clear the other existing monsters
#-----------------------------------------------------
def clearMons(field):
    for row in range(0, len(field)):
        for col in range(0,len(field[0])):
            if field[row][col] == None or field[row][col].get('boss') == True:
                pass
            else:
                unit_tf = field[row][col].get('defender')
                if unit_tf:
                    pass
                else:
                    field[row][col] = None

#-----------------------------------------------------
# loadBoss()    
#
#   this function is used to spawn the boss
#   before the boss is spawned the field will be cleared
#   of existing monsters and the boss's minions will be spawned
#-----------------------------------------------------
def loadBoss(boss,field,minion):

    row_minion = 0
        
    row = ((len(field)-1)/2)

    row = math.floor(row)

    clearMons(field)
    bossMob(minion,boss,field)
    
    field[row][-1] = {    'name' : boss['name'],
                          'hp' : boss['maxHP'],
                          'boss' : True
                     }                
#-----------------------------------------------------
# fieldChecking()    
#
#   this function is important, as it enables the
#   defender attacking and monster movement
#   and for musketeer since it attacks in the other lanes
#   this function will check the other lanes for a monster
#-----------------------------------------------------
def fieldChecking(field):
    
    for row in range(0, len(field)):
        
        for col in range(0,len(field[0])):
            
            if field[row][col] == None:
                pass
            
            else:
                unit_tf = field[row][col].get('defender')
                if unit_tf:
                    
                    if field[row][col].get('name').lower() == 'musketeer':

                        for muskCheck in range(col,len(field[0])):

                            if row-1 < 0:
                                pass
                            else:
                                if field[row-1][muskCheck] != None:

                                    muskCheck_tf = field[row-1][muskCheck].get('defender')

                                if field[row-1][muskCheck] == None or muskCheck_tf == True or field[row-1][muskCheck].get('boss') == True:
                                    pass
                                else:
                                    twrAttack(field[row][col].get('name'),field,row-1,col,field[row-1][muskCheck],muskCheck)
                                
                            if row+1 > (len(field)-1):
                                pass
                            else:
                                if field[row+1][muskCheck] != None:

                                    muskCheck_tf = field[row+1][muskCheck].get('defender')

                                if field[row+1][muskCheck] == None or muskCheck_tf == True or field[row+1][muskCheck].get('boss') == True:
                                    pass
                                else:
                                    twrAttack(field[row][col].get('name'),field,row+1,col,field[row+1][muskCheck],muskCheck)
                                    break
                    
                    else:    
                        for monsCheck in range(col,len(field[0])):

                            if field[row][monsCheck] != None:
                                    
                                monsCheck_tf = field[row][monsCheck].get('defender')
                                    
                            if field[row][monsCheck] == None or monsCheck_tf == True or field[row][monsCheck].get('boss') == True:
                                pass
                            else:
                                twrAttack(field[row][col].get('name'),field,row,col,field[row][monsCheck],monsCheck)
                                break
                else:
                    monster_advance(field[row][col].get('name'),field,row,col)

#-----------------------------------------------------
# loadgame()    
#
#   this function will activate when the user
#   decides to load a game from a save file
#   and based on that the game will continue
#-----------------------------------------------------
def loadgame(field,combatOption,threat_mtr,danger_lvl,boss_lvl,game_vars):
    
    while combatOption != len(combat_list):
        
        if combatOption == 3:
            
            saveGame()
                        
            print('Game Saved!')
            
            break

        if combatOption == 1:
            
            showTwrOptions(twr_list)
            twr_option = checker(twr_list,int)
            
            if twr_option != len(twr_list):
                
                twr_placing = checker(twr_option,str)
                buyTwr(twr_option,twr_placing,field)

        fieldChecking(field)
                            
        if game_vars.get('num_monsters') == 0 and boss_lvl == "no":
            
            mob = random.randint(0,(len(mobs_list)-1))
            print("{} has spawned!".format(mobs_list[mob].get('name')))
            
            spawn_monster(field,mobs_list[mob])
            
        elif game_vars.get('monsters_killed') >= game_vars.get('monster_kill_target') and boss_lvl == "no":
            print("Boss Approaching..")
            boss_lvl = "yes"
            loadBoss(skeletonking,field,skeleton)


        thretMeter(game_vars,boss_lvl)

        dangerMeter(game_vars,boss_lvl)

                    
        print("Current threat meter = {}".format(game_vars.get('threat')))        
        turnProgress(game_vars)
        
        draw_field(field)
        showGameStats(game_vars)
        
        showCombatMenu(combat_list)            

        combatOption = checker(combat_list,int)   
   
#-----------------------------------------------------
# thretMeter()    
#
#   this function will activate every other turn
#   it will increase the threat meter by 1 and the level
#   of the danger level inclusive every turn
#   if threat meter reaches 10 spaces or more
#   for every 10 spaces removed a new monster spawns
#-----------------------------------------------------
def thretMeter(game_vars,boss_lvl):

    threat_incr = 0

    mob = 0

    if game_vars.get('threat') < threat_mtr_max and boss_lvl == "no":
        
        threat_incr = random.randint(1,game_vars.get('danger'))
        game_vars['threat'] = game_vars.get('threat') + threat_incr

        game_vars.update()
            
    elif game_vars.get('threat') >= threat_mtr_max and boss_lvl == "no":
        
        for numbr in range(1,game_vars.get('threat')+1):

            if numbr % threat_mtr_max == 0:

                mob = random.randint(0,(len(mobs_list)-1))
                print("{} has spawned!".format(mobs_list[mob].get('name')))
                    
                spawn_monster(field,mobs_list[mob])
                game_vars['threat'] = game_vars.get('threat') - numbr
                    
                game_vars.update()

#-----------------------------------------------------
# dangerMeter()    
#
#   this function will increase its danger level
#   for every 12 turns
#-----------------------------------------------------
def dangerMeter(game_vars,boss_lvl):

    if game_vars.get('turn') % 12 == 0 and boss_lvl == "no":

        game_vars['danger'] = game_vars.get('danger') + 1
        game_vars.update()
                
        print("The evil grows stronger..")
        print("Danger Level increased to {}!".format(game_vars.get('danger')))


#-----------------------------------------------------
# saveGame()    
#
#   this function is used to save the game by using the
#   import function shelve
#-----------------------------------------------------
def saveGame():

    shelfFile = shelve.open('saved_game_filename')

    shelfFile['mainBoard'] = field

    shelfFile['gameStats'] = game_vars

    shelfFile['meter_threat'] = game_vars.get('threat')

    shelfFile['dangr_lvl'] = game_vars.get('danger')

    shelfFile['boss_lvl'] = boss_lvl

    shelfFile.close()
    

#============================================
#               MAIN - GAME
#============================================
showMenuScreen(menuScreen)
print()
showMenuOptions(menuOptions)

menuOption = checker(menuOptions,int)

if menuOption == 1:
    
    initialize_game(game_vars)
    spawn_monster(field,zombie)

    draw_field(field)
    showGameStats(game_vars)
    
    showCombatMenu(combat_list)

    combatOption = checker(combat_list,int)
  
    while combatOption != len(combat_list):

        #save game if user decided to save the game
        if combatOption == 3:

            saveGame()
                        
            print('Game Saved!')
            
            break

        if combatOption == 1:
            
            showTwrOptions(twr_list)
            twr_option = checker(twr_list,int)
            
            if twr_option != len(twr_list):
                
                twr_placing = checker(twr_option,str)
                buyTwr(twr_option,twr_placing,field)

        fieldChecking(field)

        #if the number of monsters decreased to 0, spawn a random mob             
        if game_vars.get('num_monsters') == 0 and boss_lvl == "no":
            
            mob = random.randint(0,(len(mobs_list)-1))
            print("{} has spawned!".format(mobs_list[mob].get('name')))
            
            spawn_monster(field,mobs_list[mob])
            
        #if the number of monsters killed reaches 20 the boss will load    
        elif game_vars.get('monsters_killed') >= game_vars.get('monster_kill_target') and boss_lvl == "no":
            print("Boss Approaching..")
            boss_lvl = "yes"
            loadBoss(skeletonking,field,skeleton)


        thretMeter(game_vars,boss_lvl)

        dangerMeter(game_vars,boss_lvl)

                    
        print("Current threat meter = {}".format(game_vars.get('threat')))        
        turnProgress(game_vars)
        
        draw_field(field)
        showGameStats(game_vars)
        
        showCombatMenu(combat_list)            

        combatOption = checker(combat_list,int)          


#if menuOption is 2 load game will activate
#if game file not found error msg will be placed
elif menuOption == 2:
    
    try:
        shelfFile = shelve.open('saved_game_filename')

        field = shelfFile['mainBoard']

        game_vars = shelfFile['gameStats']

        threat_mtr = shelfFile['meter_threat']

        danger_lvl = shelfFile['dangr_lvl']

        boss_lvl = shelfFile['boss_lvl']

        game_vars.update()

        draw_field(field)

        showGameStats(game_vars)

        showCombatMenu(combat_list)
            
        combatOption = int(input('Your choice? '))
        
        loadgame(field,combatOption,threat_mtr,danger_lvl,boss_lvl,game_vars)

        
    except KeyError:
        print("File not accessible")
        print("Existing game file unavailable")

    except FileNotFoundError:
        print("File not accessible")
        print("Existing game file unavailable")
        
    finally:
        shelfFile.close()
        
#if user decided to quit, it will end the game
else:
    print("But we just started :(")
    sys.exit()

#==========================================================
#                   DESCRIPTION OF GAME
#
# game will start by giving user option to start,load,quit game
# if user selects start new game, field will be drawn
# user has to purchase from a list of towers, archers,wall,wizard
# when user purchases a tower they are prompt to key in the position
# of where the tower is to be placed
# if user entered a incorrect position they are forced to
# re-enter the correct position
# once placed successfully the many events take place
# first based on each lanes, towers will attack first
# and if it does not kill the monsters
# monsters will move and take a next step
# if a monster is killed they are given 1 kill point and rewards
# the user needs to be wary of the threat meter and danger level as well
# the user is given upgrade options for towers such as archer and wall
# the user will need to win the game by first killed 20 monsters
# and killing the final boss which is a skeleton king



   
