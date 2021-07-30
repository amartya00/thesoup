# **The soup**
A collection of python classes and functions.

## Getting it
#### Github
Download it from github with a `git clone https://github.com/amartya00/thesoup.git`
Navigate to the root, and run all tests to ensure everything is working with `nosetests -w tst/ --nocapture`

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
    - A mutable digraph implementation with adjacensy list `AdjListGraph`
    
  - Heap
    - Min heap `Minheap`
    - Max heap `MaxHeap`
    
   - Binary trees
     - BST `BinarySearchTree`
    
  - Trie (ASCII only)

  - Sets
    - A set that keeps track of the number of occurrences of repeated elements `CountSet` 
  
## Functions
It has the following utility functions
  - Collection related
    - Flatten a nested collection `flatten`
    - Flatten a nested collection except the tuples `flatten_to_tuple`
    - Find all subsequences of a list `subsequence`
    - Foreach method that works on all collections `foreach`
    
  - Graph traversals
    - Bread first search `bfs`
    - Depth first search `dfs`
    - Dijkstra `dijkstra`
    - Specialized SP for DAGs `shortest_path_dag`
    
  - String related
    - Test if 2 strings are anagrams `is_anagram`  
    
  - Other
    - K-way merge `merge`
    
    