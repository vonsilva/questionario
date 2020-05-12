# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file
import json

app = Flask(__name__)

# Variáveis do Questionario
questoes = [
    {
        'id': 1,
        'pergunta': 'Se Maria tem duas pipocas doces e seu namorado José tem quatro pipocas, quantas pipocas Maria tem ao total?',
        'corretas': ['Duas', 'duas', 'Dois', 'dois', '2', 2]
    },
    {
        'id': 2,
        'pergunta': 'Se um mês tem 30 dias e Gustavo ganha 2 real por dia, quantos reais terá ao final do mês?',
        'corretas': ['Sessenta', 'sessenta', 60, '60']
    }
]

respostas = [{}]

resultado = [{
        "usuario": None,
        "acertos": 0,
        "erros": 0,
        "totalQuestoes": len(questoes)
    }
]


def pegarQuestao(q_id):
    for i in questoes:
        if i['id'] == q_id:
            return i

    return False


@app.route('/')
def redirecionar():
    redirect("/autoteste/login", code=302)



@app.route('/autoteste/login')
def login():
    return render_template('/questionario/questionario_index.html')



@app.route('/autoteste/criar/questao')
def criarQuestao():
    return render_template('/questionario/criarQuestao.html')



@app.route('/autoteste/criar/questao/enviar', methods=['POST'])
def enviarQuestao():
    idQuestao = questoes[(len(questoes)-1)]['id'] + 1
    enunciado = request.form['enunciado']
    resposta = request.form['resposta']

    questoes.append({
        'id': idQuestao,
        'pergunta': enunciado,
        'corretas': [resposta]
    })


    return redirect("/autoteste/reseta", code=302)



@app.route('/autoteste/questao/<int:q_id>')
def pegar_questao(q_id):
    for i in questoes:
        if i['id'] == q_id:
            return render_template('/questionario/questionario.html', id=i['id'], qt=i['pergunta']), 200

    return 'erro404', 404


@app.route('/autoteste/forms/name', methods=['POST'])
def formName():
    nome = request.form['nome']
    resultado[0]['usuario'] = nome
    respostas[0][nome] = {}
    return redirect("/autoteste/questao/1"), 302



@app.route('/autoteste/responder/<int:q_id>', methods=['POST'])
def responder(q_id):
    resposta = request.form['resposta']
    questao = pegarQuestao(q_id)

    if questao == False:
        return 'Erro 404', 404


    respostas[0][resultado[0]['usuario']][q_id] = resposta
    q_id += 1


    if q_id <= len(questoes):
        return redirect("/autoteste/questao/"+str(q_id))
    
    else:
        return redirect("/autoteste/"+resultado[0]['usuario']+"/resultados")




@app.route('/autoteste/<username>/resultados',)
def desempenho(username):

    dicrespostas = respostas[0][username]

    for i in dicrespostas:
        questao = pegarQuestao(i)
    
        if dicrespostas[i] in questao['corretas']:
            resultado[0]['acertos'] = resultado[0]['acertos'] + 1

        else:
            resultado[0]['erros'] = resultado[0]['erros'] + 1

    return redirect("/resultados/finais", code=302)


@app.route('/resultados/finais')
def resultadosFinais():
    return render_template('/questionario/fim.html', resultado=resultado[0])


@app.route('/autoteste/reseta', methods=['POST', 'GET'])
def reseta():
    respostas[0][0] = {}
    resultado[0] = {
        "usuario": None,
        "acertos": 0,
        "erros": 0,
        "totalQuestoes": len(questoes)
    }
    return redirect("/autoteste/login", code=302)



if __name__ == '__main__':
    app.debug = True
    app.run()
