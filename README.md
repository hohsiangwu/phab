# examples

```
from graph import Graph, edges_from_diffs
from models import Diff

diffs = Diff(10)
edges = edges_from_diffs(diffs)
graph = Graph(edges)
graph.topk_out_degree()
```
