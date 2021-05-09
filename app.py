# app.py
import numpy as np
import random as rd
from sklearn.cluster import AgglomerativeClustering
import json

from flask import Flask, request, jsonify
app = Flask(__name__)




def get_match_id(start_idx, target, arr, data):
    length = len(arr)
    for i in range(start_idx,length):
        if arr[i] == target:
            return data[i]["user_id"]

@app.route('/matches', methods=['POST'])
def get_matches_array():
    print(request.json)
    userData = request.json
    with open('users.json') as f:
        data = json.load(f)

    clusterData = [[userData["math"],userData["science"],userData["english"],userData["engineering"],userData["grade_level"],userData["extraversion"],userData["agreeableness"],userData["conscientiousness"],userData["neuroticism"],userData["openness"]]]
    for i in data:
        clusterData.append([i["math"], i["science"], i["english"], i["engineering"], i["grade_level"],
                        i["extraversion"], i["agreeableness"], i["conscientiousness"], i["neuroticism"], i["openness"]])
    clusterData = np.array(clusterData)

    km = AgglomerativeClustering(n_clusters=100).fit_predict(clusterData)
    print(km)
    
    res = []
    userCluster = km[0]

    for i in range(1,len(km)):
        if userCluster == km[i]:
            res.append({"id": data[i]["user_id"]})
    
    return jsonify({
        "matches": res[0:userData["numberOfMatches"]]
    })


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)