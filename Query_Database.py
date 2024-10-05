from sqlalchemy import create_engine, text, Table, MetaData
from openai import OpenAI
import random
import json
random.seed(0)

config = json.load(open('config.json'))
conn_string = config["connectionString"]
client = OpenAI(api_key=config['openai_key'])

engine = create_engine(conn_string)

create_person_table_command = text(
    """
    CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('coach', 'athlete', 'official')),
    date_of_birth DATE NOT NULL,
    active BOOLEAN NOT NULL,
    team_id int
    );
    """
)

create_team_table_command = text(
    """
    CREATE TABLE team (
    team_id int PRIMARY KEY NOT NULL ,
    team_name varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    state char(2) NOT NULL
    );
    """
)

create_swims_table_command = text(
    """
    CREATE TABLE swims (
    distance int NOT NULL,
    stroke CHAR(2) CHECK (stroke IN ('FR', 'BK', 'BR', 'FL', 'IM')),
    time TIME NOT NULL,
    date DATE NOT NULL,
    person_id int NOT NULL,
    meet_id int NOT NULL
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

def show_tables():
    table_data = ""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM person LIMIT 10"))
        for row in result:
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM team LIMIT 10"))
        for row in result:
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM swims LIMIT 10"))
        for row in result:
            table_data += str(row) + "\n"

        result = conn.execute(text("SELECT * FROM meet LIMIT 10"))
        for row in result:
            table_data += str(row) + "\n"
    return table_data



table_columns = show_tables()
meet_names = ["Winter Classic", "Summer Classic", "Spring Classic", "Fall Classic", "Holiday Invite", "National Championships", "Olympic Trials", "World Championships", "Pan Pacific Championships", "Junior Nationals", "Senior Nationals", "Sectionals", "Zones"]
pool_names = ["Aquatic Center", "Natatorium", "Swim Center", "Swim Club", "Aquatic Club", "Aquatic Complex"]
all_meets_content = "Here are the meets in the database: \n" + str(meet_names) + "\n"
all_pools_content = "Here are the pools in the database: \n" + str(pool_names) + "\n"
context = str(create_person_table_command) + str(create_team_table_command) + str(create_swims_table_command) + str(create_meet_table_command) + "Exmaple data in the tables: \n" + str(table_columns) + all_meets_content + all_pools_content
instruction = "Get only the Postgresql commands find the answer to the question: "
# question = "What is the average time for a 50 meter freestyle swim?"
while True:
    print("What would you like to know about the database?: ")
    question = input()


    prompt = context + instruction + question

    response = client.chat.completions.create(
        model= "gpt-4o",
        messages= [
            {
                "role": "system",
                "content": "You are a database administrator and will give sql commands to help answer questions about the database. Remove any extra formatting and only provide the sql command."
            },
            {
                "role": "user",
                "content": prompt
            }])

    cleaned = response.choices[0].message.content
    cleaned = cleaned.replace("```", "").replace("```", "").replace("sql", "")

    results = ""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(cleaned))
            for row in result:
                results += str(row) + "\n"
    except Exception as e:
        results = str(e)
        print(results)
        print("I'm sorry, I couldn't find the answer to that question. Would you like to ask another question? (yes/no): ")
        response = input()
        if response == "no":
            break
        else:
            continue

    natural_language_explaination = f"Respond to the question: {question} According to the database, the answer is {results}"

    natural_language_responce = client.chat.completions.create(
        model= "gpt-4o",
        messages= [
            {
                "role": "system",
                "content": "You are a database administrator and just ran a sql command to find the answer to a question. Provide a natural language explanation of the results even if the results doesn't make sense or is not reasonable. Don't make any refernce database, pretend you are explaining it to someone who doesn't know anything about databases, and you know the answer off the top of your head, but don't explain any futher."
            },
            {
                "role": "user",
                "content": natural_language_explaination
            }])

    print(natural_language_responce.choices[0].message.content)
    print("Would you like to ask another question? (yes/no): ")
    response = input()
    if response == "no":
        break
    else:
        continue