--achar certo nome 
	select * from INFORMATION_SCHEMA.COLUMNS 
		where COLUMN_NAME like '%pct%' 
		order by TABLE_NAME

--criar uma tabela
   CREATE TABLE nome_tabela (    --Tipo         --Pode ser null --valor padrão
      pesid                   serial         NOT NULL,
      pestid                  integer        not null,   
      pesrazao                varchar(200)   NOT NULL,
      pesfantasia             varchar(200)   NULL,
      pescnpj                 varchar(18)    NULL,
      pesrg                   varchar(100)   null,
      peslogin                varchar(200)   NOT NULL,
      pessenha                varchar(200)   NOT NULL,
      pessenhatemporaria      bpchar(1)      NOT NULL    DEFAULT 'S'::bpchar,
      pesdatanascimento       timestamp      null,
      pesempresanomedominio   varchar(100)   NOT NULL,
      pesinclusao             timestamp      NOT NULL    DEFAULT CURRENT_TIMESTAMP,
      pesexclusao             timestamp      NULL,
      pesalteracao            timestamp      NULL,
      CONSTRAINT pessoa_pkey PRIMARY KEY (pesid),                                             --Escolhendo chave primaria
      CONSTRAINT pessoa_pestid_fkey FOREIGN KEY (pestid) REFERENCES public.pessoatipo(pestid) --Declarando chave externa
   )

--adicionar uma coluna
   alter table nome_tabela
   	add nome_coluna varchar(1) not null default 'F' ::bpchar

--remover uma coluna
   ALTER TABLE nome_tabela DROP COLUMN nome_coluna;

--remover uma tabela
   drop table pessoa

--pegar dados de uma tabela
   SELECT * FROM information_schema.columns WHERE table_name = 'nome_tabela'

--pegar chave principal de uma tabela
   SELECT c.column_name, c.data_type
      FROM information_schema.table_constraints tc 
         JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
         JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
            AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
      WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = 'nome_tabela'
      
--Nao repetir valores (evitar)
  select distinct on (cad.cad_codigo) cad.cad_codigo , cad_razao, cad_fantasia, cad_cnpj
         from usuario usu
         
--Pegar a data atual
	current_date

--Verificar se existe valor
select exists (
	select column_id
 	from nome_tabela
   	where column_id = 'teste' and column_exclusao is null
 )

--Verifica se possui valores repetidos em column_id
select column_id , count(column_id)
	from (
      	--SQL
 	) as nq
GROUP BY column_id 
HAVING COUNT(column_id) > 1

--Verificao
	LIKE      ===>  ~~		--Comparacao simples que considera wildcards
	ILIKE     ===>  ~~*		--Comparacao que e CASE INSENSITIVE (Ignora a diferenca entre maiusculas e minusculas)
	NOT LIKE  ===> !~~		--Comparacao negativa
	NOT ILIKE ===> !~~*		--Comparacao negativa CASE INSENSITIVE
 
 --Regex para postgresql
 	regexp_replace('123.345.567-32', '[[:punct:]]', '', 'g')
         		-- valor original, regex, novo valor, parametro(s)
 	--Tipos de regex
 		--[:alnum:]  -> numeros e letras maiusculo e minusculo
 		--[:alpha:]  -> letras maiusculo e minusculo
 		--[:ascii:]  -> caracteres ascii
 		--[:blank:]  -> espaco em branco e tabs
 		--[:cntrl:]  -> caracteres de control
 		--[:digit:]  -> numeros
 		--[:graph:]  -> caracteres visiveis (tudo exceto cntrl e blank)
 		--[:lower:]  -> letras minusculo
 		--[:upper:]  -> letras maiuculo
 		-- [:word:]  -> numeros, letras e underscore (_)
 		--[:punct:]  -> pontuacao
 		--[:space:]  -> todos os espaco em branco
 		--[:xdigit:] -> digitos em hexadecimal (a-f/0-9)
 	--Tipos de flags
 		-- i 	-> ignora diferencas entre maisculo e minusculo
 		-- g	-> verifica todas as condicoes ao inves de somente a primeira
 		-- m	-> multiline
 		-- s	-> dotall 
 		-- u	-> unicode
 		-- y	-> sticky
 	

