/*
    The program expects a python list in a textfile as input.
    Avg. runtime of Selectionsort: O(n²)
*/

import java.util.Arrays;
import java.util.Scanner;

public class Selectionsort {

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

        selectionsort();
        System.out.println(Arrays.toString(numbers));
    }

    public static void selectionsort() {
        for (int i=0; i<numbers.length-1; i++) {
            int minIndex = i;
            for (int j=i+1; j<numbers.length; j++) {
                if (numbers[j] < numbers[minIndex])
                    minIndex = j;
            }
            int tmp = numbers[i];
            numbers[i] = numbers[minIndex];
            numbers[minIndex] = tmp;
        }
    }
}
