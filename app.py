from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'  # Defina uma chave secreta para sessões

# Lista de usuários (Simulação de banco de dados simples)
users = {
    'marcio': {'password': 'marcio123', 'role': 'admin'},
    'port': {'password': 'port123', 'role': 'cliente'}
}

# Lista de registros (Simulação de banco de dados simples)
records = []

# Rota para o login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('register' if session['role'] == 'cliente' else 'view_records'))
        else:
            return "Credenciais incorretas", 403
    return render_template('login.html')

# Rota para o formulário de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' not in session or session['role'] != 'cliente':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        rg = request.form['rg']
        placa = request.form['placa']
        casa = request.form['casa']
        autorizador = request.form['autorizador']
        tipo = request.form['tipo']
        visitante = request.form['visitante']  # Captura o tipo de visitante
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Criando o registro com o novo campo "visitante"
        record = {
            'nome': nome,
            'rg': rg,
            'placa': placa,
            'casa': casa,
            'autorizador': autorizador,
            'tipo': tipo,
            'visitante': visitante,  # Armazenando o tipo de visitante
            'data_hora': data_hora
        }
        records.append(record)

        # Flash message de sucesso
        flash("Registro realizado com sucesso!", "success")

        return redirect(url_for('register'))
    
    return render_template('register.html')

# Rota para ver os registros (somente para admin)
@app.route('/records')
def view_records():
    if 'user' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    return render_template('records.html', records=records)

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
