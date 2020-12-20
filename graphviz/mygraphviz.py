from graphviz import Digraph

g = Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()