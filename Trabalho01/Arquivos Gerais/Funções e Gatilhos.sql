-- Função para verificar de CNPJ é válido:

drop function validarCNPJ(p_cnpj varchar);
create or replace function validarCNPJ(p_cnpj varchar) returns boolean as
$$
declare check_sum int default 0;
declare check_num1 int default 0;
declare check_num2 int default 0;
declare nums varchar[];
declare vetor_pesos int[] default '{6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2}';
begin
	nums := regexp_split_to_array(p_cnpj, '');
	for i in 1..12	 loop
		check_sum := check_sum + (cast(nums[i] as int) * vetor_pesos[i+1]);
	end loop;
	
	check_num1 := 0;
	if (check_sum % 11) < 2 then
		check_num1 := 0;
	else
		check_num1 := 11 - check_sum % 11;
	end if;
	
	check_sum := 0;
	for i in 1..12 loop
		check_sum := check_sum + (cast(nums[i] as int) * vetor_pesos[i]);
	end loop;
	check_sum := check_sum + 2*check_num1;
	
	check_num2 := 0;
	if (check_sum % 11) < 2 then
		check_num2 := 0;
	else
		check_num2 := 11 - check_sum % 11;
	end if;
	
	if (check_num1 = cast(nums[13] as int) and check_num2 = cast(nums[14] as int)) then
		return true;
	end if;
	return false;
end;
$$
language plpgsql;

-- Gatilho para verificar o CNPJ de fornecedor antes de inserir ou fazer update na tabela:

drop function verificaCNPJ() cascade;
create or replace function verificaCNPJ() returns trigger as
$$
begin
	if(validarCNPJ(new.cnpj) = true) then
		return new;
	end if;
	raise exception 'CNPJ inválido!';
	return old;
end;
$$
language plpgsql;

drop trigger verificaCnpjGatilho on fornecedor;
create trigger verificaCnpjGatilho before insert or update on fornecedor for each row execute procedure verificaCNPJ();

-- Função para verificar se o VIN (Chassi internacional) é válido:

-- (1) Remove all of the letters from the VIN by transliterating them with their numeric counterparts. Numerical counterparts can be found in the table below.
-- (2) Multiply this new number, the yield of the transliteration, with the assigned weight. Weights can be found in the table below.
-- (3) Sum the resulting products.
-- (4) Modulus the sum of the products by 11, to find the remainder.
-- (5) If the remainder is 10 replace it with X.

-- Obs.: funções letraNumeroChassi() arrumada e validarChassi() (11/11/2022 às 01:06).

drop function validarChassi(p_chassi varchar);
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

drop function letraNumeroChassi(letra char);
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

drop function validarChassiGatilho() cascade;
create or replace function validarChassiGatilho() returns trigger as
$$
begin
	if validarChassi(new.chassi) = true then
		return new;
	end if;
	raise exception 'Chassi inválido!';
	return old;
end;
$$
language plpgsql;

drop trigger verificaChassi on veiculo;
create trigger verificaChassi before insert or update on veiculo for each row execute procedure validarChassiGatilho();

-- Função que valida a chave de acesso de nota fiscal:

drop function validarNota(p_cod varchar(44));
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

-- Gatilho para verificar nota fiscal antes de ser inserida em nota_fiscal:

drop function verificaNota() cascade;
create or replace function verificarNota() returns trigger as
$$
begin
	if validarNota(new.cod_nota) = true then
		return new;
	end if;
	raise exception 'cod nota (chave da nota fiscal) inválido!';
	return old;
end;
$$
language plpgsql;

drop trigger verificarNotaGatilho on nota_fiscal;
create trigger verificarNotaGatilho before insert or update on nota_fiscal for each row execute procedure verificarNota();

-- Gatilho para não permitir que um departamento de compra personalize veículo:

drop function verificaDepartamentoDeCompra() cascade;
create or replace function verificaDepartamentoDeCompra() returns trigger as
$$
begin
	if(select 1 from departamento d where d.cod_dept = new.cod_dept and d.tipo = 'compra') then
		raise exception 'Um departamento de compras não pode produzir carros!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger verificaDepartamentoDeCompraOnVeiculoGatilho on veiculo;
create trigger verificaDepartamentoDeCompraOnVeiculoGatilho before insert or update on veiculo for each row execute procedure verificaDepartamentoDeCompra();

drop trigger verificaDepartamentoDeCompraOnComponenteNecessarioGatilho on componente_necessario;
create trigger verificaDepartamentoDeCompraOnComponenteNecessarioGatilho before insert or update on componente_necessario for each row execute procedure verificaDepartamentoDeCompra();

-- Gatilho para não permitir que um departamento de personalização veiculo atue como departamento de compra:

