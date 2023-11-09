import requests
import pprint
import json
import csv
import time
import datetime

data_map = {}

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


def extract_skills(access_token):
    print("extraction started")
    global data_map
    url_emis = "https://emsiservices.com/skills/versions/latest/extract"

    for url, data in data_map.items():
    #    print(f"URL: {url}, DATA: {data}")

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
        data = json.loads(response.text)

        # Create a dictionary to store skill names and their corresponding type names
        skill_type_mapping = {}

        # Extract skill names and type names
        for item in data["data"]:
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

        #print("hard skills\n", hard_skills)
        #print("soft skills\n", soft_skills)
        data_map[url]['Hard Skills'] = hard_skills
        data_map[url]['Soft Skills'] = soft_skills
    #for url, data in data_map.items():
     #   print(f"URL: {url}, Data: {data['Data']}, Hard Skills: {data['Hard Skills']}, Soft Skills: {data['Soft Skills']}")
    print("extraction ended")
    
    

def read_file(filename):
    print("start read file")
    csv_file = f'job_descriptions\\{filename}'

    # Initialize an empty dictionary to store the data
    global data_map

    # Open and read the CSV file as a dictionary
    with open(csv_file, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        # Iterate through the rows and store them in the dictionary
        for row in reader:
            url = row['URL']
            loc = row['Location']
            data = row['Data']

            # Check if the URL is already in the dictionary
            if url not in data_map:
                data_map[url] = {'Location': [] ,'Data': [], 'Hard Skills': [], 'Soft Skills': []}  # Initialize tables (lists) for the URL
            
            data_map[url]['Data'].append(data)  # Add data to the table
            data_map[url]['Location'] = (loc)
    print("end read file")

def save_to_json():
    global data_map

    # Save the URLs to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the file name with the timestamp
    json_filename = f"job_data_{timestamp}.json"

    # Save data_map to a JSON file
    with open(f"job_data\\{json_filename}", 'w') as json_file:
        json.dump(data_map, json_file, indent=4)

    print(f"Data saved to {json_filename}")

def extract_data(filename):
    read_file(filename)
    extract_skills(authentication())
    save_to_json()

#if __name__ == "__main__":
def run(filename):
    start_time = time.time()
    #filename = "job_descriptions_20231018233047.csv"
    extract_data(filename)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")