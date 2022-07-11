CREATE TABLE IF NOT EXISTS users  (
    id             SERIAL  PRIMARY KEY NOT NULL,
    username       TEXT    UNIQUE NOT NULL,
    password       TEXT    NOT NULL,
    email          TEXT    UNIQUE NOT NULL,
    admin          INT     DEFAULT 0 NOT NULL,
    gender         TEXT    NOT NULL,
    birth_year     INT     NOT NULL,
);

-- CREATE TABLE IF NOT EXISTS saved_posts (
--     userID INT NOT NULL;
--     postID INT NOT NULL;
-- )

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    published_date DATE NOT NULL DEFAULT CURRENT_DATE,
    authorID INT NOT NULL DEFAULT 0,
    topic INT NOT NULL,
    tags INT[] DEFAULT [] -- Array of tags ID

    CONSTRAINT fk_author
        FOREIGN KEY (authorID)
        REFERENCES users(id)
         -- Provide option to delete their posts &
         -- comments when account is delete
);

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT UNIQUE NOT NULL,
);

CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT UNIQUE NOT NULL,
);

CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY NOT NULL,
    type INT UNIQUE NOT NULL,
    postID INT NOT NULL,

    CONSTRAINT fk_post
        FOREIGN KEY (postID)
        REFERENCES posts(id)
);

ALTER TABLE posts ADD FOREIGN KEY (topic) REFERENCES topics(id);
