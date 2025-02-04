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

create or replace function salarioFunc(arg_nome varchar) returns float as
$$
declare new_salario float default 0;
declare old_salario float default 0;
declare num_dependentes integer default 0;
begin
	select count(*) from empregado e join dependente d on e.ssn = d.essn where (d.parentesco = 'FILHO' or d.parentesco = 'FILHA') and e.pnome = arg_nome group by e.ssn into num_dependentes;
	select e.salario from empregado e where e.pnome = arg_nome into old_salario;
	new_salario := old_salario;
	for i in 1..num_dependentes loop
		new_salario := new_salario + old_salario*(0.02);
	end loop;
	return new_salario;
end;
$$ language plpgsql;

select * from empregado;
select count(*) from empregado e join dependente d on e.ssn = d.essn where (d.parentesco = 'FILHO' or d.parentesco = 'FILHA') and e.pnome = 'Franklin' group by e.ssn;
select e.salario from empregado e where e.pnome = 'Franklin';
select * from salarioFunc('Franklin');

-- Correção: faltava o 'into num_dependentes' no primeiro select, havia um 'e.pnom' ao invés de 'e.pnome' no segundo select e o cálculo do salário estava errado(crescia de maneira composta ao invés...
-- de simples) de modo que para se arrumar isso forama criadas 2 novas variáveis('new_salario' e 'old_salario') no lugar da variável 'salario' retornando então o valor da variável 'new_salario'.

-------------------------------------------------------------------
-- Questão 01.b)

drop function horasDep;
create or replace function horasDep(arg_nome varchar) returns float as
$$
declare horas float;
begin
	--select e.pnome, sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero join departamento d on p.dnum = d.dnumero group by e.ssn into horas;
	select sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero join departamento d on p.dnum = d.dnumero where e.pnome = arg_nome and e.dno = d.dnumero group by ssn into horas;
	return horas;
end
$$ language plpgsql;

--select e.pnome, sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero join departamento d on p.dnum = d.dnumero where e.dno = d.dnumero group by ssn into horas;
select e.pnome, sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero join departamento d on p.dnum = d.dnumero where e.pnome = 'Franklin' and e.dno = d.dnumero group by ssn;

select * from empregado;
select * from horasDep('Franklin');

--Correção: o segundo select deveria ter apenas a coluna 'sum(t.horas)'.
-------------------------------------------------------------------
-- Questão 01.c) Função que retorne o nome dos empregados que têm alocação em projetos de um departamento passado
-- como parâmetro maior que a média de alocação dos empregados em todos os projetos.

drop function oldDeptFunc;
create or replace function oldDeptFunc(arg_nome_dep varchar) returns varchar[] as
$$
declare horas float;
declare mediaAloc float; 
declare num_dept int;
declare nomes varchar[];
begin
	select dnumero from departamento where dnome = arg_nome_dep into num_dept;
	select avg(sum) from (select e.ssn, sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn group by e.ssn) as aux into mediaAloc;

	cast(select e.pnome from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero where num_dept = e.dno and mediaAloc < 
	(select sum(t.horas) from empregado e join trabalha_em t on e.ssn = t.essn join projeto p on t.pno = p.pnumero where p.dnum = num_dept) as varchar[]) into nomes;
	return nomes;
	
end
$$ language plpgsql;

select * from departamento;
select * from empregado;
select * from oldDeptFunc('Pesquisa');

-- Correção: a função não está retornando a lista de nomes e tentava acessar 'empregados' ao invés de 'empregado' e 'e.nome' ao invés de 'e.pnome':

-- Correção: faltou utilizar a variável num_dept no primeiro select(into) e no terceiro select(onde havia se colocado dnumero). 
-------------------------------------------------------------------
-- Questão 02.a)

-- Gatilho para impedir que um empregado seja supervisionado por ele mesmo.

create trigger supervisao before insert or update on empregado for each row execute procedure verifica_sup();

drop function verifica_sup;
create or replace function verifica_sup() returns trigger as
$$
begin
	if new.ssn = new.superssn then
		raise exception 'um funcionario nao pode ser supervisor de si mesmo';
		return null;
	end if;
	return new;
end;
$$ language plpgsql;

select * from empregado;
insert into empregado values('Perna Longa', 'P', 'Longa', '1', '1941-06-20', '200 Berry, Bellaire,TX', 'M', 10000000, '1', 4);
delete from empregado where pnome = 'Perna Longa';

-- Correção: o retorno dentro do if deveria ser de old ao invés de null e ao invés de 'new.ssn' deveria ser 'new.snn'.

-------------------------------------------------------------------
-- Questão 02.b)

