from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

action = "null"

class ActionCollectInformation(Action):
    def name(self) -> Text:
        return "action_collect_information"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
           
            if action == "collect_location":
                location = next(tracker.get_latest_entity_values("location"), None)
                if location == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Understood! Your location is {location}.")
                    action = "null"

            elif action == "collect_salary":
                salary = next(tracker.get_latest_entity_values("salary"), None)
                if salary == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Got it! Your salary is {salary}.")
                    action = "null"

            elif action == "collect_job_type":
                action = "null"
                job_type = next(tracker.get_latest_entity_values("job_type"), None)
                if job_type == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Noted! Your job type is {job_type}.")
                    action = "null"

            elif action == "collect_company":
                company = next(tracker.get_latest_entity_values("company"), None)
                if company == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Got it! Your company is {company}.")
                    action = "null"

            elif action == "collect_year_of_xp":
                year_of_xp = next(tracker.get_latest_entity_values("year_of_xp"), None)
                if year_of_xp == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Sure! Your years of experience are {year_of_xp}.")
                    action = "null"

            elif action == "collect_education":
                education = next(tracker.get_latest_entity_values("education"), None)
                if education == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Great! Your education level is {education}.")
                    action = "null"

            elif action == "collect_soft_skills":
                soft_skills = next(tracker.get_latest_entity_values("soft_skills"), None)
                if soft_skills == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Nice! Your soft skills are {soft_skills}.")
                    action = "null"

            elif action == "collect_hard_skills":
                hard_skills = next(tracker.get_latest_entity_values("hard_skills"), None)
                if hard_skills == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Got it! Your hard skills are {hard_skills}.")
                    action = "null"

            return []
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        

class ActionSetLocation(Action):
    def name(self) -> Text:
        return "action_set_location"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_location"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetSalary(Action):
    def name(self) -> Text:
        return "action_set_salary"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_salary"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetJobType(Action):
    def name(self) -> Text:
        return "action_set_job_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_job_type"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []

class ActionSetCompany(Action):
    def name(self) -> Text:
        return "action_set_company"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_company"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetYearOfXp(Action):
    def name(self) -> Text:
        return "action_set_year_of_xp"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_year_of_xp"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetEducation(Action):
    def name(self) -> Text:
        return "action_set_education"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_education"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []

class ActionSetSoftSkills(Action):
    def name(self) -> Text:
        return "action_set_soft_skills"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_soft_skills"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetHardSkills(Action):
    def name(self) -> Text:
        return "action_set_hard_skills"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_hard_skills"
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []