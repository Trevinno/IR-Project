# Welcome to the wonderful IR Group 100 Repo 😃

This repo contains the implementation for Assignment II for the module Information Retrival.
The project consists of using BM25 with conjunction of BERT word embeddings to conduct get a relevant search of food recipies.
The dataset we will we working with is found here: https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions.

# Project Layout

The layout is divided in the following way:\
\
information-retrieval-bert/\
│\
├── data/\
│   ├── raw/               # Original document collection, not hosted in the remote repo\
│   └── processed/         # Bert embeddings preprocessed document colletion, also not hosted in the remote repo\ 
│\
├── ir_model/\
│   └── src/               # IR Model implementation\
│\
├── backend/\
│   └── /src               # Backend implementation\
│\
├── frontend/              # UI components\
│\
├── tests/                 # Tests for all components\
│\
├── README.md\
└── .gitignore

# Running the application
In order two run the application only two "programs need to be running", the backend directory and the front end directory. You would want to go inside the backend directory and run, py .\app.py. For the front end you would want to go inside the frontend directory, then the recipes_frontend directory and run, npm run dev. These two commands need to be ran after downloading the dependencies. To download the dependencies for the flask app run, pip install -r requirements.txt. To download the dependencies for the front end app run, npm install. More specific instructions are included in each of the directories where the commands need to be run. When running the application make sure to wait after each search, given that clicking the search bar several times can make the application crash. Also, to find the location where the front end app is being run, look for the localhost address shown when you run, npm run dev. Since the full version of the program with all its dependencies could
not be uploaded due to size limitations, you need to install all the libraries to be able to run the code. Look in the respective directories the README files to see what libraries to install.