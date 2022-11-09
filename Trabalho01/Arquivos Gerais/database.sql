create table departamento(
    cod_dept integer not null,
    tipo character varying(50) not null,
    primary key(cod_dept)
);

drop view numpedidos;
drop table emissao_de_nota;

create table Emissao_de_nota(
    cod_nota varchar(44),
    cod_depto_comum integer not null,
    cod_depto_compra Integer not null,
    primary key(cod_nota),
    FOREIGN KEY (cod_depto_comum ) references departamento (cod_dept),
    FOREIGN KEY (cod_depto_compra) references departamento (cod_dept)
);

create table fornecedor(
    cnpj character varying(14) not null,
    nome character varying(100) not null,
    primary key(cnpj)
);


create table pedido_de_compra(
    id integer not null,
    cod_nota integer not null,
    cnpj character varying(14) not null,
    valor numeric not null,
    primary key (id),
    FOREIGN key(cnpj) references fornecedor (cnpj)
);

create table componente(
    referencia integer not null,
    tipo character varying(50) not null,
    minimo_quant integer not null,
    quant integer not null,
    setor_armazenamento integer not null,
    cnpj_principal character varying(14) not null,
    primary key(referencia)
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

create table esta_na_lista(
    cod_dept integer not null,
    referencia integer not null,
    primary key(referencia, cod_dept),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (cod_dept) references departamento (cod_dept)

);

create table contem(
    referencia integer not null,
    id_pedido integer not null,
    primary key(referencia, id_pedido),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (id_pedido) references pedido_de_compra (id)

);

create table fornece(
    referencia integer not null,
    cnpj character varying(14) not null,
    primary key (referencia, cnpj),
    FOREIGN KEY (referencia) references componente (referencia),
    FOREIGN KEY (cnpj) references fornecedor (cnpj)
    
);

