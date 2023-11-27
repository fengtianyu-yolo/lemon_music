<template>
    <div class="sidebar">
        <div class="header">
            <div class="user-avatar">

            </div>
            <div class="username">
                {{ username }}
            </div>
            <div class="line"></div>
        </div>

        <div class="menu-container" v-for="menu_item in menu_list">
            <div class="menu-item">
                <div class="menu-item-icon">
                    <img :src="menu_item.icon">
                </div>
                <div class="menu-item-title">
                    {{ menu_item.title }}
                </div>
            </div>
        </div>

    </div>
    <div class="main">
        
    </div>
</template>

<script setup>
import { ref } from 'vue';


const menu_list = ref([
    {
        icon: 'src/assets/sidebar_home_icon.svg',
        title: 'Dashboard'
    },
    {
        icon: 'src/assets/sidebar_lib_icon.svg',
        title: '曲库管理'
    }
])

const username = ref('一双鱼')

</script>

<style scoped>

.sidebar {
    background-color: var(--sidebar-background-color);
}

.sidebar .header .user-avatar {
    width: 64px;
    height: 64px;

    border-radius: 32px;
    border-width: 0px;
    background-color: #FFFFFF;
    
    margin: 0 auto;
    margin-top: 26px;

}

.sidebar .header .username {
    
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600px;

    text-align: center;

    padding: 12px 30px;
    margin: 0 auto;
    margin-top: 12px;
}

.sidebar .line {
    height: 1px;

    margin-top: 26px;

    background-color: #BDBDBD;
}

.menu-container {
    padding-top: 16px;
    padding-left: 24px;
    padding-right: 24px;
}

.menu-item {
    height: 40px;
    background-color: var(--sidebar-selected-color);
    border-radius: 4px;

    display: flex;
    align-items: center;
    padding-left: 16px;
}

.menu-item-icon {
    width: 16px;
    height: 16px;

    /* margin-left: 16px; */
    /* margin-top: 12px; */
}

.menu-item-icon img {
    width: 16px;
    height: 16px;
}

.menu-item-title {
    font-family: 'Comic Sans MS' 'Kumbh Sans';
    font-weight: 800px;
    font-style: normal;
    font-size: 14px;
    line-height: 16px;

    color: #FFFFFF;

    padding-left: 16px;
}

/* div的选中态怎么设置 */

.main {
    background-color: #FCFAFA;
}
</style>
