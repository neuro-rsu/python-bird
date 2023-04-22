"""Модуль содержит элементы приложения, обрабатывающего данные."""

import tkinter as tk
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scripts.gui.db_forms import DataLoadForm
from scripts.stat.output_chart import OutputChart
from scripts.stat.data_analysis import DataAnalyst


def main():
    """Запускает приложение для обработки данных."""
    # Окно для получения данных из БД
    form = DataLoadForm()
    form.mainloop()

    data = form.return_data
    if not data:
        return

    # График и анализ данных
    chart = OutputChart(data)
    x, y1, y2 = chart.get_chart_points()

    analyst = DataAnalyst(data)

    # Вывод результата
    data_form = DataForms(
        chart.create_chart(x, y1, y2), analyst.create_hist(), analyst.get_describe_stat()
    )
    data_form.mainloop()


class DataForms(tk.Tk):
    """Генерирует окно приложения для обработки данных."""

    def __init__(self, chart1, chart2, describe_stat):
        super().__init__()
        self.stat = describe_stat

        # Создание Tk Canvas для каждого из графиков
        canvas1 = FigureCanvasTkAgg(chart1, master=self)
        canvas1.draw()
        canvas2 = FigureCanvasTkAgg(chart2, master=self)
        canvas2.draw()

        # Добавляет Canvas в окно Tk
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Меню для отображения статистики
        stat_menu = tk.Menu(self)
        stat_menu.add_command(label="Показать статистику", command=self.show_stat)
        self.config(menu=stat_menu)

    def show_stat(self):
        """Вызывает окно со статистикой."""
        StatInfo(self, self.stat)


class StatInfo(tk.Toplevel):
    """Класс для отображения статистики обучения."""

    def __init__(self, parent, data):
        super().__init__(parent)
        self.resizable(False, False)

        stat_field = tk.Text(self)
        stat_field.delete(1.0, tk.END)
        stat_field.insert(1.0, data)
        stat_field.pack(fill=tk.BOTH, expand=True)
        stat_field["state"] = tk.DISABLED
