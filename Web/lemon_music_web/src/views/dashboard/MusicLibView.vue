<template>
    <div class="music-lib-container">
        <div class="filter-container">
            <el-select v-model="filter" class="song-filter-select m-2" placeholder="Add filter" size="large">
                <el-option v-for="option in filterOptions" :key="option.value" :label="option.label" :value="option.value" class="search-input"></el-option>
            </el-select>

            <el-input v-model="searchValue" placeholder="Search for a song by name or singer" @change="search" @input="search"/>
        </div>

        <el-table :data="listData" stripe :row-class-name="rowClassName">
            <el-table-column prop="name" label="Name" width="180" />
            <el-table-column prop="singer" label="Singer" width="180" />
            <el-table-column prop="format" label="格式" width="180" />
            <el-table-column prop="duration" label="时长" width="180" />
        </el-table>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'

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

const listData = ref([])

onMounted( () => {
    // 请求曲库列表 
    let url = 'http://localhost:8000/api/music_list'
    axios.get(url)
    .then(
        function(response) {
            let code = response['code'] 
            if (code == 0) {
                console.log()
                listData.value = [{}]
            }
        }
    )
    .catch(
        function(err) {
            console.log(err)
        }
    )

})

function refresh() {
    
    let url = 'http://localhost:8000/refresh_music_list'
    axios.get(url)
    .then(
        function(response) {
            let code = response['code']
            console.log(code)
        }
    )
    .catch(
        function(err) {
            console.log(err)
        }
    )
}

function search() {
    console.log(searchValue.value)
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

.el-table {
    margin-left: 40px;
    margin-right: 100px;
    margin-top: 10px;

    width: 91%;
}

</style>