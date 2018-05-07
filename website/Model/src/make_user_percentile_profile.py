
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor as DT
import os
from graphviz import Source
from sklearn import tree as t
import time
import pandas as pd
from scipy import stats

#load in the data
#import src.unpickle as l

def make_user_profiles(long_key, questions, grading_Key, keys2trait, Trait_dict_keys, Trait_dict_questions):

#     long_key, questions, grading_Key, keys2trait, Trait_dict_keys, Trait_dict_questions = l.Load_pickled_files('data/Friday_mvp_checkpoint')

    # start the clock
    start = time.time()

    #Create new empty df
    Traits = Trait_dict_questions.keys()
    facet_percentiles_df = pd.DataFrame()
    traits_df = pd.DataFrame()

    # Go Through each of the 5 traits
    for trait in Traits:

        #Get the keys traits
        print(trait)
        Facet_keys = Trait_dict_questions[trait].keys()

        total = np.zeros(questions.shape[0])


        # Go through each facet one at a time
        for facet in Facet_keys:

            #Get the questions as a list
            facet_questions = list(Trait_dict_questions[trait][facet])

            #get the data sample
            facet_distribution = (questions[facet_questions].sum(axis = 1)).values

            # add tot the total for that trait for use to calculate the trait percentile
            total+=facet_distribution

            #Come up with the name
            name = str(trait)+ "-"+str(facet)

            # Do some math
            x = facet_distribution
            Percentile = stats.rankdata(facet_distribution, "average")/len(facet_distribution)
            facet_percentiles_df[name] = Percentile

        #caluclate the percentile of the total for that trait
        traits_df[trait] =  stats.rankdata(total, "average")/len(total)

    "the code you want to test stays here"
    end = time.time()
    print('-'*50)
    print('time = ',end - start)
    print('\n\n')
    return facet_percentiles_df,traits_df
