from pymongo import MongoClient
from mongoengine import *

connect("Personalização")
connection = MongoClient("mongodb://localhost:27017")
database = connection["Personalização"]
departamento = connection["Personalização"]["Departamento"]
componente = connection["Personalização"]["Componente"]

results = departamento.find({"tipo":"producao"})

departamento.insert_one({"tipo":"producao", "componente": [{"nome":"roda 1004", "quantidade":4}]})

for result in results:
    print(result)

results = componente.find({})

for result in results:
    print(result)

# class Fornecedor(Document):
#     cnpj = StringField(unique=True)
#     name = StringField(unique=True)


# # dept = Fornecedor(cnpj="11424957007003", name="Oscorp Industries")
# # dept.save()

class Componente(Document):
    __nome = StringField(unique=True)
    tipo = StringField()
    valor_compra = FloatField()
    quantidade_min = IntField()
    quantidade = IntField()
    cnpj = StringField()
    
class Componente(Document):
    __nome = StringField(unique=True)
    tipo = StringField()
    valor_compra = FloatField()
    quantidade_min = IntField()
    quantidade = IntField()
    cnpj = StringField()

# comp = Componente(__nome="roda 1004", tipo='roda', valor_compra=1000, quantidade_min=4, quantidade=4, cnpj="11424957007003")
# # comp.save()

# print(comp.__nome)