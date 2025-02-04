drop table Cobertura;
drop table Inseminação;
drop table Sequência;
drop table Tratamento;
drop table Consulta;
drop table Animal;
drop table Veterinário;
drop table Curral;
drop table Sêmen;

create table Sêmen (Tipo varchar[100], Característica varchar[100], primary key (Tipo));

create table Curral (Número integer, localização varchar[40], primary key (Número));

create table Veterinário (CRM integer, Nome varchar[100], Convênio varchar[100], primary key (CRM));

create table Animal (ID integer, Nome varchar[40], Raça varchar[40], Sexo varchar[10], Flag_Matriz bit, Número_Curral integer,
		     Flag_Reprodutor_Adquirido bit, Nome_Pai varchar[40], Nome_Mãe varchar[40], Valor float,
		     Flag_Reprodutor_Cria bit, Desmame date, Geração date, primary key (ID), foreign key (Número_Curral) references Curral(Número));

create table Consulta (Data_Consulta date, Resultado varchar[200], CRM integer, ID integer, primary key(Data_Consulta, CRM, ID), foreign key (CRM) references Veterinário(CRM), 
		       foreign key (ID) references Animal(ID));

create table Tratamento (Data_Tratamento date, Descrição varchar[200], Data_Consulta date, CRM integer, ID integer, primary key(Data_Tratamento, Data_Consulta, CRM, ID), 
			 foreign key (Data_Consulta, CRM, ID) references Consulta(Data_Consulta, CRM, ID));

create table Sequência (Consulta_Atual date, CRM_Atual integer, ID_Atual integer, Consulta_Prox date, CRM_Prox integer, ID_Prox integer, 
		  primary key(Consulta_Atual, Consulta_Prox, CRM_Atual, CRM_Prox, ID_Atual, ID_Prox), 
		  foreign key (Consulta_Atual, CRM_Atual, ID_Atual) references Consulta(Data_Consulta, CRM, ID), foreign key (Consulta_Prox, CRM_Prox, ID_Prox) references Consulta(Data_Consulta, CRM, ID));


create table Inseminação (ID_Matriz integer,  Tipo_Sêmen varchar[100], primary key (ID_Matriz, Tipo_Sêmen), foreign key (ID_Matriz) references Animal(ID), foreign key (Tipo_Sêmen) references Sêmen(Tipo));

create table Cobertura (ID_Matriz integer, ID_Reprodutor integer, primary key (ID_Matriz, ID_Reprodutor), foreign key (ID_Matriz) references Animal(ID), foreign key (ID_Reprodutor) references Animal(ID));
