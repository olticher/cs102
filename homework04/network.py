import datetime
import time
from typing import List, Tuple, Union
import igraph
from igraph import Graph, plot

from api import get_friends


def get_network(users_ids: List[int], as_edgelist=True) -> Union[List[List[int]], List[Tuple[int, int]]]:
    """ Построить граф и представить его
    либо в виде матрицы смежности (as_edgelist=False),
    либо в виде списка ребер (as_edgelist=True)
    :param user_ids: идентификаторы пользователей для построения графа
    :param as_edgelist: задает вид представления графа
    """
    edgelist = []  #ребро (лист с кортежами)
    adj_matrix = [[0] * len(users_ids) for _ in range(len(users_ids))] #матрица смежности 
    for i, user_id in enumerate(users_ids):
        
        begin = datetime.datetime.now()
        friends = get_friends(user_id)

        friends_list = friends['response']['items']
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends_list:
                if as_edgelist:
                    edgelist.append((i, j))
                else:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        end = datetime.datetime.now()
    if as_edgelist:
        return edgelist      
    return adj_matrix
    


def plot_graph(edgelist: List[Tuple[int, int]], last_names: List[str]) -> None:
    """ Выделить сообщества в графе и визуализировать результат
    :param edgelist: граф, представленный в виде списка ребер
    :param last_names: список фамилий (узлы графа)
    """
    g = Graph(vertex_attrs={"label": last_names},
              edges=edgelist, directed=False)
    N = len(last_names)
    visual_style = {
        "vertex_size": 20,
        "bbox": (1500, 1500),
        "margin": 200,
        "vertex_label_dist": 1,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=1000,
            area=N ** 3,
            repulserad=N ** 3)
        }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)

if __name__ == '__main__':

    id = 59683548
    friends_ids = []
    friends_last_names = []
    friends = get_friends(id, 'last_name')
    for friend in friends['response']['items']:
        friends_ids.append(friend.get('id'))
        friends_last_names.append(friend.get('last_name'))
        
    edgelist = get_network(friends_ids)
    print(edgelist)
    plot_graph(edgelist, friends_last_names)
    time.sleep(60)
