from flask import Flask, jsonify, request
from joblib import load
import pickle

# Your code here
app = Flask(__name__)

with open('models/model_SVD.pkl', 'rb') as f:
    model = pickle.load(f)
print(model)

@app.route('/recommender', methods=['GET'])
def get_estimated_rating():
    user_id = request.args.get('userid')
    item_id = request.args.get('itemid')
    
    if user_id is None or item_id is None:
        return jsonify({'error': 'Missing user_id or item_id'}), 400

    try:
        user_id = int(float(user_id))
        item_id = int(float(item_id))

        prediction = model.predict(user_id, item_id)
        estimated_rating = prediction.est
        # Return the estimated rating as JSON response
        return jsonify({'estimated_rating': estimated_rating})
    except ValueError:
        return jsonify({'error': 'Invalid user_id or item_id'}), 400
    #user_id = int(request.args.get('userid'))
    #item_id = int(request.args.get('itemid'))
    
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