drop function verificaDepartamentoDeProducao() cascade;
create or replace function verificaDepartamentoDeProducao() returns trigger as
$$
begin
	if(select 1 from departamento d where d.cod_dept = new.cod_dept_compra and d.tipo = 'producao') then
		raise exception 'Um departamento de produção não pode atuar como departamento de compras!';
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger verificaDepartamentoDeProducaoGatilho on pedido;
create trigger verificaDepartamentoDeProducaoGatilho before insert or update on pedido for each row execute procedure verificaDepartamentoDeProducao();

-- Gatilhos e funções extras (adicionados após a entrega 03) a partir desta linha:

-- Gatilho para ajuste da table 'componente' em inserções, se o componente já existir na tabela, sua quantidade será acrescida de acordo...
-- ... com a quantidade que seria adicionada e a quantidade miníma será a maior das duas quantidades mínimas:

drop function addComponente() cascade;
create or replace function addComponente() returns trigger as
$$
begin
	if (select count(*) from componente cn where nome = new.nome) > 0 then
		update componente cn set quantidade = quantidade + 1, minimo_quant = max(minimo_quant, new.minimo_quant) where nome = new.nome;
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger addComponeteGatilho on componente;
create trigger addComponeteGatilho before insert on componente for each row execute procedure addComponente();

-- Função auxiliar para a função acima:

drop function max(num1 numeric, num2 numeric);
create or replace function max(num1 numeric, num2 numeric) returns numeric as
$$
begin
	if num1 >= num2 then
		return num1;
	end if;
	return num2;
end;
$$
language plpgsql;

-- Gatilho para ajuste da tabela 'componente_necessario' em inserções (igual o gatilho anterior sobre a tabela componente), se o componente já existir na tabela sua quantidade será acrecscida de acordo...
-- ... com a quantidade que seria adicionada:

drop function addComponenteNecessario() cascade;
create or replace function addComponenteNecessario() returns trigger as
$$
begin
	if (select count(*) from componente_necessario where nome_componente = new.nome_componente and cod_dept = new.cod_dept) > 0 then
		update componente_necessario set quantidade = (quantidade + new.quantidade) where nome_componente = new.nome_componente and cod_dept = new.cod_dept;
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger addComponenteNecessarioGatilho on componente_necessario;
create trigger addComponenteNecessarioGatilho before insert on componente_necessario for each row execute procedure addComponenteNecessario();

-- Gatilho para ajuste da tabela 'contem' em inserções (igual o gatilho anterior sobre a tabela componente_necessario), se o componente já existir na tabela sua quantidade será acrecscida de acordo...
-- ... com a quantidade que seria adicionada:

drop function addContem() cascade;
create or replace function addContem() returns trigger as
$$
begin
	if (select count(*) from contem where nome_componente = new.nome_componente and id_pedido = new.id_pedido) > 0 then
		update contem set quantidade = (quantidade + new.quantidade) where nome_componente = new.nome_componente and id_pedido = new.id_pedido;
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger addContemGatilho on contem;
create trigger addContemGatilho before insert on contem for each row execute procedure addContem();

-- View para o número de veículos personalizados por departamento:

drop view NumCarros;
create view NumCarros(cod_dept, NumOfCarros) as select d.cod_dept, count(v.chassi) from departamento d left join veiculo v using(cod_dept) where d.tipo = 'producao' 
group by d.cod_dept;

-- View para o número de pedidos de compra por departamento(de compra):

drop view NumPedidos;
create view NumPedidos(cod_dept, NumOfPedidos) as select d.cod_dept, count(e.*) from pedido e right join departamento d on d.cod_dept = e.cod_dept_compra 
where d.tipo = 'compra' group by d.cod_dept;

-- View para obter receitas mensais:

drop view Receita;
create view Receita(valor, mes, ano) as select sum(valor_producao), extract(month from data_producao), extract(year from data_producao) from veiculo group by (extract(month from data_producao), 
extract(year from data_producao)) order by (extract(year from data_producao), extract(month from data_producao));

-- View para obter despesas mensais:

drop view Despesa;
create view Despesa(valor, mes, ano) as 
select sum(valor_compra*contem.quantidade), extract(month from data_criacao), extract(year from data_criacao) from pedido left join contem on id = id_pedido 
join (select nome, valor_compra from componente) as componente on nome = nome_componente group by extract(year from data_criacao), extract(month from data_criacao);

-- Gatilho para nome de fornecedores:

drop function nomeIgual() cascade;
create or replace function nomeIgual() returns trigger as
$$
begin
	if TG_OP = 'UPDATE' then
		if old.nome = new.nome then
			return new;
		end if;
	end if;
	if (select count(*) from fornecedor where fornecedor.nome = new.nome) > 0 then
		raise exception 'Não pode haver mais de um fornecedor com o mesmo nome!';
		return null;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger nomeIgualGatilho on fornecedor;
