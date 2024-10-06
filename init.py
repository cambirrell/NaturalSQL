from sqlalchemy import create_engine, text, Table, MetaData
import random
import datetime
import json

random.seed(0)

config = json.load(open("config.json"))
conn_string = config["connectionString"]

engine = create_engine(conn_string)


create_team_table_command = text(
    """
    CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    state char(2) NOT NULL
);
    """
)

create_person_table_command = text(
    """
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
    """
)
create_swims_table_command = text(
    """
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
    """
)

create_meet_table_command = text(
    """
    CREATE TABLE meet (
    meet_id SERIAL PRIMARY KEY,
    meet_name varchar(255) NOT NULL,
    pool_name varchar(255),
    pool_city varchar(255) NOT NULL,
    pool_state char(2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
    );
    """
)


##make data to store in the database
names = [
    "Cameron",
    "Michael",
    "Katie",
    "Lilly",
    "Ryan",
    "Caeleb",
    "Simone",
    "Regan",
    "Lia",
    "Kathleen",
]
last_names = [
    "Smith",
    "Jones",
    "Johnson",
    "Brown",
    "Williams",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
]
roles = ["coach", "athlete", "official"]
states = [
    "CA",
    "TX",
    "FL",
    "NY",
    "PA",
    "IL",
    "OH",
    "GA",
    "NC",
    "MI",
    "WA",
    "UT",
    "AZ",
    "MA",
    "IN",
    "TN",
    "NJ",
    "MO",
    "MD",
    "WI",
]
cities = [
    "Los Angeles",
    "Houston",
    "Miami",
    "New York",
    "Philadelphia",
    "Chicago",
    "Columbus",
    "Atlanta",
    "Charlotte",
    "Detroit",
    "Seattle",
    "Salt Lake City",
    "Phoenix",
    "Boston",
    "Indianapolis",
    "Nashville",
    "Newark",
    "St. Louis",
    "Baltimore",
    "Milwaukee",
]
team_names = [
    "Dolphins",
    "Sharks",
    "Piranhas",
    "Whales",
    "Orcas",
    "Stingrays",
    "Seals",
    "Otters",
    "Turtles",
    "Tigers",
    "Lions",
    "Bears",
    "Wolves",
    "Eagles",
    "Falcons",
    "Hawks",
    "Cardinals",
    "Ravens",
    "Owls",
    "Blue Jays",
    "Penguins",
]
strokes = ["FR", "BK", "BR", "FL", "IM"]
meet_names = [
    "Winter Classic",
    "Summer Classic",
    "Spring Classic",
    "Fall Classic",
    "Holiday Invite",
    "National Championships",
    "Olympic Trials",
    "World Championships",
    "Pan Pacific Championships",
    "Junior Nationals",
    "Senior Nationals",
    "Sectionals",
    "Zones",
]
pool_names = [
    "Aquatic Center",
    "Natatorium",
    "Swim Center",
    "Swim Club",
    "Aquatic Club",
    "Aquatic Complex",
]


def create_person_table():
    with engine.connect() as conn:
        conn.execute(create_person_table_command)
        # insert data
        for i in range(200):
            first_name = names[random.randint(0, len(names) - 1)]
            last_name = last_names[random.randint(0, len(last_names) - 1)]
            role = roles[random.randint(0, len(roles) - 1)]
            date_of_birth = datetime.date(
                random.randint(1970, 2005), random.randint(1, 12), random.randint(1, 28)
            )
            active = random.choice([True, False])
            team_id = random.randint(1, 20)
            insert_person = text(
                f"""
                INSERT INTO person (first_name, last_name, role, date_of_birth, active, team_id)
                VALUES ('{first_name}', '{last_name}', '{role}', '{date_of_birth}', {active}, {team_id});
                """
            )
            conn.execute(insert_person)
            conn.commit()


def create_team_table():
    with engine.connect() as conn:
        conn.execute(create_team_table_command)
        # insert data
        for i in range(21):
            team_name = team_names[i]
            city = cities[random.randint(0, len(cities) - 1)]
            state = states[random.randint(0, len(states) - 1)]
            insert_team = text(
                f"""
                INSERT INTO team (team_id, team_name, city, state)
                VALUES ({i}, '{team_name}', '{city}', '{state}');
                """
            )
            conn.execute(insert_team)
            conn.commit()


def create_swims_table():
    with engine.connect() as conn:
        conn.execute(create_swims_table_command)
        # insert data
        for i in range(2000):
            distance = random.choice([50, 100, 200, 400, 800, 1500])
            stroke = strokes[random.randint(0, len(strokes) - 1)]
            # put limits on the time so it doesn't get too crazy and is reasonable for the distance
            if distance == 50:
                time = datetime.time(0, 0, random.randint(20, 45))
            elif distance == 100:
                time = datetime.time(0, random.randint(0, 1), random.randint(0, 30))
            elif distance == 200:
                time = datetime.time(0, random.randint(1, 3), random.randint(0, 59))
            elif distance == 400:
                time = datetime.time(0, random.randint(2, 5), random.randint(0, 59))
            elif distance == 800:
                time = datetime.time(0, random.randint(5, 10), random.randint(0, 59))
            elif distance == 1500:
                time = datetime.time(0, random.randint(10, 20), random.randint(0, 59))
            date = datetime.date(
                random.randint(2010, 2021), random.randint(1, 12), random.randint(1, 28)
            )
            person_id = random.randint(1, 100)
            meet_id = random.randint(1, 13)
            insert_swim = text(
                f"""
                INSERT INTO swims (distance, stroke, time, date, person_id, meet_id)
                VALUES ({distance}, '{stroke}', '{time}', '{date}', {person_id}, {meet_id});
                """
            )
            conn.execute(insert_swim)
            conn.commit()


def create_meet_table():
    with engine.connect() as conn:
        conn.execute(create_meet_table_command)
        # insert data
        for i in range(13):
            meet_name = meet_names[i]
            pool_name = pool_names[random.randint(0, len(pool_names) - 1)]
            pool_city = cities[random.randint(0, len(cities) - 1)]
            pool_state = states[random.randint(0, len(states) - 1)]
            start_date = datetime.date(
                random.randint(2010, 2021), random.randint(1, 12), random.randint(1, 28)
            )
            end_date = start_date + datetime.timedelta(days=random.randint(1, 5))
            insert_meet = text(
                f"""
                INSERT INTO meet (meet_name, pool_name, pool_city, pool_state, start_date, end_date)
                VALUES ('{meet_name}', '{pool_name}', '{pool_city}', '{pool_state}', '{start_date}', '{end_date}');
                """
            )
            conn.execute(insert_meet)
            conn.commit()


def drop_tables():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS person"))
        conn.execute(text("DROP TABLE IF EXISTS team"))
        conn.execute(text("DROP TABLE IF EXISTS meet"))
        conn.execute(text("DROP TABLE IF EXISTS swims"))
        conn.commit()


drop_tables()

create_team_table()
print("Team table created")
create_person_table()
print("Person table created")
create_meet_table()
print("Meet table created")
create_swims_table()
print("Swims table created")


def show_tables():
    table_data = ""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM person LIMIT 5"))
        for row in result:
            print(row)
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM team LIMIT 5"))
        for row in result:
            print(row)
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM swims LIMIT 5"))
        for row in result:
            print(row)
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM meet LIMIT 5"))
        for row in result:
            print(row)
            table_data += str(row) + "\n"

    return table_data


show_tables()

print("Database setup complete!")
