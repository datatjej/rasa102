# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random

JOKES = [("Doctor", "xD xD xD"),
        ("Europe", "No I'm not!! >:("),
        ("Thermos", "Thermos be a better way to get through to you."),
        ("Water", "Water you doing? Open up the door already!")]
 
class ActionJokeSetup(Action):

    def name(self) -> Text:
        return "action_joke_setup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if(tracker.get_slot("used_jokes") is None):
            used_jokes = []
        else:
            used_jokes = tracker.get_slot("used_jokes")
        
        if(len(used_jokes)==len(JOKES)):
            dispatcher.utter_message(text="Sorry, no more jokes.")
            return [SlotSet("jix", None), SlotSet("used_jokes", None)]
        else:
            while True:
                jix = random.choice(range(len(JOKES)))
                if(jix not in used_jokes): 
                    used_jokes.append(jix)    
                    dispatcher.utter_message(text=JOKES[jix][0])
                    return [SlotSet("jix", jix), SlotSet("used_jokes", used_jokes)]

class ActionJokePunchline(Action):

    def name(self) -> Text:
        return "action_joke_punchline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jix = int(tracker.get_slot("jix"))
        joke = JOKES[jix]
        dispatcher.utter_message(text=joke[1])

        return []
