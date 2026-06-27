"""
Модуль визуализации данных
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from data_cleaner import math_round_to_hundreds

# Настройка кириллицы
plt.rcParams["font.family"] = ["DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

def plot_linear(series: pd.Series, filepath: str = "graph_linear.png"):
    """Построение линейного графика исходных данных"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(series.index, series.values, linewidth=0.8, color="#2980B9", alpha=0.7)
    ax.set_title("Линейный график исходных данных SimpleAnalysis", fontsize=14)
    ax.set_xlabel("Индекс элемента", fontsize=11)
    ax.set_ylabel("Значение", fontsize=11)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.axhline(y=0, color="red", linestyle="--", linewidth=0.7, alpha=0.5)
    fig.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    return filepath

def plot_histogram(series: pd.Series, filepath: str = "graph_histogram.png"):
    """Гистограмма с округлением до сотен"""
    rounded = series.apply(math_round_to_hundreds)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(rounded, bins=40, color="#27AE60", edgecolor="black", alpha=0.8)
    ax.set_title("Гистограмма распределения (округление до сотен)", fontsize=14)
    ax.set_xlabel("Значение (округлено до сотен)", fontsize=11)
    ax.set_ylabel("Частота", fontsize=11)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    return filepath

def plot_sorted_combined(df: pd.DataFrame, filepath: str = "graph_sorted.png"):
    """Совмещенный график сортированных данных"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Сортировка_по_возрастанию"], 
            linewidth=1.2, color="#27AE60", label="По возрастанию")
    ax.plot(df.index, df["Сортировка_по_убыванию"],
            linewidth=1.2, color="#8E44AD", label="По убыванию")
    ax.set_title("Совмещённые графики отсортированных значений", fontsize=14)
    ax.set_xlabel("Индекс элемента", fontsize=11)
    ax.set_ylabel("Значение", fontsize=11)
    ax.axhline(y=0, color="grey", linestyle="--", linewidth=0.7)
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    return filepath

def create_dataframe(series: pd.Series) -> pd.DataFrame:
    """Формирование DataFrame с сортировкой"""
    df = pd.DataFrame({
        "Исходные_значения": series.values,
        "Сортировка_по_возрастанию": np.sort(series.values),
        "Сортировка_по_убыванию": np.sort(series.values)[::-1].copy()
    })
    return df
