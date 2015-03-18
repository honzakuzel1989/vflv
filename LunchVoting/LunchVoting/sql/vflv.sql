drop table if exists users;
create table users (
	id INTEGER primary key autoincrement,
	name TEXT unique not null,
	pass TEXT not null,
	firstname TEXT default null,
	surname TEXT default null
);

drop table if exists pubs;
create table pubs (
	id INTEGER primary key autoincrement,
	title TEXT unique not null
);

drop table if exists votings;
create table votings (
	id INTEGER primary key autoincrement,
	date INTEGER not null,
	user TEXT unique not null,
	pub TEXT unique not null,
	rating INTEGER not null
);
