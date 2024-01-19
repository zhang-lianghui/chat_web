// user_control.js

document.addEventListener('DOMContentLoaded', function () {
    // 发起 GET 请求获取用户对象
    fetch('/get_user')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(user => {
            // 获取到用户对象后进行相应的操作
            const loginNavItem = document.getElementById('loginNavItem');
            const registerNavItem = document.getElementById('registerNavItem');
            const greetingNavItem = document.getElementById('greetingNavItem');
            const logoutNavItem = document.getElementById('logoutNavItem');

            if (user.is_active) {
                // 用户已登录
                loginNavItem.style.display = 'none';
                registerNavItem.style.display = 'none';
                greetingNavItem.style.display = 'block';
                greetingNavItem.innerHTML = `你好，${user.username}`;
                logoutNavItem.style.display = 'block';
            } else {
                // 用户未登录
                loginNavItem.style.display = 'block';
                registerNavItem.style.display = 'block';
                greetingNavItem.style.display = 'none';
                logoutNavItem.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching user:', error);
        });
});

