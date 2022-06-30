create database if not exists empleados;
use empleados;

create table empleados (
id int not null auto_increment,
nombre varchar(20),
correo varchar(30),
foto varchar(500),
primary key(id)
);

--insert into empleados (nombre, correo, foto) values("mario", "mario@gmail.com", "fotodemario.jpg");

--select * from empleados;
