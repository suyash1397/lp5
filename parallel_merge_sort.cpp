#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <omp.h>

using namespace std;

// Function to merge two sorted subarrays
void merge(vector<int> &arr, int left, int mid, int right)
{
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; ++i)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j)
        R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            ++i;
        }
        else
        {
            arr[k] = R[j];
            ++j;
        }
        ++k;
    }

    while (i < n1)
    {
        arr[k] = L[i];
        ++i;
        ++k;
    }

    while (j < n2)
    {
        arr[k] = R[j];
        ++j;
        ++k;
    }
}

// Sequential merge sort
void mergeSortSequential(vector<int> &arr, int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
        mergeSortSequential(arr, left, mid);
        mergeSortSequential(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

// Parallel merge sort
void mergeSortParallel(vector<int> &arr, int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
#pragma omp parallel sections
        {
#pragma omp section
            mergeSortParallel(arr, left, mid);
#pragma omp section
            mergeSortParallel(arr, mid + 1, right);
        }
        merge(arr, left, mid, right);
    }
}

int main()
{

    int size = 10000;
    vector<int> arr(size);

    for (int i = 0, j = size; i < size; i++, j--)
    {
        arr[i] = j;
    }

    auto start = chrono::high_resolution_clock::now();
    mergeSortSequential(arr, 0, arr.size() - 1);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> seq_time = end - start;
    cout << seq_time.count() << " " << endl;

    vector<int> arr_parr(size);

    for (int i = 0, j = size; i < size; i++, j--)
    {
        arr_parr[i] = j;
    }

    start = chrono::high_resolution_clock::now();
    mergeSortParallel(arr_parr, 0, arr_parr.size() - 1);
    end = chrono::high_resolution_clock::now();
    chrono::duration<double> par_time = end - start;
    cout << par_time.count() << endl;

    return 0;
}
