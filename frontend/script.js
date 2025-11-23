// 全局变量
let currentUser = null;

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 检查URL参数确定当前页面
    const path = window.location.pathname.split('/').pop();
    
    // 初始化页面
    if (path === 'login.html') {
        initLoginPage();
    } else if (path === 'register.html') {
        initRegisterPage();
    } else if (path === 'chat.html') {
        initChatPage();
    }
});

// 初始化登录页面
function initLoginPage() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            let isValid = true;
            
            // 重置错误信息
            document.getElementById('username-error').textContent = '';
            document.getElementById('password-error').textContent = '';
            
            // 验证用户名
            if (!username) {
                document.getElementById('username-error').textContent = '请输入用户名';
                isValid = false;
            }
            
            // 验证密码
            if (!password) {
                document.getElementById('password-error').textContent = '请输入密码';
                isValid = false;
            }
            
            if (isValid) {
                // 模拟登录成功
                currentUser = username;
                localStorage.setItem('currentUser', username);
                window.location.href = 'chat.html';
            }
        });
    }
}

// 初始化注册页面
function initRegisterPage() {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('reg-username').value.trim();
            const password = document.getElementById('reg-password').value.trim();
            const confirmPassword = document.getElementById('reg-confirm').value.trim();
            let isValid = true;
            
            // 重置错误信息
            document.getElementById('reg-username-error').textContent = '';
            document.getElementById('reg-password-error').textContent = '';
            document.getElementById('reg-confirm-error').textContent = '';
            
            // 验证用户名
            if (!username) {
                document.getElementById('reg-username-error').textContent = '请输入用户名';
                isValid = false;
            } else if (username.length < 3) {
                document.getElementById('reg-username-error').textContent = '用户名至少3个字符';
                isValid = false;
            }
            
            // 验证密码
            if (!password) {
                document.getElementById('reg-password-error').textContent = '请输入密码';
                isValid = false;
            } else if (password.length < 6) {
                document.getElementById('reg-password-error').textContent = '密码至少6个字符';
                isValid = false;
            }
            
            // 验证确认密码
            if (!confirmPassword) {
                document.getElementById('reg-confirm-error').textContent = '请确认密码';
                isValid = false;
            } else if (password !== confirmPassword) {
                document.getElementById('reg-confirm-error').textContent = '两次输入的密码不一致';
                isValid = false;
            }
            
            if (isValid) {
                // 模拟注册成功
                alert('注册成功！请登录您的账户');
                window.location.href = 'login.html';
            }
        });
    }
}

// 初始化聊天页面
function initChatPage() {
    // 检查用户是否登录
    const savedUser = localStorage.getItem('currentUser');
    if (!savedUser) {
        window.location.href = 'login.html';
        return;
    }
    
    currentUser = savedUser;
    document.getElementById('current-user').textContent = currentUser;
    
    // 发送按钮事件
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const messageContainer = document.getElementById('message-container');
    
    if (sendBtn && userInput && messageContainer) {
        // 发送消息函数
        function sendMessage() {
            const message = userInput.value.trim();
            if (message) {
                // 添加用户消息
                addMessage(message, 'user');
                
                // 清空输入框
                userInput.value = '';
                
                // 模拟机器人回复（延迟）
                setTimeout(() => {
                    const botResponse = getBotResponse(message);
                    addMessage(botResponse, 'bot');
                }, 1000);
            }
        }
        
        // 发送按钮点击事件
        sendBtn.addEventListener('click', sendMessage);
        
        // 输入框回车事件
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // 自动调整输入框高度
        userInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
    
    // 退出按钮事件
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('currentUser');
            window.location.href = 'index.html';
        });
    }
}

// 添加消息到聊天窗口
function addMessage(content, sender) {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;
    
    const now = new Date();
    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = sender === 'bot' ? '🤖' : '👤';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    
    const messagePara = document.createElement('p');
    messagePara.textContent = content;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'time';
    timeSpan.textContent = timeString;
    
    contentDiv.appendChild(messagePara);
    contentDiv.appendChild(timeSpan);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    messageContainer.appendChild(messageDiv);
    
    // 滚动到底部
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// 获取机器人回复（简单模拟）
function getBotResponse(userMessage) {
    const lowerMsg = userMessage.toLowerCase();
    
    if (lowerMsg.includes('你好') || lowerMsg.includes('hello')) {
        return '您好！很高兴为您服务。请问有什么可以帮您的？';
    } else if (lowerMsg.includes('谢谢') || lowerMsg.includes('感谢')) {
        return '不客气！随时为您效劳。';
    } else if (lowerMsg.includes('订单') || lowerMsg.includes('购买')) {
        return '您可以访问我们的订单页面查看详情。需要我帮您查询特定订单吗？';
    } else if (lowerMsg.includes('退货') || lowerMsg.includes('退款')) {
        return '我们的退货政策允许在收到商品后30天内申请退货。您需要帮助处理退货吗？';
    } else if (lowerMsg.includes('联系') || lowerMsg.includes('电话')) {
        return '客服热线：400-123-4567（工作日9:00-18:00）';
    } else if (lowerMsg.includes('再见') || lowerMsg.includes('拜拜')) {
        return '再见！感谢您使用我们的服务，祝您有美好的一天！';
    } else {
        const responses = [
            '我明白了，还有其他问题吗？',
            '这是一个很好的问题，让我为您查找相关信息...',
            '根据您的情况，我建议...',
            '我注意到您提到了几个关键点，让我们逐一分析...',
            '感谢您的耐心等待，我已找到解决方案...'
        ];
        return responses[Math.floor(Math.random() * responses.length)];
    }
}