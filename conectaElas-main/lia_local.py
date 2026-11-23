"""Tutor local educativo: não executa códigos e não utiliza serviços externos."""
import ast
import json
import re

def respond(question, code='', language='', mode='explain', level='iniciante', context=''):
    q = question.lower()
    language = language.lower()
    issues = []
    tips = []
    if code.strip():
        if language == 'python':
            try:
                ast.parse(code)
                tips.append('A análise sintática do Python não encontrou erros. Isso não garante que a lógica esteja correta.')
            except SyntaxError as e:
                issues.append(f'Linha {e.lineno}: {e.msg}. Verifique a indentação, os dois-pontos, parênteses e aspas.')
        elif language == 'json':
            try:
                json.loads(code)
                tips.append('O JSON é válido sintaticamente.')
            except json.JSONDecodeError as e:
                issues.append(f'Linha {e.lineno}, coluna {e.colno}: {e.msg}.')
        elif language in ('javascript', 'java', 'css'):
            if code.count('{') != code.count('}'):
                issues.append('A quantidade de chaves de abertura e fechamento é diferente.')
            if code.count('(') != code.count(')'):
                issues.append('A quantidade de parênteses de abertura e fechamento é diferente.')
            tips.append('Esta é uma verificação básica, não um compilador ou interpretador.')
        elif language == 'html':
            if not re.search(r'<[a-z][^>]*>', code, re.I):
                issues.append('Não encontrei uma tag HTML reconhecível.')
            tips.append('Confira a hierarquia, as tags de fechamento e os atributos.')
        elif language == 'sql':
            if not re.search(r'\b(select|insert|update|delete|create|alter)\b', code, re.I):
                issues.append('Não identifiquei um comando SQL comum.')
            tips.append('Verifique nomes de tabelas, condições WHERE e parâmetros; nenhuma consulta foi executada.')
    if mode == 'lines' and code.strip():
        rows = [f'Linha {i}: {line.strip()[:140]} — '+('linha vazia ou de espaçamento' if not line.strip() else 'identifique o comando, seus argumentos e seu efeito no programa') for i,line in enumerate(code.splitlines()[:25],1)]
        return 'Leitura guiada (não é uma interpretação automática completa):\n'+'\n'.join(rows)+'\n\nExperimente explicar com suas palavras o que cada linha faz.'
    if issues:
        return 'Encontrei possíveis problemas:\n'+'\n'.join('• '+i for i in issues)+'\n\nCorrija um ponto por vez e teste no ambiente apropriado.'
    if code.strip():
        return 'Análise local do código:\n'+'\n'.join('• '+x for x in tips)+'\n\nPara investigar a lógica, descreva o resultado esperado e compare com o resultado real. A LIA local não executou seu código.'
    topics = [
      (('variável','variavel'), 'Uma variável guarda um valor para reutilizar. Exemplo em Python: `idade = 16`. O valor pode mudar durante o programa.'),
      (('for','laço','laco','repetição','repeticao'), 'O laço `for` repete uma ação para cada item. Exemplo: `for numero in range(3): print(numero)` percorre 0, 1 e 2.'),
      (('lista','array'), 'Uma lista armazena vários itens em ordem. Exemplo: `cores = ["roxo", "azul"]`; `cores[0]` acessa o primeiro item.'),
      (('função','funcao'), 'Uma função reúne instruções reutilizáveis. Exemplo: `def dobro(x): return x * 2`.'),
      (('html',), 'HTML organiza o conteúdo de uma página usando elementos como `<h1>`, `<p>` e `<button>`.'),
      (('css',), 'CSS define a aparência da página. Exemplo: `h1 { color: purple; }` muda a cor dos títulos.'),
      (('javascript','js'), 'JavaScript permite interatividade no navegador, como responder a cliques e atualizar elementos da página.'),
      (('sql','banco de dados'), 'SQL permite consultar e modificar dados. Exemplo: `SELECT nome FROM alunos;` consulta a coluna nome.'),
      (('python',), 'Python é uma linguagem de programação com sintaxe legível. Comece com variáveis, condições, laços e funções.'),
    ]
    answer = next((a for keys,a in topics if any(k in q for k in keys)), None)
    if not answer:
        answer = 'Posso ajudar com Python, HTML, CSS, JavaScript, SQL e lógica. Diga qual conceito você está estudando ou cole um trecho de código para uma verificação básica.'
    if mode == 'hint':
        return 'Pista: qual é a entrada, qual resultado você espera e qual pequeno passo pode testar primeiro?\n\n'+answer
    if level == 'avancado':
        return answer+'\n\nConsidere também testes, tratamento de erros e legibilidade.'
    if level == 'iniciante':
        return answer+'\n\nQuer tentar um exemplo simples com esse conceito?'
    return answer
