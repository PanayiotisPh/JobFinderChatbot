from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

#TODO
# main problem is that values can change in any point of the conv even if chatbot ask something else
# getting action name does not work
# list is not part of entities but is a part of slots so the below code must change to affect slots
# how to check when to affect slots is the problem
# possible solution but not desirable for later is the use of public variables
# difficult option
# CHANGE YOUR WHOLE APPROACH

class ActionCollectInformation(Action):
    def name(self) -> Text:
        return "action_collect_information"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            intent = tracker.latest_action_name
            print(intent)
            # Check the intent and collect information for corresponding slots
            if intent == "collect_location":
                location = next(tracker.get_latest_entity_values("location"), None)
                # Perform actions with location information (e.g., store in a database)
                dispatcher.utter_message(f"Understood! Your location is {location}.")
            elif intent == "collect_salary":
                salary = next(tracker.get_latest_entity_values("salary"), None)
                # Perform actions with salary information (e.g., store in a database)
                dispatcher.utter_message(f"Got it! Your salary is {salary}.")
            elif intent == "collect_job_type":
                job_type = next(tracker.get_latest_entity_values("job_type"), None)
                # Perform actions with job_type information (e.g., store in a database)
                dispatcher.utter_message(f"Noted! Your job type is {job_type}.")
            elif intent == "collect_company":
                company = next(tracker.get_latest_entity_values("company"), None)
                # Perform actions with company information (e.g., store in a database)
                dispatcher.utter_message(f"Got it! Your company is {company}.")
            elif intent == "collect_year_of_xp":
                year_of_xp = next(tracker.get_latest_entity_values("year_of_xp"), None)
                # Perform actions with year_of_xp information (e.g., store in a database)
                dispatcher.utter_message(f"Sure! Your years of experience are {year_of_xp}.")
            elif intent == "collect_education":
                education = next(tracker.get_latest_entity_values("education"), None)
                # Perform actions with education information (e.g., store in a database)
                dispatcher.utter_message(f"Great! Your education level is {education}.")
            elif intent == "collect_soft_skills":
                soft_skills = next(tracker.get_latest_entity_values("soft_skills"), None)
                # Perform actions with soft_skills information (e.g., store in a database)
                dispatcher.utter_message(f"Nice! Your soft skills are {soft_skills}.")
            elif intent == "collect_hard_skills":
                hard_skills = next(tracker.get_latest_entity_values("hard_skills"), None)
                # Perform actions with hard_skills information (e.g., store in a database)
                dispatcher.utter_message(f"Got it! Your hard skills are {hard_skills}.")

            return []
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
