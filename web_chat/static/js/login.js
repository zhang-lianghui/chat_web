document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const username = formData.get('username');
        const password = formData.get('password');

        try {
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `grant_type=password&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
            });

            if (response.ok) {
                const data = await response.json();
                const accessToken = data.access_token;

                // 存储访问令牌，这里简单地使用 localStorage
                localStorage.setItem('access_token', accessToken);

                // 在这里可以进行其他操作，例如页面跳转等
                console.log('Login successful');
            } else {
                // 处理登录失败的情况
                console.error('Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    });
});
