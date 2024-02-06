from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import threading
import datetime
import time
import concurrent.futures
import math
import re

# Create an empty Pandas DataFrame to store the results
urls = []
description = []
dataframe_lock = threading.Lock()

# Function to scrape job data from a URL and return it as a Pandas DataFrame
#TODO fix min
def years_of_experience_finder(data):
    exp = re.search(r'(\d+(?:-\d+)?\+?)\s*(years?)', data)

    if exp:
        year_of_exp = f'"{exp.group(1)}"'

        result = math.inf
        nums = list(map(int, re.findall('[0-9]+', year_of_exp)))
        for i in nums:
            year_of_exp = min(result, i)
        return year_of_exp
    else:
        return "not given"

def employment_type_finder(data):
    emptype = {
        "Fulltime": ["Full Time", "Fulltime", "full-time", "full time"],
        "Parttime": ["Part Time", "Parttime", "part-time", "part time"],
        "Flexible": ["Flexible", "flexible"],
        "Hybrid": ["Hybrid", "hybrid"],
        "Permanent": ["Permanent", "permanent"],
        "Temporary": ["Temporary", "temporary"],
        "Remote": ["Remote", "remote"]
    }
    #emptype = ['Full Time', 'Part Time', 'Flexible', 'Hybrid', 'Permanent', 'Temporary', 'Remote']
    emptype_found = []
    data_lower = data.lower()

    for key, synonyms in emptype.items():
        for synonym in synonyms:
            # Check if synonym is in data
            if synonym.lower() in data_lower:
                emptype_found.append(key)
                break  # Break to avoid adding the same employment type more than once

    return emptype_found
    
def education_level_finder(data):
    levels = ['BSc', 'BA', 'MSc', 'MCA', 'MA', 'PHD', 'Ph.D.', 'DCs', 'Master','Doctor' ,'BCA', 'B Tech', "Bachelor's degree"]
    levels_found = []
    for level in levels:
        if level in data:
            levels_found.append(level)
    return levels_found


# Function to scrape job data from a URL and return it as a Pandas DataFrame
def scrape_job_data(url, loc, file_name):
    try:
        # Create a Chrome WebDriver with the configured options
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)

        i = 0
        while i < 5:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            element_with_id = soup.find(class_ = "JobDetails_jobDescription__6VeBn JobDetails_blurDescription__fRQYh")
            company_with_id = soup.find(class_ = 'EmployerProfile_employerName__Xemli')
            if element_with_id:
                break
            else:
                i = i + 1

        if element_with_id:
            data = element_with_id.get_text()
        else:
            data = "Element with the specified ID not found."

        if company_with_id:
            temp = company_with_id.get_text()
            company = re.sub(r'\d.*$', '', temp)
        else:
            company = "Element with the specified ID not found."
        

    finally:
        driver.quit()

    data = data.replace("\n", " ")
    employment_type = employment_type_finder(data)
    year_of_exp = years_of_experience_finder(data)
    education_level = education_level_finder(data)

    with dataframe_lock:
        job_data = {'URL': url, 'Location': loc,
                     'Company': company, 'Employment Type': ', '.join(employment_type),
                       'Years of Exp': year_of_exp, 'Education Level': ', '.join(education_level),
                         'Data': data}
        df = pd.DataFrame(columns=['URL', 'Location',
                                    'Company','Employment Type',
                                    'Years of Exp', 'Education Level',
                                      'Data'])
        df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)

        dir = f"C:/Users/pphot/Desktop/Thesis/scrapper/glassdoor/job_descriptions/{file_name}"
        # Save the result DataFrame to a CSV file
        df.to_csv(dir, mode='a', encoding='utf-8', index=False, header=False)


# Read the list of URLs from the file
def run(url_list):
#if __name__ == "__main__":
    start_time = time.time()
    # Set the maximum number of threads you want to run concurrently
    max_threads = 10  # Change this number to your desired limit
    
    # Save the URLs to a text file
    # Create the file name with the timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"job_descriptions_{timestamp}.csv"
    dir = f"C:/Users/pphot/Desktop/Thesis/scrapper/glassdoor/job_descriptions/{file_name}"
    headers = ['URL', 'Location', 'Company', 'Employment Type', 'Years of Exp','Education Level' , 'Data']
    header_df = pd.DataFrame([headers])

    header_df.to_csv(dir, index=False, header=False)

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        for _, row in url_list.iterrows():
            executor.submit(scrape_job_data,row['URL'], row['Location'], file_name)


    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return file_name
