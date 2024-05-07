-- Drop existing tables if they exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS chunks;
DROP TABLE IF EXISTS communities;
DROP TABLE IF EXISTS lore;
DROP TABLE IF EXISTS belongings;

-- Create tables

-- Human Users; There can be AI users, but the human users must be registered with email
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  chunk_name TEXT REFERENCES chunks(name)
);

CREATE TABLE chunks(
  name TEXT PRIMARY KEY,
  profile TEXT,
  community_id INTEGER REFERENCES communities(id),
  parent_chunk TEXT REFERENCES chunks(name)
);

CREATE TABLE communities(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- "Knowledge"
CREATE TABLE lore(
  id SERIAL PRIMARY KEY,
  lore_text TEXT NOT NULL,
  about_chunk TEXT REFERENCES chunks(name)
);

-- "Data"/"Information"
CREATE TABLE belongings(
  id SERIAL PRIMARY KEY,
  content TEXT,
  owner TEXT REFERENCES chunks(name)
);
