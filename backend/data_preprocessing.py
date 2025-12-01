import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load and preprocess the raw ratings data
ratings = pd.read_csv('../data/raw/ml-1m/ratings.dat', sep='::', engine='python', names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
user_item_matrix = ratings.pivot(index='UserID', columns='MovieID', values='Rating').fillna(0)
print("Data Preprocessing: User-Item matrix extracted successfully.")
item_user_matrix = user_item_matrix.T.fillna(0)
print("Data Preprocessing: Item-User matrix converted successfully.")
item_similarity_matrix = cosine_similarity(item_user_matrix)
print("Data Preprocessing: Cosine similarity matrix computed successfully.")

user_mean = item_user_matrix.mean(axis=1)
adjusted_item_user_matrix = item_user_matrix.sub(user_mean, axis=0).fillna(0)
adjusted_item_similarity_matrix = cosine_similarity(adjusted_item_user_matrix)
print("Data Preprocessing: Adjusted cosine similarity matrix computed successfully.")

# Save the processed matrices for local storage
user_item_matrix.to_pickle('../data/processed/user_item_matrix.pkl')
print("Data Preprocessing: User-Item matrix saved successfully.")

item_user_matrix.to_pickle('../data/processed/item_user_matrix.pkl')
print("Data Preprocessing: Item-User matrix saved successfully.")

item_similarity_matrix_df = pd.DataFrame(item_similarity_matrix, index=item_user_matrix.index, columns=item_user_matrix.index)
item_similarity_matrix_df.to_pickle('../data/processed/item_similarity_matrix_df.pkl')
print("Data Preprocessing: Cosine similarity matrix saved successfully.")

adjusted_item_similarity_matrix_df = pd.DataFrame(adjusted_item_similarity_matrix, index=item_user_matrix.index, columns=item_user_matrix.index)
adjusted_item_similarity_matrix_df.to_pickle('../data/processed/adjusted_item_similarity_matrix_df.pkl')
print("Data Preprocessing: Adjusted cosine similarity matrix saved successfully.")

# Popularity data preprocessing
popularity = ratings.groupby('MovieID')["Rating"].count().reset_index()
popularity.columns = ['MovieID', 'NumRatings']
popularity.to_pickle('../data/processed/popularity.pkl')
print("Data Preprocessing: Popularity data saved successfully.")

# Optional preprocessing for other .dat files
users = pd.read_csv('../data/raw/ml-1m/users.dat', sep='::', engine='python', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
users['Gender'] = users['Gender'].map({'F': 0, 'M': 1}) # Gender encoding
users.to_pickle('../data/processed/users.pkl')
print("Data Preprocessing: Users data saved successfully.")

movies = pd.read_csv('../data/raw/ml-1m/movies.dat', sep='::', engine='python', names=['MovieID', 'Title', 'Genres'], encoding='latin-1')
movies["GenresStr"] = movies["Genres"] # Preserve original genres text
genres_split = movies['Genres'].str.get_dummies(sep='|') # One-hot encoding for genres
movies = pd.concat([movies[['MovieID', 'Title', 'GenresStr']], genres_split], axis=1)
movies.to_pickle('../data/processed/movies.pkl')
print("Data Preprocessing: Movies data saved successfully.")

# Content similarity matrix computation
content_similarity_matrix_one_hot = cosine_similarity(genres_split)
pd.DataFrame(content_similarity_matrix_one_hot, index=movies['MovieID'], columns=movies['MovieID']).to_pickle('../data/processed/content_similarity_matrix_one_hot.pkl')
print("Data Preprocessing: Content similarity matrix (one-hot) saved successfully.")

movies["ContentText"] = movies['Title'] + " " + movies['GenresStr']

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['ContentText'])
tfidf_similarity_matrix = cosine_similarity(tfidf_matrix)
pd.DataFrame(tfidf_similarity_matrix, index=movies['MovieID'], columns=movies['MovieID']).to_pickle('../data/processed/content_similarity_matrix_tfidf.pkl')
print("Data Preprocessing: Content similarity matrix (TF-IDF) saved successfully.")

# User correlation matrix computation
user_correlation_matrix = user_item_matrix.T.corr()
user_correlation_matrix.to_pickle('../data/processed/user_correlation_matrix.pkl')
print("Data Preprocessing: User correlation matrix saved successfully.")