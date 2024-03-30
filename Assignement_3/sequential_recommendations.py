import pandas as pd
from itertools import islice
import numpy as np
import csv
import os

def create_user_ratings_dataframe(input_df, users):
    # Estrai tutti i movieId distinti dalla tabella fornita
    distinct_movie_ids = set(input_df['movieId'])
    
    # Crea un dizionario per memorizzare i rating degli utenti per ciascun movieId
    user_ratings_dict = {f'user_{user}': [] for user in users}
    user_ratings_dict['movieId'] = []
    
    # Riempie il dizionario con i valori di rating corrispondenti agli utenti
    for movie_id in distinct_movie_ids:
        user_ratings_dict['movieId'].append(movie_id)
        for user in users:
            # Trova il rating corrispondente all'utente e al movieId
            rating = input_df[(input_df['movieId'] == movie_id) & (input_df['userId'] == user)]['rating'].values
            if len(rating) > 0:
                user_ratings_dict[f'user_{user}'].append(rating[0])
            else:
                # Se non c'è un rating per quell'utente, assegna 0
                user_ratings_dict[f'user_{user}'].append(0)
    
    # Crea un nuovo DataFrame utilizzando il dizionario dei rating degli utenti
    user_ratings_df = pd.DataFrame(user_ratings_dict)
    
    return user_ratings_df



def commonIdMovie(predictions_df, users):
    result_rows = []
    
    unique_movie_ids = set(predictions_df['movieId'])

    # Crea i nomi delle colonne in base all'indice degli utenti nella lista 'users'
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
    
    
    # Ordina il dataframe per 'movieId'
    new_data = new_data.sort_values(by='movieId', ascending=True)
    
    return new_data

# Funzione che restituisce i primi k movie presenti nel data frame di gruppo, 
def topKMovies_group(data, k):
    # Controlla se k è maggiore della lunghezza del dataframe
    if k >= len(data):
        return set(data['movieId'])
    
    # Restituisci i primi k movieId
    return set(data['movieId'].head(k))


#Funzione SAT, prende: un user, intero k, ids dei top k movie gruppo, Dataframe predizioni singolare
def sat(user, k, setTopkMovie, dataPredictions, new_predictions):

    df = dataPredictions
    
    # New prediction per Auij
    data = new_predictions

    # Ordina le righe in base ai valori di rating in ordine decrescente
    sorted_df = data.sort_values(by=f'user_{user}', ascending=False)
    
    # Prendi solo le prime k righe
    top_10_df = sorted_df.head(k)

    # Calcola la somma di tutti i valori di rating presenti
    #denominator = top_10_df[f'user_{user}'].sum()
    denominator=0
    numerator = 0
    for index, row in top_10_df.iterrows():
        value = row[f'user_{user}']
        denominator+=value
        
    numerator = 0  # Inizializzazione della variabile per accumulare i valori delle celle

    for movie in setTopkMovie.keys(): # itero sulle chiavi cioè sui movie id
        # Seleziona tutte le righe del DataFrame con movieId uguale a movie
        selected_rows = df[df['movieId'] == movie]

        # Estrai il valore dalla colonna user_{user} per le righe selezionate
        user_column_values = selected_rows[f'user_{user}'].values

        # Aggiungi i valori estratti alla variabile per l'accumulo
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
    
    # Calcoliamo difference e calcolo anche la groupSat e la inserisco nel csv
    list_sat = []
    for user in users:
        temp = sat(user, k, setTopkMovies, dataPredictions, new_predictions)
        list_sat.append(temp)
    #difference = max(list_sat) - min(list_sat)
    #difference = max(list_sat)
    #difference = np.mean(list_sat)
    difference = calculate_standard_deviation(users, list_sat,)

    group_sat = np.mean(list_sat)
    
    # Aggiungiamo una nuova riga al file CSV
    csv_columns = []

    csv_columns.append("iteration") # Aggiungo la colonna dell'iterazione corrente
    for user in users:
        csv_columns.append(f"user_{user}")
    
    # Aggiungiamo la colonna "groupDis" e "groupSat" se non esiste già
    csv_columns.append("groupDis")
    csv_columns.append("groupSat")
    

    
    csv_file = "output/satisfaction.csv"
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
    
    # Aggiungiamo i valori alla riga
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
    
    # Creazione del dizionario con chiave movieId e valore rating
    movie_ratings = {}

    # Selezione delle colonne in base alla lista degli utenti
    colonne_utenti = [f'user_{user}' for user in users]

    # Iterazione attraverso ogni riga del DataFrame
    for index, row in new_predictions.iterrows():
        # Salva il valore della colonna "movieId"
        movie_id = int(row['movieId'])

        # Calcolo della media e minimo dei valori delle colonne per gli utenti specificati
        valori_utenti = [row[colonna] for colonna in colonne_utenti]
        average_score = sum(valori_utenti) / len(valori_utenti)
        least_score = min(valori_utenti)
        score = ( (1-alfa) * average_score) + ( alfa * least_score)
    
        # Aggiunta della coppia movieId-rating al dizionario
        movie_ratings[movie_id] = score
    
    # Ordina il dizionario in ordine decrescente basato sui valori di rating
    sorted_ratings = dict(sorted(movie_ratings.items(), key=lambda item: item[1], reverse=True))
    

    # Ottieni solo i primi 10 elementi di sorted_ratings
    first_10_items = dict(islice(sorted_ratings.items(), k))

    
    return first_10_items

def change_predictions(all_movies_predictions, setTopKmovies):
    # Converte il set di id dei film in un insieme per una ricerca più efficiente
    setTopKmovies = set(setTopKmovies)
    
    # Filtra le righe in cui il movieId non è presente nel setTopKmovies
    filtered_predictions = all_movies_predictions[~all_movies_predictions['movieId'].isin(setTopKmovies)]
    
    return filtered_predictions





    








