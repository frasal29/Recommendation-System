import pandas as pd
import predictions as pred
import sequential_recommendations as seq
import sequential_recommendations_revisited as new_seq
import os
import plot as pl

def load_movie_data(file_path):
    # Load data from the CSV file
    movie_data = pd.read_csv(file_path)
    # Return data as a dictionary where keys are movie IDs
    return {row['movieId']: {'title': row['title'], 'genres': row['genres']} for _, row in movie_data.iterrows()}



def main():
              
    users = []
    # Load the data
    movie_data = load_movie_data("dataset/ml-latest-small/movies.csv")
    data = pd.read_csv("dataset/ml-latest-small/ratings.csv")
    

    # Create output folder if it doesn't already exist
    if not os.path.exists("output"):
        # If the folder doesn't exist, create it
        os.makedirs("output")
       
    while True:
        print("Enter the desired users (from 1 to 610) separated by comma (e.g., 1,2,3):")
        user_input = input()
        users = [int(user_id.strip()) for user_id in user_input.split(',')]
        
        if len(users) < 2 or len(users) > 10:
            print("Make sure to enter a number of users in range 3-10. Please try again.")
        else:
            break

    while True:
        print("Enter the number of most similar neighbors to compare for each user (from 5 to 50):")
        neighbors = input()
        
        try:
            neighbors = int(neighbors)
            if neighbors < 5 or neighbors > 50:
                print("Make sure to enter a number between 5 and 50. Please try again.")
            else:
                break
        except ValueError:
            print("Make sure to enter an integer. Please try again.")

    # Generate predictions for the users
    print("Generating predictions for the selected users...")
    predictions = pred.generate_group_predictions(users, data, movie_data, neighbors)

    # Sort predictions by user_id
    predictions.sort(key=lambda x: x['userId'])

    # Write predictions to a CSV file
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv('output/dataset_with_also_predictions.csv', index=False)
    
    # consider all calculated predictions, not just those common to all users
    all_movies_predictions = seq.create_user_ratings_dataframe(predictions_df, users)
    all_movies_predictions.to_csv("output/all_movies.csv", index=False)
    
    
    '''  
# Main starts from here if predictions are already available
#############################    
    data = pd.read_csv("dataset/ml-latest-small/ratings.csv")
    movie_data = load_movie_data("dataset/ml-latest-small/movies.csv")
    users = [34,22,75,64,4]
    all_movies_predictions = pd.read_csv('output/all_movies.csv')
#############################
    '''
    while True:
        print("Enter the value of how many top k items must to be considered:")
        k = input()

        if not k.isdigit() or int(k) < 2 or int(k) > 10:
            print("Make sure to enter a value between 2 to 10. Please try again.")
        else:
            break

    topk = int(k)

    # Variables for original algorithm
    final_topk_movies_original = [] # list of all k movies for all iterations
    setTopKmovies_original = {}  # Using a dictionary
    new_predictions_original = all_movies_predictions # temporary variable for the first iteration
        
    # Variables for revisited algorithm
    final_topk_movies_revisited = [] # list of all k movies for all iterations
    setTopKmovies_revisited = {}  # Using a dictionary
    new_predictions_revisited = all_movies_predictions # temporary variable for the first iteration




    # check if previous predictions CSV file is present, and if so, remove it
    csv_file_original = "output/satisfaction_original.csv"
    if os.path.exists(csv_file_original):
        os.remove(csv_file_original)
    
    csv_file_revisited = "output/satisfaction_revisited.csv"
    if os.path.exists(csv_file_revisited):
        os.remove(csv_file_revisited)
    

        # Execute the loop for the desired number of iterations
    for j in range(11):
        print(f"Iteration {j}")
        
        if j == 0:
            # In the first iteration, use the original predictions
            
            # ORIGINAL ALGORITHM
            setTopKmovies_original = seq.sdda(users, j, topk, setTopKmovies_original, all_movies_predictions, new_predictions_original)
            final_topk_movies_original.append(setTopKmovies_original)

            # REVISITED ALGORITHM
            setTopKmovies_revisited = new_seq.sdda(users, j, topk, setTopKmovies_revisited, all_movies_predictions, new_predictions_revisited)
            final_topk_movies_revisited.append(setTopKmovies_revisited)


        else:
            # Remove the selected movies from previous iterations from the predictions
            # Calculate the new top-k movies and update setTopKmovies
            
            # ORIGINAL ALGORITHM
            new_predict_original = seq.change_predictions(new_predictions_original, setTopKmovies_original)
            
            setTopKmovies_original = seq.sdda(users, j, topk, setTopKmovies_original, all_movies_predictions, new_predict_original)
            
            final_topk_movies_original.append(setTopKmovies_original)
            
            new_predictions_original = new_predict_original
            
            # REVISITED ALGORITHM
            new_predict_revisited = new_seq.change_predictions(new_predictions_revisited, setTopKmovies_revisited)
            
            setTopKmovies_revisited = new_seq.sdda(users, j, topk, setTopKmovies_revisited, all_movies_predictions, new_predict_revisited)
            
            final_topk_movies_revisited.append(setTopKmovies_revisited)
            
            new_predictions_revisited = new_predict_revisited


        
        print(f"Iteration {j} --> Top k movies: {setTopKmovies_original}\n")
        print(f"Iteration {j} --> Top k movies: {setTopKmovies_revisited}\n")
    
    # create a dataframe and then a CSV file with all recommendations from all iterations
    seq.create_df_csv_movie_recommendations(final_topk_movies_original, movie_data)
    new_seq.create_df_csv_movie_recommendations(final_topk_movies_revisited, movie_data)

    # Plotting
    pl.plot_scores_from_csv(users, csv_file_original) # satisfaction plot for each user for each iteration ORIGINAL ALGORITHM
    pl.plot_scores_from_csv(users, csv_file_revisited) # satisfaction plot for each user for each iteration REVISITED ALGORITHM

    pl.plot_groupDis_and_groupSat_from_csv(csv_file_original) # groupDis and groupSat values plot for each iteration ORIGINAL ALGORITHM
    pl.plot_groupDis_and_groupSat_from_csv(csv_file_revisited) # groupDis and groupSat values plot for each iteration REVISITED ALGORITHM


if __name__ == "__main__":
    main()
