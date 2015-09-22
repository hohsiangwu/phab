# examples

```
from graph import Graph, edges_from_diffs
from models import Diff

diffs = Diff.query(limit=500)
edges = edges_from_diffs(diffs)
graph = Graph(edges)
graph.topk_out_degree()
```
