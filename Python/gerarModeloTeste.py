import pandas as pd
from sqlalchemy import create_engine
import math

master_input = input('O banco é o master? S/N  ')
master = False

if master_input == 'S':
   master = True
   db_name = "ncsMasterHomologacao"
   host = "10.1.1.115"
else:
   master = False
   db_name = "leandroRevest0816"
   host = "10.1.1.115"

nome_tabela = input('Qual o nome da tabela? ')
password = "ewqiop90"
port = "5432"
user = "postgres"

def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, db_name
        )
    )

getcolunas = f" select * from {nome_tabela} limit 200" #
sql_property = f"SELECT is_nullable, column_name, character_maximum_length, data_type FROM information_schema.columns WHERE table_name = '{nome_tabela}'"
primary_column = f"""SELECT c.column_name, c.data_type
FROM information_schema.table_constraints tc 
JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{nome_tabela}'"""

connection=get_connection()

with connection.connect().execution_options(autocommit=True) as conn:
    df = pd.read_sql(getcolunas, con = conn)
    property = pd.read_sql(sql_property, con = conn)
    key = pd.read_sql(primary_column, con= conn)


principal = key['column_name'].item()

nome_model = nome_tabela.capitalize()
nome_arquivo = nome_model+".ts"
file = open(nome_arquivo, "w")
inclusao_column = ''
alteracao_column = ''
exclusao_column = ''
first = 0

for column in df:
   if ('exclusao' in column):
      exclusao_column = column
   elif ('inclusao' in column):
      inclusao_column = column
   elif ('alteracao' in column):
      alteracao_column = column

def get_tipo(coluna):
   type = property[property['column_name'] == coluna]['data_type'].item()
   if type == 'integer' or type == 'double precision':
      return 'number'
   elif 'timestamp' in type:
      return 'DateTime'
   else:
      return 'string'
   # if tipo == 'int64' or tipo == 'float64':
   #    return 'number'
   # elif tipo == 'object':
   #    return 'string'
   # else:
   #    return 'DateTime'

def get_tempo(coluna, tipo):
   if(coluna == inclusao_column):
      return '.dateTime({autoCreate:true, '
   elif(coluna == alteracao_column):
      return '.dateTime({autoUpdate:true, '
   elif(coluna == exclusao_column or tipo == 'DateTime'):
      return '.dateTime({'
   else:
      return '({'

def get_principal(coluna):
   if(coluna == principal):
      return 'isPrimary: true '
   else:
      return ''

file.write("""
import { column,  beforeFetch, beforeFind, BaseModel,ModelQueryBuilderContract } from '@ioc:Adonis/Lucid/Orm'
import { DateTime } from 'luxon'
import NcsModel from '../../../Models/NcsModel';

export default class """+ nome_model +""" extends NcsModel {

""")

#
for column in df:
   file.write(f"   static readonly _field{column.capitalize()} = '{column}';")
   file.write("\n")

#declarao tabela
file.write("\n")
file.write(f"   public static table      = '{nome_tabela}'")
file.write("\n\n")

file.write("   constructor(){\n")
file.write("      super( {model}.table, {model}._field{principal}, {model}._field{exclusao} )".format(
   model=nome_model,
   principal=principal.capitalize(),
   exclusao=exclusao_column.capitalize()
))
file.write("\n   }\n\n")

#campos
for column in df:
   tipo = get_tipo(column)
   file.write("   @column"+  get_tempo(column, tipo) +"columnName: '"+column+"', serializeAs: '"+column+"', "+ get_principal(column) +"})\n")
   file.write("   public "+ column +": "+tipo+";")
   file.write("\n\n")

#caso campo exclusao existe
if (exclusao_column != ''):
   file.write("""
   /***
   * SOFT DELETE
   **/
   @beforeFind()
   @beforeFetch()
       public static ignoreDeleted(query: ModelQueryBuilderContract<typeof BaseModel>) {
       query.whereNull( this._field"""+exclusao_column.capitalize()+"""  )
   }

   public delete = async () => {
     this."""+exclusao_column+""" = DateTime.local()
     await this.save()
   }
   """)
