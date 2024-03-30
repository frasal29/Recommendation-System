import pandas as pd
import csv
from pearson_similarity import pearson_similarity
from predict_rating import predict_rating_for_movie


def predict_ratings_for_unrated_movie(user_id, n, data, neighbors, correlation, movie_data):
    # Get the set of movies not rated by the user
    unrated_movies = set(data['movieId']) - set(data[data['userId'] == user_id]['movieId'])
    
    # Get the top 40 similar users
    top_k_users = sorted(correlation.items(), key=lambda x: x[1], reverse=True)[:neighbors]
    
    predictions = {}  # Dictionary to store predictions
    
    for movie_id in unrated_movies:
        # Get the users among the top 40 who have rated the current movie
        rated_by_top_k_users = [other_user_id for other_user_id, _ in top_k_users if movie_id in set(data[data['userId'] == other_user_id]['movieId'])]
        
        # If the number of users who have rated the movie is greater than or equal to n, calculate the rating prediction
        if len(rated_by_top_k_users) >= n:
            # Filter the top 40 users to include only those who have rated the current movie
            relevant_users = {other_user_id: correlation for other_user_id, correlation in top_k_users if movie_id in set(data[data['userId'] == other_user_id]['movieId'])}
            
            # Calculate the rating prediction for the current movie
            predicted_rating = predict_rating_for_movie(user_id, movie_id, relevant_users, data)
            
            # Add the prediction to the dictionary
            predictions[movie_id] = predicted_rating
    
    return predictions


def generate_group_predictions(users, data, movie_data, neighbors):
    group_predictions = []

    for user_id in users:
        # Calculate Pearson correlations for the current user
        correlations = pearson_similarity(user_id, data)
        

        # Get rating predictions for the current user
        predictions = predict_ratings_for_unrated_movie(user_id, 1, data, neighbors, correlations, movie_data)

        # Add predictions for the single user to the group data structure
        for movie_id, predicted_rating in predictions.items():
            group_predictions.append({'userId': user_id, 'movieId': movie_id, 'rating': predicted_rating})

    return group_predictions