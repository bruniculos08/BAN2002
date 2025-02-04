
--1) Função para inserção de um mecânico.

--drop function inserirMecanico(pcpf varchar, pnome varchar, pidade int, pendereco varchar, pcidade varchar, pfuncao varchar, psetorNome varchar);
create or replace function inserirMecanico(pcpf varchar, pnome varchar, pidade int, pendereco varchar, pcidade varchar, pfuncao varchar, pCods int) returns void as
$$
declare newCodm int;
begin
	select count(*) from mecanico into newCodm;
	newCodm := newCodm + 1;
	insert into mecanico values (newCodm, pcpf, pnome, pidade, pendereco, pcidade, pfuncao, pCods);
end;
$$ language plpgsql;

select * from mecanico;
select * from setor;

select inserirMecanico('2131231', 'Alfred', 70, 'Caverna', 'Gotham', 'motor', 2);

--2) Função para exclusão de um mecânico. 
--drop function excluirMecanico(pcpf varchar);

create or replace function excluirMecanico(pcpf varchar) returns void as
$$
begin
	delete from mecanico where mecanico.cpf = pcpf;
end;
$$ language plpgsql;

select excluirMecanico('2131231');

--3) Função única para inserção, atualizar e exclusão de um cliente.
create or replace function MecanicoIAE(opcao char, pcpf varchar, pnome varchar, pidade int, pendereco varchar, pcidade varchar, pfuncao varchar, pcods int) returns void as
$$
declare newCodm int;
begin
	if upper(opcao) = 'E' then
		execute excluirMecanico(pcpf);
	elsif upper(opcao) = 'A' then 
		update mecanico set cpf = pcpf, nome = pnome, idade = pidade, endereco = pendereco, cidade = pcidade, funcao = pfuncao, cods = pcods where cpf = pcpf or nome = pnome;
	elsif upper(opcao) = 'I' then
		execute inserirMecanico(newCodm, pcpf, pnome, pidade, pendereco, pcidade, pfuncao, pCods);
	else
		raise notice 'opção inválida';
	end if;

end;
$$ language plpgsql;

select * from mecanico;
select MecanicoIAE('O', '2131231', 'Alfred', 70, 'Caverna', 'Gotham', 'motor', 2);
select MecanicoIAE('E', '02131231', 'Alfred', 70, 'Caverna', 'Gotham', 'motor', 2);
select MecanicoIAE('I', '2131231', 'Alfred', 70, 'Caverna', 'Gotham', 'motor', 2);
select MecanicoIAE('A', '02131231', 'Alfred', 70, 'Caverna', 'Gotham', 'motor', 2);

--4) Função que limite o cadastro de no máximo 10 setores na oficina mecânica.

create or replace function limiteSetores() returns void as
$$
declare counter int;
declare item record;
begin
	counter := 0;
	for item in select * from setor loop
		counter := counter + 1;
		if counter > 10 then
			delete from setor where setor.cods = item.cods;
		end if;
	end loop;
end;
$$ language plpgsql;

select * from setor;
insert into setor values (11, 'teste');
select limiteSetores();

--5) Função que limita o cadastro de um conserto apenas se o mecânico não tiver mais de 3 consertos agendados para o mesmo dia.

DROP FUNCTION inserirconserto(integer,integer,date,time without time zone);

create or replace function inserirConserto(newcodm int, newcodv int, newdata date, newhora time) returns void as
$$
declare numeroDeConsertos int;
begin
	select count(*) from conserto where conserto.codm = newcodm and data = conserto.data into numeroDeConsertos;
	if numeroDeConsertos <= 4 then
		insert into conserto values (newcodm, newcodv, newdata, newhora);
	else
		raise exception 'Mais de 3 consertos no mesmo dia!';
	end if;
end;
$$ language plpgsql;

select count(mecanico.codm), mecanico.* from mecanico join conserto on mecanico.codm = conserto.codm group by mecanico.codm;
select mecanico.*, conserto.data, conserto.hora, conserto.codv from mecanico join conserto on mecanico.codm = conserto.codm;
select count(codm), codm, data from conserto where data = '2014-06-13' group by conserto.codm, conserto.data;
select * from conserto;

