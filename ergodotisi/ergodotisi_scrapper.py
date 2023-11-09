import ergodotisi_description_scrapper
import ergodotisi_url_scrapper
import lightcast_skill_extractor
import mongodb_data_manager
import time

start_time = time.time()

url_list = ergodotisi_url_scrapper.run()
file_name = ergodotisi_description_scrapper.run(url_list)
json_filename = lightcast_skill_extractor.run(file_name)
mongodb_data_manager.upload_data(json_filename)

end_time = time.time()
duration = end_time - start_time
print(f"Program took {duration} seconds to run.")