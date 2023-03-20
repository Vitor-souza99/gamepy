import json
import os
import random
import locale
import jsonschema
import requests

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def translate_questions(questions):
    # Define a URL da API de tradução do Google
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=pt&tl=en&dt=t&q="

    # Cria uma lista para armazenar as perguntas traduzidas
    translated_questions = []

    # Loop de perguntas
    for question in questions:
        # Obtém a pergunta a ser traduzida
        original_text = question["pergunta"]

        # Faz uma requisição GET para a API de tradução do Google
        response = requests.get(url + original_text)

        # Extrai o texto traduzido da resposta
        translated_text = response.json()[0][0][0]

        # Atualiza a pergunta com o texto traduzido
        question["pergunta"] = translated_text

        # Adiciona a pergunta traduzida à lista
        translated_questions.append(question)

    return translated_questions

# Defina o esquema para validar as perguntas
questions_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "pergunta": {"type": "string"},
            "opcoes": {"type": "object", "additionalProperties": {"type": "string"}},
            "resposta": {"type": "string", "enum": ["a", "b", "c"]}
        },
        "required": ["pergunta", "opcoes", "resposta"]
    }
}

# Pede ao usuário para escolher o idioma
idioma = input("Escolha o idioma do jogo (Digite '1' para Português ou '2' para Inglês): ")
if idioma == "2":
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    # Obtém o caminho completo para o arquivo questions2.json
    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'questions2.json')
else:
    # Caso não seja escolhido o inglês, assume o português
    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'questions.json')


def run_quiz(questions):
    # Valida as perguntas contra o esquema antes de continuar
    jsonschema.validate(questions, questions_schema)
    # Inicializa a variável de acertos
    acertos = 0
    total_perguntas = len(questions)
    # Embaralha as perguntas para executá-las em ordem aleatória
    random.shuffle(questions)
    # Loop de perguntas
    for i, question in enumerate(questions):
        # Obtém as opções de resposta para a pergunta
        options = question["opcoes"]

        # Exibe a pergunta e as opções de resposta
        print(f"\nPergunta {i+1}/{total_perguntas}: {question['pergunta']}")
        print(f"a) {options['a']}")
        print(f"b) {options['b']}")
        print(f"c) {options['c']}")

        # Lê a resposta do usuário ou permite sair
        while True:
            answer = input(
                u"Qual é a resposta correta? (a/b/c) Ou digite 'sair' para encerrar o quiz.\n")
            if answer.lower() == 'sair':
                break
            elif answer.lower() in ['a', 'b', 'c']:
                break
            else:
                print("Opção inválida. Tente novamente.")

        # Verifica se a resposta está correta
        if answer.lower() == question["resposta"]:
            acertos += 1
            print("Parabéns, você acertou!")
        else:
            print(
                f"Que pena, a resposta correta era {options[question['resposta']]}")

        # Remove a pergunta já respondida da lista, se a lista não estiver vazia
        if questions:
            questions.remove(question)

        # Pergunta ao usuário se deseja continuar
        if questions:
            choice = input("Deseja continuar? (s/n)").lower()
            if choice == "n":
                break


# Obtém as perguntas do arquivo em formato json
with open(path, encoding='utf-8') as f:
    questions = json.load(f)

# Traduz as perguntas, caso a opção de jogar em inglês tenha sido escolhida
if idioma == "2":
    questions = translate_questions(questions)
    print("Perguntas traduzidas com sucesso para o inglês!")

# Inicia o quiz com as perguntas carregadas do arquivo
run_quiz(questions)


# Mensagem de despedida com a quantidade de acertos
print(f"\nVocê acertou {acertos} de {total_perguntas}. Obrigado por jogar!")
