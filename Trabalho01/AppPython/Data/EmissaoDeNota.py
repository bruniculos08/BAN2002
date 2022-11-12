from Model import *

class EmissaoDeNota():

    __codNota = None
    __codDeptoComum = None
    __codDeptoCompra = None

    def __init__(self):
        self.__codNota = ""
        self.__codDeptoComum = -1
        self.__codDeptoCompra = -1

    def codNota(self, codNota):
        self.__codNota = codNota
        return self
    
    def getCodNota(self):
        return self.__codNota
    
    def codDeptoComum(self, codDeptoComum):
        self.__codDeptoComum = codDeptoComum
        return self
    
    def getCodDeptComum(self):
        return self.__codDeptoComum
    
    def codDeptoCompra(self, codDeptoCompra):
        self.__codDeptoCompra = codDeptoCompra
        return self
    
    def getCodDeptCompra(self):
        return self.__codDeptoCompra
    
    def fromTupla(self, tupla):
        self.__codNota = tupla[0]
        self.__codDeptoComum = tupla[1]
        self.__codDeptoCompra = tupla[2]
        return self
    
    def __repr__(self):
        return u'{}:{}:{}'.format(self.__codNota, self.__codDeptoComum, self.__codDeptoCompra)

class EmissaoDeNotaDAO():
    
    __sqlSelectAll = None
    __sqlSelectNewCodDept = None
    __sqlInsert = None
    
    def __init__(self):
        self.__sqlSelectAll = "select * from emissao_de_nota"
        self.__sqlInsert = "insert into emissao_de_nota values('{}', {}, {})"

    def selectAll(self) -> list:
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlSelectAll)
        result = cursor.fetchall()
        emissoes = []
        for line in result:
            emissoes.append(EmissaoDeNota().fromTupla(line))
        return emissoes

    def insertEmissao(self, emissao):
        con = Connection()
        cursor = con.cursor()
        cursor.execute(self.__sqlInsert.format(emissao.getCodNota(), emissao.getCodDeptComum(), emissao.getCodDeptCompra()))
        con.commit()


# create table Emissao_de_nota(
#     cod_nota varchar(44),
#     cod_depto_comum integer not null,
#     cod_depto_compra Integer not null,
#     primary key(cod_nota),
#     FOREIGN KEY (cod_depto_comum ) references departamento (cod_dept),
#     FOREIGN KEY (cod_depto_compra) references departamento (cod_dept)
# );