create trigger nomeIgualGatilho before insert or update on fornecedor for each row execute procedure nomeIgual();

-- Gatilho para quando um componente for adicionado o seu fornecedor principal seja automaticamente adicionado na tabela fornece:

drop function atualizaInsertUpdateFornecedorPrincipal() cascade;
create or replace function atualizaInsertUpdateFornecedorPrincipal() returns trigger as
$$
begin
	if (select count(*) from fornece f where f.nome_componente = new.nome and f.cnpj = new.cnpj_principal) = 0 then
		insert into fornece values(new.nome, new.cnpj_principal);
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger atualizaInsertUpdateFornecedorPrincipalGatilho on componente;
create trigger atualizaInsertUpdateFornecedorPrincipalGatilho after insert or update on componente for each row execute procedure atualizaInsertUpdateFornecedorPrincipal();

-- Gatilho para impedir que um fornecedor principal seja removido da tabela fornecedor por componente:

drop function fornecedorPermanente() cascade;
create or replace function fornecedorPermanente() returns trigger as
$$
declare counter int default 0;
declare	do_trigger int default 1;
begin
	counter := (select count(*) from componente c where c.nome = old.nome_componente and c.cnpj_principal = old.cnpj);
	do_trigger := (select count(*) from variable where trigger_on = true);
	
	if do_trigger = 0 then
		if TG_OP = 'DELETE' then 
			return old;
		elsif TG_OP = 'UPDATE' then
			return new;
		end if;
	elsif TG_OP = 'DELETE' and counter > 0 then
		raise exception 'Este campo não pode ser deletado pois se trata de uma relação entre componente e fornecedor principal!';
		return null;
	elsif counter > 0 and (new.cnpj <> old.cnpj or new.nome_componente <> old.nome_componente) then
		raise exception 'Este campo não pode ser atualizado pois se trata de uma relação entre componente e fornecedor principal!';
		return old;
	elsif TG_OP = 'UPDATE' then
		return new;
	end if;
	return old;
end;
$$
language plpgsql;

drop trigger fornecedorPermanenteGatilho on fornece;
create trigger fornecedorPermanenteGatilho before update or delete on fornece for each row execute procedure fornecedorPermanente();

-- Gatilho para que o tipo de um departamento seja 'personalização' ou 'compra':

drop function tipoDepartamento() cascade;
create or replace function tipoDepartamento() returns trigger as
$$
begin
	if upper(new.tipo) <> 'COMPRA' and (upper(new.tipo) <> 'PRODUÇÃO' and upper(new.tipo) <> 'PRODUCAO') then
		raise exception 'O tipo de do deparmento deve ser compra ou personalização';
		return old;
	elsif upper(new.tipo) = 'COMPRA' then
		new.tipo := 'compra';
	elsif (upper(new.tipo) = 'PRODUCAO' or upper(new.tipo) != 'PRODUCAO') then
		new.tipo := 'producao';
	end if;
	if TG_OP = 'INSERT' then 
		new.cod_dept := (select nextval('dept_cod'));
	elsif new.tipo != old.tipo then
		if old.tipo = 'compra' and (select count(*) from pedido where cod_dept_compra = old.cod_dept) > 0 then
			raise exception 'O tipo do departamento não pode ser alterado pois ele possui pedidos de compra realizados!';
			return old;
		elsif (select count(*) from veiculo where cod_dept = old.cod_dept) > 0 then
			raise exception 'O tipo do departamento não pode ser alterado pois ele possui veiculos colocados em producao!';
			return old;
		end if;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger tipoDepartamentoGatilho on departamento;
create trigger tipoDepartamentoGatilho before insert or update on departamento for each row execute procedure tipoDepartamento();

-- View que mostra os departamentos de compra e a quantidade de pedidos em cada:

drop view pedidosPorDepartamento;
create view pedidosPorDepartamento as select d.cod_dept, count(p.id) from departamento d left join pedido p on d.cod_dept = p.cod_dept_compra 
where d.tipo = 'compra' group by d.cod_dept order by count(p.id) ASC;

-- Função que retorna o cod_dept do departamento de compra com menos pedidos feitos:

drop function getDepartamentoDeCompra() cascade;
create or replace function getDepartamentoDeCompra() returns integer as
$$
declare codigo int default 0;
begin
	if (select count(*) from pedidosPorDepartamento) = 0 then
		raise exception 'Não há departamento de compra';
		return null;
	end if;
	codigo := (select cod_dept from (select * from pedidosPorDepartamento fetch first row only) as tabela);
	return codigo;
end;
$$
language plpgsql;

-- Função que atualiza a quantidade de um determinado componente:

