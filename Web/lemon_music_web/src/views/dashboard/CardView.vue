<template>
    <div class="card-container">
        <div class="effect" :style="{ backgroundColor: effectBgColor}"></div>
        <div class="title-area">
            <div class="icon">
                <img :src="iconSrc" >
            </div>
            <div class="title-info">
                <p class="title">{{ title }}</p>
                <p class="subtitle">{{ subtitle }}</p>
            </div>
        </div>
        <div class="tag-area">
            <div class="tag">Bengaluru</div>
            <div class="tag">3 years exp</div>
        </div>
        <div class="bottom-area">
            <div class="count-area">
                <span class="total-count">{{ count }}</span>
                <span class="count-suffix" v-if="isSinger"> 个歌手</span>
                <span class="count-suffix" v-if="isMusic"> 首歌曲</span>
            </div>
            <div class="new-add">{{ newAdd }} 本周新增</div>
        </div>
        <div class="line" :style="{ backgroundColor: focusColor}"></div>    
    </div>
    
    
</template>

<script setup>
import { computed } from 'vue';
// import { ref } from 'vue';
import { CARD_TYPE } from './constant.js'

const props = defineProps({
    'title': String,
    'iconSrc': String,
    'lastUpdate': Number,
    'count': Number,
    'newAdd': Number,
    'type': Number,
})

const isSinger = computed( () => {
    return props.type == CARD_TYPE.SINGER
})

const isMusic = computed( () => {
    return props.type == CARD_TYPE.MUSIC
})

const subtitle = computed( () => {

    var suffix = "前更新";

    var currentDate = new Date().getTime(); // 定义变量: var 
    console.log('currentDate = ' + currentDate.toString()) // long转字符串的方法：date.toString()；字符串拼接：+
    console.log(props.lastUpdate)
    var diff = currentDate - props.lastUpdate; // 计算当前时间和上次更新时间的时间差，单位毫秒
    
    var minuteDuration = 1000 * 60; // 1分钟的时长
    var hourDuration = minuteDuration * 60; // 1年时长
    var dayDuration = hourDuration * 24; // 1天时长 
    var weekDuration = dayDuration * 7; // 1周时长 
    var mouthDuration = weekDuration * 7; // 1个月的时长     
    var yearDuration = mouthDuration * 12;

    var ago = '刚刚'
    if (diff > yearDuration) {
        ago = diff / yearDuration;
        ago = parseInt(ago)
        console.log(yearDuration)
        console.log(ago)
        return ago.toString + '年' + suffix;

    } else if (diff > mouthDuration) {
        ago = diff / mouthDuration;
        ago = parseInt(ago)
        return ago.toString() + '月' + suffix;

    } else if (diff > weekDuration) {
        ago = diff / weekDuration;
        ago = parseInt(ago)
        return ago.toString() + '周' + suffix;

    } else if (diff > dayDuration) {
        ago = diff / dayDuration;
        ago = parseInt(ago)
        return ago.toString() + '天' + suffix;

    } else if (diff > hourDuration) {
        ago = diff / hourDuration;
        ago = parseInt(ago)
        return ago.toString() + '小时' + suffix;

    } else if (diff > minuteDuration) {
        ago = diff / minuteDuration;
        ago = parseInt(ago)
        return ago.toString() + '分钟' + suffix;

    } else {
        return '刚刚更新'
    }
    
})

const effectBgColor = computed( () => {    
    console.log(isSinger.value)
    if (isSinger.value) {
        console.log('CF1A2C26')
        return '#CF1A2C26'
    } else if (isMusic.value) {
        console.log('29C5EE26')
        return '#29C5EE26'
    } else {
        return 'clear'
    }
})

const focusColor = computed( () => {
    if (isSinger.value) {
        return '#CF1A2C';
    } else if (isMusic.value) {
        return '#29C5EE';
    } else {
        return 'clear'
    }
})

</script>

<style scoped>
.card-container {
    padding-left: 16px;
    padding-right: 16px;
    padding-top: 16px;
    background-color: #1E1E1E;

    display: flex;
    flex-direction: column;

    width: 316px;
    height: 182px;
    border-radius: 16px;
    border-width: 0px;
    margin-right: 24px;

    position: relative;
    overflow: hidden;
    
}

.title-area {
    display: flex;
}

.icon img {
    width: 46px;
    height: 46px;
}

.title-info {
    margin-left: 12px;
}

.title-info .title {
    color: #FFFFFF;

    font-size: 18px;    
    font-weight: bold;
}

.title-info .subtitle {
    color: #898989;

    font-size: 12px;
}

.tag-area {
    display: flex;
    margin-top: 12px;
}

.tag {
    padding-left: 12px;
    padding-right: 12px;
    height: 28px;
    border-radius: 14px;
    border-width: 0px; 
    background-color: #282828;

    color: #898989;
    font-size: 12px;
    padding-top: 4px;
    margin-right: 12px;
}

.bottom-area {
    display: flex;
    justify-content: space-between;
    align-items: baseline;

    margin-top: 4px;
}

.total-count {
    font-size: 38px;
    font-weight: bold;
    color: #FFFFFF;
}

.count-suffix {
    font-size: 12px;
    color: #898989;
}

.new-add {
    color: #00B85E;
}

.line {
    width: 6px;
    height: 100%;
    background-color: #29C5EE;

    position: absolute;
    margin-left: -16px;
    margin-top: -16px;
}

.effect {
    position: absolute;
    margin-top: -36px;
    margin-left: 170px;
    
    filter: blur(24px);    

    border-radius: 75px;
    
    width: 150px;
    height: 150px;
}

</style>