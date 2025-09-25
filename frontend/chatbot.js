// Classic Chatbot Widget for Gemini AI
// Include <script src="chatbot.js"></script> in any page

(function() {
    // Create chatbot container
    const chatbot = document.createElement('div');
    chatbot.id = 'chatbot-widget';
    chatbot.innerHTML = `
        <div id="chatbot-toggle" style="position:fixed;bottom:30px;right:30px;z-index:9999;">
            <button id="chatbot-open" style="background:#9b5de5;color:#fff;border:none;border-radius:50%;width:60px;height:60px;font-size:2em;box-shadow:0 2px 8px rgba(0,0,0,0.2);cursor:pointer;">💬</button>
        </div>
        <div id="chatbot-box" style="display:none;position:fixed;bottom:100px;right:30px;width:350px;max-width:95vw;height:480px;background:#fff;border-radius:18px;box-shadow:0 8px 32px rgba(0,0,0,0.18);z-index:9999;overflow:hidden;flex-direction:column;">
            <div style="background:#9b5de5;color:#fff;padding:16px 20px;font-size:1.2em;font-weight:bold;display:flex;align-items:center;justify-content:space-between;">
                <span>Legal Advisor AI</span>
                <button id="chatbot-close" style="background:none;border:none;color:#fff;font-size:1.3em;cursor:pointer;">×</button>
            </div>
            <div id="chatbot-messages" style="flex:1;overflow-y:auto;padding:18px 16px 8px 16px;background:#f7f6fa;"></div>
            <form id="chatbot-form" style="display:flex;flex-direction:column;padding:12px 16px 16px 16px;background:#fff;">
                <textarea id="chatbot-input" rows="2" placeholder="Type your question..." style="resize:none;padding:10px;border-radius:8px;border:1px solid #ccc;font-size:1em;margin-bottom:8px;"></textarea>
                <input type="file" id="chatbot-image" accept="image/*" style="margin-bottom:8px;">
                <button type="submit" style="background:#9b5de5;color:#fff;border:none;border-radius:8px;padding:10px 0;font-size:1.1em;cursor:pointer;font-weight:bold;">Send</button>
            </form>
        </div>
    `;
    document.body.appendChild(chatbot);

    // Widget logic
    const openBtn = document.getElementById('chatbot-open');
    const closeBtn = document.getElementById('chatbot-close');
    const box = document.getElementById('chatbot-box');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const imageInput = document.getElementById('chatbot-image');
    const messages = document.getElementById('chatbot-messages');

    openBtn.onclick = () => { box.style.display = 'flex'; };
    closeBtn.onclick = () => { box.style.display = 'none'; };

    function addMessage(text, sender, imageUrl) {
        let cleanText = text.replace(/\*\*|--|__|\*|\n|\r/g, '').replace(/\s+/g, ' ').trim();
        let html = `<div style="margin-bottom:12px;display:flex;${sender==='user'?'justify-content:flex-end':'justify-content:flex-start'};">
            <div style="max-width:80%;background:${sender==='user'?'#e0e7ff':'#fff'};color:#333;padding:10px 14px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.07);font-size:1em;">
                ${imageUrl ? `<img src="${imageUrl}" style="max-width:120px;border-radius:8px;margin-bottom:8px;display:block;">` : ''}
                ${cleanText}
            </div>
        </div>`;
        messages.innerHTML += html;
        messages.scrollTop = messages.scrollHeight;
    }

    form.onsubmit = function(e) {
        e.preventDefault();
        const question = input.value.trim();
        const imageFile = imageInput.files[0];
        if (!question && !imageFile) return;
        addMessage(question, 'user', imageFile ? URL.createObjectURL(imageFile) : null);
        input.value = '';
        imageInput.value = '';
        // Prepare request
        let formData = new FormData();
        formData.append('complaintType', question);
        if (imageFile) formData.append('image', imageFile);
        fetch('http://localhost:5000/api/gemini/suggest', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            let response = data.suggestions ? data.suggestions.join(' ') : (data.error || 'AI could not generate advice.');
            addMessage(response, 'ai');
        })
        .catch(() => {
            addMessage('Error contacting AI. Try again later.', 'ai');
        });
    };
})();
