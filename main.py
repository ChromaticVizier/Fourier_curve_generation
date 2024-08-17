import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FourierSeriesGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fourier Series Generator - Created by ChromaticVizier and his cat.')
        self.setGeometry(100, 100, 570, 400)

        # 创建中央窗口
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # 创建主布局
        main_layout = QHBoxLayout(centralWidget)

        # 创建左侧输入面板布局
        control_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)

        # 输入框和标签
        self.terms_input = self.create_input_field(control_layout, 'Number of Terms:')
        self.seed_input = self.create_input_field(control_layout, 'Random Seed:')
        self.decay1_input = self.create_input_field(control_layout, 'Decay Factor 1:')
        self.decay2_input = self.create_input_field(control_layout, 'Decay Factor 2:')
        self.step_input = self.create_input_field(control_layout, 'Step Size:')

        # 添加按钮
        self.generate_button = QPushButton('Generate Path', self)
        self.generate_button.clicked.connect(self.plot_fourier_series)
        control_layout.addWidget(self.generate_button)

        # 添加Matplotlib画布
        self.canvas = FigureCanvas(plt.Figure(figsize=(4, 4)))
        main_layout.addWidget(self.canvas)

        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())
        # 禁止最大化按钮
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

    def create_input_field(self, layout, label_text):
        label = QLabel(label_text, self)
        layout.addWidget(label)
        line_edit = QLineEdit(self)
        layout.addWidget(line_edit)
        return line_edit

    def validate_inputs(self, n_terms, seed, decay_factor1, decay_factor2, step_size):
        try:
            n_terms = int(n_terms)
            seed = int(seed)
            decay_factor1 = float(decay_factor1)
            decay_factor2 = float(decay_factor2)
            step_size = float(step_size)

            if n_terms <= 0 or step_size <= 0 or decay_factor1 <= 0 or decay_factor2 <= 0:
                raise ValueError

            return n_terms, seed, decay_factor1, decay_factor2, step_size
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid positive numbers.\nFractions are not allowed, please enter decimals.")
            return None

    def plot_fourier_series(self):
        inputs = self.validate_inputs(
            self.terms_input.text(),
            self.seed_input.text(),
            self.decay1_input.text(),
            self.decay2_input.text(),
            self.step_input.text()
        )

        if inputs is None:
            return

        n_terms, seed, decay_factor1, decay_factor2, step_size = inputs

        # 设置随机种子
        np.random.seed(seed)

        # 生成随机傅里叶系数
        a_cos = np.random.uniform(-1, 1, n_terms)
        b_sin = np.random.uniform(-1, 1, n_terms)

        # 时间变量
        t = np.linspace(0, 2 * np.pi, int(1000 * step_size))

        # 初始化 x(t) 和 y(t)
        x_t = np.zeros_like(t)
        y_t = np.zeros_like(t)

        # 生成路径函数
        for n in range(1, n_terms + 1):
            x_t += (a_cos[n - 1] * np.cos(n * t) + b_sin[n - 1] * np.sin(n * t)) / n**decay_factor1
            y_t += (a_cos[n - 1] * np.sin(n * t) - b_sin[n - 1] * np.cos(n * t)) / n**decay_factor2

        # 绘制路径
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x_t, y_t)
        ax.set_title('Fourier Series Path')
        ax.axis('equal')
        self.canvas.draw()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 适应Windows缩放
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    ex = FourierSeriesGenerator()
    ex.show()
    sys.exit(app.exec_())
