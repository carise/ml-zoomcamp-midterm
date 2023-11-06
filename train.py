import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, auc, mutual_info_score, roc_auc_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


def train_random_forest_classifier(df_train, y_train, max_depth=None, min_samples_leaf=1, n_estimators=100):
    train_dicts = df_train[categorical + numerical].to_dict(orient='records')

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(train_dicts)

    model = RandomForestClassifier(random_state=seed,
                                   max_depth=max_depth,
                                   min_samples_leaf=min_samples_leaf,
                                   n_estimators=n_estimators)
    model.fit(X_train, y_train)

    return dv, model


def predict_random_forest_classifier(df, dv, model):
    val_dicts = df[categorical + numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts)

    y_pred = model.predict_proba(X_val)[:, 1]

    return y_pred


seed = 1
output_file = 'model_random_forest.bin'

orig_df = pd.read_csv('data/heart.csv')
orig_df.columns = orig_df.columns.str.replace(r'\W+', '_', regex=True).str.lower()
categorical = ['sex', 'chestpaintype', 'fastingbs']
numerical = ['age', 'restingbp', 'cholesterol', 'maxhr']

# cholesterol = 0 and restingbp = 0 are not realistic, so set the 0 values to NaN
orig_df.cholesterol = np.where(orig_df['cholesterol'] == 0, np.nan, orig_df['cholesterol'])
orig_df.restingbp = np.where(orig_df['restingbp'] == 0, np.nan, orig_df['restingbp'])
mod_df = orig_df.dropna()
orig_df.shape, mod_df.shape


df_full_train, df_test = train_test_split(mod_df, test_size=0.2, random_state=seed)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=seed)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_train.heartdisease.values
y_val = df_val.heartdisease.values
y_test = df_test.heartdisease.values

del df_train['heartdisease']
del df_val['heartdisease']
del df_test['heartdisease']

# final random forest model
# parameters were determined in notebooy.ipynb
dv, model_rf = train_random_forest_classifier(df_train, y_train, max_depth=5, min_samples_leaf=3, n_estimators=70)
y_pred = predict_random_forest_classifier(df_val, dv, model_rf)

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model_rf), f_out)

print(f'Model saved to {output_file}')
