# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,EventType
from rasa_sdk.executor import CollectingDispatcher
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



class ActionCityTracker(Action):

    def name(self) -> Text:
        return "action_city_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response_city = requests.get('http://api.travelpayouts.com/data/en/cities.json').json()
        response_airport=requests.get('http://api.travelpayouts.com/data/en/airports.json').json()
        entities = tracker.latest_message['entities']
        print(entities)
        city = None
        for e in entities:
            if e['entity'] == 'city':
                city = e['value']
        message="Please enter correct city name"
        city_code = None
        for data in response_city:
            if data['name'] == city.title():
                city_code = data['code']

                print(data)
                #message = "code: "+ data["code"]
        for x in response_airport:
            if x['city_code'] == city_code:
        
                print(x)
                message="Airport :" + x['name']
                

        print(message)

        dispatcher.utter_message(message)

        return []