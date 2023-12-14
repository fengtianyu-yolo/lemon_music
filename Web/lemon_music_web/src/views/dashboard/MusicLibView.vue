<template>
    <div class="music-lib-container">
        <div class="filter-container">
            <el-select v-model="filter" class="song-filter-select m-2" placeholder="Add filter" size="large">
                <el-option v-for="option in filterOptions" :key="option.value" :label="option.label" :value="option.value"
                    class="search-input"></el-option>
            </el-select>

            <el-input v-model="searchValue" placeholder="Search for a song by name or singer" @change="search"
                @input="search" />
        </div>
        <div class="table-container">
            <el-table :data="listData" stripe :row-class-name="rowClassName">
                <el-table-column prop="name" label="Name" />
                <el-table-column prop="singer" label="Singer" />
                <el-table-column prop="format" label="格式" />
                <el-table-column prop="duration" label="时长" />
            </el-table>
        </div>

    </div>
</template>

<script setup>
import { inject, ref } from 'vue';
import axios from 'axios'
import { format_duration } from '../../tool';

const filter = ref('');

const searchValue = ref('')

const filterOptions = ref([
    {
        value: 'name',
        label: 'Name'
    },
    {
        value: 'singer',
        label: 'Singer'
    }
])

const songList = inject('song_list')

console.log('get songs ')
console.log(songList)

const listData = songList

function search() {
    if (searchValue.value == '') {
        listData.value = songList
    } else {
        // 请求曲库列表 
        let url = 'http://localhost:8000/api/search?name=' + searchValue.value
        axios.get(url)
            .then(
                function (response) {
                    let code = response.data['code']
                    if (code == 0) {
                        let data_list = response.data['list']
                        console.log(data_list)
                        let songs = []
                        for (const item of data_list) {
                            const song_name = item['song_name']
                            const duration = item['duration']
                            const media_type = item['media_type']
                            const singer = item['singers'].map( singer => singer['singer_name']).toString()                        
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

}


function rowClassName() {
    return 'row'
}

</script>

<style scoped>
.music-lib-container {
    background-color: #FFFFFF;
}

.filter-container {
    margin-left: 40px;
    margin-right: 100px;

    height: 48px;
    background-color: clear;

    display: flex;
}

:deep(.el-input) {
    height: 46px;
    --el-border-color: clear;
    --el-select-border-color-hover: clear;
    --el-select-input-focus-border-color: clear;
}


:deep(.el-input__wrapper) {
    background-color: #F0FAFA;
}

:deep(.el-select .el-input__wrapper) {
    background-color: #FFFFFF;
}

.song-filter-select {
    width: 132px;
    height: 48px;
}

.table-container {
    margin-left: 40px;
    margin-right: 100px;
    margin-top: 10px;
    background-color: aqua;
}
</style>

