root project is 'dental' which has directories 
1. chatbot - bot server
2. dentist_server - dentist server
3. timeslot_server - timeslot server
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
5. cd chatbot
6. python3 __init__.py

Bot server will run on port 5000

To deploy and run dentist server, at project directory, with the dot(.) in 2nd step
1. cd dentist_server
2. docker build -t dentist:latest .
3. docker run -p 7000:5000 -t dentist:latest

dentist server will run on port 7000

To deploy and run timeslot server, , with the dot(.) in 2nd step
1. cd timeslot_server
2. docker build -t timeslot:latest .
3. docker run -p 8000:5000 -t timeslot:latest

timeslot server will run on port 8000