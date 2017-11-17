create database movies;
use movies;
create table movies(id int NOT NULL, name varchar(200), description text, has_female_lead boolean, genre varchar(200));
ALTER TABLE movies ADD PRIMARY KEY(id);
INSERT INTO MOVIES VALUES (1, "It", "A group of bullied kids band together when a monster, taking the appearance of a clown, begins hunting children.", false, 'horror'),
(2, "The Hitman's Bodyguard", "The world's top bodyguard gets a new client, a hit man who must testify at the International Court of Justice.", false, "action"),
(3, "baywatch", "Devoted lifeguard Mitch Buchannon butts heads with a brash new recruit, as they uncover a criminal plot that threatens the future of the bay.", true, "comedy"),
(4, "the fate of the furious", "When a mysterious woman seduces Dom into the world of terrorism and a betrayal of those closest to him, the crew face trials that will test them as never before.", false, "action"),
(5, "Blue velvet", "The discovery of a severed human ear found in a field leads a young man on an investigation related to a beautiful, mysterious nightclub singer and a group of psychopathic criminals who have kidnapped her child.", true, "Drama"),
(6, "Blade Runner", "A young blade runner's discovery of a long buried secret leads him on a quest to track down former blade runner, Rick Deckard, who's been missing for thirty years.", true, "sci-fi");

create table users(id integer not null, name varchar(200));
ALTER TABLE users ADD PRIMARY KEY(id);

insert into users values (1, "John Wayne"), (2, "Juan Donovan"),(3,"Simon Donaghue"),(4,"Lester Morton"),(5, "Alan Morris"),(6, "Bruno Schiller");
create table votes (user_id int not null, movie_id int not null, rating int not null);

ALTER TABLE votes ADD PRIMARY KEY(user_id,movie_id);

insert into votes values (1,1,4),(1,2,5),(1,3,3),(1,4,4),(1,5,2),(1,6,5),(2,1,3),(2,2,4),(2,3,3),(2,4,4),(2,5,5),(2,6,4),(3,1,2),(3,2,3),(3,3,5),(3,4,5),(3,5,3),(3,6,5),(4,1,2),(4,2,5),(4,3,5),(4,4,3),(4,5,3),(4,6,3),(5,1,3),(5,2,3),(5,3,3),(5,4,4),(5,5,4),(5,6,5),(6,1,5),(6,2,4),(6,3,3),(6,4,3),(6,5,4),(6,6,4);
