CREATE TABLE game (
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID NOT NULL REFERENCES user_accounts (id),
    game_step        VARCHAR NOT NULL,
    wait_status      VARCHAR NOT NULL,
    status           VARCHAR NOT NULL,
    current_questions UUID[] DEFAULT '{}' REFERENCES questions (id),
    step_percentage  FLOAT DEFAULT 0,
    completed_question UUID[] DEFAULT '{}' REFERENCES user_questions (id),
    is_deleted       TIMESTAMPTZ DEFAULT NULL,
    completed_at     TIMESTAMPTZ DEFAULT NULL
);

CREATE INDEX game_user_id_idx ON game (user_id);