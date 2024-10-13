from fitness_center_database import get_db_connection_new
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

# Member schema
class MemberSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    age = fields.Int(required=True)

    class Meta:
        fields = ("id", "name", "age")

# Instantiate member schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Workout session schema
class WorkoutSessionSchema(ma.Schema):
    session_id = fields.Int(dump_only=True)
    member_id = fields.Int(required=True)  # Changed to Int
    session_date = fields.Date(required=True)  # Use Date type for proper validation
    session_time = fields.String(required=True)  # 24 hours
    activity = fields.String(required=True)

    class Meta:
        fields = ("session_id", "member_id", "session_date", "session_time", "activity")

# Instantiate workout session schemas
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

@app.route('/')
def home():
    return "welcome have fun in sql and flask!"

@app.route('/members', methods=["GET"])
def get_members():
    try:
        conn = get_db_connection_new()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        return members_schema.jsonify(members)
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members', methods=["POST"])
def add_members():
    members_data = request.json  

    # Validate that the incoming data is a list
    if not isinstance(members_data, list):
        return jsonify({"error": "Invalid input format, expected a list of members."}), 400

    conn = get_db_connection_new()
    cursor = conn.cursor()

    # Initialize a list to collect validation errors
    errors = []

    # Iterate through each member data
    for member_data in members_data:
        try:
            # Validate each member's data using the single member schema
            member = member_schema.load(member_data)  
            new_member = (member['name'], member['age'])
            query = "INSERT INTO members (name, age) VALUES (%s, %s)"
            cursor.execute(query, new_member)
        except ValidationError as e:
            # Collect validation errors for individual member data
            errors.append({"member_data": member_data, "errors": e.messages})

    # Commit the transaction
    conn.commit()
    cursor.close()
    conn.close()

    if errors:
        return jsonify({"message": "Some members were not added due to validation errors.", "errors": errors}), 400

    return jsonify({"message": "New members added successfully."}), 201

@app.route('/members/<int:id>', methods=["PUT"])
def update_members(id):
    members_data = member_schema.load(request.json)
    conn = get_db_connection_new()
    cursor = conn.cursor()
    update_members = (members_data['name'], members_data['age'], id)
    query = "UPDATE members SET name = %s, age = %s WHERE id = %s"  
    cursor.execute(query, update_members)
    conn.commit()
    return jsonify({"message": "updated"}), 201

@app.route('/members/<int:id>', methods=["DELETE"])
def delete_member(id):
    conn = get_db_connection_new()
    cursor = conn.cursor()
    
    # Check if the member exists
    cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
    member = cursor.fetchone()

    if not member:
        return jsonify({"message": "member not found"}), 404

    # Proceed with deletion
    cursor.execute("DELETE FROM members WHERE id = %s", (id,))
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return jsonify({"message": "member deleted successfully"}), 200

@app.route('/members/<int:member_id>/workout_sessions', methods=["GET"])
def get_workout_sessions_by_member(member_id):
    try:
        conn = get_db_connection_new()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        
        # Query to retrieve workout sessions for the specified member
        query = "SELECT * FROM workout_sessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        workout_sessions = cursor.fetchall()

        # Check if any workout sessions exist for the member
        if not workout_sessions:
            return jsonify({"message": "No workout sessions found for this member."}), 404

        return workout_sessions_schema.jsonify(workout_sessions)
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/WorkoutSessions', methods=["GET"])
def get_workout_sessions():
    try:
        conn = get_db_connection_new()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workout_sessions"
        cursor.execute(query)
        workout_sessions = cursor.fetchall()
        return workout_sessions_schema.jsonify(workout_sessions)
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/WorkoutSessions', methods=["POST"])
def add_workout_sessions():
    if not isinstance(request.json, list):
        return jsonify({"error": "Invalid input format, expected a list of workout sessions."}), 400
    
    # Validate and load the list of workout session data
    workout_sessions_data = workout_sessions_schema.load(request.json)

    conn = get_db_connection_new()
    cursor = conn.cursor()

    for session in workout_sessions_data:
        new_workout_session = (
            session['member_id'],
            session['session_date'],
            session['session_time'],
            session['activity']
        )
        
        query = "INSERT INTO workout_sessions (member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, new_workout_session)
    
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New Workout Sessions added"}), 201

@app.route('/WorkoutSessions/<int:session_id>', methods=["PUT"])
def update_workout_session(session_id):
    workout_session_data = workout_session_schema.load(request.json)
    conn = get_db_connection_new()
    cursor = conn.cursor()
    updated_workout_session = (
        workout_session_data['member_id'],
        workout_session_data['session_date'],
        workout_session_data['session_time'],
        workout_session_data['activity'],
        session_id
    )
    query = "UPDATE workout_sessions SET member_id = %s, session_date = %s, session_time = %s, activity = %s WHERE session_id = %s"
    cursor.execute(query, updated_workout_session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Workout session updated"}), 200

@app.route('/WorkoutSessions/<int:session_id>', methods=["DELETE"])
def delete_workout_session(session_id):
    conn = get_db_connection_new()
    cursor = conn.cursor()

    # Check if the workout session exists
    cursor.execute("SELECT * FROM workout_sessions WHERE session_id = %s", (session_id,))
    workout_session = cursor.fetchone()

    if not workout_session:
        return jsonify({"message": "Workout session not found"}), 404

    # Proceed with deletion
    cursor.execute("DELETE FROM workout_sessions WHERE session_id = %s", (session_id,))
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return jsonify({"message": "Workout session deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True) 












