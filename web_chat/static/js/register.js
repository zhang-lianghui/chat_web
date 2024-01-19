document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // 进行密码匹配和其他验证
        if (password !== confirmPassword) {
            const pwdConsistencyEle = document.getElementById('pwd-consistency');
            pwdConsistencyEle.textContent = '两次输入的密码不匹配';
            return;
        }

        console.log(username);
        console.log(password);

        // 发送注册请求到后端，处理注册逻辑
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (response.ok) {
                // 注册成功，可以进行页面跳转或其他操作
                console.log('Registration successful');
            } else {
                // 处理注册失败的情况
                const errorData = await response.json();
                console.error('Registration failed:', errorData.detail);
                const errorMessageElement = document.getElementById('error-message');
                errorMessageElement.textContent = errorData.detail;
            }
        } catch (error) {
            console.error('Error during registration:', error);
        }
    });
});

