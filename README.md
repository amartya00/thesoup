# **The soup**
A collection of python classes and functions.

## Getting it
Download it from github with a `git clone https://github.com/amartya00/thesoup.git`
Navigate to the root, and run all tests to ensure everything is working with `nosetests -w tst/ --nocapture`

**NOTE**: If you do not have nose tests, install it with `sudo pip3 install nose`

**NOTE**: This is python3 only

Now install with `sudo pip3 install .`

## Components
### Classes
It has the following utility classes:
  - Graphs
    - Abstract class for directed graph `DiGraph`
    - Abstract class for directed mutable graph `MutableDiGraph`
    - A mutable digraph implementation with adjacensy list `AdjListGraph`
    
  - Heap
    - Min heap `Minheap`
    - Max heap `MaxHeap`
    
  - Trie (ASCII only)
  
## Functions
It has the following utility functions
  - Collection related
    - Flatten a nested collection `flatten`
    - Flatten annested collection except the tuples `flatten_to_tuple`
    
  - Graph traversals
    - Bread first search `bfs`
    - Depth first search `dfs`
    - Dijkstra `dijkstra`
    
    