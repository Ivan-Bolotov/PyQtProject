CREATE TABLE saved_notes (
    id   INTEGER   PRIMARY KEY AUTOINCREMENT
                   UNIQUE
                   NOT NULL,
    type TEXT (16) NOT NULL,
    data TEXT      NOT NULL
);