import streamlit as st
import graphviz

# Настройка страницы
st.set_page_config(page_title="Алгоритм реабилитации ЭД", layout="wide")

st.title("Алгоритм комплексной реабилитации пациентов с ангидротической эктодермальной дисплазией")
st.markdown("---")

# Боковая панель для ввода данных (Интерактивная часть)
st.sidebar.header("Диагностика и Осмотр")

# Этапы, которые проходят все (Линейная часть)
st.sidebar.markdown("**Этап 1:** Хирургическая санация полости рта")
st.sidebar.markdown("**Этап 2:** Реконструктивная костно-пластическая операция")
st.sidebar.markdown("**Этап 3:** Дентальная имплантация")

st.sidebar.markdown("---")

# Ветвление 1
metal_showing = st.sidebar.radio(
    "Наблюдается ли просвечивание металла через слизистую (дефицит мягких тканей)?",
    ("Нет", "Да")
)

# Ветвление 2
jaw_deformation = st.sidebar.radio(
    "Имеется ли сочетанная деформация челюстей (мезиальная окклюзия, III класс)?",
    ("Нет", "Да")
)

# --- Визуализация графа ---
st.subheader("Визуализация клинического пути")

# Создаем граф
graph = graphviz.Digraph()
graph.attr(rankdir='TB') # Сверху вниз

# Стили узлов
default_style = {'shape': 'box', 'style': 'filled', 'fillcolor': '#e1f5fe', 'color': '#0277bd', 'fontname': 'Arial'}
decision_style = {'shape': 'diamond', 'style': 'filled', 'fillcolor': '#fff9c4', 'color': '#fbc02d', 'fontname': 'Arial'}
action_style = {'shape': 'box', 'style': 'filled', 'fillcolor': '#ffe0b2', 'color': '#ef6c00', 'fontname': 'Arial'}

# Добавляем узлы (Nodes)
graph.node('Start', 'Пациент с ангидротической\nэктодермальной дисплазией', **default_style)
graph.node('Step1', 'Хирургическая санация:\nудаление временных/нежизнеспособных зубов', **default_style)
graph.node('Step2', 'Реконструктивная костно-пластическая операция\n(теменные аутотрансплантаты)', **default_style)
graph.node('Step3', 'Дентальная имплантация', **default_style)

# Узел решения 1
graph.node('Decision1', 'Просвечивание металла\nчерез слизистую?', **decision_style)

# Узел действия по ветке Да
if metal_showing == "Да":
    graph.node('Action1', 'Установка формирователей десны\nс коррекцией мягких тканей', **action_style, penwidth='2.0')
else:
    graph.node('Action1', 'Установка формирователей десны\nс коррекцией мягких тканей', **action_style)

# Узел решения 2
graph.node('Decision2', 'Сочетанная деформация челюстей\n(III класс по Энглю)?', **decision_style)

# Узел действия по ветке Да
if jaw_deformation == "Да":
    graph.node('Action2', 'Ортогнатическая операция', **action_style, penwidth='2.0')
else:
    graph.node('Action2', 'Ортогнатическая операция', **action_style)

graph.node('Final', 'Изготовление и установка\nортопедической конструкции', **default_style, fillcolor='#c8e6c9', color='#2e7d32')

# --- Связи (Edges) ---
# Базовый путь
graph.edge('Start', 'Step1')
graph.edge('Step1', 'Step2')
graph.edge('Step2', 'Step3')
graph.edge('Step3', 'Decision1')

# Логика первого ветвления
if metal_showing == "Да":
    graph.edge('Decision1', 'Action1', label='Да', color='red', penwidth='2.0')
    graph.edge('Action1', 'Decision2', color='red', penwidth='2.0')
    graph.edge('Decision1', 'Decision2', label='Нет', style='dashed', color='gray')
else:
    graph.edge('Decision1', 'Action1', label='Да', style='dashed', color='gray')
    graph.edge('Action1', 'Decision2', style='dashed', color='gray')
    graph.edge('Decision1', 'Decision2', label='Нет', color='green', penwidth='2.0')

# Логика второго ветвления
if jaw_deformation == "Да":
    graph.edge('Decision2', 'Action2', label='Да', color='red', penwidth='2.0')
    graph.edge('Action2', 'Final', color='red', penwidth='2.0')
    graph.edge('Decision2', 'Final', label='Нет', style='dashed', color='gray')
else:
    graph.edge('Decision2', 'Action2', label='Да', style='dashed', color='gray')
    graph.edge('Action2', 'Final', style='dashed', color='gray')
    graph.edge('Decision2', 'Final', label='Нет', color='green', penwidth='2.0')

# Отображаем граф
st.graphviz_chart(graph)

# --- Итоговое заключение ---
st.markdown("### Итоговый план лечения для данного пациента:")
treatment_plan = [
    "1. Хирургическая санация полости рта.",
    "2. Реконструктивная костно-пластическая операция (синуслифтинг + аутотрансплантаты).",
    "3. Дентальная имплантация."
]

if metal_showing == "Да":
    treatment_plan.append("4. **Установка формирователей десны с коррекцией мягких тканей.**")
else:
    treatment_plan.append("4. (Этап коррекции мягких тканей не требуется).")

if jaw_deformation == "Да":
    treatment_plan.append("5. **Ортогнатическая операция.**")
else:
    treatment_plan.append("5. (Ортогнатическая операция не требуется).")

treatment_plan.append("6. Изготовление и установка ортопедической конструкции.")

for item in treatment_plan:
    st.write(item)
