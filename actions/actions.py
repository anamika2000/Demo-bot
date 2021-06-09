# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List,Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from rasa_sdk.forms import FormAction

import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get('https://api.covid19india.org/data.json').json()
        #response = requests.get('https://github.com/ashhadulislam/JSON-Airports-India/blob/master/airports.json').json()
        entities = tracker.latest_message['entities']
        print(entities)
        state = None
        for e in entities:
            if e['entity'] == 'state':
                state = e['value']
        message="Please enter correct state name"
        if state == 'india':
            state = 'Total'
        for data in response['statewise']:
            if data['state'] == state.title():
                print(data)
                message = "Active: "+ data["active"] +"Confirmed: "+ data["confirmed"]+"Recovered: "+ data["recovered"]+"Deaths: "+data["deaths"]+"Last Update Data: "+data["lastupdatedtime"]

        

        print(message)
        dispatcher.utter_message(message)
        return []

    class ContactForm(Action):

        def name(self) -> Text:
            return "user_details_form"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict) -> List[EventType]:

            required_slot = ["name","number","email","standard"]

            for slot_name in required_slot:
                if tracker.slots.get(slot_name) is None:
                    return [SlotSet("required_slot",slot_name)]

            return [SlotSet("required_slot",None)]
    
    class ActionSubmit(Action):
        def name(self) -> Text:
            return "action_submit"
        def run(
            self,
            dispatcher,
            tracker : Tracker,
            domain: "DomainDict",
        ) -> List[Dict[Text,Any]]:
    
            dispatcher.utter_message(template="utter_details_thanks",Name=tracker.get_slot('name'),Mobile_number=tracker.get_slot('number'),Email=tracker.get_slot('email'),Standard=tracker.get_slot('standard'))
            return []



class TripplanForm(FormAction):
    def name(self):
        return "trip_plan_form"

    def required_slots(self,tracker) -> List[Text]:
        return ["travel_date","travel_period","trip_type","adults","child","budget","Email","phno"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "travel_date": [
                self.from_text(),
            ],
            "travel_period": [
                self.from_text(),
            ],
            
            "trip_type": [
                self.from_text(),
            ],
            "adults": [
                self.from_text(),
            ],
            "child": [
                self.from_text(),
            ],
            "budget": [
                self.from_text(),
            ],
            "Email": [
                self.from_text(),
            ],
            "phno": [
                self.from_text(),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]: 
    
        dispatcher.utter_message("Thank you so much for showing your intrest in traveling with us")
        return []