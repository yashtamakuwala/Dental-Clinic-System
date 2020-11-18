root project is 'dental' which has directories 
1. chatbot - bot server
2. dentist - dentist server
3. timeslot - timeslot server
4. website - UI of bot

Installing Bot UI
1. cd website
2. npm install
3. npm start

Website will start running at port 3000

Installing Bot Server
1. cd chatbot
2. python3 -m venv ./venv
3. source ./venv/bin/activate
4. pip3 install -r requirements.txt
5. cd chatbot-service
6. python3 __init__.py

Bot server will run on port 5000

To deploy and run dentist server,
1. cd dentist

