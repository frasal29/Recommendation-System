
def predict_rating_for_movie(user_id, movie_id, relevant_users, data):
    # Calculate the numerator and denominator for rating prediction
    numerator = 0
    denominator = 0
    
    for other_user_id, similarity in relevant_users.items():
        # Extract the rating of the current user for the current movie
        other_user_rating = data[(data['userId'] == other_user_id) & (data['movieId'] == movie_id)]['rating'].iloc[0]
        
        # Calculate the mean rating of the current user
        other_user_mean = data[data['userId'] == other_user_id]['rating'].mean()
        
        # Update numerator and denominator
        numerator += similarity * (other_user_rating - other_user_mean)
        denominator += abs(similarity)
    
    # Calculate the predicted rating
    user_mean = data[data['userId'] == user_id]['rating'].mean()
    predicted_rating = user_mean + (numerator / denominator) if denominator != 0 else 0
    
    return predicted_rating


