import glassdoor_description_scrapper
import glassdoor_url_scrapper
import lightcast_skill_extractor
import time

start_time = time.time()

url_list = glassdoor_url_scrapper.run()
file_name = glassdoor_description_scrapper.run(url_list)
lightcast_skill_extractor.run(file_name)

end_time = time.time()
duration = end_time - start_time
print(f"Program took {duration} seconds to run.")