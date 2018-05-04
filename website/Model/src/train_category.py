from sklearn.tree import DecisionTreeRegressor as DT
from sklearn.model_selection import train_test_split

def train_category(X,y,traits_df,max_depth):

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    model = DT(max_depth = max_depth)
    model.fit(X_train,y_train)


    return model,X_test,y_test
