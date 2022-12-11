from pymongo import MongoClient
from mongoengine import *

connect("Personalização")
connection = MongoClient("mongodb://localhost:27017")

class Departamento(Document):
    tipo = StringField(required=True)
    componente_necessario = ListField()

generic_dept = type(Departamento())
dept = generic_dept.objects()

to_add = {"nome":"roda teste append 1000", "quantidade":0}
dept.update(componente_necessario = [to_add])

to_add_01 = {"nome":"roda 1111", "quantidade":0}
to_add_02 = {"nome":"roda 1112", "quantidade":0}

info = {"tipo":"producao", "componente_necessario":[to_add_01, to_add_02]}
item = generic_dept(**info)
item.save()

# database = connection["Personalização"]
# departamento = connection["Personalização"]["Departamento"]
# componente = connection["Personalização"]["Componente"]

# results = departamento.find({"tipo":"producao"})

# string = {}
# string["tipo"] = "producao"
# string["componente"] = [{"nome":"roda 1007", "quantidade":4}]

# departamento.insert_one(string)

# pass

# for result in results:
#     print(result)

# results = componente.find({})

# for result in results:
#     print(result)

# class Fornecedor(Document):
#     cnpj = StringField(unique=True)
#     name = StringField(unique=True)


# # dept = Fornecedor(cnpj="11424957007003", name="Oscorp Industries")
# # dept.save()

# class Componente(Document):
#     __nome = StringField(unique=True)
#     tipo = StringField()
#     valor_compra = FloatField()
#     quantidade_min = IntField()
#     quantidade = IntField()
#     cnpj = StringField()
    
# class Componente(Document):
#     __nome = StringField(unique=True)
#     tipo = StringField()
#     valor_compra = FloatField()
#     quantidade_min = IntField()
#     quantidade = IntField()
#     cnpj = StringField()

# comp = Componente(__nome="roda 1004", tipo='roda', valor_compra=1000, quantidade_min=4, quantidade=4, cnpj="11424957007003")
# # comp.save()

# print(comp.__nome)