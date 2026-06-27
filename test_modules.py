"""
Модуль тестирования SimpleAnalysis
Покрытие: data_generator, data_cleaner, analyzer, visualizer
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys

# Добавляем путь для импорта
sys.path.insert(0, os.path.dirname(__file__))

from data_generator import generate_series
from data_cleaner import clean_series, math_round_to_hundreds
from analyzer import calculate_statistics, calculate_by_ranges
from visualizer import create_dataframe, plot_linear, plot_histogram, plot_sorted_combined

class TestDataGenerator(unittest.TestCase):
    """Тестирование модуля генерации данных"""
    
    def test_generate_series_length(self):
        """Проверка количества генерируемых элементов"""
        series = generate_series(n=1000)
        self.assertEqual(len(series), 1000, "Должно генерироваться 1000 элементов")
    
    def test_generate_series_range(self):
        """Проверка диапазона значений"""
        series = generate_series(n=500, low=-10000, high=10000, seed=123)
        self.assertTrue(series.min() >= -10000, "Минимум не должен быть меньше -10000")
        self.assertTrue(series.max() <= 10000, "Максимум не должен превышать 10000")
    
    def test_generate_series_reproducibility(self):
        """Проверка воспроизводимости при одинаковом seed"""
        s1 = generate_series(n=100, seed=42)
        s2 = generate_series(n=100, seed=42)
        pd.testing.assert_series_equal(s1, s2)

class TestDataCleaner(unittest.TestCase):
    """Тестирование модуля очистки данных"""
    
    def test_math_round_to_hundreds_positive(self):
        self.assertEqual(math_round_to_hundreds(1250), 1300)
        self.assertEqual(math_round_to_hundreds(1249), 1200)
        self.assertEqual(math_round_to_hundreds(1355), 1400)
    
    def test_math_round_to_hundreds_negative(self):
        self.assertEqual(math_round_to_hundreds(-1250), -1300)
        self.assertEqual(math_round_to_hundreds(-1249), -1200)
        self.assertEqual(math_round_to_hundreds(-3781), -3800)
    
    def test_clean_series_nan(self):
        """Очистка NaN значений"""
        dirty = pd.Series([1, 2, np.nan, 4, None, 6])
        cleaned, report = clean_series(dirty, low=-10000, high=10000)
        self.assertEqual(report["удалено_NaN"], 2)
        self.assertFalse(cleaned.isna().any())
    
    def test_clean_series_out_of_range(self):
        """Фильтрация выхода за диапазон"""
        dirty = pd.Series([100, 50000, -20000, 500, 9999])
        cleaned, report = clean_series(dirty, low=-10000, high=10000)
        self.assertEqual(report["удалено_вне_диапазона"], 2)
        self.assertTrue((cleaned >= -10000).all() and (cleaned <= 10000).all())
    
    def test_clean_series_duplicates_count(self):
        """Подсчет дубликатов"""
        data = pd.Series([1,2,2,3,3,3,4])
        cleaned, report = clean_series(data)
        self.assertEqual(report["найдено_дубликатов"], 3)

class TestAnalyzer(unittest.TestCase):
    """Тестирование модуля анализа"""
    
    def test_calculate_statistics_basic(self):
        series = pd.Series([1,2,3,4,5])
        stats = calculate_statistics(series)
        self.assertEqual(stats["минимум"], 1)
        self.assertEqual(stats["максимум"], 5)
        self.assertEqual(stats["сумма"], 15)
        self.assertAlmostEqual(stats["среднее"], 3.0)
        self.assertAlmostEqual(stats["медиана"], 3.0)
    
    def test_calculate_statistics_duplicates(self):
        series = pd.Series([1,2,2,3,3,3])
        stats = calculate_statistics(series)
        self.assertEqual(stats["количество_уникальных_дубликатов"], 2)  # 2 и 3
        self.assertEqual(stats["общее_количество_повторов"], 3)  # 1 повтор двойки + 2 повтора тройки
    
    def test_calculate_by_ranges(self):
        series = pd.Series([-6000, -1000, 1000, 6000])
        ranges = calculate_by_ranges(series)
        self.assertEqual(ranges["отрицательные_<-5000"], -6000)
        self.assertEqual(ranges["положительные_>5000"], 6000)

class TestVisualizer(unittest.TestCase):
    """Тестирование модуля визуализации"""
    
    def test_create_dataframe_structure(self):
        series = pd.Series([3,1,2])
        df = create_dataframe(series)
        self.assertEqual(list(df.columns), ["Исходные_значения", "Сортировка_по_возрастанию", "Сортировка_по_убыванию"])
        self.assertEqual(len(df), 3)
        # Проверка сортировки
        self.assertTrue((df["Сортировка_по_возрастанию"].values == np.array([1,2,3])).all())
        self.assertTrue((df["Сортировка_по_убыванию"].values == np.array([3,2,1])).all())
    
    def test_plot_files_created(self):
        """Проверка создания файлов графиков"""
        series = generate_series(n=50, seed=1)
        df = create_dataframe(series)
        
        f1 = plot_linear(series, "test_linear.png")
        f2 = plot_histogram(series, "test_hist.png")
        f3 = plot_sorted_combined(df, "test_sorted.png")
        
        self.assertTrue(os.path.exists(f1))
        self.assertTrue(os.path.exists(f2))
        self.assertTrue(os.path.exists(f3))
        
        # Очистка тестовых файлов
        for f in [f1, f2, f3]:
            if os.path.exists(f):
                os.remove(f)

def run_tests_verbose():
    """Запуск тестов с подробным выводом"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("ОТЧЕТ О ТЕСТИРОВАНИИ SimpleAnalysis")
    print("="*60)
    print(f"Всего тестов запущено: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Пропущено: {len(result.skipped)}")
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
    print(f"Процент успешности: {success_rate:.1f}%")
    print("="*60)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests_verbose()
    sys.exit(0 if success else 1)
