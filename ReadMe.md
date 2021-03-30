Code that creates folders named after addresses of abandoned houses on your Google Drive according to needed folder tree. Also it adds unique id to main folder of each house and create there spreadsheet named the same as folder according to template spreadsheet.

1. Insert your personal data into personal_data.py
2. Prepare *.txt file with adresses of houses
3. Launch code by running "python main.py *.txt"


Frequent troubles:
If your access token "*.pickle" is outdated just delete it and launch code again. You will need to authorise your web-application one more time.

Important: 

Before launching code prepare your web-applications to work with Google Drive API

Official instruction from Google of how to do it: https://developers.google.com/drive/api/v3/about-sdk

If you want to change folder tree go to folder_tree.py and add/remove folders metadate here
