import re
from collections import Counter

with open("85/first_task.txt", "r") as file:
    text = file.read()

text = re.sub(r"\d+", "", text)
text = text.lower()

# подсчет гласных букв
vowels = "aeiou"
total_vowels = sum(1 for char in text if char in vowels)
total_chars = sum(1 for char in text if char.isalpha())
vowel_ratio = total_vowels / total_chars if total_chars > 0 else 0

# подсчет слов
words = re.findall(r"\b\w+\b", text)
word_count = Counter(words)

sorted_word_counts = sorted(word_count.items(), key=lambda item: item[1], reverse=True)

with open("answers/words_first_task.txt", "w") as output_file:
    for word, freq in sorted_word_counts:
        output_file.write(f"{word}:{freq}\n")
    output_file.write(f"\nКоличество гласных букв: {total_vowels}\n")
    output_file.write(f"\nДоя гласных букв: {vowel_ratio:.2%}")


print("Частота слов записана в файл words_first_task.txt")
print(f"Количество гласных букв: {total_vowels}")
print(f"Доя гласных букв: {vowel_ratio:.2%}")
