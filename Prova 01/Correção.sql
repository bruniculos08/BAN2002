-------------------------------------------------------------------
--Criação do Esquema de Dados
-------------------------------------------------------------------

--Tabela Empregado
CREATE TABLE empregado(
	pnome varchar NOT NULL,
	minicial char(1) NOT NULL,
	unome varchar NOT NULL,
	ssn char(9) NOT NULL PRIMARY KEY,
	datanasc Date NOT NULL,
	endereco varchar NOT NULL,
	sexo char(1) NOT NULL,
	salario integer NOT NULL,
	superssn char(9),
	dno integer,
	FOREIGN KEY (superssn) REFERENCES empregado(ssn)
);

-------------------------------------------------------------------
--Tabela Departamento
CREATE TABLE departamento(
	dnome varchar NOT NULL,
	dnumero integer NOT NULL PRIMARY KEY,
	gerssn char(9) NOT NULL,
	gerdatainicio Date NOT NULL,
	FOREIGN KEY (gerssn) REFERENCES empregado(ssn)
);

-------------------------------------------------------------------
-- Tabela de Localização do Departamento
CREATE TABLE depto_localizacoes(
	dnumero integer NOT NULL,
	dlocalizacao varchar NOT NULL,
	PRIMARY KEY(dnumero,dlocalizacao),
	FOREIGN KEY (dnumero) REFERENCES departamento(dnumero)
);

-------------------------------------------------------------------
-- Tabela Projeto
CREATE TABLE projeto(
	pjnome varchar NOT NULL,
	pnumero integer NOT NULL PRIMARY KEY,
	plocalizacao varchar NOT NULL,
	dnum integer NOT NULL,
	FOREIGN KEY (dnum) REFERENCES departamento(dnumero)
);

-------------------------------------------------------------------
-- Tabela Trabalha_em
CREATE TABLE trabalha_em(
	essn char(9) NOT NULL,
	pno integer NOT NULL,
	horas numeric(3,1),
	PRIMARY KEY(essn,pno),
	FOREIGN KEY (pno) REFERENCES projeto(pnumero),
	FOREIGN KEY (essn) REFERENCES empregado(ssn)
);

-------------------------------------------------------------------
-- Tabela Dependente
CREATE TABLE dependente(
	essn char(9) NOT NULL,
	nome_dependente varchar NOT NULL,
	sexo char(1) NOT NULL,
	datanasc Date NOT NULL,
	parentesco varchar NOT NULL,
	PRIMARY KEY(essn,nome_dependente),
	FOREIGN KEY (essn) REFERENCES empregado(ssn)
);

-------------------------------------------------------------------
--Dados
-------------------------------------------------------------------

INSERT INTO empregado VALUES
	('James','E','Borg','888665555','1937-11-10','450 Stone, Houston, TX','M',55000,null,1),
	('Franklin','T','Wong','333445555','1955-12-08','638 Voss, Houston, TX','M',40000,888665555,5),
	('Jennifer','S','Wallace','987654321','1941-06-20','291 Berry, Bellaire,TX','F',43000,888665555,4),
	('John','B','Smith','123456789','1965-01-09','731 Fondren, Houston, TX','M',30000,333445555,5),
	('Alicia','J','Zelaya','999887777','1968-01-19','3321 Castle, Spring, TX','F',25000,987654321,4),
	('Ramesh','K','Narayan','666884444','1962-09-15','975 Fire Oak, Humble, TX','M',38000,333445555,null),
	('Joyce','A','English','453453453','1972-07-31','5631 Rice, Houston, TX','F',25000,null,5),
	('Ahmad','V','Jabbar','987987987','1969-03-29','980 Dallas, Houston, TX','M',25000,987654321,4);

-------------------------------------------------------------------
	
INSERT INTO departamento VALUES
	('Pesquisa',5,'333445555','1988-05-22'),
	('Administração',4,'987654321','1995-01-01'),
	('Recursos Humanos',2,'987987987','2000-01-01'),
	('Sede Administrativa',1,'888665555','1981-06-19');

-------------------------------------------------------------------

INSERT INTO depto_localizacoes VALUES
	(1,'Houston'),
	(4,'Stafford'),
	(5,'Bellaire'),
	(5,'Sugarland');

-------------------------------------------------------------------

INSERT INTO projeto VALUES
	('ProdutoX',1,'Bellaire',5),
	('ProdutoY',2,'Suaarland',5),
	('ProdutoZ',3,'Houston',5),
	('ProdutoW',4,'Albuquerque',5),
	('Automatização',10,'Stafford',4),
	('Reorganização',20,'Houston',1),
	('Novos Benefícios',30,'Stafford',4);

-------------------------------------------------------------------

