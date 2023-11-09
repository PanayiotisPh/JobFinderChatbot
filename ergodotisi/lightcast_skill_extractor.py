import requests
import json
import csv
import time
import datetime

data_list = []

def authentication():
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


def extract_skills(access_token, data_list):
    print("extraction started")
    #global data_map
    url_emis = "https://emsiservices.com/skills/versions/latest/extract"

    for data in data_list:

        job_description = data['Data']
        payload = json.dumps({
            "text": f"""{ job_description }""",
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
        soft_skills = []

        for skill_name, type_name in skill_type_mapping.items():
            if type_name == "Common Skill":
                soft_skills.append(skill_name)
            else:
                hard_skills.append(skill_name)

        data['Hard Skills'] = hard_skills
        data['Soft Skills'] = soft_skills
    print("extraction ended")
    
    

def read_file(filename):
    print("start read file")
    csv_file = f'ergodotisi\\job_descriptions\\{filename}'

    # Open and read the CSV file as a dictionary
    with open(csv_file, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        # Iterate through the rows and store them in the dictionary
        for row in reader:
            job_data = {
                'URL': row['URL'],
                'Location': [location.strip() for location in row['Location'].split(',')],  # Split and strip spaces
                'Company': row['Company'],
                'Employment Type': row['Employment Type'],
                'Data': [row['Data']],  # Initialize the Data as a list
                'Years of Exp': row['Years of Exp'],
                'Education Level': [item.strip() for item in row['Education Level'].split(',')],
            }

            data_list.append(job_data)
            

    print("end read file")

def save_to_json(data_list):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    for data in data_list:
        data.pop('Data')
    json_filename = f"job_data_{timestamp}.json"

    # Save data_map to a JSON file
    with open(f"ergodotisi\\job_data\\{json_filename}", 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

    print(f"Data saved to {json_filename}")
    return json_filename

def extract_data(filename):
    read_file(filename)
    extract_skills(authentication(), data_list)
    file = save_to_json(data_list)
    return file

#if __name__ == "__main__":
def run(filename):
    start_time = time.time()
    json_filename = extract_data(filename)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return json_filename