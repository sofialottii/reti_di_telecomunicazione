
import sys

#inizializzo un nodo
class Node:
    def __init__(self, name):
        self.name = name         # Nome del nodo
        self.routing_table = {name: 0}  # Tabella instradamento per ogni nodo. {nome-nodo: costo percorso più breve}
        self.neighbors = {}      # Distanze dirette verso i vicini


    """Confronta le informazioni nella tabella di routing attuale con quelle
    ricevute dai nodi vicini. Se trova un percorso più beve, aggiorna la tabella.
    Return: true se c'è stato un aggiornamento, false altrimenti """

    def update_routing_table(self):
        updated = False
        for neighbor, cost in self.neighbors.items():
            for dest, actual_cost in neighbor.routing_table.items():
                if dest == self.name:  #il costo verso sé stessi rimane 0
                    continue
                new_cost = cost + actual_cost
                if dest not in self.routing_table or new_cost < self.routing_table[dest]:
                    self.routing_table[dest] = new_cost
                    updated = True
        return updated


    """Tramite questo metodo, possiamo rappresentare in maniera chiara e
    leggibile la tabella di routing """

    def __str__(self):
        table = f"Tabella di instradamento per nodo {self.name}:\n"
        for dest, cost in sorted(self.routing_table.items()):
            table += f"  Verso {dest}: {cost}\n"
        return table

"""Classe che rappresenta la rete, gestisce i nodi e le connessioni"""
class Network:
    def __init__(self):
        self.nodes = {}

    """crea un nodo con il nome name e lo aggiunge alla rete """
    def add_node(self, name):
        self.nodes[name] = Node(name)


    """ora aggiungiamo un collegamento tra due nodi, specificando il costo.
    Vengono aggiornate anche le tabelle di routing iniziali dei due nodi"""

    def add_link(self, node1_name, node2_name, cost):
        node1 = self.nodes[node1_name]
        node2 = self.nodes[node2_name]
        node1.neighbors[node2] = cost
        node2.neighbors[node1] = cost
        node1.routing_table[node2_name] = cost
        node2.routing_table[node1_name] = cost


    """Questa è la funzione che simula il funzionamento della distance vector.
    In pratica, mostra le tabelle di routing iniziali, poi esegue i cicli in cui
    i nodi aggiornano le loro tabelle fino alla convergenza (quindi fino a che
    non è possibile più alcun aggiornamento) e le tabelle di routing finali"""

    def simulate(self):
        print("TABELLE DI INSTRADAMENTO INIZIALI")
        self.print_routing_tables()

        while True:
            updates = 0
            for node in self.nodes.values():
                if node.update_routing_table():
                    updates += 1

            if updates == 0:
                break

        print("\nTabelle di Routing finali:\n")
        self.print_routing_tables()

    def print_routing_tables(self):
        for node in self.nodes.values():
            print("----------------------")
            print(node)
            print("----------------------\n")


if __name__ == "__main__":
    network = Network()
    
    #Creazione nodi
    for node_name in ["A", "B", "C", "D"]:
        network.add_node(node_name)

    #Creazione connessioni (link) e relativi costi
    network.add_link("A", "B", 1)
    network.add_link("A", "C", 4)
    network.add_link("B", "C", 2)
    network.add_link("B", "D", 6)
    network.add_link("C", "D", 3)

    #Simulazione del protocollo di routing
    network.simulate()
