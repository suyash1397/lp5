#include <iostream>
#include <vector>
#include <stack>
#include <omp.h>

using namespace std;

class Graph
{
    int V;
    vector<vector<int>> adj;

public:
    Graph(int V)
    {
        this->adj = vector<vector<int>>(V);
        this->V = V;
    }
    void addEdge(int v, int w)
    {
        adj[v].push_back(w);
        adj[w].push_back(v);
    }
    void parallelDFS(int start)
    {
        vector<bool> visited(V, false);
        stack<int> stk;
        stk.push(start);
        while (!stk.empty())
        {
            int v = stk.top();
            stk.pop();
            if (!visited[v])
            {
                cout << v << " ";
                visited[v] = true;
#pragma omp parallel for
                for (int i = 0; i < adj[v].size(); i++)
                {
                    int n = adj[v][i];
                    if (!visited[n])
                    {
                        stk.push(n);
                    }
                }
            }
        }
    }
};

int main()
{
    Graph g(7);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);
    g.addEdge(2, 5);
    g.addEdge(2, 6);

    cout << "Depth-first search (DFS): ";
    g.parallelDFS(0);
    cout << endl;

    return 0;
}