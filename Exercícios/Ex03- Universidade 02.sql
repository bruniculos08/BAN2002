drop table leciona;
drop table titulo;
drop table responsavel;
drop table habilitacao;
drop table requisito;
drop table grade;
drop table matricula;
drop table inscricao;
drop table area;
drop table professor;
drop table disciplina;
drop table aluno;
drop table curso;

create table curso (sigla_curso char(10), nome varchar(100), titulação varchar(100), primary key (sigla_curso));

create table aluno (cpf char(11) primary key, nome varchar(100), rua varchar(255), numero int, estado char(2), cidade varchar(100), cep int);

create table disciplina (sigla_disc char(10) primary key, nome varchar(100), carga_horaria int);

create table professor (reg_mec int primary key, nome varchar(100), rua varchar(255), numero int, cidade varchar(100), estado char(2), cep int);

create table area (cod_area int primary key, descricao varchar(100));

create table inscricao (matricula int primary key, sigla_curso char(10), cpf char(11), foreign key (sigla_curso) references curso(sigla_curso), foreign key (cpf) references aluno(cpf) on delete cascade);

create table matricula (ano date, matricula int, sigla_disc char(10), semestre int, primary key(ano, matricula, sigla_disc, semestre), foreign key (matricula) references inscricao(matricula),
			foreign key (sigla_disc) references disciplina(sigla_disc));

create table grade (sigla_curso char(10), sigla_disc char(10), primary key (sigla_curso, sigla_disc), foreign key (sigla_curso) references curso(sigla_curso), 
		    foreign key (sigla_disc) references disciplina(sigla_disc) on delete cascade);

create table requisito (sigla_disc_req char(10), sigla_curso_req char(10), sigla_disc char(10), sigla_curso char(10), primary key (sigla_disc_req, sigla_curso_req, sigla_disc, sigla_curso),
			foreign key (sigla_disc_req, sigla_curso_req) references grade(sigla_disc, sigla_curso) on delete cascade, 
			foreign key (sigla_disc, sigla_curso) references grade(sigla_disc, sigla_curso) on delete cascade);

create table habilitacao (sigla_disc char(10), reg_mec int, primary key (sigla_disc, reg_mec), foreign key (sigla_disc) references disciplina(sigla_disc), 
			  foreign key (reg_mec) references professor(reg_mec) on delete cascade);

create table responsavel (reg_mec int, cod_area int, ate date, primary key (reg_mec, cod_area), foreign key (reg_mec) references professor(reg_mec) on delete set null on update cascade);

create table titulo (reg_mec int, cod_area int, data_de_titulacao date, primary key(reg_mec, cod_area), foreign key (reg_mec) references professor(reg_mec), foreign key (cod_area) references area(cod_area));

create table leciona (sigla_disc char(10), reg_mec int, ano date, semestre int, primary key(sigla_disc, reg_mec, ano, semestre), foreign key (sigla_disc) references disciplina(sigla_disc), 
		      foreign key (reg_mec) references professor(reg_mec) on delete set null on update cascade);
