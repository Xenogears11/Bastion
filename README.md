# Bastion
Bastion is a simple test bot for Discord.

## Requirements
- Python 3.5+
- [discord.py](https://github.com/Rapptz/discord.py)

## How to Run
- Create file /config/token/token.txt and place your bot's token there.
- Run bastion.py

## Docker
- Pull image from DockerHub: docker pull xenogears/bastion:latest
- Mount directory with your token.txt into /app/config/token and run container: 
docker run -v yourDir:/app/config/token
