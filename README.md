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

# Distribution of labor

Ozge - UI & Backend\
Ricardo & Fred - BERT & BM25\
Georgia - Video