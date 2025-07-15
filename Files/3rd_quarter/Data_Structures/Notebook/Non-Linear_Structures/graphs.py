"""
Instructions given by teacher:

Make a graph program where you give me the options to create, insert a vertex and delete a vertex

Made by:
- Sergio Barrera Chan
- Ariel Joel Buenfil Góngora
- Juan Antonio Cel Vazquez
- Diego Monroy Minero
"""


class Error(Exception):
    def __init__(self, message, code):
        super().__init__(message, code)
        self.mensaje = message

class Graph:
    def __init__(self):
        """
        ### Summary
        Class made to create a Graph Tree with the capacity to add nodes, connect nodes, delete connetions, delete nodes and displaying the tree view.
        
        ### Inputs 
            Expects no inputs

        ### Return
            Returns nothing
    
        ### Methods
        - add_node(): Method to add a node to the graph. Possible Errors: 1
        - add_connection(): Method to connect between 2 nodes. Possible Errors: 2, 3, 4
        - del_connection(): Method to delete the connection between 2 nodes. Possible Errors: 5, 6
        - del_node(): Method to delete a node from the graph. Possible Errors: 7
        - print(): When using the 'print()' function on a 'Graph' object, it displays all the graphs and their connections

        ### Possible Errors
        1. Raised when trying to add a node that is already in the graph tree.
        2. Raised when the node to be connected with does not exist in the graph tree.
        3. Raised when the node to be connected does not exist in the graph tree.
        4. Raised when the node to be connected with and the node to be connected already have a connection.
        5. Raised when the node to be deleted from does not exist in graph.
        6. Raised when the node to be deleted does not exist in graph.
        """
        
        self.__nodes = {}

    def __str__(self):
        string = ''
        for node in self.__nodes:
            string += f"- {node} is not connected." if len(self.__nodes[node].keys()) == 0 else f"- {node} is connected to:\n"
            for connection in self.__nodes[node]:
                string += f"\t{'<' if self.__nodes[node][connection] else '-'}----> {connection}\n"
            string += '\n'
        return string + '\n\n'

    def add_node(self,node):
        """
        ### Summary
        Method created to add a node to the graph.
        
        ### Inputs 
            - node: Expects any type of data

        ### Return
            Returns nothing, but raises errors if:
            - The node already exist in graph.
        """
        
        keys = self.__nodes.keys()
        if node in keys:
            raise Error('Error: Node already exist in graph.', 1)
        else:
            self.__nodes[node] = {}
    
    def add_connection(self,primary_node,secondary_node,bidirectional=False):
        """
        ### Summary
        Method created to connect two nodes between them. 
        
        ### Inputs 
            - primary_node = Expects any kind of existing data from the graph. It will be the node in which 'secondary_node' will be store as a connection.
            - secondary_node = Expects any kind of existing data from the graph. It is an existing node from the graph which will be stored as a connection in 'primary_node'.
            - bidirectional = Expects Bool data only. If set to True, it will also add the connection of the 'primary_node' to the 'seconday_node'.  Default behaviour is set to False to generate a unidirectional connection.

        ### Return
            Returns nothing, but raises errors if:
            - 'primary_node' is not a valid node.
            - 'secondary_node' is not a valid node.
            - 'primary_node' and 'secondary_node' already had a connection.
        """
        if not(primary_node in self.__nodes.keys()):
            raise Error('Error: Primary node is not in graph', 2)
        elif not(secondary_node in self.__nodes.keys()):
            raise Error('Error: Secondary node is not in graph', 3)
        
        if secondary_node in self.__nodes[primary_node].keys():
            raise Error('Error: Primary node already has connection with Secondary Node.', 4)
        else:
            self.__nodes[primary_node][secondary_node] = bidirectional
            if bidirectional:
                self.__nodes[secondary_node] = { primary_node : bidirectional }

    def del_connection(self,primary_node,secondary_node):
        """
        ### Summary
        Method created to delete a connection from a existing node in the graph.
        
        ### Inputs 
            - primary_node: Expects a valid node from the graph. It is the node in which the connection with 'secondary_node' will be deleted.
            - secondary_node: Expects a valid node from the graph. It is the node to delete from 'primary_connetion'

        ### Return
            Returns nothing, but raises errors if:
            - 'primary_node' is not in graph.
            - 'primary_node' does not have connection with 'secondary_node'
        """
        if not(primary_node in self.__nodes.keys()):
            raise Error('Error: Primary node is not in graph.', 5)
        
        if not(secondary_node in list(self.__nodes[primary_node].keys())):
            raise Error("Error: Primary node does not have connection with Secondary node.", 6)
        else:
            bidirectional = self.__nodes[primary_node].pop(secondary_node)
            if bidirectional: self.__nodes[secondary_node].pop(primary_node)
        
    def del_node(self,node):
        """
        ### Summary
        Method created to delete a node and its connections. If a Node is linked to another node, a confirmation statement will be displayed to delete those connections.
        
        ### Inputs 
            - node: Expects any valid node from Graph.

        ### Return
            Returns nothing, but raises errors if:
            - Node is not in graph
        """
        if not(node in self.__nodes.keys()):
            raise Error("Error: Node to delete is not in graph.", 7)
        
        connected_nodes = []
        for parent_node in self.__nodes:
            if node in self.__nodes[parent_node].keys():
                connected_nodes.append(parent_node)

        if len(connected_nodes) != 0:
            confirmation = True if (input('Node is linked to other nodes.\n\nDelete those references?(y/n): ')).lower() == 'y' else False
        else:
            confirmation = True
            
        
        if confirmation:
            self.__nodes.pop(node)
            for connected_node in connected_nodes:
                self.__nodes[connected_node].pop(node)
        

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
        
        else:
            print(tree.__nodes)
            break


    print('\n\nGood bye...!')

