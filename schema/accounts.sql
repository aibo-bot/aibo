CREATE TABLE IF NOT EXISTS accounts(
    user_id BIGINT PRIMARY KEY NOT NULL,
    currency INTEGER DEFAULT 0 NOT NULL,
    level SMALLINT DEFAULT 1 NOT NULL,
    exp INTEGER DEFAULT 0 NOT NULL,
    max_exp INTEGER DEFAULT 100 NOT NULL,
    description VARCHAR(50) NOT NULL DEFAULT '*This user has no custom about me*'
);