INSERT INTO trabalha_em VALUES
	('123456789',1,'32.5'),
	('123456789',2,'7.5'),
	('453453453',1,'20.0'),
	('453453453',2,'20.0'),
	('333445555',2,'10.0'),
	('333445555',3,'10.0'),
	('333445555',10,'10.0'),
	('333445555',20,'10.0'),
	('999887777',30,'30.0'),
	('999887777',10,'10.0'),
	('987987987',10,'35.0'),
	('987987987',30,'5.0'),
	('987654321',30,'20.0'),
	('987654321',20,'15.0'),
	('888665555',20,null);

-------------------------------------------------------------------

INSERT INTO dependente VALUES
	('333445555','Alice','F','1986-04-05','FILHA'),
	('333445555','Theodore','M','1983-10-25','FILHO'),
	('333445555','Joy','F','1958-05-03','CÔNJUGE'),
	('987654321','Abner','M','1942-02-28','CÔNJUGE'),
	('123456789','Michael','M','1988-01-04','FILHO'),
	('123456789','Alice','F','1988-12-30','FILHA'),
	('123456789','Elizabeth','F','1967-05-05','CÔNJUGE');

-------------------------------------------------------------------
-- Questão 01.a)

--Função que calcule e retorne o salário do empregado passado por parâmetro com acréscimo de 2% para cada dependente com parentesco do tipo ‘filho’ e ‘filha’.

select * from empregado;
select * from dependente;

drop function getSalario(p_ssn varchar(9));
create or replace function getSalario(p_ssn varchar(9)) returns float as
$$
declare num_filhos int default 0;
declare salario_emp float default 0;
begin
	-- Sem parenteses para a seleção de parentesco dá bug;
	num_filhos := (select count(*) from dependente where (parentesco = 'FILHO' or parentesco = 'FILHA') and essn = p_ssn);
	salario_emp := (select salario from empregado where ssn = p_ssn);
	return (salario_emp + (salario_emp*0.02*cast(num_filhos as float)));
end;
$$
language plpgsql;

select getSalario('333445555');

-------------------------------------------------------------------
-- Questão 01.b)

--Função que retorne a soma das horas trabalhadas pelo empregado passado como parâmetro em projetos do mesmo departamento em que ele está alocado.

select * from projeto;
select * from trabalha_em;

drop function empregadoHorasDepartamentoAlocado;
create or replace function empregadoHorasDepartamentoAlocado(p_ssn varchar) returns numeric as
$$
declare num_departamento int;
declare soma numeric default 0;
begin
	num_departamento := (select dno from empregado where ssn = p_ssn);
	soma := (select sum(horas) from trabalha_em t join projeto p on t.pno = p.pnumero where t.essn = p_ssn and p.dnum = num_departamento);
end;
$$
language plpgsql;

-------------------------------------------------------------------
-- Questão 01.c) Função que retorne o nome dos empregados que têm alocação em projetos de um departamento passado
-- como parâmetro maior que a média de alocação dos empregados em todos os projetos.

drop function alocacaoProjetos(p_dnumero int);
create or replace function alocacaoProjetos(p_dnumero int) returns varchar[] as
$$
declare average float default 0;
declare nomes varchar[];
declare reg record;
begin
	average := (select avg(count) from (select count(*), e.ssn from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on p.pnumero = t.pno 
				group by e.ssn) as aux);
	
	for reg in (select aux.pnome from (select count(*), e.pnome, e.ssn, p.dnum from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on p.pnumero = t.pno 
				where p.dnum = p_dnumero group by e.ssn, p.dnum) as aux where count >= average) loop
				--raise notice '%', reg.pnome;
				nomes := array_append(nomes, reg.pnome);
	end loop;
	return nomes;
end;
$$
language plpgsql;

-- Extra: fazer a mesma coisa mas por hora em vez de quantidade de alocações:

drop function alocacaoProjetosHoras(p_dnumero int);
create or replace function alocacaoProjetosHoras(p_dnumero int) returns varchar[] as
$$
declare average float default 0;
declare nomes varchar[];
declare reg record;
begin
	average := (select avg(sum) from (select sum(t.horas), e.ssn from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on p.pnumero = t.pno 
				group by e.ssn) as aux);
	
	for reg in (select aux.pnome from (select sum(t.horas), e.pnome, e.ssn, p.dnum from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on p.pnumero = t.pno 
				where p.dnum = p_dnumero group by e.ssn, p.dnum) as aux where sum >= average) loop
				--raise notice '%', reg.pnome;
				nomes := array_append(nomes, reg.pnome);
	end loop;
	return nomes;
end;
$$
language plpgsql;

select alocacaoProjetosHoras(4);

-------------------------------------------------------------------
-- Questão 02.a)

-- Gatilho para impedir que um empregado seja supervisionado por ele mesmo.

