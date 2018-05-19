# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# от -5 до 2 сделать 100 точек.Чем больше точек, тем точнее график.
x = np.linspace(-5, 2, 100)
# y1...y4 - линии одного графика, для каждой линии свой набор точек.
y1 = x**3 + 5*x**2 + 10
y2 = 3*x**2 + 10*x
y3 = 6*x + 10
y4 = 5*x**2 + 10

# будет 1 график, на нем 4 линии:
fig, ax = plt.subplots()
# функция y1(x), синий, надпись y(x)
ax.plot(x, y1, color="blue", label="голубая линия")
# функция y2(x), красный, надпись y'(x)
ax.plot(x, y2, color="red", label="красная линия")
# функция y3(x), зеленый, надпись y''(x)
ax.plot(x, y3, color="green", label="зелёная линия")
# функция y3(x), зеленый, надпись y''(x)
ax.plot(x, y4, color="black", label="черная линия")
# подпись у горизонтальной оси х
ax.set_xlabel("x")
# подпись у вертикальной оси y
ax.set_ylabel("y")
# показывать условные обозначения
ax.legend()

'''
Тут нужно сделать выбор в пользу одного действия. Либо вы показываете на окне 
векторный график, либо записываете график в картинку png
'''
#показать рисунок
plt.show()
# сохранить в файл 1.png
#fig.savefig('1.png')