import mysql.connector
import bcrypt

# Função para conectar ao banco de dados MySQL
def connect_db():
   return mysql.connector.connect(
       host="localhost",
       user="root",
       password="",
       database="users_db"
   )

# Função para registrar usuários
def register_user(username, password):
   conn = connect_db()
   cursor = conn.cursor()
   # Gerando um SALT único e criando o hash da senha
   salt = bcrypt.gensalt()
   hashed_password = bcrypt.hashpw(password.encode(), salt)
   try:
       cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
       conn.commit()
       print("\nUsuário registrado com sucesso!")
   except mysql.connector.errors.IntegrityError:
       print("Erro: Nome de usuário já existe.")
   finally:
       cursor.close()
       conn.close()

# Função para login
def login(username, password):
   conn = connect_db()
   cursor = conn.cursor()
   cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
   user = cursor.fetchone()
   if user:
       stored_hash = user[0].encode()  # Convertendo para bytes se necessário
       if bcrypt.checkpw(password.encode(), stored_hash):
           print("Login bem-sucedido!")
       else:
           print("Senha incorreta! Tente novamente.")
   else:
       print("Usuário não encontrado.")
   cursor.close()
   conn.close()

# Função para ataque de dicionário
def dictionary_attack(username, wordlist):
   conn = connect_db()
   cursor = conn.cursor()
   cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
   user = cursor.fetchone()
   if not user:
       print("Usuário não encontrado.")
       return
   hashed_password = user[0].encode()  # Convertendo para bytes
   for word in wordlist:
       if bcrypt.checkpw(word.encode(), hashed_password):
           print(f"\n🔓 Senha encontrada: {hashed_password}")
           return
   print("\nNenhuma senha da wordlist corresponde.")
   cursor.close()
   conn.close()

# Solicitação de credenciais ao usuário
user_teste = input("\nInforme o seu usuário.........: ").strip()
senha_teste = input("Informe a sua senha............: ").strip()

# Registrando usuário no banco de dados
register_user(user_teste, senha_teste)

# Tentativa de login
login(user_teste, senha_teste)

# Realizando ataque de dicionário
ataque_login = str(input('\nDigite o login.............:'))
ataque_senha = str(input('Digite a senha do usuário..:'))

if ataque_login != True and ataque_senha != True:
    print("\nNenhuma senha da wordlist corresponde.")
else:
    dictionary_attack(user_teste, ["123456", senha_teste, "password", ataque_login, ataque_senha])