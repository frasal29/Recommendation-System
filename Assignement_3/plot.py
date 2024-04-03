import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_scores_from_csv(user_ids, csv_file):

    # Find the index of the first '_' and the dot in the file path
    first_underscore_index = csv_file.find('_')
    dot_index = csv_file.find('.')

    # Extract the substring between the underscore and the dot
    if first_underscore_index != -1 and dot_index != -1:
        extracted_text = csv_file[first_underscore_index + 1:dot_index]

    # Read data from the CSV file
    df = pd.read_csv(csv_file)

    # Extract columns of scores for the specified users
    user_columns = [f"user_{user_id}" for user_id in user_ids]

    # Convert scores to numbers (float)
    df[user_columns] = df[user_columns].apply(pd.to_numeric, errors='coerce')

    # Calculate the total number of users
    num_users = len(user_ids)
    num_iterations = len(df)

    # Generate unique colors for each user
    color_palette = plt.cm.tab10.colors
    user_colors = dict(zip(user_ids, color_palette[:num_users]))

    # Create subplots for each iteration
    fig, axs = plt.subplots(1, num_iterations, figsize=(8*num_iterations, 10))

    for i, (_, row) in enumerate(df.iterrows()):
        iteration_scores = row[user_columns].values
        
        # Bars for each user
        bars = axs[i].bar(np.arange(num_users), iteration_scores, color=[user_colors[user_id] for user_id in user_ids], width=0.9)
        axs[i].set_title(f'Iteration {i+1}', fontsize=20)
        axs[i].set_xlabel('User ID', fontsize=15)
        axs[i].set_ylabel('Satisfaction', fontsize=15)
        axs[i].set_ylim(0, 1)  # Set y limit from 0 to 1
        axs[i].grid(axis='y', linestyle='--', alpha=0.8)
        
        # Set finer values on the y-axis
        axs[i].set_yticks(np.arange(0, 1.1, 0.1))
        
        # User labels on the x-axis
        axs[i].set_xticks(np.arange(len(user_ids)))
        axs[i].set_xticklabels(user_ids, rotation=45, ha='right')

        # Add labels above the bars
        for bar, score in zip(bars, iteration_scores):
            axs[i].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{score:.2f}', ha='center', va='bottom', fontsize=10)

    fig.savefig(f"output/satisfaction_plot_{extracted_text}.png")



def plot_groupDis_and_groupSat_from_csv(csv_file):
    
    # Find the index of the first '_' and the dot in the file path
    first_underscore_index = csv_file.find('_')
    dot_index = csv_file.find('.')

    # Extract the substring between the underscore and the dot
    if first_underscore_index != -1 and dot_index != -1:
        extracted_text = csv_file[first_underscore_index + 1:dot_index]

    
    
    
    # Read data from the CSV file
    df = pd.read_csv(csv_file)

    # Extract groupDis and groupSat values
    groupDis_values = df['groupDis'].values
    groupSat_values = df['groupSat'].values

    # Calculate the total number of rows in the DataFrame
    num_iterations = len(df)

    # Generate values for the x-axis (Iteration)
    x_values = range(1, num_iterations + 1)

    # Generate the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, groupDis_values, marker='o', color='skyblue', linewidth=2, markersize=8, label='groupDis')
    plt.plot(x_values, groupSat_values, marker='o', color='salmon', linewidth=2, markersize=8, label='groupSat')
    plt.title('groupDis and groupSat per Iteration', fontsize=20)
    plt.xlabel('Iterations', fontsize=15)
    plt.ylabel('Values', fontsize=15)
    plt.xticks(x_values)
    plt.grid(True, linestyle='--', alpha=0.8)
    plt.legend()
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(f"output/groupDis_groupSat_plot_{extracted_text}.png")
