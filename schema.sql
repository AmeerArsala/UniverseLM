-- Drop existing tables if they exist
DROP TABLE IF EXISTS belongings;
DROP TABLE IF EXISTS chunks_lore;
DROP TABLE IF EXISTS lore;
DROP TABLE IF EXISTS chunks;
DROP TABLE IF EXISTS users_communities;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS communities;

-- Create tables

-- Human Users
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE
);

CREATE TABLE communities(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE -- this is more like an @, which is unique to each community
);

-- Junction table between users and communities for many-to-many relationship 
CREATE TABLE users_communities(
  user_id INTEGER REFERENCES users(id),
  community_id INTEGER REFERENCES communities(id)
);

CREATE TABLE chunks(
  id BIGINT PRIMARY KEY,

  name TEXT NOT NULL,
  profile TEXT NOT NULL,
  community_id INTEGER REFERENCES communities(id),
  parent_chunk INTEGER REFERENCES chunks(id),  -- can be NULL if no parent Chunk

  UNIQUE(community_id, name) -- query with this
);

-- "Knowledge"
CREATE TABLE lore(
  id SERIAL PRIMARY KEY,
  lore_text TEXT NOT NULL,

  UNIQUE(lore_text)
);

-- Junction table between chunks and lore to deal with the many-to-many relationships
CREATE TABLE chunks_lore(
  chunk_id BIGINT REFERENCES chunks(id),
  lore_id INTEGER REFERENCES lore(id),

  CONSTRAINT chunks_lore_pk PRIMARY KEY(chunk_id, lore_id)
);

-- "Data"/"Information"
CREATE TABLE belongings(
  id SERIAL PRIMARY KEY,
  content TEXT,
  owner BIGINT REFERENCES chunks(id)
);
