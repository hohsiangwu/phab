from collections import Counter

import networkx as nx

def edges_from_diffs(diffs):
  edges = [(diff.authorPHID, reviewer) for diff in diffs for reviewer, _ in diff.accepted_by if 'USER' in reviewer]
  return [(source, target, weight) for (source, target), weight in Counter(edges).items()]

class Graph(object):
  def __init__(self, edges):
    self.DG = nx.DiGraph()
    self.DG.add_weighted_edges_from(edges)

  def topk_out_degree(self, topk=50):
    out_degree = []
    for node in self.DG.nodes():
      out_degree.append((node, self.DG.out_degree(node)))
    return sorted(out_degree, key=lambda n: -n[1])[:topk]

  def topk_in_degree(self, topk=50):
    in_degree = []
    for node in self.DG.nodes():
      in_degree.append((node, self.DG.in_degree(node)))
    return sorted(in_degree, key=lambda n: -n[1])[:topk]

  def k_clique_communities(self, k):
    return list(nx.k_clique_communities(self.DG.to_undirected(), k))

  def topk_betweenness_centrality(self, topk=50):
    return sorted(nx.betweenness_centrality(self.DG).items(), key=lambda n: -n[1])[:topk]

  def topk_authorities_hubs(self, topk=50):
    hubs, authorities = nx.hits(self.DG)
    return (sorted(hubs.items(), key=lambda x: -x[1])[:topk],
            sorted(authorities.items(), key=lambda x: -x[1])[:topk])

  def topk_pagerank(self, topk=50):
    return sorted(nx.pagerank(self.DG).items(), key=lambda x: -x[1])[:topk]
