# This files contains your custom actions which can be used to run
# custom Python code.
#
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("from", None), SlotSet("to", None), SlotSet("date", None), SlotSet("meal", None),
               SlotSet("oneway", None), SlotSet("return", None), SlotSet("confirm_onewaytrip", None),
               SlotSet("confirm_returntrip", None)]


class BookingForm(FormAction):

    def name(self) -> Text:
        return "booking_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill in before responding to the user's request"""

        if(tracker.get_slot("oneway")==False):
            return ["from", "to", "date", "meal", "oneway", "return", "confirm_returntrip"]
        else:
            return ["from", "to", "date", "meal", "oneway", "confirm_onewaytrip"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        #return {}
        return {"oneway": [
            self.from_intent(intent="affirm", value=True),
            self.from_intent(intent="deny", value=False)],
            "from": [self.from_entity(entity="from")],
            "to": [self.from_entity(entity="to")],
            "date": [self.from_entity(entity="date")],
            "meal": [self.from_entity(entity="meal")],
            "return": [self.from_entity(entity="return")],
            "confirm_onewaytrip": [
            self.from_intent(intent="affirm", value=True),
            self.from_intent(intent="deny", value=False)],
            "confirm_returntrip": [
            self.from_intent(intent="affirm", value=True),
            self.from_intent(intent="deny", value=False)]}

    def validate_to(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
        """Validate destination value."""

        if value.lower()!=tracker.get_slot('from').lower():
            return {"to": value}
        else:
            dispatcher.utter_message(template="utter_wrong_to")
            # validation failed, set slot to None
            return {"to": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        if(tracker.get_slot('oneway')==True and tracker.get_slot('confirm_onewaytrip')==True):  
            dispatcher.utter_message(template='utter_submit')
            return []
        elif(tracker.get_slot('oneway')==False and tracker.get_slot('confirm_returntrip')==True):
            dispatcher.utter_message(template='utter_submit')
            return []
        else:
            dispatcher.utter_message(text="Let's start over.")
            return [SlotSet("from", None), SlotSet("to", None), SlotSet("date", None), SlotSet("meal", None),
            SlotSet("oneway", None), SlotSet("return", None), SlotSet("confirm_onewaytrip", None), 
            SlotSet("confirm_returntrip", None), FollowupAction("booking_form")]