select count(*) from conserto where conserto.codm = 2 and data = '2014-06-13';
select inserirConserto(2, 6, '2014-06-13', '09:10:00');

--6) Função para calcular a média geral de idade dos Mecânicos e Clientes.

create or replace function mediaIdadeGeral() returns void as
$$
declare media float;
begin
	select avg(idade) from (select mecanico.idade from mecanico union select cliente.idade from cliente) as idade into media;
	raise notice '%', media;
end;
$$ language plpgsql;

select mediaIdadeGeral();


--7) Função única que permita fazer a exclusão de um Setor, Mecânico, Cliente ou Veículo.

create or replace function excluirSMCV(opcao char, chave int) returns void as
$$
begin
	if(opcao = 'S') then
		delete from setor where cods = chave;
	elsif(opçao = 'M') then
		delete from mecanico where codm = chave;
	elsif(opçao = 'C') then
		delete from cliente where codc = chave;
	else
		delete from veiculos where codv = chave;
	end if;
end;
$$ language plpgsql;

--8) Considerando que na tabela Cliente apenas codc é a chave primária, faça uma função que remova clientes com CPF repetido, deixando apenas um cadastro para cada CPF. 
-- Escolha o critério que preferir para definir qual cadastro será mantido: aquele com a menor idade, que possuir mais consertos agendados, etc. 
-- Para testar a função, não se esqueça de inserir na tabela alguns clientes com este problema.

create or replace function cpfRepetido() returns void as
$$
declare item record;
declare maiorIdade int;
begin
	for item in select count(cpf), cpf from cliente group by cpf loop
		if item.count > 1 then
			select max(idade) from cliente where cpf = item.cpf into maiorIdade;
			delete from cliente where cpf = item.cpf and idade < maiorIdade;
		end if;
	end loop;
end;
$$ language plpgsql;

select cpfRepetido();
select * from cliente;
insert into cliente values(8, '20000220000', 'William', 29, 'Harlem', 'New York');
update cliente set idade = 20 where codc = 8;

--9) Função para calcular se o CPF é válido*.

DROP FUNCTION cpfValido(p_cpf varchar(11));

create or replace function cpfValido(p_cpf varchar(11)) returns boolean as
$$
declare somaPrimeiroDigito int default 0;
declare somaSegundoDigito int default 0;
declare primeiroDigito int default 0;
declare segundoDigito int default 0;
declare count int default 0;
declare cpf_array int[];
begin
	-- pode se utilizar cast (como feito pelo professor)
	cpf_array := regexp_split_to_array(regexp_replace(p_cpf, '[^0-9]', '', 'g'), '');
	-- raise notice 'teste';
	-- (1) Verificando o primeiro dígito:
	-- Andar na posição 1 até 9 pois o somatório não utiliza os dois últimos dígitos
	-- raise notice '% cpf digito 1º', cpf_array[10];
	for i in 1..9 loop
		-- raise notice 'somando % vezes %', 11-i, cpf_array[i];
		somaPrimeiroDigito := somaPrimeiroDigito + (11-i)*cpf_array[i];
		-- raise notice '% na posição %', cpf_array[i], i;
	end loop;
	--raise notice 'soma do primeiro digito = %', somaPrimeiroDigito;
	
	if somaPrimeiroDigito%11 >= 2 then
		primeiroDigito := 11 - (somaPrimeiroDigito%11);
	end if;
	--raise notice 'primeiro digito = %', primeiroDigito;

	-- (2) Verificando o segundo dígito:
	-- faz se o mesmo somatório como no primeiro dígito porém se adiciona o primeiro dígito multiplicado por 2
	for i in 1..9 loop
		--raise notice 'somando % vezes %', 12-i, cpf_array[i];
		somaSegundoDigito := somaSegundoDigito + (12-i)*cpf_array[i];
	end loop;
	
	somaSegundoDigito := somaSegundoDigito + 2*primeiroDigito;

	--raise notice 'soma do segundo digito = %', somaSegundoDigito;

	if somaSegundoDigito%11 >= 2 then
		segundoDigito := 11 - (somaSegundoDigito%11);
	end if;

	--raise notice 'segundo digito = %',segundoDigito;

	if primeiroDigito != cpf_array[10] or segundoDigito != cpf_array[11] then
		return false;
	end if;
	
	return true;