file.write("\n}")
file.close()

nome_controller = nome_model+"Controller.ts"
filec = open(nome_controller, "w")

def get_tipo_controller(coluna):
   type = property[property['column_name'] == coluna]['data_type'].item()
   if type == 'integer' or type == 'double precision':
      return 'number'
   elif 'timestamp' in type:
      return 'date'
   else:
      return 'string'

def get_optional(coluna, edit):
   is_nullable = property[property['column_name'] == coluna]['is_nullable'].item()
   if(is_nullable == 'YES' or edit == True):
      return '.optional'
   else:
      return ''

def get_rules(coluna):
   type = property[property['column_name'] == coluna]['data_type'].item()
   if type == 'integer' or type == 'double precision':
      return ''
   elif 'timestamp' in type:
      return ''
   else:
      is_max_length = property[property['column_name'] == coluna]['character_maximum_length'].item()
      if(not math.isnan(is_max_length)):
         max_length = ', [rules.maxLength({0})]'.format(int(is_max_length))
      else:
         max_length = ''
      return "{{trim: true}}{0}".format(max_length)

   # if(tipo == 'object'):
   #    is_max_length = property[property['column_name'] == coluna]['character_maximum_length'].item()
   #    if(not math.isnan(is_max_length)):
   #       max_length = ', [rules.maxLength({0})]'.format(int(is_max_length))
   #    else:
   #       max_length = ''
   #    return "{{trim: true}}{0}".format(max_length)
   # else:
   #    return ''



def write_schema(column, edit):
   if(column != inclusao_column and column != exclusao_column and column != alteracao_column and column != principal):
      filec.write(("         {coluna}:            schema.{tipo}{optional}({rules}),").format(
            coluna=column, 
            tipo=get_tipo_controller(column), 
            rules=get_rules(column), 
            optional=get_optional(column, edit)
         ))

      filec.write("\n")

filec.write("""
import { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { schema, rules } from '@ioc:Adonis/Core/Validator'
import NcsController from 'App/Controllers/Http/NcsController';
""")

if(master):
   filec.write("import {0} from 'App/Modulos/Admin/Models/{0}'".format(nome_tabela.capitalize()))
   filec.write("\n\nexport default class {0}Controller extends NcsController".format(nome_tabela.capitalize()) + " {")
else:
   filec.write("import NcsPersistencia from 'App/Utils/NcsPersistencia';")
   filec.write("import {0} from 'App/Modulos/Tenant/Models/{0}'".format(nome_arquivo))
   filec.write("\n\nexport default class {0}Controller extends NcsController".format(nome_tabela.capitalize()) + " {")



filec.write(("""
   constructor(){{
      super( new {model}() );
      this.defaultModel = {model};
   }}
""").format(model=nome_model))

filec.write("""
   public async store({ request, auth } : HttpContextContract){
      await this.setConnection( auth )

      const schemaValidator = schema.create({
""")

for column in df:
   write_schema(column, False)

filec.write(("""      })

      const data     = await request.validate({ schema: schemaValidator }) as any
"""))  

if(not master):
   filec.write("""data.{principal}  = await NcsPersistencia.nextID( this.connection, '{banco}', '{principal}')""".format(principal=principal, banco=nome_tabela))

filec.write(("""
      const object   = await this.defaultModel.create( data );

      return object;
   }
"""))


filec.write("""
   public async update({ request, params, auth } : HttpContextContract ){
      await this.setConnection( auth )

      const object      = await this.defaultModel.findOrFail( params.id );

      const schemaValidator = schema.create({
""")

for column in df:
   write_schema(column, True)

filec.write("""      })

      await request.validate({ schema: schemaValidator });

      const data = request.only([
""")
for column in df:
   if(column != inclusao_column and column != exclusao_column and column != alteracao_column and column != principal):
      filec.write("           '{0}',\n".format(column))

filec.write("""      ])

      object.merge( data );
      return await object.save();
   }
""")

filec.write("\n}")
filec.close()