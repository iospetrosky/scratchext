--deployed on Lenovo

CREATE TABLE sessions (
    ID         INTEGER    PRIMARY KEY AUTOINCREMENT,
    session_id CHAR (10)  DEFAULT 'XXX',
    user_id    INT default 1000
);

CREATE TABLE users (
    ID         INTEGER    PRIMARY KEY AUTOINCREMENT,
    name    char(30) not null,
    email   char(200) not null unique
);

insert into users (id, name, email) values (1000, 'Lorenzo','lorenzo.pedrotti@gmail.com');
insert into sessions (session_id, user_id) values ('XYZ12345',1000);
