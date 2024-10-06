CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    state char(2) NOT NULL
);

CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('coach', 'athlete', 'official')),
    date_of_birth DATE NOT NULL,
    active BOOLEAN NOT NULL,
    team_id INT,
    CONSTRAINT fk_team_id FOREIGN KEY (team_id) REFERENCES team(team_id)
);


CREATE TABLE meet (
    meet_id SERIAL PRIMARY KEY,
    meet_name varchar(255) NOT NULL,
    pool_name varchar(255),
    pool_city varchar(255) NOT NULL,
    pool_state char(2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE swims (
    distance INT NOT NULL,
    stroke CHAR(2) CHECK (stroke IN ('FR', 'BK', 'BR', 'FL', 'IM')),
    time TIME NOT NULL,
    date DATE NOT NULL,
    person_id INT NOT NULL,
    meet_id INT NOT NULL,
    CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES person(person_id),
    CONSTRAINT fk_meet_id FOREIGN KEY (meet_id) REFERENCES meet(meet_id)
);
