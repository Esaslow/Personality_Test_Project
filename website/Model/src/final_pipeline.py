
import pandas as pd
import numpy as np
#import src.pipeline as P
import os


def create_long_key(key_path):
    key = pd.read_csv(key_path)
    long_key = key.loc[~np.isnan(key["Full#"]), :]
    long_key.pop('Short#')
    return long_key


'''Read the data in from the data folder'''

def read_ipip(filepath):
    '''
    Read the data in from the filepath
    Return two things, data frame for the meta data and a dataframe for questions answers
    Does not have the columns set the questions yet.
    '''
    age = []
    year = []
    Q = []
    country = []
    sex = []
    number = []
    month = []
    day = []
    hour = []
    minutes = []
    sec = []
    with open(filepath) as F:
        F.readline()
        for i,line in enumerate(F):

            data = F.readline()
            data = list(data)

            number.append(int("".join(data[0:8])))
            sex.append(data[8])
            age.append(int("".join(data[9:11])))
            sec.append(int("".join(data[11:13])))
            minutes.append(int("".join(data[13:15])))
            hour.append(int("".join(data[15:17])))
            day.append(int("".join(data[17:19])))
            month.append(int("".join(data[19:21])))
            year.append(1900 + int("".join(data[21:24])))
            country.append("".join(data[24:35]))
            Q.append([int(x) for x in data[35:-1]])
    meta_data = pd.DataFrame()
    meta_data["age"] = age
    meta_data["sex"] = sex
    meta_data["number"] = number
    meta_data["country"] = country
    meta_data["year"] = year
    meta_data['month'] = month

    # Could add the Date in the Future
    return meta_data, Q




def load_Graded_data():
    '''
    First function, gives back the loaded questions and a grading key.  As well
    these are formatted nicely:
    Graded_df is a pandas DataFrame
    INPUT: none
    OUTPUT: Loaded questions, grading key  in nice formats
    '''



    meta,questions = read_ipip('data/IPIP300.dat')

    #Path to the key file
    key_path = 'data/IPIP-NEO-ItemKey_csv.csv'

    #Call the function short key to create the short key
    long_key = create_long_key(key_path)

    long_key = long_key.sort_values('Full#')

    #Build the questions DataFrame
    questions = pd.DataFrame(questions,
                             columns=long_key.Item.values,
                            index = meta.number)

    print(questions.shape)

    # Grab only the columns that include Key, Facet, and Item
    grading_Key = long_key[['Key','Facet','Item']]


    Graded_df = Grade_scores(grading_Key,questions)
    Graded_df.index.names = ['UserID']
    return long_key, questions, grading_Key, Graded_df, meta


    '''
    Make a dictionary system:
    '''

def create_k2t(long_key):

    '''
    Create the key: (trait, facet) ditcionary
    '''


    #Name of all of the traits I will be using
    Traits = ['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']

    #create an empty dictionary of traits
    Trait_dict_keys = {}
    keys2trait = {}

    #go through each trait and store all of the keys
    for Trait in Traits:
        Keys = [Trait[0]+str(i) for i in range(1,6)]
        Trait_dict_keys[Trait] = Keys

    #and the Reverse:
    for Trait in Traits:
        Keys = [Trait[0]+str(i) for i in range(1,6)]
        for key in Keys:
            facet = long_key[long_key.Key == key].Facet.unique()[0]
            keys2trait[key] = (Trait,facet)
    return keys2trait, Trait_dict_keys


def nested_dict(Trait_dict_keys,long_key):
    #creates the nest dictionary
    Trait_dict_questions = {}
    # go through each trait
    for Trait,facet in Trait_dict_keys.items():
        temp = {}
        # Go through each key
        for key in facet:
            Facet_questions = long_key.loc[long_key.Key == key,'Item']
            temp[key] = set(Facet_questions.values)

        Trait_dict_questions[Trait] = temp
    return Trait_dict_questions


def Grade_scores(grading_Key, questions):
    """
    INPUTS:
    Grading key: that contains the cols Key, facet, and ITEM
    questions Data frame: contains users as rows and questions as columns

    OUTPUT:
    Graded DataFrame: cols are facets and rows are users
    """
    # Create a sorted list of the categories
    categories = sorted(list(set(grading_Key.Key)))

    # create new DataFrame
    Graded_df = pd.DataFrame()

    # go through each of the categories from the key
    for cat in categories:

        # Find all the questions that fall into that category
        cat_questions = grading_Key[grading_Key.Key == cat].Item.values

        # find the name of the facet:
        facet = grading_Key[grading_Key.Key == cat].Facet.unique()[0]

        # create the facet name:
        name = cat + ": " + facet

        # Add sum of those answers to the specific facet in the datafram
        Graded_df[name] = questions[cat_questions].sum(axis=1)

    return Graded_df



if __name__ == '__main__':
    long_key, questions, grading_Key,graded_df = load_Graded_data()

    keys2trait, Trait_dict_keys = create_k2t(long_key)

    #nested_dictionary
    Trait_dict_questions = nested_dict(Trait_dict_keys,long_key)

    import src.make_user_percentile_profile as m

    percentile_df, traits_df = m.make_user_profiles(long_key, questions, grading_Key, keys2trait, Trait_dict_keys, Trait_dict_questions)

    #set the index for percentile and traits
    percentile_df = percentile_df.set_index(questions.index.values)
    traits_df = traits_df.set_index(questions.index.values)

    import pickle
    print('pickling')
    # write a file
    with open('data/Friday_mvp_checkpoint1', 'wb') as handle:
        pickle.dump(long_key, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(questions, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(grading_Key, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(keys2trait, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(Trait_dict_keys, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(Trait_dict_questions, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(graded_df, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(percentile_df, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(traits_df, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
