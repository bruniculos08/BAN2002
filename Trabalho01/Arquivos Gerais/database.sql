drop sequence dept_cod;
create sequence dept_cod increment by 1 maxvalue 99999999999999 minvalue 32 cache 1;

drop table departamento cascade;
create table departamento(
    cod_dept integer not null,
    tipo character varying(50) not null,
    primary key(cod_dept)
);

drop table fornecedor cascade;
create table fornecedor(
    cnpj character varying(14) not null,
    nome character varying(100) not null,
    primary key(cnpj)
);

drop sequence pedido_id;
create sequence pedido_id increment by 1 maxvalue 99999999999999 minvalue 1 cache 1;

drop table pedido cascade;
create table pedido(
    id integer not null,
    data_criacao date not null,
    cnpj character varying(14) not null,
    cod_dept_compra integer not null, -- lembrar de alterar para not null após testes!
    primary key (id),
    foreign key(cnpj) references fornecedor(cnpj),
    foreign key (cod_dept_compra) references departamento(cod_dept)
);

drop table Nota_fiscal cascade;
create table Nota_fiscal(
    cod_nota varchar(44),
    id_pedido integer not null,
    primary key (cod_nota),
    foreign key (id_pedido) references pedido(id) on delete cascade on update cascade
);

drop table componente cascade;
create table componente(
    nome character varying(50) not null,
    tipo character varying(50) not null,
	valor_compra float not null,
    minimo_quant integer not null,
    quantidade integer,
    cnpj_principal character varying(14) not null,
    primary key(nome),
    foreign key(cnpj_principal) references fornecedor(cnpj)
);

drop table veiculo cascade;
create table veiculo(
    chassi character varying(17) not null,
    valor_producao float not null,
    data_producao date, -- 'YYYY-MM-DD' 
    cod_dept integer not null,
	estagio varchar(50),
    primary key(chassi),
    FOREIGN KEY (cod_dept) references departamento (cod_dept)
);

-- Quando é adicionado um veículo na lista de veículos produzidos supões se que o departamento responsável pela fabricação adicione as peças para fabricação de...
-- ... tal veículo à tabela "componente_necessario" (antiga "esta_na_lista"), assim cada linha desta tabela indica o departamento que precisa de uma unidade de um tal componente (se forem mais unidades...
-- ... haverão mais linhas.

drop table componente_necessario cascade;
create table componente_necessario(
    cod_dept integer not null,
    nome_componente character varying(50) not null,
    quantidade integer not null,
    primary key(cod_dept, nome_componente),
    FOREIGN KEY (cod_dept) references departamento (cod_dept) on update cascade on delete cascade,
    FOREIGN KEY (nome_componente) references componente (nome) on update cascade on delete cascade
);

drop table contem cascade;
create table contem(
    nome_componente character varying(50) not null,
    id_pedido integer not null,
	quantidade integer not null,
    primary key(nome_componente, id_pedido),
    FOREIGN KEY (nome_componente) references componente (nome) on update cascade on delete cascade,
    FOREIGN KEY (id_pedido) references pedido (id) on update cascade on delete cascade
);

drop table fornece cascade;
create table fornece(
    nome_componente character varying(50) not null,
    cnpj character varying(14) not null,
    primary key (nome_componente, cnpj),
    FOREIGN KEY (nome_componente) references componente (nome) on update cascade on delete cascade,
    FOREIGN KEY (cnpj) references fornecedor (cnpj)
    
);