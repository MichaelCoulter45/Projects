import random
import keyboard
import sys


game_running = True
hokey_stop = '.'

""" 

Make a simple function call that determines if the user wins or loses.


scissors > paper
paper > rock
rock > scissors

if scissors and paper are chosen then who chose scissors wins
if paper and rock are chosen then who chose paper wins
if rock and scissors are chosen then who chose rock wins. 

if player chose winning weapon, player wins, else loses


if user_input == scissors:
    if bot == paper:
        user wins

if user_input == paper:
    if bot == rock:
        user wins
"""

def stop_game():
    sys.exit()


def bot_weapon():
    weapons = ['rock', 'paper', 'scissors']
    outcome = random.randrange(0,len(weapons))
    
    # outcome = rock, paper, or scissors
    return weapons[outcome]


def battle(user_input, bot):
    if user_input == bot:
        print(f"IT'S A TIE!!")
    else:
        


def results(results):
    if results == 'win':
        print(f"You won! Nice!")
    else:
        print(f"You lost..")






def main():
    global game_running
    keyboard.add_hotkey(hokey_stop, stop_game)
    
    while game_running:
        print(f"Enter Rock, Paper, or Scissors! (Press {hokey_stop} to stop)")
        user_input = str(input()).lower()
        bot = bot_weapon()
        print(f"The bot chose: {bot}!")
        print(f"Which means...")
        
        battle(user_input, bot)




if __name__ == "__main__":
    main()