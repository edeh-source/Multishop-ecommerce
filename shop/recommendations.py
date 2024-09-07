from surprise import Dataset, Reader, SVD, KNNBasic
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV
from surprise import accuracy
import pandas as pd
from .models import Review  # Import your Rating model

def train_recommendation_model():
    # Get ratings from your Django model
    ratings = Review.objects.all().values('user_id', 'product_id', 'rating')
    
    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(ratings)
    print(df.head())
    
    # Create Surprise dataset
    reader = Reader(rating_scale=(1, 5))  # Adjust if your scale is different
    data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
    print("This is the data", data)
    
    # Split the data
    trainset, testset = train_test_split(data, test_size=0.25)
    
    # Define the parameter grid for SVD
    param_grid = {
        'n_factors': [50, 100, 150],
        'n_epochs': [20, 30, 40],
        'lr_all': [0.002, 0.005, 0.01],
        'reg_all': [0.02, 0.1, 0.2]
    }


    
    
    # Perform grid search
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)
    gs.fit(data)
    
    # Get the best algorithm based on RMSE
    best_algo = gs.best_estimator['rmse']
    
    # Train the best algorithm on the entire training set
    best_algo.fit(trainset)
    
    # Test the algorithm on the test set
    predictions = best_algo.test(testset)
    
    # Compute and print RMSE
    accuracy.rmse(predictions, verbose=True)
    
    return best_algo

def get_top_recommendations(user_id, n=5):
    user_ratings = Review.objects.filter(user_id=user_id)
    if not user_ratings.exists():
        return []
    
    # Get all products
    all_products = set(Review.objects.values_list('product_id', flat=True).distinct())
    
    # Get products the user has already rated
    user_rated = set(Review.objects.filter(user_id=user_id).values_list('product_id', flat=True))
    
    # Find products the user hasn't rated
    products_to_predict = list(all_products - user_rated)
    
    # Load the trained model (you might want to cache this)
    algo = train_recommendation_model()
    
    # Make predictions
    predictions = [algo.predict(user_id, product_id) for product_id in products_to_predict]
    
    # Sort predictions by estimated rating
    top_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    
    return [(pred.iid, pred.est) for pred in top_predictions]
