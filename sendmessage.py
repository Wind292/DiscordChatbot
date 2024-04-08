import http.client
import json
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

channel_id = config["discord"]["channel_id"]
token = config["discord"]["user_token"]

header_data = { 
    "Content-Type": "application/json", 
    "User-Agent": "DiscordBot", 
    "Authorization": token  
} 

def __get_connection(): 
    return http.client.HTTPSConnection("discord.com", 443) 

def __send_message(conn, channel_id, message_data): 
    try: 
        conn.request("POST", f"/api/v10/channels/{channel_id}/messages", message_data, header_data) 
        resp = conn.getresponse() 
         
        if 199 < resp.status < 300: 
            print("Message Sent.") 
        else: 
            print(f"HTTP {resp.status}: {resp.reason}")
    except: 
        print("Error.") 

def run(message): 
    message_data = { 
        "content": message, 
        "tts": False
    } 

    __send_message(__get_connection(), channel_id, json.dumps(message_data)) 


