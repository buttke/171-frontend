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

        print('COMBINED')
        print(combined_df)
        self.diagnose_unknown_categories(combined_df)
        return self.preprocessor.transform(combined_df)














    ### FUCK

    def diagnose_unknown_categories(self, df):
            # Get the transformer by name or by index. Here we assume 'one_hot' is the name you've given to your OneHotEncoder within the transformers.
        one_hot_encoder = self.preprocessor.named_transformers_['one_hot']

        # Now we can correctly access the categories_
        known_categories = one_hot_encoder.categories_

        # Getting the names of the columns that were transformed by the OneHotEncoder
        categorical_features = self.preprocessor.transformers_[0][2]

        # Check each categorical column in the input DataFrame
        for col, known_cats in zip(categorical_features, known_categories):
            # Find the set of unique values in the DataFrame column
            input_cats = set(df[col].unique())

            # Find any values in the input data that are not known to the encoder
            unknown_cats = input_cats - set(known_cats)

            # If there are any unknown categories, print them out
            if unknown_cats:
                print(f"Column '{col}' has unknown categories:")
                for c in unknown_cats:
                    print(f"\t {c}; {type(c)}")



