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

```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
DATASET_PATH=
DATASTORE_DIR=
```

- Dataset path is the path to the dataset folder eg. `"/Users/kimstocker/projects/pdfsReadingAgent/data"`
- Datastore is the PersistentDB path eg.`"/Users/kimstocker/projects/pdfsReadingAgent/PersistentDB"`

add .env to

# Run app

```
uv run streamlit run app.py --server.port=8510
```
