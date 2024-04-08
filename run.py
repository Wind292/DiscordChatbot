import requests
import time
import json
import yaml
import sendmessage
import io
import ollama
import loghandler

# Pull config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# discord
channel_id = config["discord"]["channel_id"]
user_id = config["discord"]["user_id"]
model = config["ollama"]["model"]
token = config["discord"]["user_token"]
# settings
do_logging = config["settings"]["log"]
do_replace_at = config["settings"]["replace_@"]
# ollama
bot_name = config["ollama"]["name"]

# Returns the latest message
def ret_messages(channel_id):
    headers = {
        "authorization" : config["discord"]["authorization"]
    }
    messages_obj = requests.get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers=headers)
    return json.loads(messages_obj.text)[0]

print("Discord Chatbot started!")

before = ret_messages(channel_id)
while True:
    try:
        time.sleep(.1)
        after = ret_messages(channel_id)

        # If there was a new message sent
        if before != after:
            message = after["content"]

            if f"<@{user_id}>" in message: # Check if the message is @ the bot
                if do_replace_at: message.replace(f"<@{user_id}>", bot_name)
                else: message.replace(f"<@{user_id}>", "")

                # log
                print("Generating response to : " + message)

                # Prevent empty message Error
                if message == "": message = " " 

                # Generate response from LLM    
                image_prompt_list = []
                if config["ollama"]["vision"]: # Check for visoin in config to be enabled
                    for attachment in after["attachments"]:
                        if attachment["content_type"].startswith("image"):
                            response = requests.get(attachment["url"])
                            file_like_obj = io.BytesIO(response.content)
                            image_prompt_list.append(file_like_obj)

                sender = after["author"]["global_name"]
                instructions = config["ollama"]["instructions"]
                ai_response = ollama.chat(model=model, messages= [
                    {
                        "role": "system",
                        "content": f"Your name is {bot_name}. You are speaking to '{sender}'. Keep your message under 2000 characters. {instructions}"
                    },
                    {
                        "role": "user",
                        "content": message,
                        "images":  image_prompt_list
                    }
                ])
                message_response = ai_response['message']['content'];            
                if do_logging: loghandler.log(message, sender, message_response, channel_id)
                
                print("Generated:")
                print(message_response)

                sendmessage.run(message_response)

            before = after
    except Exception as e:
        print(f"Error: {e}")
        continue
