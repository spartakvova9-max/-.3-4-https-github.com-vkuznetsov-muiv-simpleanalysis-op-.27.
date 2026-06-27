"""
Модуль очистки данных от цифрового мусора
"""
import pandas as pd
import numpy as np
import math
from typing import Dict

def math_round_to_hundreds(x: int) -> int:
    """
    Округление числа до сотен по математическому правилу
    
    Примеры:
        1250 -> 1300
        -1250 -> -1300
        1249 -> 1200
        -3781 -> -3800
    """
    # Корректное математическое округление для отрицательных чисел
    if x >= 0:
        return int(math.floor(x / 100 + 0.5)) * 100
    else:
        return int(math.ceil(x / 100 - 0.5)) * 100

def clean_series(series: pd.Series, 
                 low: int = -10000, 
                 high: int = 10000,
                 remove_duplicates: bool = False) -> tuple[pd.Series, Dict]:
    """
    Очистка данных от цифрового мусора
    
    Выполняемые проверки:
    1. Удаление NaN / null значений
    2. Проверка типа данных
    3. Фильтрация выхода за допустимый диапазон
    4. Поиск и обработка дубликатов
    5. Проверка аномальных значений
    
    Returns:
        (очищенная_series, отчет_очистки)
    """
    report = {}
    original_count = len(series)
    report["исходное_количество"] = original_count
    
    # Шаг 1: удаление NaN
    nan_count = series.isna().sum()
    series_clean = series.dropna()
    report["удалено_NaN"] = int(nan_count)
    
    # Шаг 2: приведение типа
    try:
        series_clean = series_clean.astype(int)
        report["приведение_типа"] = "int - успешно"
    except Exception as e:
        report["приведение_типа"] = f"ошибка: {e}"
    
    # Шаг 3: фильтрация диапазона
    out_of_range_mask = (series_clean < low) | (series_clean > high)
    out_of_range_count = out_of_range_mask.sum()
    series_clean = series_clean[~out_of_range_mask]
    report["удалено_вне_диапазона"] = int(out_of_range_count)
    
    # Шаг 4: дубликаты (только подсчет, по ТЗ удалять не обязательно)
    duplicates = series_clean.duplicated().sum()
    report["найдено_дубликатов"] = int(duplicates)
    if remove_duplicates:
        series_clean = series_clean.drop_duplicates()
        report["дубликаты_удалены"] = True
    else:
        report["дубликаты_удалены"] = False
    
    # Шаг 5: аномалии (z-score > 3, для равномерного распределения информативно)
    mean = series_clean.mean()
    std = series_clean.std()
    if std > 0:
        z_scores = np.abs((series_clean - mean) / std)
        anomalies = (z_scores > 3).sum()
    else:
        anomalies = 0
    report["аномалий_zscore_>3"] = int(anomalies)
    
    report["итоговое_количество"] = len(series_clean)
    report["удалено_всего"] = original_count - len(series_clean)
    report["процент_очистки"] = round(report["удалено_всего"] / original_count * 100, 2) if original_count > 0 else 0
    
    return series_clean.reset_index(drop=True), report

def clean_with_logging(series: pd.Series) -> pd.Series:
    """Очистка с выводом лога в консоль"""
    cleaned, report = clean_series(series)
    print("\n=== ОТЧЕТ ОБ ОЧИСТКЕ ДАННЫХ ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print("================================\n")
    return cleaned

if __name__ == "__main__":
    # Тест очистки на замусоренных данных
    test_data = pd.Series([100, 200, None, 50000, -15000, 200, np.nan, 300])
    cleaned, rep = clean_series(test_data)
    print(rep)
    print(cleaned.tolist())