end;
$$ language plpgsql;

--10) Função que calcula a quantidade de horas extras de um mecânico em um mês de trabalho. 
--O número de horas extras é calculado a partir das horas que excedam as 160 horas de trabalho mensais. 
--O número de horas mensais trabalhadas é calculada a partir dos consertos realizados. Cada conserto tem a duração de 1 hora.

create or replace function horasExtra(p_nome varchar(50), mes int, ano int) returns int as 
$$
declare horasConserto int default 0;
begin
	--select count(m.codm) from conserto c join mecanico m on c.codm = m.codm where m.nome = p_nome and c.data = mes and c.data = ano into horasConserto;
	select count(m.codm) from conserto c join mecanico m on c.codm = m.codm where m.nome = p_nome and EXTRACT(MONTH FROM c.data) = mes and EXTRACT(YEAR FROM c.data) = ano into horasConserto;
	if horasConserto > 160 then
		return horasConserto-160;
	end if;
	return 0;
end;
$$ language plpgsql;

select c.data, m.nome from conserto c join mecanico m on c.codm = m.codm;

select horasExtra('Carlos', 6, 2014);
--* Como calcular se o CPF é válido:

--O CPF é composto por onze algarismos, onde os dois últimos são chamados de dígitos verificadores, ou seja, os dois últimos dígitos são criados a partir dos nove primeiros. 
--O cálculo é feito em duas etapas utilizando o módulo de divisão 11. Para exemplificar melhor será usado um CPF hipotético, por exemplo, 222.333.444-XX.

--O primeiro dígito é calculado com a distribuição dos dígitos colocando-se os valores 10,9,8,7,6,5,4,3,2 conforme a representação abaixo:

--2 2 2 3 3 3 4 4 4

--10 9 8 7 6 5 4 3 2

--Na seqüência multiplica-se os valores de cada coluna:

--2    2    2    3    3    3    4    4    4

--10  9    8    7    6    5    4    3    2

--20 18  16  21  18  15  16  12   8

--Em seguida efetua-se o somatório dos resultados (20+18+...+12+8), o resultado obtido (144) deve ser divido por 11.
--Considere como quociente apenas o valor inteiro, o resto da divisão será responsável pelo cálculo do primeiro dígito verificador. 
--144 dividido por 11 tem-se 13 de quociente e 1 de resto da divisão. 
--Caso o resto da divisão seja menor que 2, o primeiro dígito verificador se torna 0 (zero), caso contrário subtrai-se o valor obtido de 11. 
--Como o resto é 1 então o primeiro dígito verificador é 0 (222.333.444-0X).

--Para o cálculo do segundo dígito será usado o primeiro dígito verificador já calculado. 
--Monta-se uma tabela semelhante a anterior só que desta vez é usado na segunda linha os valores 11,10,9,8,7,6,5,4,3,2, já que é incorporado mais um algarismo para esse cálculo.

--2    2   2  3  3  3  4  4  4  0

--11 10  9  8  7  6  5  4  3  2

--Na próxima etapa é feita como na situação do cálculo do primeiro dígito verificador, multiplica-se os valores de cada coluna:

--2     2    2    3    3    3    4    4    4   0

--11  10   9    8    7    6    5    4    3   2

--22  20  18  24  21  18  20  16  12  0

--Depois efetua-se o somatório dos resultados: 22+20+18+24+21+18+20+16+12+0=171.

--Agora, pega-se esse valor e divide-se por 11. 
--Considere novamente apenas o valor inteiro do quociente, e com o resto da divisão, no caso 6, usa-se para o cálculo do segundo dígito verificador, assim como na primeira parte. 
--Se o valor do resto da divisão for menor que 2, esse valor passa automaticamente a ser zero, caso contrário é necessário subtrair o valor obtido de 11 para se obter o dígito verificador, 
--nesse caso 11-6=5. Portanto, chega-se ao final dos cálculos e descobre-se que os dígitos verificadores do CPF hipotético são os números 0 e 5, portanto o CPF fica:

--222.333.444-05
