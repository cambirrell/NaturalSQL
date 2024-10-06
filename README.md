## Natural Language SQL Interface

### Description of Database
There is a database called "swims" maintained by USA Swimming which details all official races of the past maybe 20 years.
I thought I'd make and interact with a synthetic version of it. I make random people, teams, and meets. Each swimmer has a team. Each swim is connected to a person and a meet.
I populated with synthetic data with random dates and times and randomly picking from a list of names, meet names, and places.
The purpose of the real data base is to be able to track the performance and times of swimmers.


### Example question that worked well
What would you like to know about the database?: 
Who is the fasted 100 breaststroke swimmer from the west coast?
SELECT p.first_name, p.last_name, s.time
FROM swims s
JOIN person p ON s.person_id = p.person_id
JOIN meet m ON s.meet_id = m.meet_id
WHERE s.distance = 100 AND s.stroke = 'BR' AND m.pool_state IN ('CA', 'OR', 'WA')
ORDER BY s.time ASC
LIMIT 1;
The fastest 100 breaststroke swimmer from the west coast is Lia Brown, who remarkably completed the swim in just one second.
Would you like to ask another question? (yes/no): 

### Example question that didn't work well
Who won the most silver medals at the last olympics and how many?

SELECT person.first_name, person.last_name, COUNT(swims.person_id) AS silver_medals
FROM swims
JOIN person ON swims.person_id = person.person_id
JOIN meet ON swims.meet_id = meet.meet_id
WHERE meet.meet_name = 'Olympic Trials' AND meet.start_date >= '2021-07-23' AND meet.end_date <= '2021-08-08'
AND swims.position = 2
GROUP BY person.first_name, person.last_name
ORDER BY silver_medals DESC
LIMIT 1;

(psycopg2.errors.UndefinedColumn) column swims.position does not exist
LINE 7: AND swims.position = 2
            ^

[SQL: 
SELECT person.first_name, person.last_name, COUNT(swims.person_id) AS silver_medals
FROM swims
JOIN person ON swims.person_id = person.person_id
JOIN meet ON swims.meet_id = meet.meet_id
WHERE meet.meet_name = 'Olympic Trials' AND meet.start_date >= '2021-07-23' AND meet.end_date <= '2021-08-08'
AND swims.position = 2
GROUP BY person.first_name, person.last_name
ORDER BY silver_medals DESC
LIMIT 1;
]
(Background on this error at: https://sqlalche.me/e/20/f405)
I'm sorry, I couldn't find the answer to that question. Would you like to ask another question? (yes/no): 


### Different prompts tested


