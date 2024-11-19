import numpy as np
import pandas as pd

matrix = np.load("01/first_task.npy")

total_sum = np.sum(matrix)
total_avg = np.mean(matrix)

main_diag_sum = np.sum(np.diag(matrix))
main_diag_avg = np.mean(np.diag(matrix))

side_diag_sum = np.sum(np.diag(np.fliplr(matrix)))
side_diag_avg = np.mean(np.diag(np.fliplr(matrix)))

max_value = np.max(matrix)
min_value = np.min(matrix)

results = {
    "sum": total_sum,
    "avr": total_avg,
    "sumMD": main_diag_sum,
    "avrMD": main_diag_avg,
    "sumSD": side_diag_sum,
    "avrSD": side_diag_avg,
    "max": max_value,
    "min": min_value,
}

pd.Series(results).to_json("01/matrix_results_01.json", indent=4)

normalize_matix = (matrix - min_value) / (max_value - min_value)
np.save("01/normalized_matrix_01.npy", normalize_matix)

print(
    "Результаты сохранены в martix_results_01.json, нормализованная матрица - в normalized_matrix_01.npy"
)
