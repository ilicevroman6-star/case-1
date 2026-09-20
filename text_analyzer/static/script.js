// Самая надёжная проверка загрузки страницы
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

function initApp() {
    const button = document.getElementById('analyzeBtn');
    console.log("Поиск кнопки analyzeBtn:", button); // Выведет лог в консоль браузера

    if (button) {
        button.addEventListener('click', analyzeText);
    } else {
        console.error("Кнопка с id='analyzeBtn' не найдена на странице!");
    }
}

function analyzeText() {
    const textInput = document.getElementById('textInput');
    const outputElement = document.getElementById('output');

    if (!textInput || !outputElement) {
        console.error("Элементы ввода или вывода не найдены!");
        return;
    }

    const text = textInput.value;

    // Сразу меняем текст, чтобы увидеть, что клик сработал!
    outputElement.innerText = "⏳ Анализирую, подождите...";

    // Отправляем запрос на сервер
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        outputElement.innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        outputElement.innerText = `❌ Ошибка запроса:\n${error.message}\n\nВозможно, забыли запустить Redis!`;
        console.error('Error:', error);
    });
}
