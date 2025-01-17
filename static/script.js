document.getElementById('generateBtn').addEventListener('click', async () => {
    const age = document.getElementById('age').value;
    const theme = document.getElementById('theme').value;
    const length = document.getElementById('length').value;

    // Show loading state
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('storyContainer').classList.add('hidden');

    try {
        const response = await fetch('/generate-story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ age, theme, length })
        });

        const data = await response.json();

        // Update story text
        document.getElementById('storyText').textContent = data.story;

        // Update audio
        const audio = document.getElementById('storyAudio');
        audio.src = `data:audio/mp3;base64,${data.audio}`;
        
        // Show story container
        document.getElementById('storyContainer').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('Įvyko klaida generuojant pasaką. Bandykite dar kartą.');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
});