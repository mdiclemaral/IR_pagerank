'''
PageRank Algorithm

Implemented by Maral Dicle Maral, Jan 22

PageRank-based method to identify the most important
people occurring in news articles. The data.txt file is a plain text file containing an undirected
and unweighted graph of social network of co-occurrence in news articles. The graph has been
constructed from a subset of 3000 news articles from the Reuters-21578 corpus by identifying the
person names. The vertices of the graph are defined as distinct people. An edge is constructed
between two people if their names appear in the same news article. The resulting social network
consists of 459 nodes and 1422 edges.

'''

'''
File handler for data.txt
Returns dict vertices = {vertex_name1 = vertexID1, .. } and dict edges = {v1 = [v2iv5..], v2 = ..}
'''
def file_handler(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    counter = 0
    limit = 0
    vertices = {}
    edges = {}
    for line in lines:
        if line.startswith('*Edges'):
            continue
        l = line.strip().split()
        if line.startswith('*Vertices'):
            limit = int(l[1])
            continue
        #Creates a map of vertices and their ID
        if counter < limit:
            vertices[int(l[0])] = l[1]

        #Creates a directed network as: for each edge [vertex1 vertex2], there is an edge of [vertex2 vertex1]
        else:
            pre = int(l[0])
            suf = int(l[1])
            if pre not in edges:
                edges[pre] = [suf]
                if suf not in edges:
                    edges[suf] = [pre]
                else:
                    edges[suf].append(pre)
            else:
                edges[pre].append(suf)
                if suf not in edges:
                    edges[suf] = [pre]
                else:
                    edges[suf].append(pre)
        counter += 1
    return vertices, edges, limit

'''
Creates the transition matrix (p) for page rank algorithm. 
Returns a (num_vertices x num_vertices) matrix with edges' corresponding Pij probabilities. 
'''
def create_transition_matrix(ver_edges, num_vertices, t):

    empty_teleport = t / num_vertices  # The teleportation rate for empty edges in vertices with other edges

    # Creates an empty transition matrix
    transition_matrix = []
    for n in range(num_vertices):
        listofzeros = [empty_teleport] * num_vertices
        transition_matrix.append(listofzeros)

    # Fills the transition matrix according to the given edge information in ver_edges
    for vertex, edges in ver_edges.items():
        if len(edges) == 0:  # If the vertex has no edges, teleport with a probability of  1 / num_vertices
            empty_vertex_edges = 1 / num_vertices
            for n in range(num_vertices):
                transition_matrix[vertex-1][n] = empty_vertex_edges
        else:  # If the vertex has edges, teleport with a probability  empty_teleport = t / num_vertices
            full_edges = (1 - empty_teleport) * (1 / len(edges))
            for edge in edges:
                transition_matrix[vertex-1][edge-1] += full_edges

    return transition_matrix

def page_rank(transition_matrix, x, vertices):

    #while True:
    for i in range(2):
        prev_x = x
        temp_x = []
        for i in range(len(x)):
            a = 0
            for n in range(len(transition_matrix)):
                a += transition_matrix[n][i] * x[i]
            temp_x.append(a)
        x = temp_x
        if prev_x == x:
            break

    page_ranks = {}
    for vertex_id in range(len(x)):
        page_ranks[vertices[vertex_id + 1]] = x[vertex_id]
    print(page_ranks)

def main():
    vertices, edges, num_vertices = file_handler('data.txt')  # Reads the data
    t = 0.15  # Teleportation rate
    transition_matrix = create_transition_matrix(edges, num_vertices, t)

    x = [1/num_vertices] * num_vertices  # Starting x matrix for random walk in page_rank with uniform distr.
    page_rank(transition_matrix, x, vertices)

if __name__ == '__main__':
    main()