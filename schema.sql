PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
  user_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  name         TEXT NOT NULL,
  email        TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resumes (
  resume_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id          INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  title            TEXT NOT NULL,
  address          TEXT,
  linkedin         TEXT,
  career_objective TEXT,
  created_date     TEXT NOT NULL DEFAULT (datetime('now')),
  last_modified    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS education (
  edu_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  resume_id       INTEGER NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
  institution     TEXT NOT NULL,
  degree          TEXT NOT NULL,
  graduation_year INTEGER NOT NULL CHECK (graduation_year BETWEEN 1950 AND 2100),
  result          TEXT
);
CREATE TABLE IF NOT EXISTS experience (
  exp_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  resume_id        INTEGER NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
  company          TEXT NOT NULL,
  job_title        TEXT NOT NULL,
  duration         TEXT NOT NULL,
  responsibilities TEXT
);
-- Covers Skill (ER) + AdditionalInfo (class diagram): technical, soft, language, certification, other
CREATE TABLE IF NOT EXISTS skills (
  skill_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  resume_id  INTEGER NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
  skill_name TEXT NOT NULL,
  category   TEXT NOT NULL CHECK (category IN ('technical','soft','language','certification','other'))
);
