// 1. Находим нужные элементы на странице один раз
const button = document.getElementById('analyzeBtn');
const textInput = document.getElementById('textInput');
const outputElement = document.getElementById('output');

// 2. Вешаем на кнопку событие "клик". При нажатии сработает функция analyzeText
button.addEventListener('click', analyzeText);

// 3. Главная функция для работы с сервером (async означает, что внутри будет асинхронное ожидание)
async function analyzeText() {
    // Показываем пользователю статус загрузки
    outputElement.innerText = "⏳ Анализирую, подождите...";

    try {
        // Отправляем текст на сервер и ждем (await) ответа
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textInput.value })
        });

        // Достаем из ответа сервера готовые данные (JSON)
        const data = await response.json();

        // Выводим результат на экран в красивом текстовом формате
        outputElement.innerText = JSON.stringify(data, null, 2);

    } catch (error) {
        // Если что-то пошло не так (нет интернета, упал сервер) — показываем ошибку
        outputElement.innerText = "❌ Ошибка запроса! Проверьте бэкенд и базу данных Redis.";
    }
}