document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `grant_type=password&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
            });
            
            if (response.ok) {
                // 在这里可以进行其他操作，例如页面跳转等
                console.log('Login successful');
                window.location.href = '/chat'
            } else {
                // 处理登录失败的情况
                const pwdErrorEle = document.getElementById('pwd-error')
                pwdErrorEle.textContent = '用户名或密码错误'

                console.error('Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    });
});
