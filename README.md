# 💰 Finance API — Controle de Despesas Pessoais

API REST desenvolvida em **Python + FastAPI** para gerenciar **transações financeiras pessoais** (receitas e despesas).  
O projeto utiliza **Delta Lake (com PyArrow)** para persistência de dados em disco, garantindo eficiência, integridade e fácil manipulação sem necessidade de bancos SQL.

---

## 🚀 Tecnologias utilizadas

- **Python 3.11+**
- **FastAPI** — framework web moderno e performático
- **Pydantic** — validação e tipagem de dados
- **Delta Lake** + **PyArrow** — armazenamento colunar e transacional
- **Uvicorn** — servidor ASGI
- **Passlib** + **python-jose** — autenticação JWT (usuários)
- **Faker** — geração de dados falsos para testes

---

## 📂 Estrutura do projeto
finance-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── seq.py
│   │   └── delta_mini_db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── category.py
│   │   └── transaction.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── users.py
│   │   ├── accounts.py
│   │   ├── categories.py
│   │   └── transactions.py
│   └── utils/
│       └── hashing.py
├── data/
│   ├── delta/
│   │   ├── users/
│   │   ├── accounts/
│   │   ├── categories/
│   │   └── transactions/
│   └── seq/
│       ├── users.seq
│       ├── accounts.seq
│       ├── categories.seq
│       └── transactions.seq
├── scripts/
│   └── seed.py
├── tests/
│   └── test_smoke.py
├── .env.example
├── requirements.txt
└── README.md

---

## ⚙️ Instalação e execução local

### Clone o repositório  
git clone https://github.com/seu-usuario/finance-api.git
cd finance-api

### Crie seu ambiente virtual

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate   # Windows

### Instale as dependências
pip install -r requirements.txt

### Configure seu arquivo .env baseando-se no .env.example

### Executando o servidor
uvicorn app.main:app --reload

### Acesse:
🌐 API Root: http://127.0.0.1:8000
📘 Swagger UI: http://127.0.0.1:8000/docs
