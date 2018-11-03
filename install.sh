echo "Enter your todoist API token:"
read -r
touch ~/.todoistApiToken
echo $REPLY > ~/.todoistApiToken
touch ~/.todoistCache
touch ~/.todoist.json
sudo cp ./src/* /usr/bin/