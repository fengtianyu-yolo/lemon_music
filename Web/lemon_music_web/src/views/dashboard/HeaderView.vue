<template>
    <div class="header-container">
        <div class="title">
            {{ title }}
        </div>
        <div class="logout-btn">
            Logout
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';


const title = ref('Dashboard')

</script>

<style scoped>
.header-container {
    background-color: #FFFFFF;
    padding-left: 60px;
    padding-right: 60px;

    display: flex;
    justify-content: space-between;
}

.title {
    
}

.logout-btn {
    background-color: var(--global-highlight-color);
}

</style>