from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados
db = SQLAlchemy(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Nome do usuário
    username = db.Column(db.String(10), unique=True, nullable=False)  # Usuário
    password = db.Column(db.String(100), nullable=False)  # Senha com hash
    sector = db.Column(db.String(50), nullable=False)  # Setor do usuário

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota de Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se o usuário existe
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Login bem-sucedido
            session['user_id'] = user.id
            session['sector'] = user.sector
            if user.sector == 'rh':
                return redirect(url_for('rh_dashboard'))
            elif user.sector == 'pesquisa':
                return redirect(url_for('pesquisa_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'error')

    return render_template('login.html')

# Rota genérica do Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Rota para RH
@app.route('/rh', methods=['GET', 'POST'])
def rh_dashboard():
    if 'user_id' not in session or session.get('sector') != 'rh':
        return redirect(url_for('error_page'))

    if request.method == 'POST':
        # Adicionar novo usuário
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        sector = request.form['sector']

        if User.query.filter_by(username=username).first():
            flash('Usuário já existe!', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(name=name, username=username, password=hashed_password, sector=sector)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Usuário {name} adicionado com sucesso!', 'success')

    users = User.query.all()
    return render_template('rh.html', users=users)

# Rota para Pesquisa
@app.route('/pesquisa')
def pesquisa_dashboard():
    if 'user_id' not in session or session.get('sector') != 'pesquisa':
        return redirect(url_for('error_page'))
    return render_template('pesquisa.html')

# Rota de Erro
@app.route('/error')
def error_page():
    return render_template('error.html')

# Rota para Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('sector', None)
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('login'))

# Adicionar um usuário inicial (para testes)
@app.cli.command('create-user')
def create_user():
    name = input('Digite o nome do usuário: ')
    username = input('Digite o nome de usuário numérico: ')
    password = input('Digite a senha: ')
    sector = input('Digite o setor (rh/pesquisa): ')
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(name=name, username=username, password=hashed_password, sector=sector)
    db.session.add(new_user)
    db.session.commit()
    print(f'Usuário {name} do setor {sector} criado com sucesso!')

@app.cli.command('reset-database')
def reset_database():
    """Apaga todas as tabelas e recria o banco de dados."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Banco de dados resetado com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)
