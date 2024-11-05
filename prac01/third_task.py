def replace_na_with_mean(numbers):
    result = []

    for i in range(len(numbers)):
        if numbers[i] == "N/A":
            left = int(numbers[i - 1]) if i > 0 and numbers[i - 1] != "N/A" else None
            right = (
                int(numbers[i + 1])
                if i < len(numbers) - 1 and numbers[i + 1] != "N/A"
                else None
            )

            # если бы не было гарантии, что NA только между числами
            if left is not None and right is not None:
                result.append((left + right) / 2)
            elif left is not None:
                result.append(left)
            elif right is not None:
                result.append(right)
            else:
                result.append(0)

        else:
            result.append(int(numbers[i]))

    return result


with open("85/third_task.txt", "r") as input_file, open(
    "answers/third.txt", "w"
) as output_file:
    for line in input_file:
        numbers = line.strip().split()

        replaced_numbers = replace_na_with_mean(numbers)

        filtered_numbers = [num for num in replaced_numbers if num % 3 == 0]

        line_sum = sum(filtered_numbers)

        output_file.write(f"{int(line_sum)}\n")

print("Результаты записаны в third.txt")
