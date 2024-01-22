from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json
import requests

action = "null"

info_location = ""
#info_salary = ""
info_job_type = ""
info_company = ""
info_year_of_xp = ""
info_education = ""
info_education_level = ""
info_soft_skills = ""
info_hard_skills = ""

class ActionCollectInformation(Action):
    def name(self) -> Text:
        return "action_collect_information"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            global info_location
            #global info_salary
            global info_job_type
            global info_company
            global info_year_of_xp
            global info_education
            global info_education_level
            global info_soft_skills
            global info_hard_skills

            if action == "collect_location":
                location = list(tracker.get_latest_entity_values("location"))
                if not location:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    locations_text = ", ".join(location)
                    info_location = location
                    dispatcher.utter_message(f"Understood! Your location is {locations_text}.")
                    action = "null"

            # elif action == "collect_salary":
            #     salary = next(tracker.get_latest_entity_values("salary"), None)
            #     if salary == None:
            #         dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
            #     else:
            #         dispatcher.utter_message(f"Got it! Your salary is {salary}.")
            #         info_salary = salary
            #         action = "null"

            elif action == "collect_job_type":
                action = "null"
                job_type = next(tracker.get_latest_entity_values("job_type"), None)
                if job_type == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    dispatcher.utter_message(f"Noted! Your job type is {job_type}.")
                    info_job_type = job_type
                    action = "null"

            elif action == "collect_company":
                company = list(tracker.get_latest_entity_values("company"))
                none_company = tracker.latest_message['intent'].get('name')

                if not company and none_company is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    if company:
                        companies_text = ", ".join(company)
                        dispatcher.utter_message(f"Got it! Your company is {companies_text}.")
                        info_company = company
                    else:
                        dispatcher.utter_message(f"Got it! Your do not have a preference")
                        info_company = "None"
                    action = "null"

            elif action == "collect_year_of_xp":
                year_of_xp = next(tracker.get_latest_entity_values("year_of_xp"), None)
                none_year_of_xp = tracker.latest_message['intent'].get('name')

                if year_of_xp is None and none_year_of_xp is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    if year_of_xp is None or year_of_xp == '0':
                        dispatcher.utter_message(f"Sure! You have 0 years of experience")
                        info_year_of_xp = 0
                    else:
                        dispatcher.utter_message(f"Sure! Your years of experience are {year_of_xp}.")
                        info_year_of_xp = year_of_xp
                    action = "null"

            elif action == "collect_education":
                education = list(tracker.get_latest_entity_values("education"))
                education_level = list(tracker.get_latest_entity_values("education_level"))
                none_education = tracker.latest_message['intent'].get('name')
                if education is None and none_education is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    if education or education_level:
                        education_text = ", ".join(education)
                        education_level_text = ", ".join(education_level)
                        dispatcher.utter_message(f"Great! Your education is {education_text} on level {education_level_text}.")
                        info_education = education
                        info_education_level = education_level
                    else:
                        dispatcher.utter_message(f"Sure! looking for a job with no degree")
                        info_education = ""
                        info_education_level = ""
                    action = "null"
    

            elif action == "collect_soft_skills":
                soft_skills = list(tracker.get_latest_entity_values("soft_skills"))
                if not soft_skills:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    soft_skills_text = ", ".join(soft_skills)
                    dispatcher.utter_message(f"Nice! Your soft skills are {soft_skills_text}.")
                    info_soft_skills = soft_skills
                    action = "null"

            elif action == "collect_hard_skills":
                hard_skills = list(tracker.get_latest_entity_values("hard_skills"))
                if not hard_skills:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                else:
                    hard_skills_text = ", ".join(hard_skills)
                    dispatcher.utter_message(f"Got it! Your hard skills are {hard_skills_text}.")
                    info_hard_skills = hard_skills
                    action = "null"

            return []
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSentInformation(Action):
    def name(self) -> Text:
        return "action_sent_information"
    
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global info_location
            # global info_salary
            global info_job_type
            global info_company
            global info_year_of_xp
            global info_education
            global info_education_level
            global info_soft_skills
            global info_hard_skills

            info_hard_skills.extend(info_education)

            job_info = {
                "Location": info_location,                
                "Company": info_company,
                "Employment Type": info_job_type,
                "Years of Exp": info_year_of_xp,
                "Education Level": info_education_level,
                "Education Type": info_education,
                # "Salary": info_salary,
                "Hard Skills": info_hard_skills,
                "Soft Skills": info_soft_skills,
            }

            json_data = json.dumps(job_info, indent=2)
            print(json_data)

            api_url = "http://127.0.0.1:5000/get-results"

            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, data=json_data, headers=headers)

            if response.status_code == 200:
                print("POST request successful.")
                dispatcher.utter_message(f"Your results are {response.text}.")
            else:
                print(f"Error: {response.status_code}")
                print(response.text)

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
        
# class ActionSetSalary(Action):
#     def name(self) -> Text:
#         return "action_set_salary"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         try:
#             global action
#             action = "collect_salary"
#         except Exception as e:
#             print(f"Exception: {str(e)}")
#             return []
        
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