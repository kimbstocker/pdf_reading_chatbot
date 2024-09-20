# Envrionemnt Setup

Install `python` and `uv` for 'Extremely fast Python package installer and resolver, written in Rust'

```
brew install python
brew install uv
```

# Install dependencies:

```
uv sync
```

# Create a local .env file

You will need set up a number of API keys for this to work.
Openai and Mistralai require you to setup a payment plan and add payment credit for the API keys to work
Once created the API keys, on your terminal run the below command

```
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
export LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"

```

And in your .env file, add the below env vars

```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
DATASET_PATH=
DATASTORE_DIR=

OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"
MISTRALAI_API_KEY="YOUR_MISTRALAI_API_KEY"
DATASET_PATH="/Users/{YOUR_USERNAME}/{PROJECT_DIR}/model/data"
DATASTORE_DIR="/Users/{YOUR_USERNAME}/{PROJECT_DIR}/model/PersistentDB"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_TRACING_V2="true"

```

- Dataset path is the path to the dataset folder eg. `"/Users/kimstocker/projects/pdfsReadingAgent/data"`
- Datastore is the PersistentDB path eg.`"/Users/kimstocker/projects/pdfsReadingAgent/PersistentDB"`

add .env to

# Run app

```
uv run streamlit run app.py --server.port=8510
```
