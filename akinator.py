"""
=============================================================
  Mini Akinator — Árvore de Decisão com BFS e DFS
=============================================================
  Estrutura:
    - Classe Node para representar nós da árvore
    - Árvore com 7+ nós (perguntas e respostas)
    - DFS: percorre em profundidade (pré-ordem)
    - BFS: percorre em largura (nível por nível)
    - Jogo interativo de adivinhação
    - Aprendizado incremental (extensão)
=============================================================
"""

from collections import deque

# ─────────────────────────────────────────
# PARTE 1 — Estrutura de dados: Nó da árvore
# ─────────────────────────────────────────

class Node:
    """
    Representa um nó da árvore de decisão.

    Atributos:
        question (str): Pergunta do nó interno (None se for folha)
        answer   (str): Resposta final do nó folha (None se for interno)
        yes      (Node): Filho para resposta 'sim'
        no       (Node): Filho para resposta 'não'
    """
    def __init__(self, question=None, answer=None):
        self.question = question   # nó interno
        self.answer   = answer     # nó folha
        self.yes      = None
        self.no       = None

    def is_leaf(self):
        return self.answer is not None

    def __repr__(self):
        if self.is_leaf():
            return f"[Resposta: {self.answer}]"
        return f"[Pergunta: {self.question}]"


# ─────────────────────────────────────────
# Construção da árvore de decisão
#
#                    Vive na água?
#                   /             \
#                 SIM              NÃO
#                 /                  \
#          É mamífero?            Tem asas?
#          /        \             /       \
#       Golfinho  Tubarão     Tem penas?   Cachorro
#                              /      \
#                            Águia   Morcego
# ─────────────────────────────────────────

def build_tree():
    """Monta e retorna a raiz da árvore de decisão."""

    # ── Folhas (respostas finais) ──────────
    golfinho = Node(answer="Golfinho")
    tubarao  = Node(answer="Tubarão")
    aguia    = Node(answer="Águia")
    morcego  = Node(answer="Morcego")
    cachorro = Node(answer="Cachorro")

    # ── Nós internos ──────────────────────
    mamifero = Node(question="É mamífero?")
    mamifero.yes = golfinho
    mamifero.no  = tubarao

    penas = Node(question="Tem penas?")
    penas.yes = aguia
    penas.no  = morcego

    asas = Node(question="Tem asas?")
    asas.yes = penas
    asas.no  = cachorro

    raiz = Node(question="Vive na água?")
    raiz.yes = mamifero
    raiz.no  = asas

    return raiz


# ─────────────────────────────────────────
# PARTE 2 — DFS (Busca em Profundidade)
# ─────────────────────────────────────────

def dfs(node, depth=0):
    """
    Percorre a árvore em pré-ordem (DFS).
    Imprime cada nó visitado com indentação de profundidade.

    Retorna a lista de nós na ordem de visita.
    """
    if node is None:
        return []

    indent = "  " * depth
    if node.is_leaf():
        print(f"{indent}📌 Resposta → {node.answer}")
    else:
        print(f"{indent}❓ Pergunta → {node.question}")

    visited = [node]
    visited += dfs(node.yes, depth + 1)
    visited += dfs(node.no,  depth + 1)
    return visited


# ─────────────────────────────────────────
# PARTE 3 — BFS (Busca em Largura)
# ─────────────────────────────────────────

def bfs(root):
    """
    Percorre a árvore nível por nível (BFS).
    Imprime cada nó com seu nível correspondente.

    Retorna a lista de nós na ordem de visita.
    """
    if root is None:
        return []

    queue   = deque([(root, 0)])   # (nó, nível)
    visited = []
    current_level = -1

    while queue:
        node, level = queue.popleft()

        if level != current_level:
            current_level = level
            print(f"\n  ── Nível {level} ──────────────────")

        if node.is_leaf():
            print(f"  📌 Resposta → {node.answer}")
        else:
            print(f"  ❓ Pergunta → {node.question}")

        visited.append(node)

        if node.yes:
            queue.append((node.yes, level + 1))
        if node.no:
            queue.append((node.no,  level + 1))

    return visited


# ─────────────────────────────────────────
# PARTE 4 — Simulação do jogo
# ─────────────────────────────────────────

