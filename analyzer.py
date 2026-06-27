"""
Модуль количественного анализа данных
"""
import pandas as pd
import numpy as np
import math
from typing import Dict

def calculate_statistics(series: pd.Series) -> Dict:
    """
    Расчет стандартных числовых характеристик
    
    Returns:
        dict со статистиками
    """
    stats = {}
    stats["минимум"] = int(series.min())
    stats["максимум"] = int(series.max())
    stats["сумма"] = int(series.sum())
    stats["среднее"] = float(series.mean())
    stats["медиана"] = float(series.median())
    stats["среднеквадратическое_отклонение"] = float(series.std(ddof=0))
    stats["дисперсия"] = float(series.var(ddof=0))
    
    # Количество повторяющихся значений
    value_counts = series.value_counts()
    duplicates = value_counts[value_counts > 1]
    stats["количество_уникальных_дубликатов"] = int(len(duplicates))
    stats["общее_количество_повторов"] = int(duplicates.sum() - len(duplicates)) if len(duplicates) > 0 else 0
    
    # Дополнительные характеристики
    stats["количество"] = int(series.count())
    stats["размах"] = stats["максимум"] - stats["минимум"]
    
    return stats

def print_statistics(stats: Dict) -> None:
    """Вывод статистик в консоль с пояснениями"""
    print("\n=== СТАНДАРТНЫЕ ЧИСЛОВЫЕ ХАРАКТЕРИСТИКИ ===")
    print(f"Минимальное значение: {stats['минимум']}")
    print(f"Максимальное значение: {stats['максимум']}")
    print(f"Сумма чисел: {stats['сумма']}")
    print(f"Среднее арифметическое: {stats['среднее']:.4f}")
    print(f"Медиана: {stats['медиана']:.4f}")
    print(f"Среднеквадратическое отклонение: {stats['среднеквадратическое_отклонение']:.4f}")
    print(f"Дисперсия: {stats['дисперсия']:.4f}")
    print(f"Количество повторяющихся уникальных значений: {stats['количество_уникальных_дубликатов']}")
    print(f"Общее количество повторов: {stats['общее_количество_повторов']}")
    print(f"Размах вариации: {stats['размах']}")
    print("============================================\n")

def save_statistics(stats: Dict, filepath: str = "statistics.txt") -> None:
    """Сохранение статистик в текстовый файл"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Результаты статистического анализа SimpleAnalysis\n")
        f.write("="*50 + "\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

def calculate_by_ranges(series: pd.Series) -> Dict:
    """Расчет суммарных данных по выбранным диапазонам"""
    ranges = {
        "отрицательные_<-5000": series[series < -5000].sum(),
        "отрицательные_-5000_0": series[(series >= -5000) & (series < 0)].sum(),
        "положительные_0_5000": series[(series >= 0) & (series <= 5000)].sum(),
        "положительные_>5000": series[series > 5000].sum(),
    }
    return {k: int(v) for k, v in ranges.items()}

if __name__ == "__main__":
    test = pd.Series([1,2,2,3,4,5])
    s = calculate_statistics(test)
    print_statistics(s)
