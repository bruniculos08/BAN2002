--1) Gatilho para impedir a inserção ou atualização de Clientes com o mesmo CPF.

-- Onde: Cliente
-- Quando: before
-- Operações: insert or update
-- Nível: each row

-- note que essa função não funciona para updata (pois se o cpf o sempre vai cair no primeiro if)
-- raise exception encerra a execução (e o que foi feito é desfeito)
--create or replace function verificaCPF() returns trigger as 
--$$
--begin
--	if (select 1 from cliente where cpf = new.cpf and codc != new.codc) then
--		raise exception 'Cliente com cpf repetido!';
--	end if;
--	return new;
--end;
--$$ language plpgsql;

create or replace function verificaCPF() returns trigger as
$$
begin
	if TG_OP = 'insert' then
		if (select 1 from cliente where cpf = new.cpf) then
			raise exception 'Cliente com cpf repetido!';
		end if;
	elsif TG_OP = 'update' then
		if (old.cpf <> new.cpf) then
			if (select 1 from cliente where cpf = new.cpf) then
				raise exception 'Cliente com cpf repetido!';
			end if;
		end if;
	end if;
	return new;
end;
$$ language plpgsql;

create trigger verificaCPF before insert or update on cliente for each row execute procedure verificaCPF();

select * from cliente;
insert into cliente values(8, '20000200000', 'Torvalds', 20, 'Central Park', 'New York');
update cliente set cpf = '20000200000' where cliente.nome = 'Rachel';

--2) Gatilho para impedir a inserção ou atualização de Mecânicos com idade menor que 20 anos.

create or replace function verifica_mec_idade() returns trigger as
$$
begin
	if new.idade < 20 then 
		raise exception 'a idade miníma de mecânico é 20 anos!';
	end if;
	return new;
end;
$$ language plpgsql;

create trigger idade_mec before insert or update on mecanico for each row execute procedure verifica_mec_idade();

select * from mecanico;
insert into mecanico values(6, '12331414123', 'Paulão da Regulagem', 21, 'Lapa', 'São William', 'câmbio', null);

--3) Gatilho para atribuir um cods (sequencial) para um novo setor inserido.

-- uma sequecia serve como uma variável global
create sequence new_cods start 100;

create or replace function generate_cods() returns trigger as
$$
begin
	-- incrementa a sequência e atribui ao novo cods:
	new.cods := nextval('novo_cods');
	return new;
end;
$$ language plpgsql;

create trigger atribui_new_cods before insert on setor for each row execute procedure generate_cods();

select * from setor;

insert into setor values(1111, 'vaga de taxi do Agostinho Carrara');

--4) Gatilho para impedir a inserção de um mecânico ou cliente com CPF inválido.

create or replace function func_inserir_cpf_valido() returns trigger as
$$
begin
	if cpfValido(new.cpf) = false then
		raise exception 'cpf invalido!';
		return null;
	end if;
	return new;
end;
$$ language plpgsql;

select * from cliente;
insert into cliente values (10, '88787055511', 'Bernardo', 32, 'Lapa', 'São William');
 
create trigger inserir_cpf_valido_mecanico before insert on mecanico for each row execute procedure func_inserir_cpf_valido();
create trigger inserir_cpf_valido_cliente before insert on cliente for each row execute procedure func_inserir_cpf_valido();


--5) Gatilho para impedir que um mecânico seja removido caso não exista outro mecânico com a mesma função.

create or replace function func_mecanico_unico() returns trigger as
$$
declare funcao_counter int default 0;
begin
	select count(*) from mecanico m where m.funcao = old.funcao into funcao_counter;
	raise notice '%i', funcao_counter;
	if funcao_counter > 1 then
		raise exception  'mecanico nao pode ser removido pois é o único em sua função!';
	end if;
	return null;
end;
$$ language plpgsql;

