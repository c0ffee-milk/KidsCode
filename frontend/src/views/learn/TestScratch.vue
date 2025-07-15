<template>
  <div class="scratch-game">
    <header class="game-header">
      <h1>拯救公主 - 关卡 {{ currentLevel }}</h1>
      <button @click="$router.push('/')">返回首页</button>
    </header>
    <section class="game-story">
      <h2>故事背景</h2>
      <p>{{ currentPass.desc }}</p>
    </section>
    <section class="game-levels">
      <h2>地图</h2>
      <div class="map">
        <div v-for="(row, rIdx) in currentPass.map" :key="rIdx" class="map-row">
          <span v-for="(cell, cIdx) in row" :key="cIdx" :class="cellClass(cell)">
            {{ cellSymbol(cell) }}
          </span>
        </div>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const aiPort = ref('')
const savedPort = ref('')
const passes = [
  {
    map: [[1,0,0,2]],
    desc: '主要为下一关的循环执行做引入，主要是顺序执行的思想'
  },
  {
    map: [[1,0,0,0,0,0,0,0,0,2]],
    desc: '引入循环while的思想，可以在此处引入“重复执行...直到终点”的动作'
  },
  {
    map: [
      [1,0,-1,0,2],
      [-4,0,0,0,-4]
    ],
    desc: '引入if条件语句的思想，为后续for与if结合使用做铺垫'
  },
  {
    map: [
      [1,0,0,-1,-4,-4,-4,-4],
      [-4,-4,0,0,0,0,-1,-4],
      [-4,-4,-4,-4,-4,0,0,2]
    ],
    desc: 'for与if的结合，终点处的标识可以替换为鲜花'
  },
  {
    map: [
      [1,0,-1,0,0,0,-1,0,0,0,-1,0,2],
      [-4,0,0,0,-1,0,0,0,-1,0,0,0,-1]
    ],
    desc: 'for与if的结合，难度提升，终点处的标识可以替换为鲜花'
  },
  {
    map: [
      [1,0,-2,-1,-4],
      [-4,-4,0,0,2]
    ],
    desc: '-2处为迷雾，当点击运行时才揭晓-2处是否存在怪兽。旨在传递if-else思想'
  },
  {
    map: [
      [1,0,-2,-1,-1,-1,-1,-1,0,0,2],
      [-1,-1,0,0,-2,-1,0,0,-2,-1,-1],
      [-1,-1,-1,-1,0,0,-2,-1,-1,-1,-1]
    ],
    desc: '前文所说的各操作的结合，障碍物1与障碍物2应区分，不相同，终点处即为公主。'
  }
]

const currentLevel = ref(1)
const currentPass = computed(() => {
  let level = parseInt(route.params.level)
  if (isNaN(level) || level < 1 || level > passes.length) {
    level = 1
  }
  return passes[level - 1]
})

watch(
  () => route.params.level,
  (newLevel) => {
    let num = parseInt(newLevel)
    if (isNaN(num) || num < 1 || num > passes.length) {
      num = 1
    }
    currentLevel.value = num
  },
  { immediate: true }
)

onMounted(() => {
  const port = localStorage.getItem('aiPort')
  if (port) {
    savedPort.value = port
    aiPort.value = port
  }
})

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
  const portVal = aiPort.value.trim()
  if (!portVal || !/^\d{2,5}$/.test(portVal)) {
    alert('请输入有效端口号（2-5位数字）')
    return
  }
  savedPort.value = portVal
  localStorage.setItem('aiPort', portVal)
}
</script>

<style scoped>
/* 原有样式保持不变 */
.map-row {
  display: flex;
}
.start {
  background: #e0f7fa;
  border-radius: 50%;
  padding: 2px 6px;
}
.end {
  background: #ffe0b2;
  border-radius: 50%;
  padding: 2px 6px;
}
.obstacle1 {
  background: #ffcdd2;
  border-radius: 4px;
  padding: 2px 6px;
}
.unreachable {
  background: #bdbdbd;
  color: #fff;
  border-radius: 4px;
  padding: 2px 6px;
}
.fog {
  background: #cfd8dc;
  border-radius: 4px;
  padding: 2px 6px;
}
.empty {
  background: #fff;
  padding: 2px 6px;
}
</style>