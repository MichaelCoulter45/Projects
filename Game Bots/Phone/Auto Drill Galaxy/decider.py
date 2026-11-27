# decider.py
# Decides what the bot does
import phases





""" 
Dictionary of what conditions to do what.
"""
actions = {
    "prestige":phases.prestige()
    
}


##############
def decider(actions):
    """ Decides what to do """