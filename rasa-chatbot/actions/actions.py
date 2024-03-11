from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    FollowupAction,
    EventType,
)

import json
import requests

USER_INTENT_OUT_OF_SCOPE = "out_of_scope"

class ActionCollectInformation(Action):

    def authentication(self):
        url = "https://auth.emsicloud.com/connect/token"

        payload = "client_id=qn2hk51fh4z9vzcj&client_secret=8YkRlh2e&grant_type=client_credentials&scope=emsi_open"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            return access_token
        else:
            print("Error:", response.status_code, response.text)

    def extract_soft_skills(self,access_token, data):
        #global data_map
        url_emis = "https://emsiservices.com/skills/versions/latest/extract"

        payload = json.dumps({
            "text": f"""{ data }""",
            "confidenceThreshold": 0.6
        })
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': "application/json"
            }
        response = requests.request("POST", url_emis, data=payload, headers=headers)
        # Parse the JSON data
        emis_data = json.loads(response.text)
        # Create a dictionary to store skill names and their corresponding type names
        skill_type_mapping = {}
        # Extract skill names and type names
        for item in emis_data["data"]:
            if "skill" in item:
                skill = item["skill"]
                if "name" in skill:
                    skill_name = skill["name"]
                    if "type" in skill:
                        type_name = skill["type"]["name"]
                        skill_type_mapping[skill_name] = type_name
        soft_skills = []
        for skill_name, type_name in skill_type_mapping.items():
            if type_name == "Common Skill":
                soft_skills.append(skill_name)
                
        return soft_skills
    
    def extract_hard_skills(self, access_token, data):
        #global data_map
        url_emis = "https://emsiservices.com/skills/versions/latest/extract"

        payload = json.dumps({
            "text": f"""{ data }""",
            "confidenceThreshold": 0.6
        })
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': "application/json"
            }
        response = requests.request("POST", url_emis, data=payload, headers=headers)

        # Parse the JSON data
        emis_data = json.loads(response.text)

        # Create a dictionary to store skill names and their corresponding type names
        skill_type_mapping = {}

        # Extract skill names and type names
        for item in emis_data["data"]:
            if "skill" in item:
                skill = item["skill"]
                if "name" in skill:
                    skill_name = skill["name"]
                    if "type" in skill:
                        type_name = skill["type"]["name"]
                        skill_type_mapping[skill_name] = type_name

        hard_skills = []
        for skill_name, type_name in skill_type_mapping.items():
            if type_name != "Common Skill":
                hard_skills.append(skill_name)

        return hard_skills

    def get_github_user_languages(self, username):
        repos_url = f'https://api.github.com/users/{username}/repos'
        languages = set()

        try:
            # Fetch the list of repositories for the given user
            repos_response = requests.get(repos_url)
            repos_response.raise_for_status()  # Raise an exception for HTTP errors
            repos = repos_response.json()

            for repo in repos:
                # Fetch the languages for each repository
                languages_url = repo['languages_url']
                languages_response = requests.get(languages_url)
                repo_languages = languages_response.json()

                # Add the languages to the set
                languages.update(repo_languages.keys())
        
        except requests.RequestException as e:
            print(f'Error fetching data from GitHub API: {e}')

        return list(languages)

    def name(self) -> Text:
        return "action_collect_information"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            url = f"http://localhost:5000/get_action/{tracker.sender_id}"
            response = requests.request("GET", url)
            action = response.text
            action = action.replace('"', '')
            action = action.replace('\n', '')

            if action == "collect_location":
                location = list(tracker.get_latest_entity_values("location"))
                if not location:
                    print("No location found")
                    try:
                        dispatcher.utter_message(text = "Sorry, I didn't get that. Can you rephrase it?")
                    except Exception as e:
                        print(f"Exception: {str(e)}")
                    return [FollowupAction("utter_ask_location")]
                else:
                    location = list(dict.fromkeys([loc.capitalize() for loc in location]))
                    payload = {"location": location}
                    url = f"http://localhost:5000/info_location/{tracker.sender_id}"
                    requests.request("POST", url, json=payload)
                    locations_text = ", ".join(location)
                    dispatcher.utter_message(f"Understood! Your location is {locations_text}.")
                    return [FollowupAction("action_set_job_type")]

            # elif action == "collect_salary":
            #     salary = next(tracker.get_latest_entity_values("salary"), None)
            #     if salary == None:
            #         dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
            #     else:
            #         dispatcher.utter_message(f"Got it! Your salary is {salary}.")
            #         info_salary = salary
            #         action = "null"

            elif action == "collect_job_type":
                job_type = next(tracker.get_latest_entity_values("job_type"), None)
                if job_type == None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_job_type")]
                else:
                    payload = {"job_type": job_type}
                    requests.request("POST", f"http://localhost:5000/info_job_type/{tracker.sender_id}", json=payload)
                    dispatcher.utter_message(f"Noted! Your job type is {job_type}.")
                    return [FollowupAction("action_set_company")]

            elif action == "collect_company":
                company = list(tracker.get_latest_entity_values("company"))
                none_company = tracker.latest_message['intent'].get('name')

                if not company and none_company is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_company")]
                else:
                    if company:
                        company = list(dict.fromkeys([com.capitalize() for com in company]))
                        companies_text = ", ".join(company)
                        dispatcher.utter_message(f"Got it! Your company is {companies_text}.")
                        payload = {"company": company}
                        requests.request("POST", f"http://localhost:5000/info_company/{tracker.sender_id}", json=payload)
                    else:
                        dispatcher.utter_message(f"Got it! Your do not have a preference")
                        payload = {"company": "None"}
                        requests.request("POST", f"http://localhost:5000/info_company/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_set_year_of_xp")]

            elif action == "collect_year_of_xp":
                year_of_xp = next(tracker.get_latest_entity_values("year_of_xp"), None)
                none_year_of_xp = tracker.latest_message['intent'].get('name')

                if year_of_xp is None and none_year_of_xp is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_year_of_xp")]
                else:
                    if year_of_xp is None or year_of_xp == '0':
                        dispatcher.utter_message(f"Sure! You have 0 years of experience")
                        payload = {"years_of_exp": 0}
                        requests.request("POST", f"http://localhost:5000/info_years_of_exp/{tracker.sender_id}", json=payload)
                    else:
                        dispatcher.utter_message(f"Sure! Your years of experience are {year_of_xp}.")
                        payload = {"years_of_exp": year_of_xp}
                        requests.request("POST", f"http://localhost:5000/info_years_of_exp/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_set_education")]

            elif action == "collect_education":
                education = list(tracker.get_latest_entity_values("education"))
                education_level = list(tracker.get_latest_entity_values("education_level"))
                none_education = tracker.latest_message['intent'].get('name')
                if education is None and none_education is None:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_education")]
                else:
                    if education or education_level:
                        education = list(dict.fromkeys([edu.capitalize() for edu in education]))
                        education_level = list(dict.fromkeys([edu.capitalize() for edu in education_level]))
                        education_text = ", ".join(education)
                        education_level_text = ", ".join(education_level)
                        dispatcher.utter_message(f"Great! Your education is {education_text} on level {education_level_text}.")
                        payload = {"education_type": education, "education_level": education_level}
                        requests.request("POST", f"http://localhost:5000/info_education/{tracker.sender_id}", json=payload)
                    else:
                        dispatcher.utter_message(f"Sure! looking for a job with no degree")
                        payload = {"education": "", "education_level": ""}
                        requests.request("POST", f"http://localhost:5000/info_education/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_set_soft_skills")]
    
            elif action == "collect_soft_skills":
                #soft_skills = list(tracker.get_latest_entity_values("soft_skills"))
                user_message = tracker.latest_message.get('text')
                soft_skills = []
                if user_message:
                    try:
                        soft_skills = self.extract_soft_skills(self.authentication(), user_message)
                    except Exception as e:  # Generic exception handling for demonstration
                        print(f"Error extracting soft skills: {e}")
                else:
                    print("No message found in the tracker.")

                if not soft_skills:
                    dispatcher.utter_message("Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_soft_skills")]
                else:
                    soft_skills_text = ", ".join(soft_skills)
                    dispatcher.utter_message(f"Nice! Your soft skills are {soft_skills_text}.")
                    payload = {"soft_skills": soft_skills}
                    requests.request("POST", f"http://localhost:5000/info_soft_skills/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_set_hard_skills")]

            elif action == "collect_hard_skills":
                #hard_skills = list(tracker.get_latest_entity_values("hard_skills"))
                user_message = tracker.latest_message.get('text')
                hard_skills = []
                if user_message:
                    hard_skills = self.extract_hard_skills(self.authentication(), user_message)
                else:
                    print("No message found in the tracker.")

                if not hard_skills:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_hard_skills")]
                else:
                    hard_skills_text = ", ".join(hard_skills)
                    dispatcher.utter_message(f"Got it! Your hard skills are {hard_skills_text}.")
                    payload = {"hard_skills": hard_skills}
                    requests.request("POST", f"http://localhost:5000/info_hard_skills/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_set_github_username")]
                
            elif action == "collect_github_username":
                github_username = list(tracker.get_latest_entity_values("github_username"))
                no_username = tracker.latest_message['intent'].get('name')

                if not github_username and not no_username:
                    dispatcher.utter_message(f"Sorry, I didn't get that. Can you rephrase it?")
                    return [FollowupAction("utter_ask_github_username")]
                elif github_username:
                    language = self.get_github_user_languages(github_username[0])
                    language_text = ", ".join(language)
                    dispatcher.utter_message(f"Understood! Your github username is {github_username[0]} and the detected languages are {language_text}.")
                    payload = {"languages": language}
                    requests.request("POST", f"http://localhost:5000/info_github_username/{tracker.sender_id}", json=payload)
                    return [FollowupAction("action_sent_information")]
                else:
                    dispatcher.utter_message(f"Sure! You do not have a github account.")
                    return [FollowupAction("action_sent_information")]


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
            response = requests.request("GET", f"http://localhost:5000/get_rasa/{tracker.sender_id}")
            if response.status_code == 200:
                data = response.json()
                job_info = {
                    "Location": data["info_location"],
                    "Company": data["info_company"],
                    "Employment Type": data["info_job_type"],
                    "Years of Exp": data["info_years_of_exp"],
                    "Education Level": data["info_education_level"],
                    "Education Type": data["info_education_type"],
                    "Hard Skills": data["info_hard_skills"] + data["info_education_type"],
                    "Soft Skills": data["info_soft_skills"],
                }

            json_data = json.dumps(job_info, indent=2)
            print(json_data)

            api_url = "http://127.0.0.1:5000/get-results"

            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, json=job_info, headers=headers)

            if response.status_code == 200:
                print("POST request successful.")
                dispatcher.utter_message(f"Your results are {response.text}.")
                requests.request("POST", f"http://localhost:5000/reset_rasa/{tracker.sender_id}")
            else:
                requests.request("POST", f"http://localhost:5000/reset_rasa/{tracker.sender_id}")
                print(f"Error: {response.status_code}")
                print(response.text)


            dispatcher.utter_message("To start over, type 'hi'.")

            return [FollowupAction("action_restart")]   
             
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_location")
            return [FollowupAction("utter_ask_location")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_job_type")
            return [FollowupAction("utter_ask_job_type")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_company")
            return [FollowupAction("utter_ask_company")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_year_of_xp")
            return [FollowupAction("utter_ask_year_of_xp")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_education")
            return [FollowupAction("utter_ask_education")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_soft_skills")
            return [FollowupAction("utter_ask_soft_skills")]
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
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_hard_skills")
            return [FollowupAction("utter_ask_hard_skills")]
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []
        
class ActionSetGithubUsername(Action):
    def name(self) -> Text:
        return "action_set_github_username"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            global action
            action = "collect_github_username"
            requests.request("POST", f"http://localhost:5000/action/{tracker.sender_id}/collect_github_username")
            return [FollowupAction("utter_ask_github_username")]
        except Exception as e:
            print(f"Exception: {str(e)}")
            return []