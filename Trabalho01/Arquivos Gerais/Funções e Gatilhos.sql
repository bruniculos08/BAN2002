select * from veiculo;
select * from departamento;
select * from Nota;
select * from pedido;

insert into departamento values(1, 'Carros Azuis');
insert into departamento values(2, 'Carros Amarelos');
insert into departamento values(5, 'Carros Voadores');
insert into departamento values(7, 'O cara da grana');
insert into veiculo values('1M8GDM9AXKP042788', true, true, true, 1);
insert into veiculo values('9BRPRWHEXG0107792', true, true, true, 1);
insert into veiculo values('9BRPRWHEXG0107744', true, true, true, 2);

-- Função para verificar se o código do chassi é válido:

-- (1) Remove all of the letters from the VIN by transliterating them with their numeric counterparts. Numerical counterparts can be found in the table below.
-- (2) Multiply this new number, the yield of the transliteration, with the assigned weight. Weights can be found in the table below.
-- (3) Sum the resulting products.
-- (4) Modulus the sum of the products by 11, to find the remainder.
-- (5) If the remainder is 10 replace it with X.

-- Obs.: funções letraNumeroChassi() arrumada e validarChassi() (11/11/2022 às 01:06).
select validarChassi(cast('4KKf00EhutTjg1530' as varchar));

create or replace function validarChassi(p_chassi varchar) returns boolean as
$$
declare check_sum int default 0;
declare word varchar[];
declare vetor_pesos int[] default '{8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2}';
begin	
	word := regexp_split_to_array(p_chassi, '');
	
	-- VIN não pode ter as letras Q, I ou O:
	for i in 1..17 loop
		if upper(word[i]) = 'Q' or upper(word[i]) = 'I' or upper(word[i]) = 'O' then
			return false;
		end if;
	end loop;
	
	-- VIN tem 17 caracteres:
	if length(p_chassi) <> 17 then
		return false;
	end if;

	-- VIN verifica soma:
	for i in 1..17 loop
		check_sum := check_sum + vetor_pesos[i]*letraNumeroChassi(cast(word[i] as char));
	end loop;

	--raise notice '%', check_sum;
	check_sum := check_sum % 11;

	if check_sum = 10 and upper(cast(word[9] as char)) = 'X'then
		return true;
	elsif check_sum = letraNumeroChassi(cast(word[9] as char)) then
		return true;
	end if;

	return false;
end;
$$ language plpgsql;

-- Função que recebe uma letra e retorna um número de acordo com a tabela de dígitos para chassi:
create or replace function letraNumeroChassi(letra char) returns int as
$$
begin	
	letra := upper(letra);

	if letra = 'A' or letra = 'J' then
		return 1;
	elsif letra = 'B' or letra = 'K' or letra = 'S' then
		return 2;
	elsif letra = 'C' or letra = 'L' or letra = 'T' then
		return 3;
	elsif letra = 'D' or letra = 'M' or letra = 'U' then
		return 4;
	elsif letra = 'E' or letra = 'N' or letra = 'V' then
		return 5;
	elsif letra = 'F' or letra = 'W' then
		return 6;
	elsif letra = 'G' or letra = 'P' or letra = 'X' then
		return 7;
	elsif letra = 'H' or letra = 'Y' then
		return 8;
	elsif letra = 'R' or letra = 'Z' then
		return 9;
	end if;
	return cast(letra as integer);
end;
$$ language plpgsql;

-- Gatilho para verificar VIN (chassi) antes de inserir ou de fazer update na tabela veículo:

create or replace function validarChassiGatilho() returns trigger as
$$
begin
	if validarChassi(new.chassi) = true then
		return new;
	end if;
	raise notice 'Chassi inválido!';
	return old;
end;
$$
language plpgsql;

create trigger verificaChassi before insert or update on veiculo for each row execute procedure validarChassiGatilho();

-- Função que valida a chave de acesso de nota fiscal:

create or replace function validarNota(p_cod varchar(44)) returns boolean as
$$
declare vetor_pesos int[] default '{4, 3, 2, 9, 8, 7, 6, 5}';
declare size_pesos int default 8;
declare check_sum int default 0;
declare word int[];
begin
	word := regexp_split_to_array(p_cod, '');
	
	for i in 1..43 loop
		check_sum := check_sum + (word[i])*(vetor_pesos[(i-1)%8 + 1]);
	end loop;
	
	--raise notice 'check sum = %', check_sum;
	check_sum := check_sum%11;
	
	if (check_sum = 0 or check_sum = 1) and word[44] = '0' then
		return true;
	elsif check_sum = 11 - cast(word[44] as integer) then
		return true;
	end if;
	return false;
end;
$$
language plpgsql;


insert into fornecedor values('88672068908640', 'Corleone');
delete from fornecedor where cnpj = '88672068908640';
select * from departamento;
select * from veiculo;
select * from fornece;
select * from componente_necessario;
select * from pedido;
select * from nota_fiscal where cod_nota = '42221039766179000128650200000524051005241115';
delete from nota_fiscal where cod_nota = '42221039766179000128650200000524051005241115'
select validarNota('13181017921427000125650010000000309887251170');
select validarNota('42221039766179000128650200000524051005241115');


-- Gatilho para verificar nota fiscal antes de ser inserida em nota_fiscal:

create or replace function verificarNota() returns trigger as
$$
begin
	if validarNota(new.cod_nota) = true then
		return new;
	end if;
	raise notice 'cod nota (chave da nota fiscal) inválido!';
	return old;
end;
$$
language plpgsql;

create trigger verificarNotaGatilho before insert or update on nota_fiscal for each row execute procedure verificarNota();

-- Gatilho para não permitir que um departamento de compra personalize veículo:

create or replace function verificaDepartamentoDeCompra() returns trigger as
$$
begin
	if(select count(1) from pedido p where p.cod_dept_compra = new.cod_dept) > 0 then
		raise notice 'Um departamento de compras não pode produzir carros!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

create trigger verificaDepartamentoDeCompraGatilho before insert or update on veiculo for each row execute procedure verificaDepartamentoDeCompra();

-- Gatilho para não permitir que um departamento que personalização veiculo atue como departamento de compra:
update pedido set cod_depto_compra = 2;
select * from pedido;

create or replace function verificaDepartamentoDeProducao() returns trigger as
$$
begin
	if(select count(1) from veiculo where cod_dept = new.cod_dept_compra) > 0 then
		raise notice 'Um departamento de produção não pode atuar como departamento de compras!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

create trigger verificaDepartamentoDeProducaoGatilho before insert or update on pedido for each row execute procedure verificaDepartamentoDeProducao();

-- View para o número de veículos personalizados por departamento:

create view NumCarros(dept, NumOfCars) as select d.cod_dept, count(v.chassi) from departamento d left join veiculo v on d.cod_dept = v.cod_dept group by d.cod_dept;
create view NumCarros(dept, NumOfCars) as select d.cod_dept, count(v.chassi) from departamento d left join veiculo v using(cod_dept) group by d.cod_dept;

drop view NumCarros;
select * from NumCarros;

-- View para o número de pedidos de compra por departamento(de compra):
select * from pedido;

create view NumPedidos(dept, NumOfPedidos) as select d.cod_dept, count(e.*) from pedido e right join departamento d on d.cod_dept = e.cod_dept_compra group by d.cod_dept;

drop view NumPedidos;
select * from NumPedidos;
