<template>
    <div class="scratch-game">
        <header class="game-header">
            <h1>拯救公主</h1>
            <div class="medals">
                <span v-if="maxPass >= 3" class="medal star">☆ 星星勋章</span>
                <span v-if="maxPass >= 5" class="medal flower">🌸 鲜花勋章</span>
                <span v-if="maxPass >= 7" class="medal princess">👸 公主勋章</span>
            </div>
        </header>
        <section class="game-story">
            <h2>故事背景</h2>
            <p>
                你是王国的一位骑士，公主被怪兽抓走了，你需要闯过关卡，获得星星☆和鲜花最终击败怪兽拯救公主。
            </p>
        </section>
        <section class="game-actions">
            <h2>人物动作</h2>
            <ul>
                <li>向上、向下、向左、向右、攻击</li>
                <li>如果遇到（障碍物1）就...</li>
                <li>重复执行...直到终点</li>
                <li>如果遇到（迷雾/怪兽）就... 否则...</li>
                <li>如果遇到（障碍物2）就...</li>
            </ul>
        </section>
        <section class="game-levels">
            <h2>关卡</h2>
            <div class="level">
                <h3>Pass1</h3>
                <div class="map">
                    <div v-for="(row, rIdx) in passes[0].map" :key="rIdx" class="map-row">
                        <span v-for="(cell, cIdx) in row" :key="cIdx" :class="cellClass(cell)">
                            {{ cellSymbol(cell) }}
                        </span>
                    </div>
                </div>
                <p>{{ passes[0].desc }}</p>
            </div>
        </section>
        <section class="ai-port">
            <h2>AI通信端口</h2>
            <div class="port-info">
                <label>端口：</label>
                <input v-model="aiPort" placeholder="请输入AI端口" />
                <button @click="savePort">保存</button>
            </div>
            <div v-if="savedPort" class="saved-port">
                已保存端口：{{ savedPort }}
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const passes = [
    {
        map: [[1,0,0,2]],
        desc: '主要为下一关的循环执行做引入，主要是顺序执行的思想'
    }
]

const aiPort = ref('')
const savedPort = ref('')
const maxPass = ref(0)

function cellSymbol(cell) {
    switch(cell) {
        case 1: return '🏇'
        case 2: return '🏁'
        case -1: return '🧱'
        case -4: return '❌'
        case -2: return '🌫️'
        default: return '⬜'
    }
}
function cellClass(cell) {
    switch(cell) {
        case 1: return 'start'
        case 2: return 'end'
        case -1: return 'obstacle1'
        case -4: return 'unreachable'
        case -2: return 'fog'
        default: return 'empty'
    }
}
function savePort() {
    savedPort.value = aiPort.value
}

function updateMedal() {
    // 假设通过关卡数由后端/AI返回，这里用最大关卡数模拟
    maxPass.value = Math.max(maxPass.value, passes.length)
}
updateMedal()
</script>

<style scoped>
.scratch-game {
    font-family: 'Comic Sans MS', 'Arial', sans-serif;
    background: #f6f6f6;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 2px 8px #ccc;
    max-width: 900px;
    margin: 0 auto;
}
.game-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.medals {
    display: flex;
    gap: 12px;
}
.medal {
    font-size: 1.2em;
    padding: 4px 12px;
    border-radius: 8px;
    background: #ffe;
    border: 1px solid #ccc;
}
.star { color: #f7c948; }
.flower { color: #e75480; }
.princess { color: #eab1d6; }
.game-story, .game-actions, .game-levels, .ai-port {
    margin-top: 24px;
}
.game-actions ul {
    list-style: disc;
    margin-left: 24px;
}
.level {
    margin-bottom: 18px;
    background: #fff;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 1px 4px #eee;
}
.map {
    display: flex;
    flex-direction: column;
    margin-bottom: 8px;
}
.map-row {
    display: flex;
}
.map-row span {
    width: 32px;
    height: 32px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3em;
    margin: 2px;
    border-radius: 4px;
    border: 1px solid #ddd;
    background: #fafafa;
}
.start { background: #b3e5fc; }
.end { background: #ffe082; }
.obstacle1 { background: #e57373; }
.unreachable { background: #bdbdbd; }
.fog { background: #cfd8dc; }
.empty { background: #fff; }
.port-info {
    display: flex;
    align-items: center;
    gap: 8px;
}
.saved-port {
    margin-top: 8px;
    color: #388e3c;
}
</style>