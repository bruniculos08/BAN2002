create table pulbic.departamento(
    cod_dept integer not null,
    tipo character varying(50) not null,
    primary key(cod_dept)
);

create table public.Emissao_de _nota(
    cod_nota integer not null,
    cod_depto_comum integer not null,
    cod_depto_compra Integer not null,
    primary key(cod_nota)
    FOREIGN KEY (cod_depto_comum ) references public.departamento (cod_dept)
    FOREIGN KEY (cod_depto_compra) references public.departamento (cod_dept)
);

create table public.fornecedor(
    cnpj character varying(14) not null,
    nome character varying(100) not null,
    primary key(cnpj)
);

create table public.componente(
    referencia integer not null,
    tipo character varying(50) not null,
    minimo_quant integer not null,
    quant integer not null,
    setor_armazenamento integer not null,
    cnpj_principal character varying(14) not null,
    primary key(referencia)
);

create table public.veiculo(
    chassi character varying(17) not null,
    manual_automatico boolean not null, -- 0 manual 1 automatico
    arcondicionado boolean not null,
    vidro_travas boolean not null,
    cod_dept integer not null,
    primary key(chassi)
    FOREIGN KEY (cod_dept) references public.departamento (cod_dept)
);

create table public.esta_na_lista(
    cod_dept integer not null,
    referencia integer not null,
    primary key(referencia),
    primary key(cod_dept)
    FOREIGN KEY (referencia) references public.componente (referencia)
    FOREIGN KEY (cod_dept) references public.departamento (cod_dept)

);

create table public.contem(
    referencia integer not null,
    id_pedido integer not null,
    primary key(referencia),
    primary key (id_pedido),
    FOREIGN KEY (referencia) references public.componente (referencia),
    FOREIGN KEY (id_pedido) references public.pedido_de_compra (id)

);

create table public.fornece(
    referencia integer not null,
    cnpj character varying(14) not null,
    primary key (referencia),
    primary key (cnpj),
    FOREIGN KEY (referencia) references public.componente (referencia)
    FOREIGN KEY (cnpj) references public.fornecedor (cnpj)
    
);

create table public.pedido_de_compra(
    id integer not null,
    cod_nota integer not null,
    cnpj character varying(14) not null,
    valor numeric not null,
    primary key (id) not null,
    FOREIGN key(cnpj) references puclic.fornecedor cnpj
);
