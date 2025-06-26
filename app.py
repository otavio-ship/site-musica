from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de músicas (armazenamento em memória)
musicas = []

# Página principal
@app.route('/')
def index():
    duracao_total = 0
    i = 0
    while i < contar(musicas):
        duracao = musicas[i]['duracao']
        if duracao != "":
            duracao_total = duracao_total + float(duracao)
        i = i + 1
    return render_template('index.html', musicas=musicas, duracao_total=duracao_total)

# Página de adicionar
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        cantor = request.form['cantor']
        duracao = request.form['duracao']
        nova_musica = {
            'id': gerar_id(),
            'nome': nome,
            'cantor': cantor,
            'duracao': duracao
        }
        musicas.append(nova_musica)
        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Página de editar
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    musica = buscar_por_id(id)
    if musica != None:
        if request.method == 'POST':
            musica['nome'] = request.form['nome']
            musica['cantor'] = request.form['cantor']
            musica['duracao'] = request.form['duracao']
            return redirect(url_for('index'))
        return render_template('editar.html', musica=musica)
    return "Música não encontrada"

# Excluir música
@app.route('/excluir/<int:id>')
def excluir(id):
    nova_lista = []
    i = 0
    while i < contar(musicas):
        if musicas[i]['id'] != id:
            nova_lista.append(musicas[i])
        i = i + 1
    musicas.clear()

    i = 0
    while i < contar(nova_lista):
        nova_lista[i]['id'] = i
        musicas.append(nova_lista[i])
        i = i + 1
    return redirect(url_for('index'))

# Função para contar elementos
def contar(lista):
    total = 0
    for _ in lista:
        total = total + 1
    return total

# Gerar próximo ID
def gerar_id():
    maior_id = -1
    i = 0
    while i < contar(musicas):
        if musicas[i]['id'] > maior_id:
            maior_id = musicas[i]['id']
        i = i + 1
    return maior_id + 1

# Buscar música por ID
def buscar_por_id(id):
    i = 0
    while i < contar(musicas):
        if musicas[i]['id'] == id:
            return musicas[i]
        i = i + 1
    return None

if __name__ == '__main__':
    app.run(debug=True)
