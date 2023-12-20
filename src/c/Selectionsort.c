/*
    The program expects an python list as arguments.
    The list should have a maximum of 100000 elements.
    Avg. runtime of Selectionsort: O(n²)
    Compiler optimization: -O2
*/

#include <stdio.h>
#define MAX_NUMBERS 100000

int selectionsort (int aCount, int *a)
{
    for (int i=0; i<aCount-1; i++)
    {
        int minIndex = i;
        for (int j=i+1; j<aCount; j++)
        {
            if (a[j] < a[minIndex])
                minIndex = j;
        }
        int tmp = a[i];
        a[i] = a[minIndex];
        a[minIndex] = tmp;
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
    selectionsort(numbersCount, numbers);
    printArray(numbersCount, numbers);
    printf("\n");
    return 0;
}