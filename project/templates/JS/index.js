/*
 * @Author: Jeff_L
 * @Date: 2024-02-02 16:43:03
 * @LastEditors: Jeff_L && yanxinluo28@gmail.com
 * @LastEditTime: 2024-02-02 16:43:31
 * @FilePath: \project\templates\JS\index.js
 * @Description: 
 * 
 * Copyright (c) 2024 by ${yanxinluo28@gmail.com}, All Rights Reserved. 
 */
// script.js

function performLogin() {
    // Simulate an asynchronous operation (e.g., sending a login request to a server)
    setTimeout(function () {
        // Simulate redirect to home.html after successful login
        window.location.href = 'home.html';
    }, 1000); // Simulate the time needed for the login operation (1 second in this case)
}
