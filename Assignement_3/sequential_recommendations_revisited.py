import pandas as pd
from itertools import islice
import numpy as np
import csv
import os

def create_user_ratings_dataframe(input_df, users):
    # Extract all distinct movieIds from the provided table
    distinct_movie_ids = set(input_df['movieId'])
    
    # Create a dictionary to store user ratings for each movieId
    user_ratings_dict = {f'user_{user}': [] for user in users}
    user_ratings_dict['movieId'] = []
    
    # Populate the dictionary with corresponding rating values for users
    for movie_id in distinct_movie_ids:
        user_ratings_dict['movieId'].append(movie_id)
        for user in users:
            # Find the rating corresponding to the user and movieId
            rating = input_df[(input_df['movieId'] == movie_id) & (input_df['userId'] == user)]['rating'].values
            if len(rating) > 0:
                user_ratings_dict[f'user_{user}'].append(rating[0])
            else:
                # If there's no rating for that user, assign 0
                user_ratings_dict[f'user_{user}'].append(0)
    
    # Create a new DataFrame using the user ratings dictionary
    user_ratings_df = pd.DataFrame(user_ratings_dict)
    
    return user_ratings_df

def create_df_csv_movie_recommendations(final_topKmovies, moviedata):
    # Creating an empty DataFrame
    df = pd.DataFrame(columns=['iteration', 'movieId', 'title', 'rating'])

    # Iterating over each map in the final_topKmovies list
    for iteration, movie_map in enumerate(final_topKmovies, start=0):
        for movie_id, rating in movie_map.items():
            # Add a row to the DataFrame with corresponding values
            title = moviedata[movie_id]['title']
            df = pd.concat([df, pd.DataFrame({'iteration': [iteration], 'movieId': [movie_id], 'title': [title], 'rating': [rating]})])

    # Save the DataFrame to a CSV file
    df.to_csv("output/topkmovies_revisited.csv", index=False)


def commonIdMovie(predictions_df, users):
    result_rows = []
    
    unique_movie_ids = set(predictions_df['movieId'])

    # Create column names based on the index of users in the 'users' list
    columns = ['movieId'] + [f'user_{i}' for i in range(1, len(users) + 1)]

    for movie_id in unique_movie_ids:
        ratings = []
        all_users_have_ratings = True
        
        for user in users:
            rating = predictions_df[(predictions_df['movieId'] == movie_id) & (predictions_df['userId'] == user)]['rating'].values
            if len(rating) > 0:
                ratings.append(rating[0])
            else:
                all_users_have_ratings = False
                break
        
        if all_users_have_ratings:
            result_rows.append({**{'movieId': movie_id}, **{f'user_{i}': rating for i, rating in enumerate(ratings, start=1)}})
    
    new_data = pd.DataFrame(result_rows, columns=columns)
    
    # Sort the dataframe by 'movieId'
    new_data = new_data.sort_values(by='movieId', ascending=True)
    
    return new_data

# Function that returns the first k movies present in the group dataframe
def topKMovies_group(data, k):
    # Check if k is greater than the length of the dataframe
    if k >= len(data):
        return set(data['movieId'])
    
    # Return the first k movieIds
    return set(data['movieId'].head(k))

# SAT function, takes: a user, integer k, ids of the top k group movies and its ratings, Single predictions DataFrame, and new users's prediction without the previous top k group films
def sat(user, k, setTopkMovie, dataPredictions, new_predictions):
    df = dataPredictions
    data = new_predictions

    sorted_df = data.sort_values(by=f'user_{user}', ascending=False)
    
    top_10_df = sorted_df.head(k)

    denominator = 0
    for index, row in top_10_df.iterrows():
        value = row[f'user_{user}']
        denominator += value
        
    numerator = 0

    for movie in setTopkMovie.keys():
        selected_rows = df[df['movieId'] == movie]
        user_column_values = selected_rows[f'user_{user}'].values
        numerator += user_column_values[0]
        
    sat = numerator / denominator

    return sat

def calculate_standard_deviation(users, list_sat):
    average = np.mean(list_sat)
    sum_score = 0
    for score in list_sat:
        sum_score += (score - average)**2
    
    return np.sqrt(sum_score/len(users))

def groupDis(j, users, setTopkMovies, k, dataPredictions, new_predictions):
    list_sat = []
    for user in users:
        temp = sat(user, k, setTopkMovies, dataPredictions, new_predictions)
        list_sat.append(temp)
    #difference = max(list_sat) - min(list_sat)
    difference = calculate_standard_deviation(users, list_sat)

    group_sat = np.mean(list_sat)
    
    csv_columns = []
    csv_columns.append("iteration")
    for user in users:
        csv_columns.append(f"user_{user}")
    
    csv_columns.append("groupDis")
    csv_columns.append("groupSat")
    
    csv_file = "output/satisfaction_revisited.csv"
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        data_dict = {}
        for user, sat_score in zip(users, list_sat):
            data_dict[f"user_{user}"] = sat_score
        data_dict["groupDis"] = difference
        data_dict["groupSat"] = group_sat
        data_dict["iteration"] = j
        writer.writerow(data_dict)

    return difference

def sdda(users, j, k, set_previous_TopKMovies, dataPredictions, new_predictions):
    if j == 0:
        alfa = 0
    else:
        alfa = groupDis(j, users, set_previous_TopKMovies, k, dataPredictions, new_predictions)
    
    movie_ratings = {}

    colonne_utenti = [f'user_{user}' for user in users]

    for index, row in new_predictions.iterrows():
        movie_id = int(row['movieId'])
        valori_utenti = [row[colonna] for colonna in colonne_utenti]
        average_score = sum(valori_utenti) / len(valori_utenti)
        least_score = min(valori_utenti)
        score = ( (1-alfa) * average_score) + ( alfa * least_score)
        movie_ratings[movie_id] = score
    
    sorted_ratings = dict(sorted(movie_ratings.items(), key=lambda item: item[1], reverse=True))
    
    first_10_items = dict(islice(sorted_ratings.items(), k))
    
    return first_10_items

def change_predictions(all_movies_predictions, setTopKmovies):
    setTopKmovies = set(setTopKmovies)
    
    filtered_predictions = all_movies_predictions[~all_movies_predictions['movieId'].isin(setTopKmovies)]
    
    return filtered_predictions