import json
import os
import random
import locale
import jsonschema

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
opcao_invalida = True

input("Bem vindo(a) ao Quiz AWS, bons estudos!")
while opcao_invalida:
    # Pede ao usuário para escolher o idioma
    idioma = input(
        "Escolha o idioma do jogo (Digite '1' para Português ou '2' para Inglês e pressione enter): ")

    if idioma == "2":
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        # Obtém o caminho completo para o arquivo questions2.json
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'questions2.json')
        opcao_invalida = False
    elif idioma == "1":
        # Caso seja escolhido o português, assume o questions.json
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'questions.json')
        opcao_invalida = False
    else:
        input("Opção inválida. Tente novamente...")


acertos = 0


def run_quiz(questions):
    # Valida as perguntas contra o esquema antes de continuar
    jsonschema.validate(questions, questions_schema)

    # Inicializa a variável de acertos
    global acertos
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
                print(
                    f"\nVocê acertou {acertos} de {i+1} do total de {total_perguntas} perguntas. Obrigado por jogar!")
                print("Até a próxima! :)")
                return acertos
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
                f"Errado, a resposta correta é {options[question['resposta']]}")

            # Pergunta ao usuário se deseja continuar
            if questions:
                choice = input("Deseja continuar? (s/n)").lower()
            if choice == "n":
                 break
            

    # Exibe o total de acertos
    print(
        f"\nVocê acertou {acertos} de {i+1} do total de {total_perguntas} perguntas. Obrigado por jogar! :)")
    print("Até a próxima!")
    return acertos


# Obtém as perguntas do arquivo em formato json
with open(path, encoding='utf-8') as f:
    questions = json.load(f)


# Inicia o quiz com as perguntas carregadas do arquivo
run_quiz(questions)

# Exibe a mensagem para finalizar o programa
input("\nPressione Enter para finalizar o quiz.")
