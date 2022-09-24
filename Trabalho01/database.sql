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
    nome haracter varying(100) not null,
    primary key(cnpj)
);

create table public.componente();

create table public.veiculo();

create table public.esta_na_lista();

create table public.contem();

create table public.fornece();

create table public.pedido_de_compra();
