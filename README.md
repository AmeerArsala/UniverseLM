# UniverseLM

UniverseLM is All You Need

## Description

UniverseLM is a multi-agent system simulator / text adventure that allows users to create societies of agents and be able to chat with them. Through this process, lore may be created (of a society), of which agents will know about and users will be able to speak to them about. As the lore increases, so too will the worldbuilding of the society. Have fun!

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
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
