--Descrição: Considerando o esquema da mecânica automotiva, faça a especificação dos comandos SQL para as seguintes consultas:

--1) Recupere o CPF e o nome dos mecânicos que trabalham nos setores número 1 e 2 (faça a consulta utilizado a cláusula IN).

select m.cpf, m.nome from mecanico m join setor s using(cods) where cods in (1, 2);

--2) Recupere o CPF e o nome dos mecânicos que trabalham nos setores 'Funilaria' e 'Pintura' (faça a consulta utilizando sub-consultas aninhadas).

select m.cpf, m.nome from mecanico m join setor s using(cods) where s.nome = 'Funilaria' or s.nome = 'Pintura';

select m.cpf, m.nome from mecanico m join setor s using(cods) where m.codm in (select m.codm from mecanico m join setor s using (cods) where s.nome = 'Funilaria' or s.nome = 'Pintura');

--3) Recupere o CPF e nome dos mecânicos que atenderam no dia 13/06/2014 (faça a consulta usando INNER JOIN).

select m.cpf, m.nome from mecanico m inner join conserto c on m.codm = c.codm where c.data = '2014-06-13';

select * from mecanico m inner join conserto c on m.codm = c.codm where c.data = '2014-06-13';

--4) Recupere o nome do mecânico, o nome do cliente e a hora do conserto para os consertos realizados no dia 12/06/2014 (faça a consulta usando INNER JOIN).

select mecanico.nome, cliente.nome, conserto.hora from mecanico inner join conserto using(codm) inner join veiculo using(codv) inner join cliente using(codc);

--5) Recupere o nome e a função de todos os mecânicos, e o número e o nome dos setores para os mecânicos que tenham essa informação.

select m.nome, m.funcao, s.cods, s.nome from mecanico m inner join setor s using(cods) where cods is not null; 

select m.nome, m.funcao, s.cods, s.nome from mecanico m left join setor s using(cods); -- note que desta maneira aparece um mecânico sem setor 

--6) Recupere o nome de todos os mecânicos, e as datas dos consertos para os mecânicos que têm consertos feitos (deve aparecer apenas um registro de nome de mecânico para cada data de conserto).

select m.nome, c.data from mecanico m join conserto c using(codm) group by c.data, m.nome; 

--7) Recupere a média da quilometragem de todos os veículos dos clientes.

select avg(v.quilometragem) from veiculo v;

--8) Recupere a soma da quilometragem dos veículos de cada cidade onde residem seus proprietários.

select sum(v.quilometragem) from veiculo v join cliente c using(codc) group by v.codc, c.cidade;

--9) Recupere a quantidade de consertos feitos por cada mecânico durante o período de 12/06/2014 até 19/06/2014

select m.nome, count(m.codm) from mecanico m join conserto c using(codm) where c.data >= '12/06/2014' and c.data <= '19/06/2014' group by m.nome, m.codm; -- usar group by

select m.nome, c.data from mecanico m join conserto c using(codm); -- usar group by

--10) Recupere a quantidade de consertos feitos agrupada pela marca do veículo.

select v.marca, count(m.codm) from mecanico m join conserto c using(codm) join veiculo v using(codv) group by codv, marca; -- por que marca em group by

--11) Recupere o modelo, a marca e o ano dos veículos que têm quilometragem maior que a média de quilometragem de todos os veículos.

select v.modelo, v.marca, v.ano from veiculo v where v.quilometragem > (select avg(v.quilometragem) from veiculo v);

--12) Recupere o nome dos mecânicos que têm mais de um conserto marcado para o mesmo dia.

select m.nome from mecanico m join conserto using(codm) where (select count(codm) from mecanico m join conserto c using(codm)) > 1 group by m.nome;

