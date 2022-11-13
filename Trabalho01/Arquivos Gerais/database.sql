
drop sequence dept_cod;
create sequence dept_cod increment by 1 maxvalue 99999999999999 minvalue 1 cache 10;
select currval('dept_cod');
select nextval('dept_cod');

select * from componente;
delete from departamento;
select * from fornecedor;

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

drop table componente cascade;
select * from componente;

create table componente(
    nome character varying(50) not null,
    tipo character varying(50) not null,
    minimo_quant integer not null,
    quantidade integer not null,
    cnpj_principal character varying(14) not null,
    primary key(nome),
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

drop table componente_necessario;
select * from departamento;
select * from componente_necessario;
insert into componente_necessario values(1, 'motor do batmóvel', 1); 


create table componente_necessario(
    cod_dept integer not null,
    nome_componente character varying(50) not null,
    quantidade integer not null,
    primary key(cod_dept, nome_componente),
    FOREIGN KEY (cod_dept) references departamento (cod_dept),
    FOREIGN KEY (nome_componente) references componente (nome)
);

create table contem(
    nome_componente character varying(50) not null,
    id_pedido integer not null,
    primary key(nome_componente, id_pedido),
    FOREIGN KEY (nome_componente) references componente (nome),
    FOREIGN KEY (id_pedido) references pedido (id)

);

create table fornece(
    nome_componente character varying(50) not null,
    cnpj character varying(14) not null,
    primary key (nome_componente, cnpj),
    FOREIGN KEY (nome_componente) references componente (nome),
    FOREIGN KEY (cnpj) references fornecedor (cnpj)
    
);

-- Gatilho para ajuste da table 'componente' em inserções:
create or replace function addComponente() returns trigger as
$$
begin
	if (select count(*) from componente cn where nome = new.nome) > 0 then
		update componente cn set quantidade = quantidade + 1, minimo_quant = max(minimo_quant, new.minimo_quant) where nome = new.nome;
		
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

create trigger addComponeteGatilho before insert on componente for each row execute procedure addComponente();

-- Função auxiliar para a função acima:
create or replace function max(num1 numeric, num2 numeric) returns numeric as
$$
begin
	if num1 >= num2 then
		return num1;
	end if;
	return num2;
end;
$$
language plpgsql;

-- Gatilho para ajuste da tabela 'componente_necessario' em inserções:
create or replace function addComponenteNecessario() returns trigger as
$$
begin
	if (select count(*) from componente_necessario where nome_componente = new.nome_componente and cod_dept = new.cod_dept) > 0 then
		update componente_necessario set quantidade = quantidade + new.quantidade where nome_componente = new.nome_componente and cod_dept = new.cod_dept;
		return old;
	end if;
	return new;
end;
$$
language plpgsql;

create trigger addComponenteNecessarioGatilho before insert on componente_necessario for each row execute procedure addComponenteNecessario();

-- Gatilho para manter a tabela 'componente' atualizada:

select * from pedido;
select * from componente_necessario;

create or replace function atualizaComponente() returns trigger as
$$
declare numeroComponente int default 0;
declare minComponente int default 0;
declare cnpjPrincipal varchar(14);
begin
	select quantidade from componente where nome = new.nome_componente into numeroComponente;
	select 
	if numeroComponente 
end;
$$
language plpgsql;

create trigger atualizaComponenteGatilho after insert or update on componente_necessario execute procedure atualizaComponente();
