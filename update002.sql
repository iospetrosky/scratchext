--developed on Lenovo
--deployed on Pythonanywhere
--deployed on 

alter table users add passwd char(20);
update users set passwd = 'shorena1' where id = 1000;
update users set name = 'lorenzo' where id = 1000;

alter table users add groups char(100);
update users set groups = 'USR ADM REG' where id = 1000;

insert into users (name, email, passwd,groups) values ('chicco','chicco.pedrotti@gmail.com','shorena1','USR');
