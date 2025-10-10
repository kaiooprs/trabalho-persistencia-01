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
├─ app/
│ ├─ main.py # Inicialização do FastAPI
│ ├─ config.py # Variáveis de ambiente e paths
│ ├─ security.py # JWT e autenticação
│ ├─ db/
│ │ ├─ seq.py # Controle de IDs automáticos
│ │ └─ delta_mini_db.py # Mini-DB baseado em Delta Lake
│ ├─ models/
│ │ ├─ transaction.py # Entidade principal (TP)
│ │ ├─ user.py # Usuário e autenticação
│ │ ├─ account.py # Contas associadas
│ │ └─ category.py # Categorias de transações
│ ├─ routers/
│ │ ├─ transactions.py # Rotas CRUD de transações
│ │ ├─ users.py # Login e cadastro de usuários
│ │ ├─ accounts.py # CRUD de contas
│ │ └─ categories.py # CRUD de categorias
│ └─ utils/
│ └─ hashing.py # Funções auxiliares de hash
├─ data/
│ ├─ delta/ # Armazenamento Delta Lake
│ └─ seq/ # Contadores de IDs (.seq)
├─ scripts/
│ └─ seed.py # Gera dados de teste
├─ tests/
│ └─ test_smoke.py # Testes iniciais
├─ .env.example # Exemplo de variáveis de ambiente
├─ requirements.txt # Dependências do projeto
└─ README.md

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
