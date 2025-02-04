
select * from mecanico;
select * from conserto;
select * from cliente;
select * from veiculo;
select * from setor;
-- ver todas as tabelas:
SELECT * FROM pg_catalog.pg_tables;
 
--1) Crie um índice para cada uma das chaves estrangeiras presentes do esquema de dados.
create index idx_foreign_mec on mecanico using btree(cods);
create index idx_foreign_conserto on conserto using btree(codm, codv);
create index idx_foreign_veiculo on veiculo using btree(codc);

--2) Crie um índice para acelerar a busca dos mecânicos pela função.
create index idx_mec_func on mecanico using hash(substr(funcao, 1, 5));
-- pode ser hash ou btree

--3) Crie um índice para acelerar a ordenação dos consertos pela data e hora.
create index idx_conserto on conserto using btree(data, hora);
-- deve ser btree

--4) Crie um índice para acelerar a busca de clientes pelo cpf.
create index idx_cliente on cliente using btree(cpf);
-- pode ser hash ou btree

--5) Crie um índice para acelerar a busca pelas primeiras 5 letras do nome dos clientes.
create index idx_clientes on cliente using btree(substr(nome, 1, 5));
-- pode ser hash ou btree

--6) Crie um índice para acelerar a busca dos clientes com CPF com final XXX.XXX.XXX-55.
create index idx_cliente_55 on cliente using btree(cpf) where cpf LIKE '%55';
create index idx_cliente_55 on cliente using btree(cpf) where cpf LIKE '___.___.___-55';
-- note: existem estas duas possibilidades e o comando 'LIKE' serve para comparação de strings(ILIKE é equivalente porém desconsidera se é caixa alta ou baixa) e não é equivalente à '='. 