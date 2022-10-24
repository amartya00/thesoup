# **The soup**
A collection of python classes and functions.

## Getting it
#### Github
Download it from GitHub with a `git clone https://github.com/amartya00/thesoup.git`
Navigate to the root, and run all tests to ensure everything is working with `nose2 -w tst/ --nocapture`

Now install with `sudo pip3 install .`

#### PyPi
This is available on [PyPi](https://pypi.org/project/thesoup/) as well. Do a `sudo pip3 install thesoup` to install.

**NOTE**: If you do not have nose tests, install it with `sudo pip3 install nose`

**NOTE**: This is python3 only

## Components
### Classes
It has the following utility classes:
  - Graphs
    - Abstract class for directed graph `DiGraph`
    - Abstract class for directed mutable graph `MutableDiGraph`
    - A mutable digraph implementation with adjacency list `AdjListGraph`
    
  - Heap
    - Min heap `Minheap`
    - Max heap `MaxHeap`
    
  - Binary trees
    - BST `BinarySearchTree`
    
  - Trie (ASCII only)

  - Sets
    - A set that keeps track of the number of occurrences of repeated elements `CountSet` 
    - A disjoint sets utility. See the [Wikipedia entry](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) `DisjointSets` for details on what it is
    
  - Utilities
    - A result class, similar to Rust's `Result`.

## Functions
It has the following utility functions
  - Collection related
    - Flatten a nested collection `flatten`
    - Flatten a nested collection except the tuples `flatten_to_tuple`
    - Find all subsequences of a list `subsequence`
    - Foreach method that works on all collections `foreach`
    - Group a collection into a map by some criteria `group_by`
    
  - Graph traversals
    - Bread first search `bfs`
    - Depth first search `dfs`
    - Dijkstra `dijkstra`
    - Specialized SP for DAGs `shortest_path_dag`
    
  - String related
    - Test if 2 strings are anagrams `is_anagram`  
    
  - Other
    - K-way merge `merge`
    
    