/*
    The program expects an python list as arguments.
    The list should have a maximum of 100000 elements.
    Avg. runtime of Quickssort: O(n*log(n))
    Compiler optimization: -O2
*/

#include <stdio.h>
#define MAX_NUMBERS 100000

int divide(int l, int r, int *a)
{
    int p = a[(l + r) / 2];
    while (1)
    {
        while (a[l] < p)
            l++;
        while (a[r] > p)
            r--;
        if (l < r)
        {
            int tmp = a[l];
            a[l] = a[r];
            a[r] = tmp;
        }
        else
            return r;
    }
}

int quicksort (int l, int r, int *a)
{
    if (l < r)
    {
        int d = divide(l, r, a);
        quicksort(l, d, a);
        quicksort(d+1, r, a);
    }
    return 0;
}

int printArray (int count, int *a)
{
    for (int i=0; i<count; i++)
    {
        printf("%d ", a[i]);
    }
    return 0;
}

int main ()
{
    int numbersCount = 0;
    int numbers[MAX_NUMBERS];
    scanf("[");
    while (scanf("%d,", &numbers[numbersCount]) == 1 && numbersCount <= MAX_NUMBERS)
    {
        numbersCount++;
    }
    quicksort(0, numbersCount-1, numbers);
    printArray(numbersCount, numbers);
    printf("\n");
    return 0;
}