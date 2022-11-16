
create sequence dept_cod increment by 1 maxvalue 99999999999999 minvalue 32 cache 1;

create table departamento(
    cod_dept integer not null,
    tipo character varying(50) not null,
    primary key(cod_dept)
);

select * from pedido;
select * from fornece;

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

create sequence pedido_id increment by 1 maxvalue 99999999999999 minvalue 1 cache 1;

create table pedido(
    id integer not null,
    valor numeric not null,
    cnpj character varying(14) not null,
    --data_de_criacao date, -- 'YYYY-MM-DD' 
    cod_dept_compra integer not null,
    primary key (id),
    foreign key(cnpj) references fornecedor(cnpj),
    foreign key (cod_dept_compra) references departamento(cod_dept)
);

create table componente(
    nome character varying(50) not null,
    tipo character varying(50) not null,
    minimo_quant integer not null,
    quantidade integer not null,
    cnpj_principal character varying(14) not null,
    primary key(nome),
    foreign key(cnpj_principal) references fornecedor(cnpj)
);

drop table veiculo cascade;
create table veiculo(
    chassi character varying(17) not null,
    valor_producao float,
    --inicio date, -- 'YYYY-MM-DD' 
    cod_dept integer not null,
    primary key(chassi),
    FOREIGN KEY (cod_dept) references departamento (cod_dept)
);

-- Quando é adicionado um veículo na lista de veículos produzidos supões se que o departamento responsável pela fabricação adicione as peças para fabricação de...
-- ... tal veículo à tabela "esta_na_lista", assim cada linha desta tabela indica o departamento que precisa de uma unidade de um tal componente (se forem mais unidades...
-- ... haverão mais linhas.

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


-- Gatilhos e funções  a partir desta linha:

-- Gatilho para ajuste da table 'componente' em inserções, se o componente já existir na tabela, sua quantidade será acrecscida de acordo...
-- ... com a quantidade que seria adicionada e a quantidade miníma será a maior das duas quantidades mínimas:
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