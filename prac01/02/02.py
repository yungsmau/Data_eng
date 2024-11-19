import math

with open("02/second_task.txt", "r") as input_file, open(
    "02/result_second_task.txt", "w"
) as output_file:
    column_values = []

    for line in input_file:
        numbers = map(int, line.split())
        sum_of_sqrt = sum(math.sqrt(num) for num in numbers if num > 0)

        int_part = int(sum_of_sqrt)
        column_values.append(int_part)

        output_file.write(f"{int_part}\n")

    max_val = max(column_values)
    min_val = min(column_values)

    output_file.write(f"\nMax: {max_val}, Min: {min_val}")

print("Результаты в result_second_task.txt")
