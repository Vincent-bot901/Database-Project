ting at huske

Vi skal huske at build databasen i python interactive shell til at starte med

så skal vi også lave en admin bruger

INSERT
INTO Users (username, password, usertype, balance)
VALUES ('admin', 'admin', 'admin', 10000);

så skal vi også preload teamsne ind. 

INSERT INTO Teams (teamname) VALUES
('Real Madrid'),
('Barcelona'),
('Atletico Madrid'),
('Sevilla'),
('Valencia'),
('Villarreal'),
('Real Sociedad'),
('Athletic Bilbao'),
('Real Betis'),
('Celta Vigo'),
('Granada'),
('Levante'),
('Osasuna'),
('Getafe'),
('Espanyol'),
('Alaves'),
('Mallorca'),
('Cadiz'),
('Elche'),
('Rayo Vallecano');


husk at password med regex