from random import choice
from typing import Hashable, Set, Optional

class Grafo:
    def __init__(self):
        self._vertices = {}

    def adiciona_vertice(self, v: Hashable) -> None:
        """
        Adiciona um novo vértice em G
        """
        self._vertices[v] = set()

    def remove_vertice(self, v: Hashable) -> None:
        """
        Remove um vértice de G, juntamente com todas as conexões
        """
        for v2 in self._vertices[v]:
            self.desconecta(v, v2)

        del self._vertices[v]

    def conecta(self, v1: Hashable, v2: Hashable) -> None:
        """
        Conecta os vértices v1 e v2 em G
        """
        self._vertices[v1].add(v2)
        self._vertices[v2].add(v1)

    def desconecta(self, v1: Hashable, v2: Hashable) -> None:
        """
        Desconecta os vértices v1 e v2 em G
        """
        self._vertices[v1].remove(v2)
        if v1 != v2:
            self._vertices[v2].remove(v1)

    def ordem(self) -> int:
        """
        Retorna o número de vértices de G
        """
        return len(self._vertices)

    def vertices(self) -> Set:
        """
        Retorna um conjunto contendo os vértices de G
        """
        return set(self._vertices.keys())

    def um_vertice(self) -> Hashable:
        """
        Retorna um vértice qualquer de G
        """
        return choice(tuple(self.vertices()))

    def adjacentes(self, v: Hashable) -> Set:
        """
        Retorna um conjunto contendo os vértices adjacentes a v em G
        """
        return set(self._vertices[v])

    def grau(self, v: Hashable) -> int:
        """
        Retorna o número de vértices adjacentes a v em G
        """
        return len(self.adjacentes(v))

    def eh_regular(self) -> bool:
        """
        Verifica se todos os vértices de G possuem o mesmo grau
        """
        grau = self.grau(self.um_vertice())

        for v in self.vertices():
            if self.grau(v) != grau:
                return False

        return True

    def eh_completo(self) -> bool:
        """
        Verifica se cada vértice de G está conectado
        a todos os outros vértices
        """
        grau = self.ordem() - 1

        for v in self.vertices():
            if self.grau(v) != grau:
                return False

        return True

    def eh_conexo(self) -> bool:
        """
        Verifica se existe pelo menos um caminho entre
        cada par de vértices de G
        """
        return self.vertices() == self.fecho_transitivo(self.um_vertice())

    def eh_arvore(self) -> bool:
        """
        Verifica se não há ciclos em G
        """
        def ha_ciclo_com(v, v_anterior, ja_visitados=None):
            """
            Privado - verifica se v faz parte de algum ciclo no grafo
            """

            ja_visitados = ja_visitados or set()

            if v in ja_visitados:
                return True

            ja_visitados.add(v)

            for v_adj in self.adjacentes(v):
                if v_adj != v_anterior:
                    if ha_ciclo_com(v_adj, v, ja_visitados):
                        return True

            ja_visitados.remove(v)

            return False

        v = self.um_vertice()

        return self.eh_conexo() and not ha_ciclo_com(v, v)

    def fecho_transitivo(self, v: Hashable,
        ja_visitados: Optional[Set] = None) -> Set:
        """
        Retorna um conjunto contendo todos os vértices de G que
        são transitivamente alcancáveis partindo-se de v
        """
        ja_visitados = ja_visitados or set()

        ja_visitados.add(v)

        for v_adj in self.adjacentes(v):
            if not v_adj in ja_visitados:
                self.fecho_transitivo(v_adj, ja_visitados)

        return ja_visitados
