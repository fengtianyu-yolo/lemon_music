<template>
    <div class="header-container">
        <div class="title">
            <slot></slot>
        </div>
        <el-button class="logout-btn" @click="logout">
            Logout
        </el-button>
    </div>
</template>

<script setup>
// import { ref } from 'vue';

// const title = ref('Dashboard')

function logout() {
    alert('click logout')
}

</script>

<style scoped>
.header-container {
    background-color: #FFFFFF;
    padding-left: 60px;
    padding-right: 60px;

    display: flex;
    justify-content: space-between;
    align-items: center;

    height: 90px;
}

.title {
    color: #424242;
    font-size: 20px;
    font-family: sans-serif;
    font-weight: 800;

}

.logout-btn {
    background-color: var(--global-highlight-color);
    width: 120px;
    height: 40px;
    border-radius: 4px;
    border-width: 0px;
    font-size: 14px;
    color: #FFFFFF;    

    text-align: center;    

    display: block;
}

</style>