try {
    // 发起请求时添加 Cookie 中的令牌
    const response = await fetch('/chats', {
        method: 'GET',
        credentials: 'include',  // 包括 Cookie
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
    } else {
        // 处理请求失败的情况
        console.error('Request failed:', response.statusText);
    }
} catch (error) {
    console.error('Error fetching data:', error);
}
