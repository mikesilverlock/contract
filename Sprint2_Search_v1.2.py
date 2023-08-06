from flask import Flask, render_template, request
from pymongo import MongoClient
import datetime

"""The version below enables the search of record data. 
Search box. Returns all database.
Created by: Gavin Love
Date: 06.08.23"""

# cient, db and collection for MongoDb

app = Flask(__name__)
client = MongoClient("mongodb+srv://mike:SKddWR9OyJnLtYva@contract-a1.dqunsnr.mongodb.net/?retryWrites=true&w=majority") # test MongoDB server on localhost
db = client['contractTool'] # name of MongoDB database
collection = db['sprint1'] # name of MongoDB collection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        third_party = request.form['third_party']
        project = request.form['project']
        date_created = request.form['date_created']
        contract_file_name = request.form['contract_file_name']
        date_entered = request.form['date_entered']
        
        data = {
            '3rd Party': third_party,
            'Project': project,
            'Date Created': date_created,
            'Contract file name': contract_file_name,
            'Date Entered': date_entered
        }
        
        collection.insert_one(data)
        
        # Retrieve all entries from the database
        all_entries = collection.find()
        
        # Create a formatted string of the database entries
        entries_str = "<br>".join([f"{entry['3rd Party']}, {entry['Project']}, {entry['Date Created']}, {entry['Contract file name']}, {entry['Date Entered']}" for entry in all_entries])

        return redirect(url_for('index'))  # Redirect to the main page after adding the contract details

    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_third_party = request.form['search_third_party']
        search_project = request.form['search_project']
        
        # Perform the search in the database based on the provided criteria
        query = {}
        if search_third_party:
            query['3rd Party'] = search_third_party
        if search_project:
            query['Project'] = search_project

        search_results = collection.find(query)
        
        return render_template('search.html', search_results=search_results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
