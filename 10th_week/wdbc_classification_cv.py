import numpy as np
from sklearn import datasets, model_selection, preprocessing
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()
    
    # Data scaling
    scaler = preprocessing.StandardScaler()
    data_scaled = scaler.fit_transform(wdbc.data)

    # Define hyperparameter grid for XGBoost
    param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7, 10],
        'min_child_weight': [1, 3, 5],
        'gamma': [0, 0.1, 0.2, 0.3],
        'subsample': [0.7, 0.8, 0.9, 1.0],
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
    }

    # Set up RandomizedSearchCV with XGBoost
    model = XGBClassifier(eval_metric='logloss', random_state=42)
    random_search = RandomizedSearchCV(model, param_grid, n_iter=30, cv=5, random_state=42, n_jobs=-1)
    random_search.fit(data_scaled, wdbc.target)
    
    # Use the best model found by RandomizedSearchCV for cross-validation
    best_model = random_search.best_estimator_
    cv_results = model_selection.cross_validate(best_model, data_scaled, wdbc.target, cv=5, return_train_score=True)

    # Evaluate the model
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')
