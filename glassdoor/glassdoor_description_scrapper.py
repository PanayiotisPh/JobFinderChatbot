from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import threading
import datetime
import time
import concurrent.futures

# Create an empty Pandas DataFrame to store the results
urls = []
description = []
dataframe_lock = threading.Lock()


# Function to scrape job data from a URL and return it as a Pandas DataFrame
def scrape_job_data(url, loc, file_name):
    try:
        # Create a Chrome WebDriver with the configured options
        driver = webdriver.Chrome()
        #driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)
        i = 0
        while i < 5:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            element_with_id = soup.find(id="JobDescriptionContainer")
            if element_with_id:
                break
            else:
                i = i + 1

        if element_with_id:
            data = element_with_id.get_text()
        else:
            data = "Element with the specified ID not found."

    finally:
        driver.quit()

    data = data.replace("\n", " ")
    with dataframe_lock:
        job_data = {'URL': url, 'Location': loc, 'Data': data}
        df = pd.DataFrame(columns=['URL', 'Location', 'Data'])
        df = pd.concat([df, pd.DataFrame([job_data])], ignore_index=True)

        # Save the result DataFrame to a CSV file
        df.to_csv(f"job_descriptions\\{file_name}", mode='a', encoding='utf-8', index=False, header=False)


# Read the list of URLs from the file
def run(url_list):
#if __name__ == "__main__":
    start_time = time.time()
    
    # Set the maximum number of threads you want to run concurrently
    max_threads = 20  # Change this number to your desired limit
    
    # Save the URLs to a text file
    # Create the file name with the timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"job_descriptions_{timestamp}.csv"

    headers = ['URL', 'Location', 'Data']
    header_df = pd.DataFrame([headers])
    header_df.to_csv(f"job_descriptions\\{file_name}", index=False, header=False)

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        for _, row in url_list.iterrows():
            executor.submit(scrape_job_data, row['URL'], row['Location'], file_name)


    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    return file_name
