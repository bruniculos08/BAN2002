-- Exercício 04 - DML (linguagem de manipulação de dados)

-- 1) Recupere o nome e o endereço de cada cliente.
select nome from cliente;

-- 2) Recupere o nome e a função dos mecânicos que trabalham no setor número 2 (cods 2).
select nome from mecanico where cods = 2;

-- 3) Recupere o CPF e o nome de todos os mecânicos que são clientes da oficina (utilize operação de conjuntos).
-- Usando join:
select mecanico.cpf from mecanico join cliente on mecanico.cpf = cliente.cpf;
-- Usando intersect:
select cpf from mecanico intersect select cpf from cliente;

-- 4) Recupere as cidades das quais os mecânicos e clientes são oriundos.
select cidade from mecanico union select cidade from cliente;
-- note que se fosse usado union all (união disjusta) haveria possibilidade de repetições, mas com union isto não acontece.

-- 5) Recupere as marcas distintas dos veículos dos clientes que moram em New York.
select veiculo.marca from veiculo join cliente on veiculo.codc = cliente.codc and cliente.cidade = 'New York';

-- 6) Recupere as funções distintas dos mecânicos da oficina.
select distinct mecanico.funcao from mecanico;

-- 7) Recupere todas as informações dos clientes que têm idade maior que 25 anos.
select all cliente from cliente where idade > 25;

-- 8) Recupere o CPF e o nome dos mecânicos que trabalham no setor de mecânica.
select mecanico.cpf, mecanico.nome from mecanico, setor where mecanico.cods = setor.cods and setor.nome = 'Mecânica';
-- tem que usar ' ao invés de "

-- 9) Recupere o CPF e nome dos mecânicos que trabalharam no dia 13/06/2014.
select cpf, nome, data from mecanico, conserto where mecanico.codm = conserto.codm and conserto.data = '2014-06-13';

-- 10) Recupere o nome do cliente, o modelo do seu veículo, o nome do mecânico e sua função para todos os consertos realizados (utilize join para realizar a junção).
select cliente.nome, veiculo.modelo, mecanico.nome, mecanico.funcao from cliente join veiculo on cliente.codc = veiculo.codc join conserto on veiculo.codv = conserto.codv join mecanico on mecanico.codm = conserto.codm;
-- foi necessário fazer de todas as tabelas sem where (como pede o enunciado).

-- 11) Recupere o nome do mecânico, o nome do cliente e a hora do conserto para as serviços realizados no dia 19/06/2014 (utilize join para realizar a junção).
select mecanico.nome, cliente.nome, conserto.hora from cliente join veiculo on cliente.codc = veiculo.codc join conserto on veiculo.codv = conserto.codv join mecanico on mecanico.codm = conserto.codm where conserto.data = '2014-06-19';

-- 12) Recupere o código e o nome dos setores que foram utilizados entre os dias 12/06/2014 e 14/06/2014 (utilize join para realizar a junção).
select setor.cods, setor.nome from setor join mecanico on setor.cods = mecanico.cods join conserto on mecanico.codm = conserto.codm where conserto.data >= '2014-06-12' and conserto.data <= '2014-06-14';