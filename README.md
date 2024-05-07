# UniverseLM

UniverseLM is All You Need

## Setup (locally)

1. Create & Activate the Conda/Mamba/Micromamba environment if not already

```
micromamba create -f environment.yml
micromamba activate universe-lm
```

2. Install extra dependencies

```
poetry install
```

3. Run the app

```
python3 app/main.py
```

OR

```
uvicorn app.main:api
```