drop function supervisorProprio();
create or replace function supervisorProprio() returns trigger as
$$
begin
	if new.ssn = new.superssn then
		raise notice 'um empregado não pode ser seu próprio supervisor!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger supervisorProprioGatilho;
create or replace trigger supervisorProprioGatilho before insert or update on empregado for each row execute procedure supervisorProprio();

-------------------------------------------------------------------
-- Questão 02.b)

-- Gatilho para impedir que um empregado que tenha mais de um cônjuge. Ou seja, tenha mais de um 
-- dependente com PARENTESCO = ‘cônjuge’

drop function verificaConjuge();
create or replace function verificaConjuge() returns trigger as
$$
declare num_conjuge int default 0;
begin
	if TG_OP = 'UPDATE' then 
		if old.parentesco = 'CÔNJUGE' then
			return new;
		end if;
	end if;
	if new.parentesco = 'CÔNJUGE' then
		num_conjuge := (select count(*) from dependente where essn = new.essn and parentesco = 'CÔNJUGE');
		if num_conjuge >= 1 then
			raise notice 'não pode haver mais de um cônjuge!';
			return old;
		end if;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger verificaConjugeGatilho;
create or replace trigger verificaConjugeGatilho before insert or update on dependente for each row execute procedure verificaConjuge();

-------------------------------------------------------------------
-- Questão 02.c)

-- Gatilho para impedir que um gerente gerencie mais do que um departamento

drop function unicoGerente();
create or replace function unicoGerente() returns trigger as
$$
declare num_gerssn int default 0;
begin
	num_gerssn := (select count(*) from departamento where gerssn = new.gerssn);
	if num_gerssn >= 1 then
		raise notice 'um mesmo gerente não pode gerenciar mais de um departamento!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger unicoGerenteGatilho;
create trigger unicoGerenteGatilho before insert or update on departamento for each row execute procedure unicoGerente();

-------------------------------------------------------------------
-- Questão 02.d)

-- Gatilho para impedir que um empregado seja supervisionado por um empregado de outro departamento diferente do dele

drop function verificaSupervisor();
create or replace function verificaSupervisor() returns trigger as
$$
declare num_dept int;
begin
	num_dept := (select dno from empregado where ssn = new.superssn);
	if num_dept != new.dno then
		raise notice 'um empregado não pode ter supervisor de outro departamento!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger verificaSupervisorGatilho;
create trigger verificaSupervisorGatilho before insert or update on empregado for each row execute procedure verificaSupervisor();

-------------------------------------------------------------------
-- Questão 03.a)

-- Visão que mostre o nome de todos os empregados, e para aqueles que estão alocados a projetos, mostre também a quantidade de horas alocadas

select * from empregado;
select * from trabalha_em;
select * from projeto;

drop view empregadosHoras;
create view empregadosHoras(nome, horas) as select e.pnome, aux.sum from empregado e 
											join (select sum(horas), essn from trabalha_em group by essn) as aux on e.ssn = aux.essn; 

-------------------------------------------------------------------
-- Questão 03.b)

-- Visão que mostre o nome dos empresados e de seus dependentes do tipo ‘filho’ e ‘filha’

select * from dependente;
select * from empregado;

drop view empregadosDependentes;
create view empregadosDependentes(nome_dependente, nome_filho) as select e.pnome, d.nome_dependente from empregado e join dependente d
																  on e.ssn = d.essn where (d.parentesco = upper('filho') or d.parentesco = upper('filha'));
													  
-- Questão 03.c)

-- Visão que mostra o nome de todos os departamentos, e para aqueles que tem projeto, mostre os nomes dos projetos e de seus empregados alocados.

select * from infoDepartamentos;
select * from infoDepartamentosMesmoDNO;

-- Esta view considera qualquer empregado que esteja em um projeto pertence aquele departamento;
drop view infoDepartamentos;
create view infoDepartamentos(nome_departamento, nome_projeto, nome_empregado) as select d.dnome, p.pjnome, e.pnome from departamento d
																			   join projeto p on d.dnumero = p.dnum join trabalha_em t on
																			   p.pnumero = t.pno join empregado e on t.essn = e.ssn;

-- Esta view só considera os empregados que pertencem aquele departamento e não importa se estão em um projeto daquele departamento;							   
drop view infoDepartamentosMesmoDNO;																		 
create view infoDepartamentosMesmoDNO(nome_departamento, nome_projeto, nome_empregado) as select d.dnome, aux.pjnome, aux.pnome from departamento d
																			   join (select p.pjnome, p.dnum, e.pnome from projeto p join trabalha_em t
																					on p.pnumero = t.pno join empregado e on t.essn = e.ssn where p.dnum = e.dno) as aux
																					on d.dnumero = aux.dnum;
																   
