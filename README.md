Fitness Center Management API




Welcome to the Fitness Center Management API! This application allows you to manage members and their workout sessions using a RESTful API built with Flask and MySQL.

Features
Create, read, update, and delete members.
Create, read, update, and delete workout sessions.
Retrieve all workout sessions for a specific member.
Prerequisites
Python 3.x
Flask
Flask-Marshmallow
MySQL Connector for Python
MySQL Server
Database Setup
Before using the API, you need to create a MySQL database. Ensure that you have MySQL installed and running on your machine.

the SQL  file you need is from the GitHub repository  The file is named is  sql_data.sql 
import into   mysql 


API Endpoints
Members
GET /members: Retrieve all members.
POST /members: Add new members.
PUT /members/<id>: Update an existing member.
DELETE /members/<id>: Delete a member.
Workout Sessions
GET /WorkoutSessions: Retrieve all workout sessions.
POST /WorkoutSessions: Add new workout sessions.
GET /WorkoutSessions/member/<int:member_id>: Retrieve all workout sessions for a specific member.
PUT /WorkoutSessions/<int:session_id>: Update an existing workout session.
DELETE /WorkoutSessions/<int:session_id>: Delete a workout session.
