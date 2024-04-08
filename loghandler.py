import time, os
def log(prompt, user, response, channelID):
    current_time_seconds = time.time()

    # Convert the current time to a struct_time object
    current_time_struct = time.localtime(current_time_seconds)

    # Extract the year, month, and day from the struct_time object
    year = current_time_struct.tm_year
    month = current_time_struct.tm_mon
    day = current_time_struct.tm_mday
    hour = current_time_struct.tm_hour
    min = current_time_struct.tm_min
    sec = current_time_struct.tm_sec

    file_path = f"./logs/ID.{channelID}/" 
    file_name = f"{user}_{year}-{month}-{day}_{hour}-{min}-{sec}.log"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(file_path+file_name, "w") as file:
        file.write("Bot responded to:\n" + prompt )
        file.write("\n\nWith: \n")
        file.write(response)