from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import threading
import concurrent.futures
import datetime
import time
import pandas as pd

# Basic data
url = 'https://www.glassdoor.com/Job/index.htm'
email = "pphotiadis@gmail.com"
password = "panartas66"
job_title = "software engineer"
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
    "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
# states = ["Alabama"]
#url_list = []
df = pd.DataFrame(columns=['URL', 'Location', 'Company'])


# Define a lock to avoid race conditions when adding URLs to url_list
url_list_lock = threading.Lock()

def initialize_and_login():
    driver = webdriver.Chrome()    
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    
    sign_in_box = driver.find_element(By.ID, "SignInButton")
    sign_in_box.click()
    time.sleep(1)
    email_box = driver.find_element(By.ID, "fishbowlCoRegEmail")
    email_box.send_keys(email)
    email_box.send_keys(Keys.ENTER)
    time.sleep(1)
    password_box = driver.find_element(By.ID, "fishbowlCoRegPassword")
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)
    time.sleep(1)
    
    return driver

def search_remove_pop_up(driver, loc):
    search_box = driver.find_element(By.ID, "searchBar-jobTitle")
    search_box.send_keys(job_title)
    
    location_box = driver.find_element(By.ID, "searchBar-location")
    location_box.send_keys(loc)
    
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # Remove pop-up if it appears
    x_coordinate = 5
    y_coordinate = 5
    script = f"document.elementFromPoint({x_coordinate}, {y_coordinate}).click();"
    driver.execute_script(script)

def expand_listing(driver):
    try:
        left_column = driver.find_element(By.ID, "left-column")
    except:
        return
    for i in range(0, 40):
        new_scroll_top = left_column.get_property("scrollHeight")
        script = f"arguments[0].scrollTop = {new_scroll_top-1000};"
        driver.execute_script(script, left_column)
        try:
            next_button = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button')           
            next_button.click()
            time.sleep(3)
        except:
            pass

        

    
def get_job_url(driver, loc):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    left_column = soup.find(id="left-column")
    all_hrefs = [a['href'] for a in left_column.find_all('a')]
    global df
    with url_list_lock:
        for href in all_hrefs:
            if "/job-listing/" in href:
                temp = "" + href
                job_data = {'URL': temp, 'Location': loc}
                df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)
                #url_list.append(temp)
    driver.quit()

def main(loc):
    driver = initialize_and_login()
    search_remove_pop_up(driver, loc)
    expand_listing(driver)
    get_job_url(driver, loc)


#if __name__ == "__main__":
def run():
    # Limit the number of concurrent threads to 10
    start_time = time.time()

    max_threads = 10

    # Use a thread pool to manage the threads
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # Submit each state to be processed concurrently
        futures = [executor.submit(main, loc) for loc in states]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    # Print the URL list size
    print("URL List Size:", len(df))

    # Save the URLs to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the file name with the timestamp
    file_name = f"job_urls_{timestamp}.csv"
    # Save the URLs to a text file with the timestamp
    #with open(f"url_files\\{file_name}", "w", encoding="utf-8") as file:
    #    for url in url_list:
    #        file.write(url + "\n")
    file_path = f"C:/Users/pphot/Desktop/Thesis/scrapper/glassdoor/url_files/{file_name}"

    df.to_csv(file_path, encoding='utf-8', index=False)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return df
