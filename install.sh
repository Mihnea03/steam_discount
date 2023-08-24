#! /bin/bash

python3 -m venv env
echo "Creating environment..."
source env/bin/activate
echo "Installing packages..."
python3 -m pip -U -r requirements.txt

echo "Done!"