select * from mecanico;
select count(*) from mecanico m where m.funcao = 'câmbio';
-- por algum motivo nao estou conseguindo deletar da tabela mecanico
delete from mecanico m where m.nome = 'Pedro';
create trigger mecanico_unico before delete on mecanico for each row execute procedure func_mecanico_unico();
drop trigger mecanico_unico on mecanico;

--6) Gatilho que ao inserir, atualizar ou remover um mecânico, reflita as mesmas modificações na tabela de Cliente. 
-- Em caso de atualização, se o mecânico ainda não existir na tabela de Cliente, deve ser inserido.

create or replace function generate_codc() returns int as 
$$
declare counter int default 0;
begin
	select max(codc) from cliente into counter;
	counter := counter + 1;
	return counter;
end;
$$ language plpgsql;

create or replace function func_reflect_mecanico_cliente() returns trigger as
$$
declare counter int default 0;
begin
	if TG_OP = 'insert' then
		insert into cliente values (generate_codc(), new.cpf, new.nome, new.idade, new.endereco, new.cidade);
	elsif TG_OP = 'delete' then
		--delete from cliente where cliente.cpf = old.cpf;
		return null;
	else
		select count(*) from cliente where cliente.cpf = new.cpf into counter;
		if counter >= 1 then
			update cliente c set c.cpf = new.cpf, c.idade = new.idade, c.endereco = new.endereco, c.cidade = new.cidade where c.cpf = new.cpf;
		else 
			insert into cliente values (generate_codc(), new.cpf, new.nome, new.idade, new.endereco, new.cidade);
		end if;
	end if;
	return null;
end;
$$ language plpgsql; 

select * from cliente;
select * from mecanico;
delete from mecanico where codm = 6;
insert into mecanico values(10, '00000000000', 'Paulão da Regulagem', 21, 'Lapa', 'São William', 'câmbio', null);


create trigger mecanico_reflect_cliente before insert or delete or update on mecanico for each row execute procedure func_reflect_mecanico_cliente();
drop trigger mecanico_reflect_cliente on mecanico;


--7) Gatilho para impedir que um conserto seja inserido na tabela Conserto se o mecânico já realizou mais de 20 horas extras no mês.

create or replace function func_conserto_max() returns trigger as
$$
declare count_hours int default 0;
declare nome_codm varchar(50);
declare mes int;
declare ano int;
begin
	select m.nome from mecanico m where codm = new.codm into nome_codm;
	mes := extract(month from new.data);
	ano := extract(year from new.data);
	count_hours := horasExtra(nome_codm, mes, ano);
	if count_hours > 20 then
		raise exception 'mecanico com mais de 20 horas extras não pode ter mais consertos no mesmo mês.';
		--return null;
	end if;
	return new;
end;
$$ language plpgsql;

create trigger conserto_max before insert on conserto for each row execute procedure func_conserto_max();

select * from conserto c where c.codm = 1 and extract(month from c.data) = '06' ;

insert into conserto values (1, 4, '2014-06-30', '19:00:00');

--8) Gatilho para impedir que mais de 1 conserto seja agendado no mesmo setor na mesma hora. 

create or replace function func_conserto_setor_hora() returns trigger as
$$
begin
	if (select count(*) from conserto c join mecanico m on c.codm = m.codm join setor s on s.cods = m.cods where m.cods = (select cods from mecanico where codm = new.codm)
	and c.data = new.data and extract(hour from c.hora) = extract(hour from new.hora)) > 0 then
		raise exception 'já há conserto no mesmo setor na mesma hora';
		return null;
	end if;
	return new;
end;
$$ language plpgsql;

select count(*) from conserto c join mecanico m on c.codm = m.codm join setor s on s.cods = m.cods where m.cods = (select cods from mecanico where codm = 1);
select * from conserto;

insert into conserto values(1, 2, '2014-06-12', '17:00:00');
create trigger conserto_setor_hora before insert or update on conserto for each row execute procedure func_conserto_setor_hora();
