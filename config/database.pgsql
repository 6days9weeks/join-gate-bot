CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    prefix TEXT
);
-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more guild-specific
-- settings.

CREATE TABLE IF NOT EXISTS join_gate(
    guild_id BIGINT PRIMARY KEY,
    enabled BOOLEAN,
    channel BIGINT,
    restrict_role BIGINT,
    staff_role BIGINT,
    default_delay BIGINT DEFAULT 10,
    default_amount BIGINT DEFAULT 5
);


CREATE TABLE IF NOT EXISTS user_settings(
    user_id BIGINT PRIMARY KEY
);
-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more user-specific
-- settings.
-- This table is not suitable for member-specific settings as there's no
-- guild ID specified.

CREATE TABLE IF NOT EXISTS blacklisted_users(
    user_id BIGINT PRIMARY KEY,
    reason TEXT
);
-- A table of blacklisted users.
-- This is required for VBU and should not be deleted.
-- This table is not suitable for guild only blacklist as there's no
-- guild ID specified.

CREATE TABLE IF NOT EXISTS command_settings(
    guild_id BIGINT,
    command TEXT,
    enabled BIGINT,
    PRIMARY KEY(guild_id, command)
);
-- A table of command settings.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more guild-specific
-- settings.
