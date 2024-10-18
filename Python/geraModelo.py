from string import Template
import psycopg2


#configs
#---master
#db_name = "ncsServiceMonitor"
#host = "apps.ncs.com.br"
#master=True

#---revest
db_name = "leandroRevest0816"
host = "10.1.1.115"
master = False

password = "ewqiop90"
nomeTabela = 'perfilacessovinculo'


def execut(db, sql):
    conn = psycopg2.connect(host=host,database=db_name,user="postgres",password=password)
    cur = conn.cursor()
    cur.execute(sql)
    d = cur.fetchall()
    c = cur.fetchone()
    z = [desc[0] for desc in cur.description]
    print(d)
    print(c)
    print(z)
    return z

getcolunas = " select * from "+nomeTabela+" LIMIT 0"
nomedaTabela = nomeTabela
nomescolunas = execut(db_name, getcolunas)
#execut(db_name, sql)

#colnames = [desc[0] for desc in curs.description]

def get_max_str(lst):
    return max(lst, key=len)

content = nomescolunas



#gerando espacamento correto
maximo_espacao = len(get_max_str(content)) + 2

print("-"*40)

nometabela= nomedaTabela.capitalize()

template = Template("""
import { column,  beforeFetch, beforeFind, BaseModel,ModelQueryBuilderContract } from '@ioc:Adonis/Lucid/Orm'
import { DateTime } from 'luxon'
import NcsModel from './NcsModel'


export default class $tabela extends NcsModel {

""").substitute(tabela=nometabela)

print(template)

#Lembra de colocar o isPrimary: true no primeiro elemento
for i in content:
    espaco = maximo_espacao-len(i)
    print("   static readonly _field"+i.capitalize()+espaco*" "+"= '"+i+"';")

print("\n")
print("   public static table      = '"+nomedaTabela+"'")
print("\n")

for i in range(len(content)):
    
    if(i == 0):
        print("   @column({isPrimary: true, columnName: '"+str(content[i])+"', serializeAs: '"+str(content[i])+"' })")
    else:
        print("   @column({columnName: '"+str(content[i])+"', serializeAs: '"+str(content[i])+"' })")
    print("   public "+str(content[i]).capitalize()+"    : string;")
    print("\n")

print("""

  @column.dateTime({ autoCreate: true })
  public createdAt: DateTime

  @column.dateTime({ autoCreate: true, autoUpdate: true })
  public updatedAt: DateTime
  
    /***
    * SOFT DELETE
    **/
    @beforeFind()
    @beforeFetch()
        public static ignoreDeleted(query: ModelQueryBuilderContract<typeof BaseModel>) {
        query.whereNull( this._fieldAuguexclusao  )
    }

    public delete = async () => {
      this.Auguexclusao = DateTime.local()
      await this.save()
    }
   """
)

print("\n\n}")


print("* - CONTROLLER - "*10)
print("\n\n")


print("""
import { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import NcsApiFilter from 'App/Utils/NcsApiFilter';
import NcsController from "./NcsController";
import NcsPersistencia from 'App/Utils/NcsPersistencia';
""")


if(master):
    az1 = Template("import $tabela from 'App/Models/Master$tabela'").substitute(tabela=nometabela)
else:
    az1 = Template("import $tabela from 'App/Models/$tabela'").substitute(tabela=nometabela)
print(az1)

print("\n")
az3 = ("export default class $tabela Controller extends NcsController {").replace('$tabela', nometabela)
print(az3)
print("\n")
az2 = Template("""
   constructor(){
      super();
      this.defaultModel = $tabela;
   }
""").substitute(tabela=nometabela)
print(az2)
print("\n\n")
print("""
   public async index({ auth } : HttpContextContract) {
      await this.setConnection( auth );
      return await this.defaultModel.all();
   }

   public async show({ response, params, auth } : HttpContextContract){
      await this.setConnection( auth );
      try {
         const raw = await this.defaultModel.findOrFail( params.id );
         return raw 
      } catch (error) {
         return response.badRequest( { error: 'registro não encontrado' })
      }
   }

   public async destroy({ params, auth } : HttpContextContract ){
      await this.setConnection( auth )
      try {
         const objeto = await this.defaultModel.findOrFail( params.id );   
         objeto.delete();
         return objeto;
      } catch (error) {
         if( error.code == 'E_ROW_NOT_FOUND') { 
            error.message = 'registro não encontrado';
         }
         
         throw( error );
      }
   }""")

print("\n\n}")
