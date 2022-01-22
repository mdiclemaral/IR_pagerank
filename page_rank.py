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
import sys

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
            full_edges = (1 - t) * (1 / len(edges))
            for edge in edges:
                transition_matrix[vertex-1][edge-1] += full_edges

    return transition_matrix


'''
Page-rank algorithm for reuters articles finding the PageRank scores of people mentioned in the reuters articles.
Returns a sorted list of people and their page-rank score: list = [(person, score),..]
'''


def page_rank(transition_matrix, x, vertices):
    while True:
        prev_x = x
        temp_x = []
        for k in range(len(x)):
            a = 0
            for i in range(len(x)):
                a += (transition_matrix[i][k] * x[i])
            temp_x.append(a)
        x = temp_x
        if prev_x == x:
            break

    page_ranks = {}  # Dictionary for people and their page rank
    for vertex_id in range(len(x)):
        page_ranks[vertices[vertex_id + 1]] = x[vertex_id]
    sorted_ranks = sorted(page_ranks.items(), key=lambda a: a[1], reverse=True)
    return sorted_ranks


'''
Prints the page rank scores of highest rated print_n people and their names on a txt file as well as the terminal.
'''


def printt(page_rank_scores, print_n):
    with open('page_rank_scores.txt', 'w') as f:
        for i in range(print_n):
            out = 'Person:  ' + str(page_rank_scores[i][0])+ '    Score: '+ str(page_rank_scores[i][1])
            f.write(out)
            f.write('\n')

    for i in range(print_n):
        print('Person:  ', str(page_rank_scores[i][0]), '    Score: ', str(page_rank_scores[i][1]))



def main():

    file_name = sys.argv[1] #'data.txt'
    print_n = int(sys.argv[2]) #50   # Number of people to print the page rank scores
    t = 0.15  # Teleportation rate

    vertices, edges, num_vertices = file_handler(file_name)  # Reads the data

    transition_matrix = create_transition_matrix(edges, num_vertices, t)

    x = [1/num_vertices] * num_vertices  # Starting x matrix for random walk in page_rank with uniform distr.
    page_rank_scores = page_rank(transition_matrix, x, vertices)
    printt(page_rank_scores, print_n)


if __name__ == '__main__':

    main()