-- Gatilho para impedir que um empregado que tenha mais de um cônjuge. Ou seja, tenha mais de um 
-- dependente com PARENTESCO = ‘cônjuge’

create trigger conjuge_unico before insert or update on dependente for each row execute procedure verifica_conjuge();

drop function verifica_conjuge;
create or replace function verifica_conjuge() returns trigger as
$$
declare conjuge_num int default 0;
begin
	select count(*) from dependente d where d.parentesco = 'CÔNJUGE' and d.essn = new.essn into conjuge_num;
	if TG_OP = 'UPDATE' and new.parentesco = 'CÔNJUGE' then
		if old.parentesco = 'CÔNJUGE' then
			return new;
		elsif conjuge_num > 0 then 
			raise exception 'mais de um conjuge';
			return old;
		end if;
	elsif TG_OP = 'INSERT' and new.parentesco = 'CÔNJUGE' and conjuge_num >= 1 then
		raise exception 'mais de um conjuge';
		return old;
	end if;
	return new;
		
end
$$ language plpgsql;

select * from dependente;
insert into dependente values('333445555', 'Spider-Man', 'M', '1986-04-05', 'CÔNJUGE');
delete from dependente where nome_dependente = 'Spider-Man';
-- Correção: o gatilho estáva setado para 'after' ao invés de 'before' e havia um 'd.parentes' ao invés de 'd.parentesco' no select. Além disso deve-se considerar que o TG_OP está...
-- ... sempre em caixa alta.

-------------------------------------------------------------------
-- Questão 02.c)

-- Gatilho para impedir que um gerente gerencie mais do que um departamento

create trigger unico_dep_ger after insert or update on departamento for each row execute procedure verifica_ger();

drop function verifica_ger;
create or replace function verifica_ger() returns trigger as
$$
declare quantidade_dep int default 0;
begin
	select count(*) from departamento d where d.gerssn = new.gerssn into quantidade_dep;
	if TG_OP = 'UPDATE' then
		if old.gerssn = new.gerssn then
			return new;
		elsif quantidade_dep > 0 then 
			raise exception 'gerente de mais de um departamento';
			return old;
		end if;
	elsif TG_OP = 'INSERT' and quantidade_dep >= 1 then
		raise exception 'gerente de mais de um departamento';
		return old;
	end if;
	return new;
		
end
$$ language plpgsql;
 
select * from departamento;
insert into departamento values('Bombas Atômicas', 0, '333445555', '1988-05-22');
delete from departamento where dnumero = 0;

-- Correção: no 'elsif' estava-se utilizando uma variável errada (conjuge_num) na comparação, que deveria ser quantidade_dep. Além disso no 'create trigger' havia 'departamente' ao invés...
-- ... de 'departamento' e não se colocou 'insert' e 'update' em caixa alta.

-------------------------------------------------------------------
-- Questão 02.d)

-- Gatilho para impedir que um empregado seja supervisionado por um empregado de outro departamento diferente do dele

create trigger dep_ger before insert or update on empregado for each row execute procedure verifica_dep_ger();

drop function verifica_dep_ger;
create or replace function verifica_dep_ger() returns trigger as
$$
declare depDoGerente int default null;
begin
	select e.dno from empregado e where e.ssn = new.superssn into depDoGerente;
	
	if new.dno != depDoGerente then
		raise exception 'supervisor de outro departamento';
		return old;
	end if;
	return new;
end
$$ language plpgsql;

select * from empregado;
insert into empregado values('Perna Longa', 'P', 'Longa', '1', '1941-06-20', '200 Berry, Bellaire,TX', 'M', 10000000, '999887777', 4);

-- Correção: atributo gerssn não existia, deveria ser superssn e depDoGerente deveria ser int ao invés de char.

-------------------------------------------------------------------
-- Questão 03.a)

-- Visão que mostre o nome de todos os empregados, e para aqueles que estão alocados a projetos, mostre também a quantidade de horas alocadas

create view dep_ger(nome, horas) as select e.pnome, aux.horas from empregado e join
(select e.ssn, sum(horas) as horas from empregado e join trabalha_em t on e.ssn = t.essn where e.ssn = t.essn group by e.ssn) as aux on e.ssn = aux.ssn;

select * from dep_ger;
select * from empregado;

select * from projeto where pnumero = 20;
select * from trabalha_em where essn = '888665555';
select * from trabalha_em where pno = 20;
select * from empregado;

-- Correção: arrumar sintaxe (faltava alias para o campo sum(horas) e para subquery).

-------------------------------------------------------------------
-- Questão 03.b)

-- visão que mostre o nome dos empresados e de seus dependentes do tipo ‘filho’ e ‘filha’




