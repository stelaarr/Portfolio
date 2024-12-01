from surprise import Dataset, SVD, Reader
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse
from surprise.dump import dump, load
import surprise
import pickle
import pandas as pd

# Load the dataset
data_path = "../data/movielens/ml-latest-small/ratings.csv"

df = pd.read_csv(data_path)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

# Check if a pre-trained model exists, if not, train a new one
try:
    _, ms_cf_svd_algo = load('models/model_SVD.pkl') 
    print("Pre-trained model loaded successfully!")
except FileNotFoundError:
    print("Training a new model...")

    trainset = data.build_full_trainset()
    ms_cf_svd_algo = SVD(n_factors=7, n_epochs=13, lr_all=0.007, reg_all=0.01)
    ms_cf_svd_algo.fit(trainset)

    # Save the trained model 
    with open('recommender_model/models/model_SVD.pkl', 'wb') as f:
        pickle.dump(ms_cf_svd_algo, f)
    print("New model trained and saved successfully!")


def estimate_rating(user_id, item_id):
    """Estimate rating for a given user and item."""
    prediction = ms_cf_svd_algo.predict(user_id, item_id)
    return prediction.est # Return both estimated rating and true rating