drop function atualizaQuantidadeComponente(nome varchar(50)) cascade;
create or replace function atualizaQuantidadeComponente(arg_nome varchar(50)) returns boolean as
$$
declare counterContem int default 0;
declare counterNecessario int default 0;
declare saldo int default 0;
declare quantidadeMinima int default 0;
declare cnpjPrincipal varchar(14);
declare newIdPedido int;
declare codDeptPedido int;
declare data_atual date;
begin
	update variable set trigger_on = false;
	
	counterContem := (select COALESCE(sum(c.quantidade),0) from contem c where c.nome_componente = arg_nome);
	counterNecessario := (select COALESCE(sum(c.quantidade),0) from componente_necessario c where c.nome_componente = arg_nome);
	quantidadeMinima := (select minimo_quant from componente c where c.nome = arg_nome);
	
	saldo := (counterContem - counterNecessario);
	
	if (saldo < quantidadeMinima) then
		newIdPedido := (select nextval('pedido_id'));
		cnpjPrincipal := (select cnpj_principal from componente c where c.nome = arg_nome);
		data_atual := (select cast(now() as date));
		codDeptPedido := (getDepartamentoDeCompra());
		if codDeptPedido = null then 
			update variable set trigger_on = true;
			raise exception 'a operação implica na necessidade de serem feitos pedidos mas não há departamento de compra para tal!';
			return false;
		end if;
		insert into pedido values(newIdPedido, data_atual, cnpjPrincipal, codDeptPedido);
		insert into contem values(arg_nome, newIdPedido, (quantidadeMinima-saldo));
		update componente set quantidade = (quantidadeMinima) where nome = arg_nome;
		update variable set trigger_on = true;
		raise notice '% pedido(s) automaticos realizados!', (quantidadeMinima-saldo);
		return true;
	end if;
	update componente set quantidade = (saldo) where nome = arg_nome;
	update variable set trigger_on = true;
	return true;
end;
$$
language plpgsql;

-- Para esta função é necessária um "variável global" para que não haja problema de recursão infinita:

drop table variable cascade;
create table variable(trigger_on boolean);
insert into variable values(true);

-- Gatilho que verifica se um componente está com a quantidade menor que a mínima e gera novo pedido automático:

drop function pedidoAutomatico() cascade;
create or replace function pedidoAutomatico() returns trigger as
$$
declare signal boolean default false;
declare	do_trigger int default 1;
begin
	do_trigger := (select count(*) from variable where trigger_on = true);
	if do_trigger = 0 then
		return new;
	end if;

	if TG_TABLE_NAME = 'componente' then
		if new.minimo_quant > 0 then
			signal := atualizaQuantidadeComponente(new.nome);
		end if;
	elsif TG_OP != 'DELETE' then
		if new.nome_componente = old.nome_componente then
			signal := atualizaQuantidadeComponente(new.nome_componente);
		else
			signal := atualizaQuantidadeComponente(old.nome_componente);
		end if;
	else
		signal := atualizaQuantidadeComponente(old.nome_componente);
	end if;
	if signal = false then
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger pedidoAutomaticoOnComponenteGatilho on componente;
create trigger pedidoAutomaticoOnComponenteGatilho after update or insert on componente for each row execute procedure pedidoAutomatico();

drop trigger pedidoAutomaticoOnComponenteNecessarioGatilho on componente_necessario;
create trigger pedidoAutomaticoOnComponenteNecessarioGatilho after update or insert or delete on componente_necessario for each row execute procedure pedidoAutomatico();

drop trigger pedidoAutomaticoOnContemGatilho on contem;
create trigger pedidoAutomaticoOnContemGatilho after update or insert or delete on contem for each row execute procedure pedidoAutomatico();

-- Gatilho para que veiculos e pedidos sejam sempre adicionados com a data do memomento da inserção:

drop function dataInsert() cascade;
create or replace function dataInsert() returns trigger as
$$
begin
	if TG_TABLE_NAME = 'pedido' then
		new.data_criacao := cast(now() as date);
	else
		new.data_producao := cast(now() as date);
		new.estagio := 'início';
	end if;
	return new;
end;
$$
language plpgsql;

drop trigger dataInsertOnPedido on pedido;
create trigger dataInsertOnPedido before insert on pedido for each row execute procedure dataInsert();

drop trigger dataInsertOnVeiculo on veiculo;
create trigger dataInsertOnVeiculo before insert on veiculo for each row execute procedure dataInsert();

-- Testando:

select * from pedido;
insert into pedido values(84, '0001-01-01', '', '');
insert into fornecedor values('121111', 'teste');

-- Comando para listar todas as funções no banco de dados:
SELECT pg_get_functiondef(p.oid) FROM pg_proc p INNER JOIN pg_namespace ns ON p.pronamespace = ns.oid WHERE ns.nspname = 'public';

-- Comando para listar todas os gatilhos no banco de dados:
select trigger_schema, trigger_name, action_statement from information_schema.triggers;