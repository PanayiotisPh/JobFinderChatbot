from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import threading
import datetime
import time
import concurrent.futures
from selenium.webdriver.common.by import By
import re
import math

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
    emptype = re.search(r'EMPLOYMENT TYPE: (\w+)', data)

    if emptype:
        return emptype.group(1)
    else:
        return "not given"
    
def education_level_finder(data):
    levels = ['BSc', 'BA', 'MSc', 'MCA', 'BCA', 'B Tech']
    levels_found = []
    for level in levels:
        if level in data:
            levels_found.append(level)
    return levels_found
    
def scrape_job_data(job_id, url, loc, file_name):
    try:
        # Create a Chrome WebDriver with the configured options
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1.5)
        #cookie accept
        try:
            cookies = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
            cookies.click()
        except:
            pass

        i = 0
        while i < 5:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            element_with_id = soup.find(id ="ctl00_ContentplaceholderSubMenu_PanelLiveContent")
            company_with_id = soup.find(id = "ctl00_ContentplaceholderSubMenu_CompanyNamelabel")
            if element_with_id:
                break
            else:
                i = i + 1

        if element_with_id:
            data = element_with_id.get_text()
        else:
            data = "Element with the specified ID not found."

        if company_with_id:
            company = company_with_id.get_text()
        else:
            company = "Element with the specified ID not found."
        

    finally:
        driver.quit()

    data = data.replace("\n", " ")
    
    employment_type = employment_type_finder(data)
    year_of_exp = years_of_experience_finder(data)
    education_level = education_level_finder(data)

    with dataframe_lock:
        job_data = {'ID': job_id, 'URL': url, 'Location': loc,
                     'Company': company, 'Employment Type': employment_type,
                       'Years of Exp': year_of_exp, 'Education Level': ', '.join(education_level),
                         'Data': data}
        df = pd.DataFrame(columns=['ID', 'URL', 'Location',
                                    'Company','Employment Type',
                                    'Years of Exp', 'Education Level',
                                      'Data'])
        df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)

        # Save the result DataFrame to a CSV file
        df.to_csv(f"scrapper\\ergodotisi\\job_descriptions\\{file_name}", mode='a', encoding='utf-8', index=False, header=False)


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

    headers = ['ID','URL', 'Location', 'Company', 'Employment Type', 'Years of Exp','Education Level' , 'Data']
    header_df = pd.DataFrame([headers])
    header_df.to_csv(f"scrapper\\ergodotisi\\job_descriptions\\{file_name}", index=False, header=False)

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        for _, row in url_list.iterrows():
            executor.submit(scrape_job_data,row['ID'], row['URL'], row['Location'], file_name)


    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return file_name
