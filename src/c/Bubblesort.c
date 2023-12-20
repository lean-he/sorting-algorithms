/*
    The program expects an python list as arguments.
    The list should have a maximum of 100000 elements.
    Avg. runtime of Bubblessort: O(n²)
    Compiler optimization: -O2
*/

#include <stdio.h>
#define MAX_NUMBERS 100000

int bubblesort (int aCount, int *a)
{
    for (int i=0; i<aCount-1; i++)
    {
        for (int j=0; j<aCount-1-i; j++)
        {
            if (a[j] > a[j+1])
            {
                int tmp = a[j];
                a[j] = a[j+1];
                a[j+1] = tmp;
            }
        }
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
    bubblesort(numbersCount, numbers);
    printArray(numbersCount, numbers);
    printf("\n");
    return 0;
}