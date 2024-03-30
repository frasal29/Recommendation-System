import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_scores_from_csv(user_ids, csv_file):
    # Leggi i dati dal file CSV
    df = pd.read_csv(csv_file)

    # Estrai le colonne dei punteggi per gli utenti specificati
    user_columns = [f"user_{user_id}" for user_id in user_ids]

    # Converti i punteggi in numeri (float)
    df[user_columns] = df[user_columns].apply(pd.to_numeric, errors='coerce')

    # Calcola il numero totale di utenti
    num_users = len(user_ids)
    num_iterations = len(df)

    # Genera colori unici per ciascun utente
    color_palette = plt.cm.tab10.colors
    user_colors = dict(zip(user_ids, color_palette[:num_users]))

    fig, axs = plt.subplots(1, num_iterations, figsize=(8*num_iterations, 10))

    for i, (_, row) in enumerate(df.iterrows()):
        iteration_scores = row[user_columns].values
        
        # Barre per ciascun utente
        bars = axs[i].bar(np.arange(num_users), iteration_scores, color=[user_colors[user_id] for user_id in user_ids], width=0.9)
        axs[i].set_title(f'Iteration {i+1}', fontsize=20)
        axs[i].set_xlabel('User ID', fontsize=15)
        axs[i].set_ylabel('Satisfaction', fontsize=15)
        axs[i].set_ylim(0, 1)  # Imposta il limite y da 0 a 1
        axs[i].grid(axis='y', linestyle='--', alpha=0.8)
        
        # Imposta valori più granulari sull'asse y
        axs[i].set_yticks(np.arange(0, 1.1, 0.1))
        
        # Etichette degli utenti sull'asse x
        axs[i].set_xticks(np.arange(len(user_ids)))
        axs[i].set_xticklabels(user_ids, rotation=45, ha='right')

        # Aggiungi le etichette sopra le barre
        for bar, score in zip(bars, iteration_scores):
            axs[i].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{score:.2f}', ha='center', va='bottom', fontsize=10)

    fig.savefig("output/satisfaction_plot.png")






def plot_groupDis_and_groupSat_from_csv(csv_file):
    # Leggi i dati dal file CSV
    df = pd.read_csv(csv_file)

    # Estrai i valori di groupDis e groupSat
    groupDis_values = df['groupDis'].values
    groupSat_values = df['groupSat'].values

    # Calcola il numero totale di righe nel DataFrame
    num_iterations = len(df)

    # Genera valori per l'asse x (Iteration)
    x_values = range(1, num_iterations + 1)

    # Genera il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, groupDis_values, marker='o', color='skyblue', linewidth=2, markersize=8, label='groupDis')
    plt.plot(x_values, groupSat_values, marker='o', color='salmon', linewidth=2, markersize=8, label='groupSat')
    plt.title('groupDis e groupSat per Iteration', fontsize=20)
    plt.xlabel('Iterations', fontsize=15)
    plt.ylabel('Values', fontsize=15)
    plt.xticks(x_values)
    plt.grid(True, linestyle='--', alpha=0.8)
    plt.legend()
    plt.tight_layout()

    # Salva il grafico come immagine
    plt.savefig("output/groupDis_groupSat_plot.png")