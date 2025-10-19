from faker import Faker
import random
from app.db.delta_minidb import db
from datetime import datetime

# Inicializa o Faker com localização brasileira
fake = Faker('pt_BR')

# Cria a tabela se ainda não existir
db.create_table_if_not_exists()

tipos = ["entrada", "saída"]
categorias = ["alimentação", "transporte", "lazer", "educação", "saúde", "moradia"]
descricoes = [
    "Compra no supermercado",
    "Mensalidade academia",
    "Pagamento de aluguel",
    "Assinatura de streaming",
    "Compra de roupas",
    "Abastecimento do carro",
    "Consulta médica",
    "Ingresso de show",
    "Curso online",
    "Farmácia"
]

for _ in range(1000):
    transaction = {
        "description": random.choice(descricoes), #Escolhe aleatoriamente um item da lista
        "amount": round(random.uniform(10, 5000), 2), #Valores entre R$10 e R$5.000, com duas casas decimais
        "date": fake.date_between(start_date="-1y", end_date="today").isoformat(), #do ultimo ano ate hoje
        "type": random.choice(tipos), #verifica o tipo da despesa
        "account_id": random.randint(1, 10), #Gera um número de 1 a 10 simulando que há 10 contas registradas.
        "category_id": random.randint(1, len(categorias)), # define quantas categorias existem.
        "user_id": random.randint(1, 20), # Simula que há até 20 usuários diferentes
    }
    db.insert(transaction)

print("1000 transações inseridas com sucesso!")