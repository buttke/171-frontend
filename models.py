import joblib
import sklearn
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

class ModelMgr:
    def __init__(self):
        self.gbdt = joblib.load('weights/gbdt_model_gscv.joblib')
        self.rf = joblib.load('weights/rf_model.joblib')


        categorical_features = ['Browser',  'OperatingSystems', 'VisitorType', 'Weekend', 'Month']
        numerical_features = ['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']

        transformers = [
                ('one_hot', OneHotEncoder(), categorical_features),
                ('scale', MinMaxScaler(), numerical_features) 
                ]

        df = pd.read_csv('./online_shoppers_intention.csv')
        x = df.drop('Revenue', axis=1)

        self.preprocessor = ColumnTransformer(transformers=transformers)
        self.preprocessor.fit(x)

    def preproc_pd_df(self, x_df):
        return self.preprocessor.transform(x_df)

    def preproc_userdata(self, userdata, leftovers):

        user_df = pd.DataFrame([userdata])
        leftovers_df = pd.DataFrame([leftovers])
        combined_df = pd.concat([user_df, leftovers_df], axis=1)

        # print('COMBINED')
        # print(combined_df)
        return self.preprocessor.transform(combined_df)
