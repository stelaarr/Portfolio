from flask import Flask, jsonify, request
import numpy as np
from prometheus_client import start_http_server, Gauge, generate_latest

app = Flask(__name__)

# Initialize variables to store feedback data
feedback_data = {
    'true_ratings': [],
    'estimated_ratings': [],
    'users': set()
}

# Metrics
rmse_gauge = Gauge('rmse', 'Root Mean Square Error of RecSys')
num_users_gauge = Gauge('num_users', 'Number of Unique Users')


@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.get_json()
    user_id = data.get('userid')
    item_id = data.get('itemid')
    true_rating = data.get('rating')
    estimated_rating = data.get('estimated_rating')
    print('true_rating:', true_rating, 'estimated_rating:', estimated_rating)

    # Save the feedback data in memory
    feedback_data['true_ratings'].append(true_rating)
    feedback_data['estimated_ratings'].append(estimated_rating)
    feedback_data['users'].add(user_id)
    #print('Users:', feedback_data['users'],flush=True)

    # Calculate and return RMSE and number of unique users
    current_rmse = calculate_rmse()
    num_users = len(feedback_data['users'])
    rmse_gauge.set(current_rmse)
    num_users_gauge.set(num_users)

    return jsonify({'message': 'Feedback received successfully', 'rmse': current_rmse, 'num_users': num_users})

def calculate_rmse():
    true_ratings = feedback_data['true_ratings']
    estimated_ratings = feedback_data['estimated_ratings']
    num_ratings = len(true_ratings)

    if num_ratings == 0:
        return 0  # Return 0 if there are no ratings

    sum_squared_diff = 0
    for true_rating, estimated_rating in zip(true_ratings, estimated_ratings):
        sum_squared_diff += (true_rating - estimated_rating) ** 2

    mean_squared_diff = sum_squared_diff / num_ratings
    rmse = np.sqrt(mean_squared_diff)
    return rmse

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

