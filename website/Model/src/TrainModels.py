from src import train_category
from sklearn import tree as t
import numpy as np

def Train_models(traits_df,questions,max_depth = 3):
    Traits = ['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']
    models = []
    print(len(Traits))
    for i,trait in enumerate(Traits):

        y = traits_df[trait].values*100
        y = [int(x) for x in y]
        X = questions.values

        # train the model

        model,X_test,y_test = train_category.train_category(X,y,traits_df,max_depth)



        #export the tree
        t.export_graphviz(model,out_file='tree.dot')
        print('\nModel: ',trait)
        error = np.round(np.mean(np.abs(model.predict(X_test)-y_test)),2)
        print('\nDone Training Model',i+1)
        print('--Remaining: ',len(Traits)- i-1,'--')
        print('Mean abs error: '+str(error)+'%','\n','-'*50)
        models.append(model)

    return Traits,models