def play(root):
    """
    Simula o mini Akinator.
    Navega pela árvore seguindo as respostas do usuário.
    Retorna o nó folha encontrado.
    """
    node = root

    while not node.is_leaf():
        while True:
            resposta = input(f"\n{node.question} (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                break
            print("  ⚠  Por favor, responda apenas 's' ou 'n'.")

        node = node.yes if resposta == "s" else node.no

    print(f"\n🎯 Você pensou em: {node.answer}")
    return node


# ─────────────────────────────────────────
# EXTENSÃO — Aprendizado incremental
# ─────────────────────────────────────────

def learn(leaf, parent, branch):
    """
    Adiciona aprendizado quando o sistema erra.

    Parâmetros:
        leaf   (Node): Nó folha onde o sistema errou
        parent (Node): Pai do nó folha (para reconexão)
        branch (str) : 'yes' ou 'no' (ramo do pai até leaf)
    """
    novo_animal  = input("\nQual animal você pensou? ").strip()
    nova_pergunta = input(
        f"Qual pergunta distingue '{novo_animal}' de '{leaf.answer}'? "
    ).strip()
    resposta_novo = input(
        f"Para '{novo_animal}', a resposta seria (s/n)? "
    ).strip().lower()

    # Novo nó folha para o animal aprendido
    novo_leaf = Node(answer=novo_animal)

    # Novo nó interno com a pergunta discriminatória
    novo_no = Node(question=nova_pergunta)

    if resposta_novo == "s":
        novo_no.yes = novo_leaf
        novo_no.no  = leaf
    else:
        novo_no.yes = leaf
        novo_no.no  = novo_leaf

    # Reconecta o nó pai ao novo nó interno
    if branch == "yes":
        parent.yes = novo_no
    else:
        parent.no  = novo_no

    print(f"\n✅ Aprendi sobre '{novo_animal}'! Obrigado.")


# ─────────────────────────────────────────
# PARTE 5 — Comparação BFS vs DFS
# ─────────────────────────────────────────

def compare(root):
    """Executa e compara BFS e DFS na mesma árvore."""

    print("\n" + "═" * 52)
    print("  DFS — Busca em Profundidade (pré-ordem)")
    print("═" * 52)
    dfs_visited = dfs(root)
    print(f"\n  Total de nós visitados (DFS): {len(dfs_visited)}")

    print("\n" + "═" * 52)
    print("  BFS — Busca em Largura (nível por nível)")
    print("═" * 52)
    bfs_visited = bfs(root)
    print(f"\n  Total de nós visitados (BFS): {len(bfs_visited)}")

    print("\n" + "═" * 52)
    print("  Análise Comparativa")
    print("═" * 52)
    print("""
  Critério              BFS                    DFS
  ─────────────────────────────────────────────────────
  Tipo de exploração    nível por nível        profundidade
  Estrutura interna     fila (queue)           pilha/recursão
  Memória               maior (guarda nível)   menor
  Velocidade p/ folha   mais lenta (explora    mais rápida
                        todos os níveis)       (segue caminho)
  Melhor para           menor caminho          explorar todas
                        (grafos com peso)      possibilidades
  No Akinator           avalia perguntas       segue sequência
                        por nível              até resposta

  Perguntas:
  ──────────
  1. Qual algoritmo encontra resposta mais rápido em árvores
     profundas?
     → DFS, pois segue um caminho direto até a folha.

  2. Qual consome mais memória?
     → BFS, pois armazena todos os nós do nível atual na fila.

  3. Quando BFS seria preferível?
     → Quando queremos o caminho mais curto (menor nº de
       perguntas) ou quando as respostas estão em níveis
       superficiais da árvore.

  4. Quando DFS seria preferível?
     → Em jogos de adivinhação e árvores de decisão, onde
       seguir um ramo até o fim é o comportamento esperado.
    """)


# ─────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────

def menu():
    tree = build_tree()

    opcoes = {
        "1": ("Jogar (mini Akinator)",        lambda: _play_loop(tree)),
        "2": ("Percorrer com DFS",            lambda: dfs(tree)),
        "3": ("Percorrer com BFS",            lambda: bfs(tree)),
        "4": ("Comparar BFS vs DFS",          lambda: compare(tree)),
        "5": ("Sair",                         None),
    }

    while True:
        print("\n" + "═" * 42)
        print("  🧞  Mini Akinator — Menu Principal")
        print("═" * 42)
        for k, (desc, _) in opcoes.items():
            print(f"  [{k}] {desc}")
        print()

        escolha = input("  Escolha uma opção: ").strip()

        if escolha == "5":
            print("\n  Até logo! 👋\n")
            break
        elif escolha in opcoes:
            _, fn = opcoes[escolha]
            print()
            fn()
        else:
            print("  ⚠  Opção inválida.")


def _play_loop(tree):
    """Loop do jogo com suporte a aprendizado incremental."""
    # Rastreamos o pai para o aprendizado incremental
    parent = None
    branch = None
    node   = tree

    while not node.is_leaf():
        while True:
            resposta = input(f"{node.question} (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                break
            print("  ⚠  Responda apenas 's' ou 'n'.")

        parent = node
        if resposta == "s":
            branch = "yes"
            node   = node.yes
        else:
            branch = "no"
            node   = node.no

    print(f"\n🎯 Você pensou em: {node.answer}")

    # Aprendizado incremental
    acerto = input("\nAcertei? (s/n): ").strip().lower()
    if acerto == "n" and parent is not None:
        learn(node, parent, branch)


# ─────────────────────────────────────────

if __name__ == "__main__":
    menu()
