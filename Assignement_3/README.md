```markdown
# Movie Sequential Recommendation System

This repository contains a Python implementation of a movie recommendation system based on collaborative filtering algorithms. The system generates movie recommendations for a group of users using both an original sequential recommendation algorithm and a revisited version of the algorithm. The predictions are made by analyzing the ratings provided by users for various movies.

## Files

- **main_assignment3.py**: The main script to execute the movie recommendation system. It orchestrates the loading of data, generation of predictions, and plotting of results.
- **pearson_similarity.py**: Contains functions to calculate Pearson correlation coefficients between users based on their movie ratings.
- **predict_rating.py**: Provides functions to predict movie ratings for users based on their similarity with other users.
- **predictions.py**: Implements functions to generate movie recommendations for a group of users using collaborative filtering techniques.
- **plot.py**: Includes functions to plot and visualize the results of the recommendation system.
- **sequential_recommendations.py**: Contains the original sequential recommendation algorithm.
- **sequential_recommendations_revisited.py**: Implements a revisited version of the sequential recommendation algorithm.

## Setup
To run the scripts in this repository, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/frasal29/Recommendation-System.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. **Download the movie dataset** (e.g., [MovieLens](https://grouplens.org/datasets/movielens/)) and place the CSV files in the `dataset/ml-latest-small/` directory.

## Usage

To use the movie recommendation system:

1. Run the `main_assignment3.py` script.
2. Follow the prompts to input the desired users and parameters for the recommendation system.
3. The system will generate predictions, plot the results, and save the output files in the `output` directory.

## Results

The output files include:

- **dataset_with_also_predictions.csv**: Contains predictions for each user.
- **all_movies.csv**: Includes all calculated predictions, not just those common to all users.
- **topkmovies_original.csv** and **topkmovies_revisited.csv**: CSV files with movie recommendations for each iteration of the original and revisited algorithms, respectively.
- **satisfaction_original.csv** and **satisfaction_revisited.csv**: CSV files with satisfaction scores and group diversity metrics for each iteration of the original and revisited algorithms, respectively.
- **satisfaction_plot_original.png** and **satisfaction_plot_revisited.png**: Plots showing user satisfaction scores for each iteration of the original and revisited algorithms, respectively.
- **groupDis_groupSat_plot_original.png** and **groupDis_groupSat_plot_revisited.png**: Plots displaying group diversity and satisfaction values for each iteration of the original and revisited algorithms, respectively.

## Contributors

- [Francesco Salienti](https://github.com/frasal29)

Feel free to contribute by forking this repository, making changes, and creating a pull request.

## Contact

For any questions or feedback, feel free to contact [francesco.salienti@gmail.com](mailto:francesco.salienti@gmail.com).
```