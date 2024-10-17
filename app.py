# app.py: Flask Application to Collect User Data and Store in MongoDB
from flask import Flask, render_template, request, redirect
import csv
import os
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Step 1: Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['income_survey']
collection = db['user_data']

# Route to display the form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Step 2: Retrieve user inputs from the form
        age = request.form.get('age')
        gender = request.form.get('gender')
        income = request.form.get('income')
        utilities = request.form.get('utilities', 0)
        entertainment = request.form.get('entertainment', 0)
        school_fees = request.form.get('school_fees', 0)
        shopping = request.form.get('shopping', 0)
        healthcare = request.form.get('healthcare', 0)

        # Step 3: Store data in MongoDB
        user_data = {
            "age": age,
            "gender": gender,
            "income": income,
            "utilities": utilities,
            "entertainment": entertainment,
            "school_fees": school_fees,
            "shopping": shopping,
            "healthcare": healthcare
        }
        collection.insert_one(user_data)

        # Step 4: Export data to CSV
        if not os.path.exists('data/user_data.csv'):
            with open('data/user_data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Age', 'Gender', 'Income', 'Utilities', 
                                 'Entertainment', 'School Fees', 
                                 'Shopping', 'Healthcare'])

        with open('data/user_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_data.values())

        return redirect('/')
    except Exception as e:
        return f"An error occurred: {e}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
