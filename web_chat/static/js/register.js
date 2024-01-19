document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const username = formData.get('username');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm-password');

        // 进行密码匹配和其他验证
        if (password !== confirmPassword) {
            alert('两次密码不匹配');
            return;
        }

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
                console.error('Registration failed');
            }
        } catch (error) {
            console.error('Error during registration:', error);
        }
    });
});
