# Recommender System Demo Project

Recommendation system has been a popular topic for research in the field of computer science. This demo project aims to allow user to mimic the video platform browsing experience, while researchers and developers may explore the performance of different recommendation strategies and methodologies. 

## Prerequisites

1. Create Python virtual environment and install all packages according to ```requirement.txt```.
2. Download MovieLens 1M Dataset from [MovieLen | GroupLens](https://grouplens.org/datasets/movielens/)
3. Unzipped downloaded dataset and extract ```ml-1m``` folder to the directory ```./data/raw```

## Installation

1. Clone or download this repository.

## Usage - Interactive Dashboard

1. Before any operation, run ```data_preprocessing.py``` under the directory ```./backend```
2. Under the root directory, run ```uvicorn backend.fast_api.main:app --reload``` to start the backend server

## Usage - Methodologies Evaluation and Experiment

1. Before any operation, run ```data_preprocessing.py``` and ```evaluation_data_preprocessing.py``` under the directory ```./backend```
2. For evaluation purpose, activate ```eval_mode``` for recommenders defined in ```recommenders.py``` under the directory ```./backend```
3. Parameter choices and alternative preprocessing or computation strategies can be explored and adjusted in ```evaluation.py``` under the directory ```./backend```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.