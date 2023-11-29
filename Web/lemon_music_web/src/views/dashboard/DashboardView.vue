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
              
              <button @click="refreshData" v-else>刷新</button>
          </div>

          <div class="music-list-content">
            <div class="list-header">
              <div class="header-filter">
                <div class="filter-item">All</div>
                <div class="filter-item">Todo</div>
                <div class="filter-item">Unknown</div>                
              </div>
              <div class="indicator-line"></div>                
            </div>
            <div class="bottom-line"></div>
            <div class="table-title">
              <div class="song-name-label">歌曲名</div>
              <div class="singer-label">歌手</div>
              <div class="duration-label">时长</div>
              <div class="format-label">格式</div>                
            </div>

            <div class="row" v-for="songItem in songList" :key="songItem.songName">
              <div class="info-row">
                <div class="info-name">{{ songItem.songName }}</div>
                <div class="info-singer">{{ songItem.singer }}</div>
                <div class="info-duration">{{ songItem.duration }}</div>
                <div class="info-format">{{ songItem.format }}</div>
              </div>
              <div class="row-line"></div>
            </div>              
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

const songList = ref([
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
},
{
  songName: '今年勇',
  singer: '许嵩',
  duration: '03:24',
  format: 'MP3'
}
])

const isLoading = ref(false)

function refreshData() {
  isLoading.value = !isLoading.value;
}

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

.music-list-content {
background-color: #FFFFFF;
border-radius: 16px;
margin-top: 16px;
width: 100%;
height: 500px;

overflow-y: scroll;
}

.list-header {
padding-left: 16px;
}

.header-filter {
display: flex;  
}
.filter-item {
width: 88px;
height: 54px;
padding-top: 14px;  
text-align: center;

font-size: 16px;
font-weight: bold;
color: #424242;
}

.indicator-line {
background-color: #2365C9;
width: 88px;
height: 2px;  
}

.bottom-line {
background-color: var(--global-highlight-color);
height: 1px;
margin-right: 44px;
}

.table-title {
display: flex;
justify-content: space-between;
align-items: center;
height: 44px;
margin-left: 16px;
margin-right: 44px;
margin-top: 14px;

background-color: #D5E7F6;
border-radius: 8px;

color: #898989;
}

.song-name-label {
width: 172px;
padding-left: 20px;
}

.format-label {
padding-right: 20px;
}

.info-row {
display: flex;
justify-content: space-between;
align-items: center;

height: 77px;
margin-left: 16px;
margin-right: 44px;
}

.info-name {
width: 172px;
padding-left: 20px;
}
.info-singer {
width: 100px;
}
.singer-label {
width: 100px;
}

.info-format {
padding-right: 20px;
}

.row-line {
height: 1px;
background-color: #D5E7F6;
margin-left: 20px;
margin-right: 20px;
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