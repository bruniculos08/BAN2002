-- Questão 01) Recupere o CPF e o nome dos mecânicos que trabalham nos setores maiores que 100 e menores que 200.
select cpf, m.cods, s.nome from mecanico m left join setor s on m.cods = s.cods;
-- Otimização: faz um seq_scan na tabela setor com chave hash como cods e então faz um seq_scan na tabela mecânico fazendo para cada linha o join em...
-- ... complexidade O(1) devido ao hash.  

-- Questão 02) Recupere o CPF e nome dos mecânicos que atenderam no dia 13/06/2018.
drop index idx_data_conserto;
create index idx_data_conserto on conserto using hash(data);

select m.cpf, m.nome from (select * from conserto where data = '2018-06-13') as c join mecanico m on m.codm = c.codm;
-- Otimização: fazer primeiro um consulta sobre a tabela conserto para que a junção seja feita apenas com as linhas cuja data é igual '2018-06-13' e...
-- ... depois realizando uma busca por índice sobre a tabela mecânico pois está ordenada por codm. Sem o index idx_data_conserto é feito um seq_scan na tabela...
-- ... conserto porém com idex idx_data_conserto é feito um bitmap index scan e um bitmap heap scan, que são processos mais rápidos.

-- Questão 03) Recupere o nome do mecânico, o nome do cliente e a hora do conserto para os consertos realizados de 12/06/2018 à 25/09/2018.
drop index idx_conserto;
create index idx_conserto on conserto using btree(data);

drop index idx_cliente;
create index idx_cliente on cliente using hash(codc);

select m.nome, c.nome, cs.hora from mecanico m left join conserto cs using(codm) left join veiculo using(codv) left join cliente c using(codc)
where cs.data < '2018-09-25' and cs.data > '2018-06-12';

-- Otimização: faz index scan da tabela mecanico, cria uma hash nesta tabela então faz bitmap heap scan na tabela conserto realizando o join via hash...
-- ... com a tabela mecanico. Faz-se então um index scan da tabela veiculo e cria-se uma hash para esta tabela então se faz o join via hash com...
-- ... a tabela resultando do join entre as tabelas conserto e mecanico. Por último há um looping aninhado para realizar o join com a tabela...
-- ... cliente sobre a qual se utiliza o índice idx_cliente.

-- Questão 4) Recupere o nome e a função de todos os mecânicos, e o número e o nome dos setores para os mecânicos que tenham essa informação.

select m.nome, m.funcao, m.cods, s.nome from mecanico m left join setor s using(cods);
-- Otimização: cria uma hash na tabela setor que recebe o cods do setor retorna o nome do setor e o próprio cods e então faz um seq_scan na tabela mecanico...
-- ... usando a hash para fazer o join (buscando o nome do setor pela hash).

-- Questão 5) Recupere o nome de todos os mecânicos, e as datas dos consertos para os mecânicos que têm consertos feitos (deve aparecer apenas um registro de nome de mecânico para cada data de conserto).

select m.nome, c.data from mecanico m left join conserto c using(codm);

-- Otimização: faz-se um seq_scan da tabela mecânico e então se cria uma hash nesta tabela, assim faz-se um seq_scan da tabela conserto para então fazer um...
-- ... join entre as duas tabelas usando o hash da tabela mecânico.

-- Questão 6) Recupere a média da quilometragem de todos os veículos dos clientes.

select avg(quilometragem) from veiculo;

-- Otimização: como se trata de uma operação muito simples e para qual se faz necessário acessar todas as linhas da tabela em questão(veiculo) se faz...
-- ... um sec_scan jogando os dados para a função de agregação(avg neste caso).

-- Questão 7) Recupere a soma da quilometragem dos veículos de cada cidade onde residem seus proprietários.

select sum(v.quilometragem), c.cidade from veiculo v join cliente c using(codc) group by cidade;

-- Otimização: faz-se um seq_scan da tabela cliente e então se cria uma hash nesta tabela, assim faz-se um seq_scan da tabela conserto para então fazer um...
-- ... join entre as duas tabelas usando o hash da tabela cliente, e por fim se passam os dados de quilometragem agrupados por cidade para a função de agregação.

-- Questão 8) Recupere a quantidade de consertos feitos por cada mecânico durante o período de 12/06/2018 até 19/10/2018.
drop index idx_conserto;
create index idx_conserto on conserto using btree(data, codm);

select count(m.codm), m.nome from mecanico m left join conserto c using(codm) where c.data > '2018-06-12' and c.data < '2018-10-19' group by codm;

-- Otimização: utiliza o index idx_conserto para fazer um bitmap index scan  e em seguida um bitmap heap scan na tabela conserto, enquanto faz um sec_scan...
-- ... na tabela mecanico e cria uma hash para tal tabela e então usa o index btree sobre o atributo data na tabela conserto e a hash na tabela mecanico para...
-- ... realizar o join. O index idx_conserto foi escolhido como btree pois é útil para uma busca com condicionais '>=' ou '<='.

-- Questão 9) Recupere a quantidade de consertos feitos agrupada pela marca do veículo.

select count(*), v.marca from conserto c left join veiculo v using(codv) group by v.marca;

-- Otimização: realiza um seq_scan da tabela veiculo e cria um hash sobre esta e eentão realiza um seq_scan da tabela conserto e faz-se um join entre a...
-- ... tabela conserto e veiculo percorrendo a primeira e usando hash para buscar os elementos da segunda respectivamente.

-- Questão 10) Recupere o modelo, a marca e o ano dos veículos que têm quilometragem maior que a média de quilometragem de todos os veículos.
drop index idx_veiculo;
create index idx_veiculo on veiculo using btree(quilometragem);

select v.modelo, v.marca, v.ano from veiculo v where v.quilometragem > (select avg(quilometragem) from veiculo) group by v.modelo, v.marca, v.ano
order by v.modelo, v.marca, v.ano;

-- Otimização: usa-se o index idx_veiculo para fazer um bitmap index scan e depois se faz na mesma tabela um bitmap heap scan buscando veiculos com a quilometragem...
-- ... maior que a média qual é calculada via um seq_scan na tabela veiculo que joga os dados na função agregadora avg e então permite a ordenação/busca dos dados...
-- ... pelo bitmap heap scan feito na tabela veiculo.

-- note que o "group by" impede a repetição de linhas (caso de veículos iguais) e também que sem a criação de idx_veiculo a ordenação que ocorre ao final da...
-- ... consulta tem cost = 523,7 enquanto com o idx_veiculo criado tem cost = 506,48.

-- Questão 11) Recupere o nome dos mecânicos que têm mais de um conserto marcado para o mesmo dia.
drop index idx_conserto;
create index idx_conserto on conserto using btree(data, codm);

select m.nome from mecanico m left join conserto c using(codm) where (select count(a.codm) from mecanico a left join conserto b using(codm) 
where a.codm = m.codm and b.data = c.data) > 1 group by codm;

-- Otimização: realiza um index only scan (que é levemente mais rápido que index scan) na tabela conserto e na tabela mecanico e então faz um loop aninhado para...
-- ... fazer o join entre as duas tabelas joga-se o resultado para a função de agregação (que conta a quantidade de consertos realizados pelo mecanico em determinada...
-- data). É também feito um sec_scan da tabela mecanico e feita uma hash para tal tabela e para a tabela conserto é feito um seq_scan que junto com o hash da tabela...
-- mecanico e o resultado da função de agregação se realiza o join entre as tabelas conserto e mecanico.