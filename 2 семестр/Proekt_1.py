import math
matrix = [
    [30, 11, 34, 51, 60, 11, 17, 18, 36, 22], [28, 15, 26, 52, 56, 15, 13, 23, 47, 34], [32, 16, 38, 52, 64, 16, 19, 25, 50, 36], [26, 19, 32, 53, 52, 19, 16, 14, 28, 22], [30, 17, 24, 53, 59, 17, 12, 13, 26, 28], [28, 12, 22, 54, 55, 13, 11, 11, 23, 30], [31, 13, 34, 54, 61, 19, 17, 19, 37, 26], [33, 11, 36, 54, 65, 16, 18, 10, 21, 38], [25, 15, 22, 55, 50, 12, 11, 12, 25, 22], [29, 16, 28, 56, 58, 11, 14, 15, 30, 34], [32, 19, 30, 56, 63, 17, 15, 13, 26, 36], [27, 17, 26, 57, 54, 18, 13, 11, 22, 26], [26, 13, 38, 58, 51, 17, 19, 25, 51, 22], [30, 19, 34, 58, 60, 18, 17, 21, 42, 30], [28, 16, 24, 59, 56, 13, 12, 19, 38, 32]
]
stroka, stolbes, porog = 15, 10, 0.5
#Считаем среднее значение для каждого столбца (признака)
srednee = [sum(ryad[j] for ryad in matrix) / stroka for j in range(stolbes)]
# Считаем сумму квадратов отклонений (для знаменателя корреляции)
dispersiya = [sum((matrix[i][j] - srednee[j]) ** 2 for i in range(stroka)) / 14 for j in range(stolbes)]
# Создаем пустую корреляционную матрицу
corr_matrix = [[0.0] * stolbes for t in range(stolbes)]
print("Корреляционная матрица:")
for i in range(stolbes):
    for j in range(stolbes):
        if i == j:
            corr_matrix[i][j] = 1.0  # На главной диагонали всегда 1
        else:
            kovariaciya = sum((matrix[k][i] - srednee[i]) * (matrix[k][j] - srednee[j])/14 for k in range(stroka))  # Считаем ковариацию между двумя признаками
            # Считаем коэффициент корреляции
            r = abs(kovariaciya / math.sqrt(dispersiya[i] * dispersiya[j]))
            # Округляем до 2 знаков
            result = round(r, 2)
            # Условие: вне диагонали не может быть строго 0 или 1
            if result <= 0: result = 0.01
            if result >= 1: result = 0.99
            corr_matrix[i][j] = result
        print(f"{corr_matrix[i][j]:6.2f}", end="")
    print()
# Алгоритм плеяд
gruppa = [n for n in range(stolbes)]  # Массив групп (изначально каждый сам по себе)
ispolzovano = [False] * stolbes  # Отметки: вычеркнут ли признак
# Ищем самый первый глобальный максимум
max_obshiy = -1
priznak1, priznak2 = 0, 0
for i in range(stolbes):
    for j in range(i + 1, stolbes):
        if corr_matrix[i][j] > max_obshiy:
            max_obshiy = corr_matrix[i][j]
            priznak1, priznak2 = i, j

ispolzovano[priznak1] = ispolzovano[priznak2] = True
if max_obshiy >= porog:
    gruppa[priznak2] = gruppa[priznak1]

# Двигаемся по цепочке рассматривая только две последние вычеркнутые строки
pred_priznak, posl_priznak = priznak1, priznak2

for t in range(stolbes - 2):
    max_local = -1
    luchshiy_kuda, luchshiy_otkuda = -1, -1

    # Проверяем строки двух последних признаков
    for stroka_id in [pred_priznak, posl_priznak]:
        for stolbes_id in range(stolbes):
            if not ispolzovano[stolbes_id] and corr_matrix[stroka_id][stolbes_id] > max_local: #Условие если признак не был использован и объект наибольший
                max_local = corr_matrix[stroka_id][stolbes_id]
                luchshiy_kuda = stolbes_id
                luchshiy_otkuda = stroka_id

    if luchshiy_kuda != -1:
        ispolzovano[luchshiy_kuda] = True
        # Если связь выше порога объединяем в одну группу
        if max_local >= porog:
            old_gruppa = gruppa[luchshiy_kuda]
            new_gruppa = gruppa[luchshiy_otkuda]
            for i in range(stolbes):
                if gruppa[i] == old_gruppa:
                    gruppa[i] = new_gruppa
        # Обновляем память цепочки
        pred_priznak, posl_priznak = luchshiy_otkuda, luchshiy_kuda

# 5. Вывод финальных групп
print("\nИтоговые группы (плеяды):")
vyvedeno = [False] * stolbes
for i in range(stolbes):
    if not vyvedeno[i]:
        now_gruppa = [n + 1 for n in range(stolbes) if gruppa[n] == gruppa[i]]
        print(f"Группа {i+1}: {now_gruppa}")
        for element in now_gruppa:
            vyvedeno[element - 1] = True