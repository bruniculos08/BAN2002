--1) Mostre o nome e a função dos mecânicos.

create view tarefas (nome, funcao) as select m.nome, m.funcao from mecanico m;

select * from tarefas;

select m.nome, m.funcao from mecanico m;

--2) Mostre o modelo e a marca dos veículos dos clientes.

create view carro_info (modelo, marca) as select v.modelo, v.marca from veiculo v;

select * from carro_info;

select v.modelo, v.marca from veiculo v;

--3) Mostre o nome dos mecânicos, o nome dos clientes, o modelo dos veículos e a data e hora dos consertos realizados.

create view histórico (mecanico, cliente, veiculo, data, hora) as 
select mecanico.nome, cliente.nome, veiculo.modelo, conserto.data, conserto.hora from cliente join veiculo using (codc) join conserto using(codv) join mecanico using(codm);

select * from histórico;

select mecanico.nome, cliente.nome, veiculo.modelo, conserto.data, conserto.hora from cliente join veiculo using (codc) join conserto using(codv) join mecanico using(codm);

--4) Mostre o ano dos veículos e a média de quilometragem para cada ano.

create view quilometragem_por_ano as select v.ano, avg(v.quilometragem) from veiculo v group by v.ano;

select * from quilometragem_por_ano;

select v.ano, avg(v.quilometragem) from veiculo v group by v.ano; 
-- group by serve apenas para funções de agregação(count, avg,...) para especificar a "agregação" feita pela função (por default ela agrega tudo).

--5) Mostre o nome dos mecânicos e o total de consertos feitos por um mecânico em cada dia.

create view conserto_por_dia as select m.nome, count(m.codm), c.data from mecanico m join conserto c using(codm) group by codm, data;

select * from conserto_por_dia;

select m.nome, count(m.codm), c.data from mecanico m join conserto c using(codm) group by codm, data;

select m.nome, count(m.codm) from mecanico m join conserto c using(codm) group by codm;

--6) Mostre o nome dos setores e o total de consertos feitos em um setor em cada dia.

create view setor_consertos_por_dia as select s.nome, c.data, count(m.codm) from setor s join mecanico m using(cods) join conserto c using(codm) group by s.nome, c.data; 

select * from setor_consertos_por_dia;

select s.nome, c.data, count(m.codm) from setor s join mecanico m using(cods) join conserto c using(codm) group by s.nome, c.data; 

--7) Mostre o nome das funções e o número de mecânicos que têm uma destas funções.

create view mecanico_por_funcao as select m.funcao, count(m.codm) from mecanico m group by m.funcao;

select * from mecanico_por_funcao;

select m.funcao, count(m.codm) from mecanico m group by m.funcao;

--8) Mostre o nome dos mecânicos e suas funções e, para os mecânicos que estejam alocados a um setor, informe também o número e nome do setor.

create view mecanico_setor (mecanico, funcao, setor, cod_setor) as select m.nome, m.funcao, s.nome, s.cods from mecanico m left join setor s using(cods);

select * from mecanico_setor;

select m.nome, m.funcao, s.nome, s.cods from mecanico m left join setor s using(cods);

--9) Mostre o nome das funções dos mecânicos e a quantidade de consertos feitos agrupado por cada função.

create view funcao_por_consertos as select m.funcao, count(m.codm) from mecanico m join conserto c using(codm) group by(codm, funcao);

select * from funcao_por_consertos;

select m.funcao, count(m.codm) from mecanico m join conserto c using(codm) group by(codm, funcao);

