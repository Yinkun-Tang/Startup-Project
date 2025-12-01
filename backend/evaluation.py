import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from recommenders import UserBasedCFRecommender, ItemBasedCFRecommender, ContentBasedRecommender, HybridRecommender

TOP_K = 10
TEST_RATIO = 0.2
RANDOM_SEED = 42

user_item_matrix = pd.read_pickle('../data/processed/user_item_matrix.pkl')

# Split data into training and test sets
np.random.seed(RANDOM_SEED)
train_matrix = user_item_matrix.copy()
test_matrix = pd.DataFrame(0, index=user_item_matrix.index, columns=user_item_matrix.columns)

for user in user_item_matrix.index:
    rated_items = user_item_matrix.loc[user][user_item_matrix.loc[user] > 0].index.tolist()
    n_test_items = max(1, int(len(rated_items) * TEST_RATIO))
    test_items = np.random.choice(rated_items, size=n_test_items, replace=False)
    
    train_matrix.loc[user, test_items] = 0
    test_matrix.loc[user, test_items] = user_item_matrix.loc[user, test_items]

def precision_recall_f1_hit(recommended, actual, k=TOP_K):
    recommended_k = recommended[:k]
    actual = set(actual[actual > 0].index)
    if not actual:
        return 0, 0, 0, 0
    
    hits = len(set(recommended_k) & actual)
    precision = hits / k
    recall = hits / len(actual)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    hit_rate = 1 if hits > 0 else 0
    return precision, recall, f1, hit_rate


models = {
"HybridRecommender": HybridRecommender(top_k=TOP_K, alpha=0.8)
}

results = defaultdict(list)

for model_name, model in tqdm(models.items(), desc="Models", position=0):
    precisions = []
    recalls = []
    f1s = []
    hit_rates = []
    
    recommended_items_all = set()
    
    for user in tqdm(train_matrix.index, desc=f"{model_name} Users", position=1, leave=False):
        recommended_items = model.recommend(user)
        actual_items = test_matrix.loc[user]
        
        precision, recall, f1, hit_rate = precision_recall_f1_hit(recommended_items, actual_items, k=TOP_K)
        
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
        hit_rates.append(hit_rate)
        
        recommended_items_all.update(recommended_items)
    
    user_coverage = np.mean(hit_rates)
    catalog_coverage = len(recommended_items_all) / user_item_matrix.shape[1]
    
    results["Model"].append(model_name)
    results["Precision"].append(np.mean(precisions))
    results["Recall"].append(np.mean(recalls))
    results["F1"].append(np.mean(f1s))
    results["UserCoverage"].append(user_coverage)
    results["CatalogCoverage"].append(catalog_coverage)

results_df = pd.DataFrame(results)
print("Evaluation Results:")
print(results_df.sort_values(by="F1", ascending=False))