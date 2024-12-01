import pandas as pd
import time
import requests
from threading import Thread

class UserSimulator():
    """
    Generates fake traffic
    """
    def __init__(self, activity_file, recommendation_endpoint, feedback_endpoint):
        """
        Create a UserSimulator object
        @param activity_file: path to the file containing the user activty tuples (userid, itemid, rating)
        @param recommendation_endpoint: the endpoint (url:port) of the recommender system service
        @param feedback_endpoint: the endpoint (url:port) of the ss
        """
        self.df = pd.read_csv(activity_file, dtype={'userId':int, 'movieId':int, 'rating':float})
        self.df = self.df.sample(frac=1)
        self.recommendation_endpoint = recommendation_endpoint
        self.feedback_endpoint = feedback_endpoint
        self.i = 0
        self.running = False
        self.daemon = None

    def get_action(self):
        """
        Draw one user action from the list
        @return res: a triplet (userid, itemid, rating)
        """
        # when input is exhausted, start over
        if self.i >= len(self.df):
            i = 0
        res = self.df.iloc[self.i].tolist()
        self.i += 1
        return res

    def start(self):
        """
        Start simulation (spawn a new thread)
        """
        self.running = True
        self.daemon = Thread(target=self.run_simulation, daemon=True, name='simulator')
        self.daemon.start()

    def stop(self):
        """
        Stop simulation (set the running variable to False, which terminates the thread)
        """
        self.running = False

    def run_simulation(self):
        """
        Extract a user action and sends it to the recommender system to get a rating back
        """
        while self.running:
            # generate one user activity entry from file
            userid, itemid, rating = self.get_action()
            userid = int(userid)
            itemid = int(itemid)
            #print( 'after change:',userid, itemid, rating)
            # sleep for some time
            time.sleep(1)
            # send the user,item pair to the recommendation endpoint to get an estimated score
            response = requests.get(self.recommendation_endpoint, params={'userid': userid, 'itemid': itemid})
            print(response, flush=True)
            estimated_rating = response.json()['estimated_rating']
            print('>>>', estimated_rating, type(estimated_rating))
            # send the true rating and estimated ratign to the feedback endpoint
            response = requests.post(self.feedback_endpoint, json={'userid':userid, 'itemid':itemid, 'rating':rating, 'estimated_rating':estimated_rating})
            print(userid, itemid, rating, estimated_rating, flush=True)
            print('rmse:', response.json()['rmse'], 'n_users:', response.json()['num_users'])
        self.daemon = None

    

