"""
Модуль генерации исходных данных
SimpleAnalysis - Ознакомительная практика
Автор: Кузнецов Владимир Александрович
"""
import numpy as np
import pandas as pd
from typing import Tuple

def generate_series(n: int = 1000, low: int = -10000, high: int = 10000, seed: int = 42) -> pd.Series:
    """
    Генерация числовых данных с помощью ГСЧ
    
    Args:
        n: количество чисел
        low: нижняя граница диапазона
        high: верхняя граница диапазона
        seed: зерно для воспроизводимости
    
    Returns:
        pd.Series с сгенерированными данными
    """
    rng = np.random.default_rng(seed)
    # high+1 т.к. upper bound exclusive
    data = rng.integers(low, high + 1, size=n)
    series = pd.Series(data, name="Исходные_значения")
    return series

def save_series(series: pd.Series, filepath: str = "dataset.csv") -> None:
    """Сохранение Series в CSV"""
    series.to_csv(filepath, index_label="index", encoding="utf-8-sig")

if __name__ == "__main__":
    s = generate_series()
    print(f"Сгенерировано: {len(s)} значений")
    print(s.head(10))
    save_series(s)
