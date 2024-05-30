CREATE TABLE people (
    id             INTEGER   PRIMARY KEY AUTOINCREMENT
                             UNIQUE
                             NOT NULL,
    name           TEXT (64) NOT NULL,
    surname        TEXT (64),
    lastname       TEXT (64),
    date_of_birth  TEXT (16),
    mother         INTEGER,
    father         INTEGER,
    alive          INTEGER   NOT NULL,
    date_of_death  TEXT (16),
    status         TEXT (16),
    newly_deceased INTEGER   NOT NULL,
    FOREIGN KEY(mother) REFERENCES people(id),
    FOREIGN KEY(father) REFERENCES people(id)
);