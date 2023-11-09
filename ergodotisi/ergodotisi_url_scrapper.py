from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading
import concurrent.futures
import datetime
import time
import pandas as pd
import re

# Basic data
states = [
    "Famagusta", "Larnaca", "Limassol", "Nicosia", "Paphos"
]
urls = [
    "https://www.ergodotisi.com/en/SearchResults.aspx?q=software%20engineer&t=Αμμόχωστος&s=Πληροφορική",
        "https://www.ergodotisi.com/en/SearchResults.aspx?q=software%20engineer&t=Λάρνακα&s=Πληροφορική",
        "https://www.ergodotisi.com/en/SearchResults.aspx?q=software%20engineer&t=Λεμεσός&s=Πληροφορική",
        "https://www.ergodotisi.com/en/SearchResults.aspx?q=software%20engineer&t=Λευκωσία&s=Πληροφορική",
        "https://www.ergodotisi.com/en/SearchResults.aspx?q=software%20engineer&t=Πάφος&s=Πληροφορική"
        ]

state_url = tuple(zip(states, urls))

df = pd.DataFrame(columns=['ID','URL', 'Location'])


# Define a lock to avoid race conditions when adding URLs to url_list
url_list_lock = threading.Lock()

def initialize(url):
    driver = webdriver.Chrome()    
    driver.get(url)
    time.sleep(3)

    try:
        cookies = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
        cookies.click()
    except:
        pass
    return driver
    

def expand_listing(driver):
    try:
        job_column = driver.find_element(By.ID, "ctl00_ContentplaceholderSubMenu_ASPxCallbackPanel1_ASPxDataView2")
    except:
        return
    for i in range(0, 15):
        new_scroll_top = job_column.get_property("scrollHeight")
        script = f"arguments[0].scrollTop = {new_scroll_top-1000};"
        driver.execute_script(script, job_column)
        try:
            next_button = driver.find_element(By.ID, 'ctl00_ContentplaceholderSubMenu_ASPxCallbackPanel1_ASPxDataView2_EPContainer')           
            next_button.click()
            time.sleep(1)
        except:
            pass   

    
def get_job_url(driver, loc):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_column = soup.find(id="ctl00_ContentplaceholderSubMenu_ASPxCallbackPanel1_ASPxDataView2")
    all_hrefs_set = set([a['href'] for a in job_column.find_all('a')])
    all_hrefs = list(all_hrefs_set)
    global df
    with url_list_lock:
        for href in all_hrefs:
            if "JobDetails/" in href:
                idtemp = re.search(r'\d+', href)
                id = idtemp.group(0)
                
                temp = "https://www.ergodotisi.com/en/" + href

                # Check if job_data already exists in df
                existing_entry = df[df['URL'] == temp]
                if not existing_entry.empty:
                    existing_index = existing_entry.index[0]
                    df.at[existing_index, 'Location'] = df.at[existing_index, 'Location'] + ', ' + loc
                else:
                    job_data = {'ID': id, 'URL': temp, 'Location': loc}
                    df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)

                #df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)
                #url_list.append(temp)
    driver.quit()

def main(loc, url):
    driver = initialize(url)
    expand_listing(driver)
    get_job_url(driver, loc)


#if __name__ == "__main__":
def run():
    # Limit the number of concurrent threads to 10
    start_time = time.time()

    max_threads = 5

    # Use a thread pool to manage the threads
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # Submit each state to be processed concurrently
        futures = [executor.submit(main, state, url) for state, url in state_url]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    # Print the URL list size
    print("URL List Size:", len(df))

    # Save the URLs to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the file name with the timestamp
    file_name = f"job_urls_{timestamp}.csv"

    # Save the URLs to a text file with the timestamp
    df.to_csv(f"ergodotisi\\url_files\\{file_name}", encoding='utf-8', index=False)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return df
