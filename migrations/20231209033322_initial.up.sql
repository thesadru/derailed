CREATE TABLE IF NOT EXISTS users (
    id BIGINT NOT NULL PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    display_name VARCHAR(32) DEFAULT NULL,
    password TEXT NOT NULL,
    flags BIGINT NOT NULL DEFAULT 0,
    invited_by BIGINT
);
CREATE TABLE IF NOT EXISTS user_settings (
    user_id BIGINT PRIMARY KEY,
    theme TEXT NOT NULL DEFAULT "dark",
    status INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS channels (
    id BIGINT PRIMARY KEY,
    type INT NOT NULL,
    name VARCHAR(32),
    last_message_id BIGINT,
    FOREIGN KEY (parent_id)
        REFERENCES channels (id)
        ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS channel_members (
    channel_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (channel_id, user_id),
    FOREIGN KEY (channel_id)
        REFERENCES channels (id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS messages (
    id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    author_id BIGINT,
    content VARCHAR(4096),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    edited_timestamp TIMESTAMP WITH TIME ZONE,
    referenced_message_id BIGINT,
    FOREIGN KEY (channel_id)
        REFERENCES channels (id)
        ON DELETE CASCADE,
    FOREIGN KEY (author_id)
        REFERENCES users (id)
        ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS read_states (
    user_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL,
    mentions BIGINT NOT NULL DEFAULT 0,
    last_message_id BIGINT,
    PRIMARY KEY (user_id, channel_id),
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    FOREIGN KEY (channel_id)
        REFERENCES channels (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS message_reactions (
    message_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    emoji TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (message_id, user_id, emoji),
    FOREIGN KEY (message_id)
        REFERENCES messages (id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS relationships (
    origin_user_id BIGINT NOT NULL,
    target_user_id BIGINT NOT NULL,
    relation INT NOT NULL,
    PRIMARY KEY (origin_user_id, target_user_id),
    FOREIGN KEY (origin_user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,
    FOREIGN KEY (target_user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS invite_codes (
    id TEXT PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    FOREIGN KEY (owner_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);