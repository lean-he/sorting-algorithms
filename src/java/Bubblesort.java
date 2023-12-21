/*
    The program expects a python list in a textfile as input.
    Avg. runtime of Bubblesort: O(n*log(n))
*/

import java.util.Arrays;
import java.util.Scanner;

public class Bubblesort {

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

        bubblesort();
        System.out.println(Arrays.toString(numbers));
    }

    public static void bubblesort() {
        for (int i=0; i<numbers.length-1; i++) {
            for (int j=0; j<numbers.length-1-i; j++) {
                if (numbers[j] > numbers[j+1]) {
                    int tmp = numbers[j];
                    numbers[j] = numbers[j+1];
                    numbers[j+1] = tmp;
                }
            }
        }
    }
}
