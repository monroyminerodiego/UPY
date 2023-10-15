class ShowError(Exception):
    def __init__(self, message, code=0):
        super().__init__(message, code)
        self.mensaje = message

class Graph:
    def __init__(self):
        self.nodes = {}

    def __str__(self):
        string = ''
        for node in self.nodes:
            string += f"- {node} is not connected." if len(self.nodes[node].keys()) == 0 else f"- {node} is connected to:\n"
            for connection in self.nodes[node]:
                string += f"\t {'<' if self.nodes[node][connection] else '-'}----> {connection}\n"
            string += '\n'
        return string + '\n\n'

    def add_node(self,node):
        keys = self.nodes.keys()
        if node in keys:
            raise ShowError('Error: Node already exist in graph.', 1)
        else:
            self.nodes[node] = {}
            print(f"Node '{node}' added")
    
    def add_connection(self,primary_node,secondary_node,bidirectional=False):
        if not(primary_node in self.nodes.keys()):
            raise ShowError('Error: Primary node is not in graph', 2)
        elif not(secondary_node in self.nodes.keys()):
            raise ShowError('Error: Secondary node is not in graph', 3)
        
        if secondary_node in self.nodes[primary_node].keys():
            raise ShowError('Error: Primary node already has connection with Secondary Node.', 4)
        else:
            self.nodes[primary_node][secondary_node] = bidirectional
            if bidirectional:
                self.nodes[secondary_node] = { primary_node : bidirectional }
            print(f'Added connection from {primary_node} to {secondary_node} in a {"bidirectional" if bidirectional == True else "unidirectional"} way')

    def del_connection(self,primary_node,secondary_node):
        if not(primary_node in self.nodes.keys()):
            raise ShowError('Error: Primary node is not in graph.', 5)
        
        if not(secondary_node in list(self.nodes[primary_node].keys())):
            raise ShowError("Error: Primary node does not have connection with Secondary node.", 6)
        else:
            bidirectional = self.nodes[primary_node].pop(secondary_node)
            if bidirectional: self.nodes[secondary_node].pop(primary_node)
            print(f"Connection from {primary_node} to {secondary_node} deleted")
        
    def del_node(self,node):
        if not(node in self.nodes.keys()):
            raise ShowError("Error: Node to delete is not in graph.", 7)
        
        connected_nodes = []
        for parent_node in self.nodes:
            if node in self.nodes[parent_node].keys():
                connected_nodes.append(parent_node)

        if len(connected_nodes) != 0:
            confirmation = True if (input('Node has attached nodes.\n\nDelete those references?(y/n): ')).lower() == 'y' else False
        else:
            confirmation = True
            
        
        if confirmation:
            self.nodes.pop(node)
            for connected_node in connected_nodes:
                self.nodes[connected_node].pop(node)
        

if __name__ == '__main__':
    tree  = Graph()
    while True:
        import os; os.system('cls')
        print(f"""{'*'*15} Graphs Program {'*'*15}
        Your current graph tree looks like this: \n{tree}\n
        1. Add Node
        2. Add Connection between nodes
        3. Delete Connection between nodes
        4. Delete Node
        5. Exit\n""")
        option = input('Enter your option: ')
        if option == '1':
            tree.add_node(input(f"\n\nEnter the node: "))
        elif option == '2':
            tree.add_connection(
                input('\n\nNode to be connected: '),
                input('Node to be connected with: '),
                True if (input('They follow a bidirectional connection?(y/n): ')).lower() == 'y' else False
            )
        elif option == '3':
            tree.del_connection(
                input('\n\nNode to be deleted from: '),
                input('Node to be deleted: ')
            )
        elif option == '4':
            tree.del_node(input('\n\nNode to be deleted: '))
        elif option == '5':
            break
    print('\n\nGood bye...!')

