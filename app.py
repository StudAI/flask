# app.py
import numpy as np
import random as rd
from sklearn.cluster import AgglomerativeClustering
import json

from flask import Flask, request, jsonify
app = Flask(__name__)

# @app.route('/getmsg/', methods=['GET'])
# def respond():
#     # Retrieve the name from url parameter
#     name = request.args.get("name", None)

#     # For debugging
#     print(f"got name {name}")

#     response = {}

#     # Check if user sent a name at all
#     if not name:
#         response["ERROR"] = "no name found, please send a name."
#     # Check if the user entered a number not a name
#     elif str(name).isdigit():
#         response["ERROR"] = "name can't be numeric."
#     # Now the user entered a valid name
#     else:
#         response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

#     # Return the response in json format
#     return jsonify(response)

# @app.route('/post/', methods=['POST'])
# def post_something():
#     param = request.form.get('name')
#     print(param)
#     # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
#     if param:
#         return jsonify({
#             "Message": f"Welcome {param} to our awesome platform!!",
#             # Add this option to distinct the POST request
#             "METHOD" : "POST"
#         })
#     else:
#         return jsonify({
#             "ERROR": "no name found, please send a name."
#         })


# returns the uuid of the next element in arr that matches the cluster of target 
def get_match_id(start_idx, target, arr, data):
    length = len(arr)
    for i in range(start_idx,length):
        if arr[i] == target:
            return data[i]["uuid"]

@app.route('/matches', methods=['POST'])
def get_matches_array():
    with open('users.json') as f:
        data = json.load(f)

    clusterData = []
    for i in data:
        clusterData.append([i["math"], i["science"], i["english"], i["engineering"], i["grade level"],
                        i["extraversion"], i["agreeableness"], i["conscientientiousness"], i["neuroticism"], i["openness"]])
    clusterData = np.array(clusterData)

    # km is a numpy array where index = index in users and the value = cluster number
    km = AgglomerativeClustering(n_clusters=12).fit_predict(clusterData)
    print(km)
    
    # the response this request should return -> an array of dictionaries where each dictionary is in the format of { person1_uuid: person2_uuid }
    res = []
    
    for i in range(len(km)):
        match_id = get_match_id(i, km[i], km, data)
        res.append({data[i]["uuid"]: match_id})
        

    # if clusterData:
    #     return jsonify({
    #         "Message": f"Welcome {param} to our awesome platform!!",
    #         # Add this option to distinct the POST request
    #         "METHOD" : "POST"
    # })
    # else:
    #     return jsonify({
    #         "ERROR": "no name found, please send a name."
    #     })
        

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)