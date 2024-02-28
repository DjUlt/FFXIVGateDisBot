#!/bin/bash -i
conda deactivate
screen -X -S discordGateBot quit
screen -dmS discordGateBot
screen -r discordGateBot -X stuff "source ~/Repos/FFXIVGateDisBot/start.sh
"
