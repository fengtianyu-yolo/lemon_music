<template>

    <div class="container">
        <div class="title">
            Welcome, Log into you account
        </div>
        <div class="login-form">
            <p>It is our great pleasure to have you on board! </p>
            <input type="text" placeholder="Enter th name" v-model="username"> 
            <input type="password" placeholder="Enter Password" v-model="password">
            <button @click="login">Login</button>
        </div>
    </div>

</template>

<script setup>
import { ref } from 'vue';


const username = ref('')
const password = ref('')

function login() {

if (username.value.length == 0) {
    alert('请输入用户名')
    return;
}
if (password.value.length == 0) {
    alert('请输入密码')
    return;
}

console.log(username.value)
console.log(password.value)
}

</script>

<style scoped>
.container {
background-color: #FCFAFA;
height: 100vh;    
padding-top: 200px;
}

.title {
margin-bottom: 48px;

font-size: 36px;
text-align: center;
font-weight: bold;
font-family: sans-serif; 
}

.login-form {

padding: 70px 130px;
background-color: #FFFFFF;
margin: 0 auto;
width: 512px;
height: 392px;
}
p {
margin-bottom: 14px;
text-align: center;   
font-family: sans-serif; 
}

input {
height: 42px;
width: 248px;
padding-left: 12px;
margin-bottom: 14px;

border-color: #A7A7A7;
border-radius: 4px;
border-width: 1px;

font-size: 14px;
font-family: sans-serif;

display: block;
}

button {
height: 44px;
width: 248px;
border-radius: 4px;
border-width: 0px;

background-color: var(--global-highlight-color);
color: #FFFFFF;
font-family: sans-serif; 
}
</style>