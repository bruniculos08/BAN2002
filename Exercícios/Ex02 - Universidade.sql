
drop table Banca;
drop table Orientador;
drop table Histórico;
drop table Registrado;
drop table Aluno_grad;
drop table Aluno;
drop table Curso;
drop table Pertence;
drop table Departamento;
drop table IP;
drop table Docente;
drop table Subsidio;
drop table Disciplina;
drop table Instrutor_Pesquisador;
drop table Pessoa;
drop table Faculdade;
drop table Disciplina_Corrente;
drop table Bolsa;

create table Faculdade (FNome varchar[50], Reitor varchar[50], Escritório varchar[50], primary key (FNome));

create table Pessoa (SNN integer, Dnasc date, Sexo varchar[9], Num integer, rua varchar[40], NumApto integer, Cidade varchar[40], Estado varchar[40], CEP integer, PNome varchar[20],
		     MInicial char, UNome varchar[20], primary key (SNN));

create table Instrutor_Pesquisador (SNN integer, primary key (SNN), foreign key (SNN) references pessoa(SNN));		     

create table Docente (SNN integer, SNN_Instrutor_Pesquisador int, Escritorio integer, Categoria varchar[30], Salário float, primary key (SNN), foreign key (SNN) references Pessoa(SNN),
		      foreign key (SNN_Instrutor_Pesquisador) references Instrutor_Pesquisador(SNN));

create table Departamento (DNome varchar[50], Dfone integer, Escritorio varchar[50], SNN_Chefia integer, FNome varchar[50], primary key (DNome), foreign key (SNN_Chefia) references Docente(SNN), 
			   foreign key (FNome) references Faculdade(FNome));

create table Pertence (DNome varchar[50], SNN_Docente integer, primary key(DNome, SNN_Docente), foreign key (DNome) references Departamento(DNome), foreign key (SNN_Docente) references Docente(SNN));

create table Curso (Curso_Nome varchar[50], UNome varchar, Curso_Descrição varchar[200], DNome varchar[50], primary key (Curso_Nome), foreign key (DNome) references Departamento(DNome));



create table Aluno (SNN integer, Turma integer, primary key (SNN), DNome varchar[50], DNome_Opta varchar[50], foreign key (SNN) references Pessoa(SNN), foreign key (DNome) references Departamento(DNome),
		    foreign key (DNome_Opta) references Departamento(DNome));

create table Aluno_grad (SNN integer, faculdade varchar[100], grau integer, ano integer, primary key (SNN), foreign key (SNN) references Aluno(SNN));

create table Orientador (SNN_Docente integer, SNN_Aluno_grad integer, primary key (SNN_Aluno_grad), foreign key (SNN_Docente) references Docente(SNN), 
			 foreign key (SNN_Aluno_grad) references Aluno_grad(SNN));
			
create table Banca (SNN_Docente integer, SNN_Aluno_grad integer, primary key (SNN_Docente, SNN_Aluno_grad), foreign key (SNN_Docente) references Docente(SNN), 
		    foreign key (SNN_Aluno_grad) references Aluno_grad(SNN));


create table Disciplina (Disciplina_Nome varchar[50], Ano integer, Trimestre integer, SNN_Inst_Pesq integer, primary key (Disciplina_Nome), foreign key (SNN_Inst_Pesq) references Instrutor_Pesquisador(SNN));

create table Disciplina_Corrente (Disciplina_Nome varchar[50], Ano integer, Trimestre integer, SNN_Inst_Pesq integer, primary key (Disciplina_Nome));

create table Bolsa (Num integer, Titulo varchar[40], Agencia integer, DataIn date, primary key (Num));

create table IP (SNN_Docente integer, Num_Bolsa integer, primary key (SNN_Docente, Num_Bolsa), foreign key (SNN_Docente) references Docente(SNN),
		 foreign key (Num_Bolsa) references Bolsa(Num));

create table Subsidio (SNN_Inst_Pesq integer, Num_Bolsa integer, Inicio date, Prazo integer, Fim date, primary key (SNN_Inst_Pesq, Num_Bolsa), foreign key (SNN_Inst_Pesq) references Instrutor_Pesquisador(SNN),
		 foreign key (Num_Bolsa) references Bolsa(Num));


create table Registrado (Disciplina_Nome varchar[50], SNN_Aluno integer, primary key(Disciplina_Nome, SNN_Aluno), foreign key (Disciplina_Nome) references Disciplina_Corrente(Disciplina_Nome),
			foreign key (SNN_Aluno) references Aluno(SNN));

create table Histórico (Nota float, Disciplina_Nome varchar[50], SNN_Aluno integer, primary key (Disciplina_Nome, SNN_Aluno), foreign key (Disciplina_Nome) references Disciplina(Disciplina_Nome),
			foreign key (SNN_Aluno) references Aluno(SNN));