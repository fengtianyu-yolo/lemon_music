<template>
    <div class="content">
        <div class="card-container">
            <CardView v-for="cardInfo in cardList" :key="cardInfo.title"
            :title="cardInfo.title"
            :lastUpdate="cardInfo.lastUpdate"
            :count="cardInfo.count"
            :iconSrc="cardInfo.iconSrc"
            :newAdd="cardInfo.newAdd"
            :type="cardInfo.type"
            ></CardView>
        </div>

        <div class="music-list">
            <div class="music-list-header">
                <label>
                    全部歌曲
                </label>
                <button>刷新</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import CardView from './CardView.vue';
import { CARD_TYPE } from './constant';

const cardList = ref([
    {
        title: '歌曲',
        lastUpdate: 1701148342000, 
        count: 304,
        newAdd: 38,
        iconSrc: 'src/assets/music_icon.svg',
        type: CARD_TYPE.MUSIC
    },
    {
        title: '歌手',
        lastUpdate: 1701061942000, 
        count: 12,
        newAdd: 3,
        iconSrc: '/src/assets/music_icon.svg',
        type: CARD_TYPE.SINGER
    }
])

</script>

<style scoped>

.content {
    padding-left: 60px;
    padding-top: 34px;
}

.card-container {
    display: flex;

}

.music-list {
    margin-top: 24px;
    margin-right: 60px;
}

.music-list-header { 
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 38px;
}

.music-list-header label {
    color: #2671B1;
    font-size: 28px;
    font-weight: bold;
}

.music-list-header button {
    height: 38px;
    width: 106px; 

    border-radius: 19px;
    border-width: 0px;
    
    background-color: #2671B1;

    font-size: 14px;
    color: #FFFFFF;
}

</style>