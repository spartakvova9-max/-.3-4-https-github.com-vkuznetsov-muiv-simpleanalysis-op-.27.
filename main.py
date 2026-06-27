"""
SimpleAnalysis - Главный модуль
Ознакомительная практика
Кузнецов Владимир Александрович
Направление: 09.03.03 Прикладная информатика
МУИВ, 2026

Репозиторий: https://github.com/vkuznetsov-muiv/simpleanalysis-op
"""
import pandas as pd
from data_generator import generate_series, save_series
from data_cleaner import clean_with_logging, clean_series
from analyzer import calculate_statistics, print_statistics, save_statistics, calculate_by_ranges
from visualizer import plot_linear, plot_histogram, plot_sorted_combined, create_dataframe

def main():
    print("="*60)
    print("SimpleAnalysis - Анализ числовых данных")
    print("Ознакомительная практика МУИВ")
    print("Кузнецов В.А., 09.03.03 Прикладная информатика")
    print("="*60)
    
    # Этап 1: Генерация данных
    print("\n[ЭТАП 1] Генерация Dataset...")
    series_data = generate_series(n=1000, low=-10000, high=10000, seed=42)
    print(f"Сгенерировано {len(series_data)} значений в диапазоне [-10000; 10000]")
    save_series(series_data, "dataset_raw.csv")
    
    # Этап 2: Очистка данных от цифрового мусора
    print("\n[ЭТАП 2] Очистка данных от цифрового мусора...")
    cleaned_series, clean_report = clean_series(series_data)
    print(f"Очистка завершена. Удалено записей: {clean_report['удалено_всего']}")
    for k, v in clean_report.items():
        print(f"  {k}: {v}")
    
    # Этап 3: Количественный анализ
    print("\n[ЭТАП 3] Расчет стандартных числовых характеристик...")
    stats = calculate_statistics(cleaned_series)
    print_statistics(stats)
    save_statistics(stats, "statistics_output.txt")
    
    # Дополнительный анализ по диапазонам
    range_sums = calculate_by_ranges(cleaned_series)
    print("Суммарные данные по диапазонам:")
    for key, value in range_sums.items():
        print(f"  {key}: {value}")
    
    # Этап 4: Визуализация
    print("\n[ЭТАП 4] Визуализация данных...")
    f1 = plot_linear(cleaned_series, "graph_linear.png")
    print(f"  Линейный график сохранен: {f1}")
    
    f2 = plot_histogram(cleaned_series, "graph_histogram.png")
    print(f"  Гистограмма сохранена: {f2}")
    
    # Этап 5: Формирование DataFrame
    print("\n[ЭТАП 5] Формирование DataFrame с сортировкой...")
    df = create_dataframe(cleaned_series)
    print(df.head(10).to_string())
    print(f"\nФорма DataFrame: {df.shape[0]} строк x {df.shape[1]} столбцов")
    df.to_csv("analysis_results.csv", index=False, encoding="utf-8-sig")
    print("  DataFrame экспортирован: analysis_results.csv")
    
    # Этап 6: Визуализация промежуточного анализа
    print("\n[ЭТАП 6] Визуализация отсортированных данных...")
    f3 = plot_sorted_combined(df, "graph_sorted.png")
    print(f"  Совмещенный график сохранен: {f3}")
    
    print("\n" + "="*60)
    print("АНАЛИЗ ЗАВЕРШЕН УСПЕШНО")
    print("Все результаты сохранены в рабочей директории")
    print("="*60)

if __name__ == "__main__":
    main()
