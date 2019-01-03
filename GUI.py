'''
System resource manager GUI.  Draws the graph to display process and resource usage.
Also detects deadlock based on a cycle of edges.
Created by: Charles Dodge
Class: CIS 452
Professor: Greg Wolffe
'''

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

#draw first graph image without edges
def draw_plot_first(dict_processes, dict_resources):
    G = nx.DiGraph()
    G.add_nodes_from(dict_processes)
    G.add_nodes_from(dict_resources)

    pos = nx.layout.bipartite_layout(G, dict_processes)

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='green')
    nx.draw_networkx_labels(G, pos, dict_processes, font_size=15)
    nx.draw_networkx_labels(G, pos, dict_resources, font_size=16)

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()

    return G

#draw new graph based on edges added with logic from engine.  Deadlock check as well
def draw_plot(graph, dict_processes, dict_resources):
    G = graph

    pos = nx.layout.bipartite_layout(G, dict_processes)

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='green')
    nx.draw_networkx_edges(G, pos, node_size=100, arrowsize=25, edge_color='red', edge_cmap=plt.cm.Blues, width=3)
    nx.draw_networkx_labels(G, pos, dict_processes, font_size=16)
    nx.draw_networkx_labels(G, pos, dict_resources, font_size=16)

    #detect deadlock by looking for cycle in graph
    try:
        deadlock = nx.find_cycle(G, orientation='original')
        plt.text(-.5,-.7, 'DEADLOCKED', fontsize=20, color='red', bbox=dict(facecolor='red', alpha=0.5))
        #plt.text(0,0, deadlock, wrap=True)
        print('deadlock path = ', deadlock)
        #time.sleep(100)

    except:
        pass

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()



