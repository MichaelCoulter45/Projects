import random
import keyboard
import sys


game_running = True
hokey_stop = '.'

win = 0
lose = 0
tie = 0




def bot_weapon():
    weapons = ['rock', 'paper', 'scissors']
    outcome = random.randrange(0,len(weapons))
    
    # outcome = 1, 2, or 3
    # returns: rock, paper, or scissors
    return weapons[outcome]


def battle(user_input, bot):
    # return win, tie, or lose
    if user_input == bot:
        return 'tie'
    else:
        if user_input == 'rock':
            if bot == 'scissors':
                return 'win'
            else:
                return 'lose'
        elif user_input == 'paper':
            if bot == 'rock':
                return 'win'
            else:
                return 'lose'
        elif user_input == 'scissors':
            if bot == 'paper':
                return 'win'
            else:
                return 'lose'
        else:
            print("Did you type that in wrong?")


def results(results):
    tally(results)
    if results == 'win':
        print(f"You won! Nice!")
    elif results == 'tie':
        print(f"IT'S A TIE!!")
    else:
        print(f"You lost..")
    print(f"""
Your tally counts are now:
    Wins: {win}
    Losses: {lose}
    Ties: {tie}""")


def tally(results):
    global win, lose, tie
    if results == 'win':
        win += 1
    elif results == 'tie':
        tie += 1
    else:
        lose += 1


def stop_game():
    global game_running
    game_running = not game_running
    print("Stopping...")


def main():
    global game_running
    
    while game_running:
        print(f"Enter Rock, Paper, or Scissors! (Enter {hokey_stop} to stop)")
        user_input = str(input()).lower()
        
        if user_input == hokey_stop:
            stop_game()
            break
        
        bot = bot_weapon()
        
        print(f"The bot chose: {bot}!")
        print(f"Which means...")
        
        results(battle(user_input, bot))


if __name__ == "__main__":
    main()



