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
                <div class="loading-container" v-if="isLoading">
                    <div class="loading">
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                </div>
                
                <button v-else>刷新</button>
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
        iconSrc: 'src/assets/dashboard_music_icon.svg',
        type: CARD_TYPE.MUSIC
    },
    {
        title: '歌手',
        lastUpdate: 1701061942000, 
        count: 12,
        newAdd: 3,
        iconSrc: '/src/assets/dashboard_singer_icon.svg',
        type: CARD_TYPE.SINGER
    }
])

const isLoading = ref(true)

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

.loading-container {
    width: 106px;
    height: 38px;
    background-color: var(--global-highlight-color);
    border-radius: 19px;
}

.loading,
.loading > div {
  position: relative;
  box-sizing: border-box;
}

.loading {
  display: block;
  font-size: 0;
  color: #fff;
  margin: 0 auto;
  padding-top: 13px;
}

.loading.la-dark {
  color: #333;
}

.loading > div {
  display: inline-block;
  float: none;
  background-color: currentColor;
  border: 0 solid currentColor;
}

.loading {
  width: 40px;
  height: 10px;
}

.loading > div {
  width: 10px;
  height: 10px;
  border-radius: 100%;
}

.loading > div:first-child {
  transform: translateX(0%);
  animation: ball-newton-cradle-left 1s 0s ease-out infinite;
}

.loading > div:last-child {
  transform: translateX(0%);
  animation: ball-newton-cradle-right 1s 0s ease-out infinite;
}

.loading.la-sm {
  width: 20px;
  height: 4px;
}

.loading.la-sm > div {
  width: 4px;
  height: 4px;
}

.loading.la-2x {
  width: 80px;
  height: 20px;
}

.loading.la-2x > div {
  width: 20px;
  height: 20px;
}

.loading.la-3x {
  width: 120px;
  height: 30px;
}

.loading.la-3x > div {
  width: 30px;
  height: 30px;
}

@keyframes ball-newton-cradle-left {
  25% {
    transform: translateX(-100%);
    animation-timing-function: ease-in;
  }

  50% {
    transform: translateX(0%);
  }
}

@keyframes ball-newton-cradle-right {
  50% {
    transform: translateX(0%);
  }

  75% {
    transform: translateX(100%);
    animation-timing-function: ease-in;
  }

  100% {
    transform: translateX(0%);
  }
}

</style>