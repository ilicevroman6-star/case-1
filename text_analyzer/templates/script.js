function analyzeText() {
    const text = document.getElementById('textInput').value;

    // 1. Отправляем запрос и ждем первый ответ (статус соединения)
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    // 2. Когда сервер ответил, превращаем данные в JSON
    .then(response => response.json())

    // 3. Когда JSON готов, выводим его на страницу
    .then(data => {
        document.getElementById('output').innerText = JSON.stringify(data);
    });
}
