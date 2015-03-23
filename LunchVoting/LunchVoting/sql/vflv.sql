drop table if exists users;
create table users (
	id INTEGER primary key autoincrement,
	name TEXT unique not null,
	pass TEXT not null,
	firstname TEXT default null,
	surname TEXT default null
);

insert into users (name, pass) values ('kuz1', '79887b3f8596d73cd7bc44cc00543f466cf3d2ccf180ca8d2046c053673ee7b4');
insert into users (name, pass) values ('kli1', '2d3bcb537ec2891aceb338f1d6ca08953aea6d85b4cc9ef4706f9a21c828c42c');
insert into users (name, pass) values ('mar5', 'b5aeaf6e2dec5352a77430c11a61aaeedc42d3b1e5624423a62daedacbcef6f5');
insert into users (name, pass) values ('kor1', '47579f662fc3d7cd6bdf78cdb6e44a17a20c46045bd188a1da05cbcaf27c73ce'); 
insert into users (name, pass) values ('dyc1', '37450720bfa246a4fc703953366131d4ac2af393161986d459d8603e2729321e');
insert into users (name, pass) values ('flo2', 'bcf8ca6b95ddbdac2772cde94ce59c490a03954640a571da5099c39569c87f80');
insert into users (name, pass) values ('bel1', '0cfa8c91525dc70d3d638320bdb14a14e21c9bf1b7fa563ce1d539055efae46f');
insert into users (name, pass) values ('kre2', '23d325dd899fef4a92ce66c97416188d5e8a8119dac688b46c1efe3165076cd2');

drop table if exists pubs;
create table pubs (
	id INTEGER primary key autoincrement,
	title TEXT unique not null
);

insert into pubs (title) values ('Aqua');
insert into pubs (title) values ('Kopec');
insert into pubs (title) values ('Kruháč');
insert into pubs (title) values ('Liďák');
insert into pubs (title) values ('Picolo');
insert into pubs (title) values ('Sladovna');
insert into pubs (title) values ('Sýpka');
insert into pubs (title) values ('Zakki');

drop table if exists votings;
create table votings (
	id INTEGER primary key autoincrement,
	date INTEGER not null,
	user TEXT not null,
	pub TEXT not null,
	rating INTEGER not null
);
