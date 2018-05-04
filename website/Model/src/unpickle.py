import pickle
def Load_pickled_files(filepath = 'website/Model/data/Model_checkpoint' ):
    '''
    INPUTS: NONE
    OUTPUTS
    ---------
    long_key: Pandas DataFrame grading key that contains all 300 questions
    questions: Pandas DataFrame containin all the data with user as index and question as col
    grading_Key: similar to long_key but with a couple fewer columns
    keys2trait: Dictionary that contains Facet key: (Trait, Facet)
    Trait_dict_keys: Trait to key dictionary
    Trait_dict_questions: Trait: key: questions dictionary

    '''
    with open(filepath, 'rb') as handle:
        long_key = pickle.load(handle)
        questions = pickle.load(handle)
        grading_Key = pickle.load(handle)
        keys2trait = pickle.load(handle)
        Trait_dict_keys = pickle.load(handle)
        Trait_dict_questions = pickle.load(handle)
        graded_df = pickle.load(handle)
        percentile_df = pickle.load(handle)
        traits_df = pickle.load(handle)
        handle.close()
    return long_key, questions, grading_Key,\
keys2trait, Trait_dict_keys, Trait_dict_questions,\
graded_df, percentile_df, traits_df
