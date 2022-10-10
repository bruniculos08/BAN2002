create table setor (cods int, nome varchar(40), primary key (cods));

create table mecânico (codm int, cpf char(11), nome varchar(80), idade int, endereço varchar(100), cidade varchar(40), função varchar(40), cods int not null,
		       primary key(codm), foreign key (cods) references setor(cods) on delete set null on update cascade); 

create table cliente (codc int, cpf char(11), nome varchar(80), idade int, endereço varchar(100), cidade varchar(40), primary key (codc));

create table veículo (codv int, renavam char(8), modelo varchar(40), marca varchar(20), ano int, quilometragem float, codc int, primary key(codv), foreign key (codc) references cliente(codc));

create table conserto (codm int, codv int, dataConserto date, hora char(5), primary key(codm, codv, dataConserto), foreign key(codm) references mecânico(codm), foreign key(codv) references veículo(codv));
