def get_index_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Toxicity Analysis Tester</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .loading {
                opacity: 0.5;
                pointer-events: none;
            }
        </style>
    </head>
    <body class="bg-gray-50">
        <div class="max-w-4xl mx-auto p-8">
            <h1 class="text-3xl font-bold mb-8">Toxicity Analysis Tester</h1>
            
            <div class="mb-6">
                <textarea
                    id="input-text"
                    placeholder="Enter text to analyze..."
                    class="w-full h-32 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                ></textarea>
            </div>

            <button
                id="analyze-btn"
                class="mb-8 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
            >
                Analyze
            </button>

            <div id="error" class="hidden mb-6 p-4 bg-red-100 rounded-lg text-red-700"></div>

            <div id="results" class="hidden">
                <h2 class="text-xl font-semibold mb-4">Analysis Results</h2>
                <div class="grid grid-cols-2 gap-4" id="results-grid"></div>
            </div>
        </div>

        <script>
            const analyzeBtn = document.getElementById('analyze-btn');
            const inputText = document.getElementById('input-text');
            const errorDiv = document.getElementById('error');
            const resultsDiv = document.getElementById('results');
            const resultsGrid = document.getElementById('results-grid');

            function getScoreColor(score) {
                if (score < 0.3) return 'bg-green-100';
                if (score < 0.7) return 'bg-yellow-100';
                return 'bg-red-100';
            }

            async function analyzeToxicity() {
                const text = inputText.value.trim();
                if (!text) return;

                // Reset UI
                errorDiv.classList.add('hidden');
                resultsDiv.classList.add('hidden');
                analyzeBtn.disabled = true;
                analyzeBtn.textContent = 'Analyzing...';

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            texts: [text],
                            batch_size: 1
                        })
                    });

                    if (!response.ok) throw new Error('Analysis failed');
                    
                    const data = await response.json();
                    const results = data.results[0];

                    // Clear previous results
                    resultsGrid.innerHTML = '';

                    // Add new results
                    Object.entries(results).forEach(([key, value]) => {
                        const resultEl = document.createElement('div');
                        resultEl.className = `p-4 rounded-lg ${getScoreColor(value)}`;
                        resultEl.innerHTML = `
                            <div class="font-medium capitalize">${key.replace(/_/g, ' ')}</div>
                            <div class="text-2xl font-bold">${(value * 100).toFixed(1)}%</div>
                        `;
                        resultsGrid.appendChild(resultEl);
                    });

                    resultsDiv.classList.remove('hidden');
                } catch (err) {
                    errorDiv.textContent = 'Error analyzing text. Please try again.';
                    errorDiv.classList.remove('hidden');
                } finally {
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = 'Analyze';
                }
            }

            analyzeBtn.addEventListener('click', analyzeToxicity);
        </script>
    </body>
    </html>
    """