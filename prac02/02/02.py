import os
import numpy as np

matrix = np.load("02/second_task.npy")

threshold = 585

indices = np.where(matrix > threshold)
x, y = indices[0], indices[1]
z = matrix[indices]

np.savez("02/filtered_02.npz", x, y, z)
np.savez_compressed("02/filtered_compressed_02.npz", x, y, z)

size_npz = os.path.getsize("02/filtered_02.npz")
size_compressed_npz = os.path.getsize("02/filtered_compressed_02.npz")

print(f"Размер обычного файла: {size_npz} байт")
print(f"Размер сжатого файла: {size_compressed_npz} байт")
print(f"Разница: {size_npz - size_compressed_npz} байт")
