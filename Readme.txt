For setting up your database please make sure you have
Flask and MongoDB install in your system and mongo is 
an environment variable

To set up DB:
1. Go to command Prompt
2. Type mongo (as it is environment variable)
3. create a DB called medicords by typing "use medicords"
4. Create collections by typing these in the cmd prompt:
4.1. db.createCollection("appointment")
4.2. db.createCollection("disease_data")
4.3. db.createCollection("doctors_details")
4.4. db.createCollection("medical_history")
4.5. db.createCollection("patient_details")
4.6. db.createCollection("posts")
4.7. db.createCollection("treats")

To run code on localhost:
1. Open command prompt
2. change directory to your project folder
3. type "python app.py"
4. open your browser
5. type localhost:8000 to see your hosted project