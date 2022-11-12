
drop sequence dept_cod;
create sequence dept_cod increment by 1 maxvalue 99999999999999 minvalue 1 cache 20;
select currval('dept_cod');
select nextval('dept_cod');


create table departamento(
    cod_dept integer not null,
    tipo character varying(50) not null,
    primary key(cod_dept)
);

select * from departamento;
--drop view numpedidos;
--drop table emissao_de_nota; 

create table Nota_fiscal(
    cod_nota varchar(44),
    id_pedido integer not null,
    primary key (cod_nota),
    foreign key (id_pedido) references pedido
);

create table fornecedor(
    cnpj character varying(14) not null,
    nome character varying(100) not null,
    primary key(cnpj)
);

--drop table pedido cascade;
create sequence pedido_id increment by 1 maxvalue 99999999999999 minvalue 1 cache 20;

create table pedido(
    id integer not null,
    valor numeric not null,
    cnpj character varying(14) not null,
    cod_dept_compra integer not null,
    primary key (id),
    foreign key(cnpj) references fornecedor(cnpj),
    foreign key (cod_dept_compra) references departamento(cod_dept)
);

create sequence componente_referencia increment by 1 maxvalue 99999999999999 minvalue 1 cache 20;

create table componente(
    referencia integer not null,
    tipo character varying(50) not null,
    minimo_quant integer not null,
    quant integer not null,
    setor_armazenamento integer not null,
    cnpj_principal character varying(14) not null,
    primary key(referencia),
    foreign key(cnpj_principal) references fornecedor(cnpj)
);

create table veiculo(
    chassi character varying(17) not null,
    manual_automatico boolean not null, -- 0 manual 1 automatico
    arcondicionado boolean not null,
    vidro_travas boolean not null,
    cod_dept integer not null,
    primary key(chassi),
    FOREIGN KEY (cod_dept) references departamento (cod_dept)
);

-- Quando é adicionado um veículo na lista de veículos produzidos supões se que o departamento responsável pela fabricação adicione as peças para fabricação de...
-- ... tal veículo à tabela "esta_na_lista", assim cada linha desta tabela indica o departamento que precisa de uma unidade de um tal componente (se forem mais unidades...
-- ... haverão mais linhas.


create table esta_na_lista(
    cod_dept integer not null,
    referencia integer not null,
    primary key(referencia, cod_dept),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (cod_dept) references departamento (cod_dept)

);

-- Supõe-se que os pedidos são unitários:

create table contem(
    referencia integer not null,
    id_pedido integer not null,
    primary key(referencia, id_pedido),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (id_pedido) references pedido (id)

);

create table fornece(
    referencia integer not null,
    cnpj character varying(14) not null,
    primary key (referencia, cnpj),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (cnpj) references fornecedor (cnpj)
    
);

