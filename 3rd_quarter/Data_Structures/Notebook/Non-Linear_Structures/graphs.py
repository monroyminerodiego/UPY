import os; os.system('cls')

class Node:
    def __init__(self,name):
        self.name = name
        self.connections = {}

    def __str__(self):
        string = ''
        if len(self.connections) == 0:
            string = f"'{self.name}' is not connected to anything"
        else:
            string = f"'{self.name}' is connected to:\n"
            for connection in self.connections:
                string += f"\t{'<' if self.connections[connection] == False else '-'}-----> {connection.name}\n"
        return string + '\n\n'
    


class Graph(Node):
    def __init__(self,name):
        super().__init__(name)

    def add_connection(self,node_to_connect,unidirection = True):
        self.connections[node_to_connect] = unidirection

    def del_connection(self,node_to_disconnect):
        if node_to_disconnect in self.connections:
            self.connections.pop(node_to_disconnect)
            string = f"'{node_to_disconnect}' disconnected succesfully"

node1 = Graph('a')
node2 = Graph('b')
node3 = Graph('c')
node4 = Graph('d')
node5 = Graph('e')

node1.add_connection(node2,False)
node2.add_connection(node3)
node1.add_connection(node4,False)
node3.add_connection(node5)

print(node1,node2,node3,node4,node5)
