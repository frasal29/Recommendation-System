import pandas as pd
import predictions as pred
import sequential_recommendations as seq
import os
import plot as pl

def load_movie_data(file_path):
    # Load data from the CSV file
    movie_data = pd.read_csv(file_path)
    # Return data as a dictionary where keys are movie IDs
    return {row['movieId']: {'title': row['title'], 'genres': row['genres']} for _, row in movie_data.iterrows()}

def create_df_csv_movie_recommendations(final_topKmovies, moviedata):
    # Creazione di un DataFrame vuoto
    df = pd.DataFrame(columns=['iteration', 'movieId', 'title', 'rating'])

    # Iterazione su ogni mappa nella lista final_topKmovies
    for iteration, movie_map in enumerate(final_topKmovies, start=0):
        for movie_id, rating in movie_map.items():
            # Aggiungi una riga al DataFrame con i valori corrispondenti
            title = moviedata[movie_id]['title']
            df = pd.concat([df, pd.DataFrame({'iteration': [iteration], 'movieId': [movie_id], 'title': [title], 'rating': [rating]})])

    # Salva il DataFrame in un fileCSV
    df.to_csv("output/topkmovies.csv", index=False)




def main():
    '''          
    users = []
    # Load the data
    movie_data = load_movie_data("dataset/ml-latest-small/movies.csv")
    data = pd.read_csv("dataset/ml-latest-small/ratings.csv")
    

    # Crea cartella di output se già non esiste
    if not os.path.exists("output"):
        # Se la cartella non esiste, creala
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
    
    # considero tutte le predizioni calcolate, non solo quelle in comune tra tutti gli users
    all_movies_predictions = seq.create_user_ratings_dataframe(predictions_df, users)
    all_movies_predictions.to_csv("output/all_movies.csv", index=False)
    
    '''
      
# Il main parte da qui se si hanno gia' le predictions
#############################    
    data = pd.read_csv("dataset/ml-latest-small/ratings.csv")
    movie_data = load_movie_data("dataset/ml-latest-small/movies.csv")
    users = [34,22,75,64,4]
    all_movies_predictions = pd.read_csv('output/all_movies.csv')
#############################
    
    while True:
        print("Enter the value of how many top k items must to be considered:")
        k = input()

        if not k.isdigit() or int(k) < 2 or int(k) > 10:
            print("Make sure to enter a value between 2 to 10. Please try again.")
        else:
            break

    topk = int(k)

    final_topk_movies = [] # lista di tutti i k movies di tutte le iterazioni
    setTopKmovies = {}  # Usiamo un dizionario
    new_predictions = all_movies_predictions # variabile di appoggio per la prima iterazione
    
    # verfico se presente file CSV con predictions precedenti, e se presente lo elimino
    csv_file = "output/satisfaction.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)

        # Esegui il ciclo per il numero di iterazioni desiderato
    for j in range(31):
        print(f"Iteration {j}")
        
        if j == 0:
            # Nella prima iterazione utilizza le previsioni originali
            
            setTopKmovies = seq.sdda(users, j, topk, setTopKmovies, all_movies_predictions, new_predictions)
            final_topk_movies.append(setTopKmovies)
        else:
            # Rimuovi i film selezionati nelle iterazioni precedenti dalle previsioni
            new_predict = seq.change_predictions(new_predictions, setTopKmovies)
        
            # Calcola i nuovi film top-k e aggiorna setTopKmovies
            setTopKmovies = seq.sdda(users, j, topk, setTopKmovies, all_movies_predictions, new_predict)
            final_topk_movies.append(setTopKmovies)
            new_predictions = new_predict
        
        print(f"Iterazione {j} --> Top k movies: {setTopKmovies}\n")
    
    # creo un df e poi un file csv con tutte le raccomandazioni di tutte le iterazioni
    create_df_csv_movie_recommendations(final_topk_movies, movie_data)

    #Grafici
    pl.plot_scores_from_csv(users, csv_file) # grafico delle satisfaction di ogni utente per ogni iterazione
    pl.plot_groupDis_and_groupSat_from_csv(csv_file) # grafico dei valori di groupDis e groupSat ad ogni iterazione




if __name__ == "__main__":
    main()
