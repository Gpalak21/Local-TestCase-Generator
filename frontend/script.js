const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const systemStatus = document.getElementById('system-status');

// Auto-resize textarea
userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') this.style.height = 'auto';
});

// Send on Enter (shifted for new line)
userInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message
    addMessage(text, 'human');
    userInput.value = '';
    userInput.style.height = 'auto';

    // 2. Add Loading State
    const loadingId = addLoadingMessage();
    systemStatus.innerText = "Generating...";
    systemStatus.style.color = "#fbbf24";

    try {
        // 3. Call Backend
        const response = await fetch('http://localhost:8000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ feature_description: text, model: "llama3.2" }),
        });

        const data = await response.json();

        // 4. Remove Loading
        removeMessage(loadingId);

        if (response.ok) {
            systemStatus.innerText = "System Ready";
            systemStatus.style.color = "white";
            // 5. Render Test Cases
            const formattedHTML = formatTestCases(data.test_cases);
            addMessage(formattedHTML, 'system', true);
        } else {
            throw new Error(data.detail || "Failed to generate");
        }

    } catch (error) {
        removeMessage(loadingId);
        systemStatus.innerText = "Error";
        systemStatus.style.color = "#ef4444";
        addMessage(`❌ Error: ${error.message}`, 'system');
    }
}

function addMessage(content, type, isHTML = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', type);

    // Icon
    const icon = type === 'human' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-bolt"></i>';

    // Content body
    let contentBody = '';
    if (isHTML) {
        contentBody = content;
    } else {
        contentBody = `<p>${content}</p>`;
    }

    msgDiv.innerHTML = `
        <div class="avatar">${icon}</div>
        <div class="content">${contentBody}</div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgDiv.id = 'msg-' + Date.now();
}

function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'system');
    msgDiv.id = id;
    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-bolt"></i></div>
        <div class="content">
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function formatTestCases(testCases) {
    let html = `<p>Here are the generated test cases:</p>`;

    testCases.forEach(tc => {
        html += `
            <div class="test-case-card">
                <h3>
                    <span>${tc.id}: ${tc.title}</span>
                    <span class="badge ${tc.priority}">${tc.priority}</span>
                </h3>
                <p><em>${tc.description}</em></p>
                <div style="margin-top: 10px;">
                    <strong>Steps:</strong>
                    <ol style="margin-left: 20px; font-size: 0.9em; opacity: 0.9;">
                        ${tc.steps.map(s => `<li>${s}</li>`).join('')}
                    </ol>
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #a3bffa;">
                    <strong>Expected:</strong> ${tc.expected_result}
                </div>
            </div>
        `;
    });

    return html;
}
