# Installation & Usage On Linux
Make sure you have python installed
First install Ollama with `curl -fsSL https://ollama.com/install.sh | sh`. Then run `pip install -r requirements.txt` to install the python dependencies

Configure the `config.yaml` file with your bot's Discord account, token and the channel ID you want the bot to listen on.
Don't forget to set what model you want to use.

Then, run `ollama pull <model name>`, where \<model name> is what model you set in the config. This will download the model.

Lastly, run `python3 run.py` and the bot should respond when you @ it in the channel you set.

# Installation & Usage On Windows
This has not been tested on Windows, but you might be able to get it to work with WSL
The steps should be the same on WSL as Linux 