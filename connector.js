document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const query = formData.get('query');

        try {
            const response = await fetch('/search', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    function displayResults(data) {
        resultsDiv.innerHTML = `
            <p>Time taken: ${data.time_taken}</p>
            <p>Query: ${data.query}</p>
            <p>Answer: ${data.answer}</p>
            <p>Score: ${data.score}</p>
            <p>Extra Info: ${data.extra_info}</p>
        `;
    }
});
