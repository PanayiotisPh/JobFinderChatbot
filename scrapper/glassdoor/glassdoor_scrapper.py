import glassdoor.glassdoor_description_scrapper as glassdoor_description_scrapper
import glassdoor.glassdoor_url_scrapper as glassdoor_url_scrapper
import glassdoor.lightcast_skill_extractor as lightcast_skill_extractor
import time

def run():
    print("""
    ============================================================================================
    ||                               Glassdoor Scrapper                                       ||
    ||                                                                                        ||
    ||                              Panagiotis Fotiadis                                       ||
    ||                                                                                        ||
    ||                                     v.1.0                                              ||
    ||                                                                                        ||
    ||                                      2023                                              ||
    ============================================================================================
    """)

    start_time = time.time()

    url_list = glassdoor_url_scrapper.run()
    file_name = glassdoor_description_scrapper.run(url_list)
    #file_name = "job_descriptions_20240312004835.csv"
    json_filename = lightcast_skill_extractor.run(file_name)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Program took {duration} seconds to run.")
    print("""
    ============================================================================================
    ||                               Glassdoor Scrapper                                       ||
    ||                                                                                        ||
    ||                            Program run successfully                                    ||
    ============================================================================================
    """)
    return json_filename