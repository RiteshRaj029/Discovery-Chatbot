from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Define the questions as per the journey map
questions = [
    {"id": 1.5, "question": "What is your first name?", "type": "text", "key": "name"},
    {"id": 3, "question": "What is your Business Unit or Department name?", "type": "text", "key": "department"},
    {"id": 4, "question": "Do you work for a specific area within your business unit/department?", "type": "boolean", "key": "specificArea"},
    {"id": 5, "question": "What is the name of the area?", "depends_on": 3, "expected_answer": "yes", "key": "areaName"},
    {"id": 7, "question": "What is the name of the process?", "type": "text", "key": "process"},
    {"id": 8, "question": "How often do you complete the process?", "options": ["Daily", "Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Yearly"], "multiple": True, "key": "processDuration"},
    {"id": 9, "question": "What is the volume per selected frequency?", "type": "text", "key": "frequency"},
    {"id": 10, "question": "What is the goal for automation?", "options": ["Cost", "Quality", "Productivity", "Employee Satisfaction", "Customer Satisfaction/Experience", "Operational Efficiency", "Accuracy and Compliance", "Scalability", "Innovation"], "multiple": True, "key": "goal"},
    {"id": 11, "question": "Is the process documented?", "type": "boolean", "key": "documented"},
    {"id": 12, "question": "To what extent does your task rely on established rules?", "options": ["Not at all rule-based", "Slightly rule-based", "Moderately rule-based", "Very rule-based", "Extremely rule-based"], "key": "rules"},
    {"id": 13, "question": "How structured is the data you work with?", "options": ["Unorganized and lacks predefined format or structure", "Slightly structured (i.e., Spreadsheets)", "Moderately Structured (i.e., Spreadsheets)", "Very Structured (Database tables)"], "key": "dataStructure"},
    {"id": 14, "question": "Is the process expected to change in the next six (6) months to a year?", "type": "boolean", "key": "processChange"},
    {"id": 15, "question": "What are the applications used to complete the process?", "type": "text", "key": "application"},
    {"id": 16, "question": "Are there any expected changes or upgrades in the application(s) within the next 6 months to a year?", "type": "boolean", "key": "applicationUpgrade"}
]


responses = {}
user_name = None

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_next_question', methods=['POST'])
def get_next_question():
    global user_name
    data = request.get_json()
    current_question_id = data.get('current_question_id', 0)
    
    if current_question_id == 0:
        return jsonify({"question": "Hi, I'm Primo Your discovery guide.", "question_id": 1, "auto_advance": True})
    
    if current_question_id == 1:
        return jsonify({"question": "What is your first name?", "question_id": 1.5})
    
    if current_question_id == 1.5:
        user_name = responses.get("What is your first name?", "")
        return jsonify({"question": f"Hi {user_name}!", "question_id": 2, "auto_advance": True})
    
    if current_question_id == 2:
        return jsonify({"question": "What is your Business Unit or Department name?", "question_id": 3})
    
    if current_question_id == 3:
        return jsonify({"question": "Do you work for a specific area within your business unit/department? (Please type 'yes' or 'no')", "question_id": 4})
    
    if current_question_id == 4:
        response_to_q3 = responses.get("Do you work for a specific area within your business unit/department?", "").lower()
        # Check if the response is valid
        if response_to_q3 not in ["yes", "no"]:
            # Remove the incorrect response
            if 4 in responses:
                del responses["Do you work for a specific area within your business unit/department?"]  # Delete incorrect response
            return jsonify({"question": "Invalid response. Please type 'yes' or 'no'.", "question_id": 3, "error": True})
        elif response_to_q3 == "yes":
            return jsonify({"question": "What is the name of the area?", "question_id": 5})
        else:
            return jsonify({"question": "Now, I would like to capture some information about the process you would like to automate.", "question_id": 6, "auto_advance": True})
    
    if current_question_id == 5:
        return jsonify({"question": "Now, I would like to capture some information about the process you would like to automate.", "question_id": 6, "auto_advance": True})
    
    if current_question_id == 6:
        return jsonify({"question": "What is the name of the process?", "question_id": 7})
    
    if current_question_id == 7:
        return jsonify({"question": "How often do you complete the process?", "question_id": 8, "options": ["Daily", "Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Yearly"], "multiple": True})
    
    if current_question_id == 8:
        return jsonify({"question": "What is the volume per selected frequency?", "question_id": 9})
    
    if current_question_id == 9:
        return jsonify({"question": "What is the goal for automation?", "question_id": 10, "options": ["Cost", "Quality", "Productivity", "Employee Satisfaction", "Customer Satisfaction/Experience", "Operational Efficiency", "Accuracy and Compliance", "Scalability", "Innovation"], "multiple": True})
    
    if current_question_id == 10:
        return jsonify({"question": "Is the process documented?", "question_id": 11})
    
    if current_question_id == 11:
        return jsonify({"question": "To what extent does your task rely on established rules?", "question_id": 12, "options": ["Not at all rule-based", "Slightly rule-based", "Moderately rule-based", "Very rule-based", "Extremely rule-based"]})
    
    if current_question_id == 12:
        return jsonify({"question": "How structured is the data you work with?", "question_id": 13, "options": ["Unorganized and lacks predefined format or structure", "Slightly structured (i.e. Spreadsheets)", "Moderately Structured (i.e. Spreadsheets)", "Very Structured (Database tables)"]})
    
    if current_question_id == 13:
        return jsonify({"question": "Is the process expected to change in the next six (6) months to a year?", "question_id": 14})
    
    if current_question_id == 14:
        return jsonify({"question": "What are the applications used to complete the process?", "question_id": 15})
    
    if current_question_id == 15:
        return jsonify({"question": "Are there any expected changes or upgrades in the application(s) within the next 6 months to a year?", "question_id": 16})
    
    if current_question_id == 16:
        with open('responses.json', 'w') as f:
            json.dump(responses, f, indent=4)  # Save responses to a JSON file
        return jsonify({"question": "Thank you for this information. Now, follow the instructions to capture your end-to-end process.", "question_id": 17})

@app.route('/save_response', methods=['POST'])
def save_response():
    global response_counter
    data = request.get_json()
    question_id = data.get('question_id')
    response = data.get('response')
    
    # Convert responses to a list if it is meant to be multiple options
    if isinstance(response, str) and ',' in response:
        response = response.split(',')
    
    for item in questions:
        if item["id"] == question_id:
            question = item["question"]
            responses[question] = response

    # responses[question_id] = response  # Save the response using question_id as the key
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
