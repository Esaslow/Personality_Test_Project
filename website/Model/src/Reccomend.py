import matplotlib.pyplot as plt
import numpy.random as rnd
from matplotlib.patches import Ellipse
import numpy as np
from numpy.random import rand
import random

from collections import Counter
import matplotlib.pyplot as plt
def reccomend(quiz,questions,percentile_df):
    ### Recommender System
    #Get the Users ratings
    uservals = quiz.df.loc[0,:]

    #Look at what others answered to the same questions
    everyone = questions[quiz.df.columns[uservals.nonzero()]]

    #Find the difference between others and current user
    everyone_abs = np.abs(everyone - uservals[quiz.df.columns[uservals.nonzero()]])

    #sort the values based on the sum
    ind = everyone_abs.sum(axis = 1).sort_values()[:30].index

    #take the mean of the closest 10 users
    percentile_df_user = percentile_df.loc[ind,:].mean(axis = 0)
    return percentile_df_user
