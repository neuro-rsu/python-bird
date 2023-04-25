"""Модуль содержит элементы приложения, обрабатывающего данные."""

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config as conf
from scripts.gui.base_form import BaseForm
from scripts.gui.db_forms import DataLoadForm
from scripts.data_processing.output_chart import OutputChart
from scripts.data_processing.data_analysis import DataAnalyst


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
    data_form = StatApp(
        chart.create_chart(x, y1, y2), analyst.create_hist(),
        analyst.get_describe_stat().to_string()
    )
    data_form.mainloop()


class StatApp(BaseForm):
    """Генерирует окно приложения для обработки данных."""

    def __init__(self, chart1, chart2, describe_stat):
        super().__init__()
        self.stat = describe_stat
        self.chart1 = chart1
        self.chart2 = chart2
        self.create_elements()
        self.set_window_params("Статистика", conf.ICONS["analysis"], True)

    def create_elements(self):
        # Создание Tk Canvas для каждого из графиков
        canvas1 = FigureCanvasTkAgg(self.chart1, master=self)
        canvas1.draw()
        canvas2 = FigureCanvasTkAgg(self.chart2, master=self)
        canvas2.draw()

        # Добавляет Canvas в окно Tk
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Меню для отображения статистических характеристик
        stat_menu = tk.Menu(self)
        stat_menu.add_command(label="Показать статистику", command=self.show_stat)
        self.config(menu=stat_menu)

    def show_stat(self):
        """Вызывает окно со статистическими характеристиками."""
        StatInfo(self, self.stat)


class StatInfo(tk.Toplevel):
    """Создает диалог для отображения описательной статистики"""

    def __init__(self, parent, data):
        super().__init__(parent)
        # Настройка параметров
        self.title("Описательная статистика")
        self.resizable(False, False)
        # Позволяет установить иконку в формате PNG
        icon = tk.PhotoImage(file=conf.ICONS["stat"])
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Генерация элементов
        stat_field = tk.Text(self)
        stat_field.delete(1.0, tk.END)
        stat_field.insert(1.0, data)
        stat_field.pack(fill=tk.BOTH, expand=True)
        stat_field["state"] = tk.DISABLED
