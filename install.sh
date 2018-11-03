echo "Enter your todoist API token:"
read -r
token=$REPLY
file="$(cat ./src/todo)"
file="${file/YOURTOKEN/$token}"
echo "Creating the executable."
sudo echo "$file" > todo
sudo chmod +x todo
sudo cp todo /usr/bin/
rm todo