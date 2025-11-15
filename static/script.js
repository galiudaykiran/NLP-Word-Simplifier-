const API_URL = 'http://localhost:5000/simplify';

const inputText = document.getElementById('inputText');
const simplifyBtn = document.getElementById('simplifyBtn');
const outputSection = document.getElementById('outputSection');
const originalText = document.getElementById('originalText');
const simplifiedText = document.getElementById('simplifiedText');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');
const newTextBtn = document.getElementById('newTextBtn');

simplifyBtn.addEventListener('click', async () => {
    const text = inputText.value.trim();
    
    if (!text) {
        showError('Please enter some text to simplify.');
        return;
    }
    
    // Show loading state
    simplifyBtn.disabled = true;
    simplifyBtn.querySelector('.btn-text').style.display = 'none';
    simplifyBtn.querySelector('.btn-loader').style.display = 'inline';
    outputSection.style.display = 'none';
    errorMessage.style.display = 'none';
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            originalText.textContent = data.original;
            simplifiedText.textContent = data.simplified;
            outputSection.style.display = 'block';
            errorMessage.style.display = 'none';
            
            // Scroll to output
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showError(data.error || 'Failed to simplify text. Please try again.');
        }
    } catch (error) {
        showError('Error connecting to the server. Make sure the backend is running on port 5000.');
        console.error('Error:', error);
    } finally {
        // Reset button state
        simplifyBtn.disabled = false;
        simplifyBtn.querySelector('.btn-text').style.display = 'inline';
        simplifyBtn.querySelector('.btn-loader').style.display = 'none';
    }
});

copyBtn.addEventListener('click', () => {
    const text = simplifiedText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copyBtn.textContent = '📋 Copy Simplified Text';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
});

newTextBtn.addEventListener('click', () => {
    inputText.value = '';
    outputSection.style.display = 'none';
    errorMessage.style.display = 'none';
    inputText.focus();
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    outputSection.style.display = 'none';
}

// Allow Enter key to submit (Ctrl+Enter or Cmd+Enter)
inputText.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        simplifyBtn.click();
    }
});

