# UniverseLM

UniverseLM is All You Need

## Description

UniverseLM is a multi-agent system simulator / text adventure that allows users to create societies of agents and be able to chat with them. Through this process, lore may be created (of a society), of which agents will know about and users will be able to speak to them about. As the lore increases, so too will the worldbuilding of the society. Have fun!

## Setup (locally)

1. (Optional; for dev) Create & Activate the Conda/Mamba/Micromamba environment if not already

```
micromamba create -f environment.yml
micromamba activate universe-lm
```

2. Install extra dependencies

```
poetry install
```

WARNING FOR DEV: due to a bug between conda envs mixed with poetry, you will also need to run this command after installing the poetry dependencies:

```
micromamba install -c conda-forge packaging=23.2
```

3. Run the app (you can remove/change the host)

```
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

4. (Optional) Run the front end (make sure you have pnpm installed)

```
cd frontend && pnpm install
```

```
pnpm run dev
```

## Roadmap

- [ ] Finish the technology
- [ ] Finish the application (the backend + database)
- [ ] Finish the front end
- [ ] User Authentication
- [ ] Switch from SvelteKit to Astro (in order to use mainly Svelte but with React thrown in for support)

## Other TODOs

- [ ] Finish API routes -> Make API keys for authenticated users who pay for no reason
- [ ] Scale with PostgresML + Pinecone

## Bloat

- [ ] Create python package for API like OpenAI API
- [ ] CLI Tool
- [ ] Discord Bot
- [ ] Slack Bot
- [ ] Multimodality (images, music, assets)
