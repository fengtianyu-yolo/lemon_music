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
                <div class="dashboard-title" v-if="currentTab == 'dashboard'">
                    <p>{{ titleItem.title }}</p>
                    <p>{{ titleItem.subtitle }}</p>
                </div>
                <div v-if="currentTab == 'musics'">
                    <el-button class="header-btn" type="primary" @click="refresh" text>编辑</el-button>
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

const titleList = [
    {
        'title': '多亏还有音乐和酒精',
        'subtitle': '不然人类澎湃的爱意该往哪里放。'
    },
    {
        'title': '那些听不见音乐的人认为那些跳舞的人疯了。',
        'subtitle': ''
    },
    {
        'title': '耳机线像是输液管，',
        'subtitle': '听音乐的时候很像生病打点滴，是一个治愈的过程。'
    },
    {
        'title': '音乐将一切平凡的画面赋予深厚的意义',
        'subtitle': ''
    },
    {
        'title': '音乐只是提供氛围，你听的都是自己的故事。',
        'subtitle': ''
    }
]
const num = parseInt(Math.random() * titleList.length)
const item = titleList[num]
const titleItem = ref(item)

const listData = ref([])
provide('song_list', listData)

const cards = ref([])
provide('cards', cards)

function requestSongs() {

    // 请求曲库列表 
    const domain = import.meta.env.VITE_API_URL
    const path = '/api/songs' 
    const url = domain + path
    axios.get(url)
        .then(
            function (response) {
                let code = response.data['code']
                if (code == 0) {
                    let data_list = response.data['list']
                    let songs = []
                    for (const item of data_list) {
                        const song_name = item['song_name']
                        const duration = item['duration']
                        const media_type = item['media_type']
                        const formatted_duration = format_duration(duration)                        
                        const singer = item['singers'].map( singer => singer['singer_name']).toString()                        

                        const obj = {
                            name: song_name,
                            format: media_type,
                            duration: formatted_duration,
                            singer: singer
                        }
                        songs.unshift(obj)
                    }
                    listData.value = songs
                }
            }
        )
        .catch(
            function (err) {
                console.log(err.toString())
            }
        )

}

function requestDashboard() {
    // 请求曲库列表 
    const path = '/api/dashboard'
    const url = import.meta.env.VITE_API_URL + path

    axios.get(url)
        .then(
            function (response) {
                let code = response.data['code']
                if (code == 0) {
                    let dataList = response.data['data']

                    let rawCards = []
                    for (const item of dataList) {
                        
                        let formatUpdated = item['last_update']
                        let cardType = item['card_type']
                        var icon = ''
                        if (cardType == 0) {
                            icon = 'src/assets/dashboard_music_icon.svg'
                        } else if (cardType == 1) {
                            icon = 'src/assets/dashboard_singer_icon.svg'
                        }
                        const card = {
                            title: item['title'],
                            lastUpdate: formatUpdated,
                            count: item['count'],
                            newAdd: item['new_add'],
                            iconSrc: icon,
                            type: cardType // CARD_TYPE.MUSIC
                        }

                        rawCards.unshift(card)
                    }
                    cards.value = rawCards
                }
            }
        )
        .catch(
            function (err) {
                console.log(err.toString())
            }
        )
}

onMounted(() => {
    requestDashboard()
    requestSongs()
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

    background-color: #bcbcbc;
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

.dashboard-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--global-highlight-color);
    font-family: 'AlimamaDaoLiTi', 'STBaoliSC-Regular';
}

.header-btn, .refresh-btn {
    width: 88px;
    height: 40px;
}

.refresh-btn {
    background-color: var(--global-highlight-color);
}

.main {
    background-color: #efeeec;
}
</style>
    