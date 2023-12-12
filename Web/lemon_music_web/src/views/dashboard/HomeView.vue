<template>
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <div class="user-avatar">

                </div>
                <div class="username">
                    {{ username }}
                </div>
                <div class="line"></div>
            </div>

            <div class="menu-container" v-for="menuItem in menuList" :key="menuItem.path">
                <RouterLink class="menu-item" active-class="menu-item-active" :to="menuItem.path">
                    <div class="menu-item-icon">
                        <img :src="menuItem.icon">
                    </div>
                    <div class="menu-item-title">
                        {{ menuItem.title }}
                    </div>
                </RouterLink>
            </div>

        </div>

        <div class="main">
            <HeaderView>
                <div v-if="currentTab == 'dashboard'">
                    Dashboard
                </div>
                <div v-if="currentTab == 'musics'">
                    <el-button class="refresh-btn" type="primary" @click="refresh">刷新</el-button>
                </div>
            </HeaderView>
            <RouterView></RouterView>
        </div>
    </div>
</template>
    
<script setup>
import { ref } from 'vue';
import { watch } from 'vue';
import { onMounted } from 'vue';
import { provide } from 'vue';

import axios from 'axios';

import { useRouter } from 'vue-router'
import HeaderView from './HeaderView.vue';

import { format_duration } from '../../tool';

const menuList = ref([
    {
        icon: 'src/assets/sidebar_home_icon.svg',
        title: 'Dashboard',
        path: '/dashboard'
    },
    {
        icon: 'src/assets/sidebar_lib_icon.svg',
        title: '曲库管理',
        path: '/music_lib'
    }
])

const username = ref('一双鱼')
const router = useRouter();
const currentTab = ref('dashboard')

watch(() => router.currentRoute.value.path, () => {
    currentTab.value = router.currentRoute.value.name
}, { immediate: true, deep: true });


const listData = ref([])

provide('song_list', listData)

function request_total_songs() {

    // 请求曲库列表 
    let url = 'http://localhost:8000/api/songs'
    axios.get(url)
        .then(
            function (response) {
                let code = response.data['code']
                if (code == 0) {
                    let data_list = response.data['list']
                    // console.log(data_list)
                    let songs = []
                    for (const item of data_list) {
                        const song_name = item['song_name']
                        const duration = item['duration']
                        const media_type = item['media_type']
                        const singer = item['singer']['singer_name']
                        const formatted_duration = format_duration(duration)

                        const obj = {
                            name: song_name,
                            format: media_type,
                            duration: formatted_duration,
                            singer: singer
                        }
                        console.log(obj)
                        songs.unshift(obj)
                    }
                    listData.value = songs
                }
            }
        )
        .catch(
            function (err) {
                console.log(err)
            }
        )

}

onMounted(() => {
    request_total_songs()
})


</script>
    
<style scoped>
.container {
    display: grid;
    grid-template-columns: 240px auto;
    height: 100vh;
    width: 100vw;
}

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

    border-radius: 4px;

    display: flex;
    align-items: center;
    padding-left: 16px;
}

.menu-item-active {
    background-color: var(--global-highlight-color);
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

.refresh-btn {
    width: 120px;
    height: 40px;
    background-color: var(--global-highlight-color);
}

/* div的选中态怎么设置 */

.main {
    background-color: #E7E7E7;
}
</style>
    