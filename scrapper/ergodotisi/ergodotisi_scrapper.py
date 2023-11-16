import ergodotisi.ergodotisi_description_scrapper as ergodotisi_description_scrapper
import ergodotisi.ergodotisi_url_scrapper as ergodotisi_url_scrapper
import ergodotisi.lightcast_skill_extractor as lightcast_skill_extractor
import time

def run():
    start_time = time.time()
    print("""
    ============================================================================================
    ||                              Erdodotisi Scrapper                                       ||
    ||                                                                                        ||
    ||                              Panagiotis Fotiadis                                       ||
    ||                                                                                        ||
    ||                                     v.1.0                                              ||
    ||                                                                                        ||
    ||                                      2023                                              ||
    ============================================================================================
    """)

    url_list = ergodotisi_url_scrapper.run()
    file_name = ergodotisi_description_scrapper.run(url_list)
    json_filename = lightcast_skill_extractor.run(file_name)

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Program took {duration} seconds to run.")
    print("""
    ============================================================================================
    ||                              Erdodotisi Scrapper                                       ||
    ||                                                                                        ||
    ||                            Program run successfully                                    ||
    ============================================================================================
    """)
    return json_filename