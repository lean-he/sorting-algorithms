/*
    The program expects a python list in a textfile as input.
    Avg. runtime of Quickssort: O(n*log(n))
*/

import java.util.Arrays;
import java.util.Scanner;

public class Quicksort {

    private static int[] numbers;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        scanner.close();

        String[] inputString = input.replaceAll("\\[|\\]|\\s", "").split(",");
        numbers = new int[inputString.length];
        for (int i=0; i<inputString.length; i++) {
            numbers[i] = Integer.parseInt(inputString[i]);
        }

        quicksort(0, numbers.length-1);
        System.out.println(Arrays.toString(numbers));
    }

    public static int divide(int l, int r) {
        int p = numbers[(l + r) / 2];
        while (true) {
            while (numbers[l] < p)
                l++;
            while (numbers[r] > p)
                r--;
            if (l < r) {
                int tmp = numbers[l];
                numbers[l] = numbers[r];
                numbers[r] = tmp;
            } else
                return r;
        }
    }

    public static void quicksort(int l, int r) {
        if (l < r) {
            int d = divide(l, r);
            quicksort(l, d);
            quicksort(d+1, r);
        }
    }
}
