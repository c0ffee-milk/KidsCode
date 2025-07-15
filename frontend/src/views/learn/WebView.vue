<template>
  <div class="level-map-bg">
    <div class="level-map-title">选择关卡</div>
    <svg
      class="level-map-svg"
      :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
      width="100%"
      :height="svgHeight"
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <!-- 优化发光效果，更柔和 -->
        <filter id="white-glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <!-- 关卡锁定时的灰色滤镜 -->
        <filter id="grayscale">
          <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0
                                               0.33 0.33 0.33 0 0
                                               0.33 0.33 0.33 0 0
                                               0 0 0 1 0" />
        </filter>
        <!-- 蓝色渐变 -->
        <linearGradient id="levelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="levelColors.start"/>
          <stop offset="100%" :stop-color="levelColors.end"/>
        </linearGradient>
        <!-- 当前关卡渐变 -->
        <linearGradient id="currentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="currentLevelColors.start"/>
          <stop offset="100%" :stop-color="currentLevelColors.end"/>
        </linearGradient>
      </defs>

      <!-- 路径线 -->
      <path :d="pathData" fill="none" stroke="rgba(255, 255, 255, 0.3)" stroke-width="8" stroke-dasharray="20 15"/>

      <!-- 关卡方块和图标 -->
      <g v-for="(level, i) in levels" :key="'level-' + i" class="level-group">
        <rect
          :x="levelPos(i).x"
          :y="levelPos(i).y"
          :width="boxSize"
          :height="boxSize"
          rx="22"
          :fill="isCurrent(i) ? 'url(#currentGrad)' : 'url(#levelGrad)'"
          stroke="#fff"
          stroke-width="4"
          :class="['level-block', { 'current': isCurrent(i), 'unlocked': isUnlocked(i), 'locked': !isUnlocked(i) }]"
          @click="handleLevelClick(i)"
          @keydown.enter="handleLevelClick(i)"
          :role="isUnlocked(i) ? 'button' : ''"
          :tabindex="isUnlocked(i) ? '0' : '-1'"
          :aria-label="`关卡 ${i + 1}`"
          :filter="!isUnlocked(i) ? 'url(#grayscale)' : ''"
        />
        <!-- 锁图标 (未解锁) -->
        <text
          v-if="!isUnlocked(i)"
          :x="levelPos(i).x + boxSize/2"
          :y="levelPos(i).y + boxSize/2 + 10"
          class="lock-icon"
        >🔒</text>
        <!-- 星星icon (已通关) -->
        <text
          v-if="level.passed"
          :x="levelPos(i).x + boxSize/2"
          :y="levelPos(i).y + boxSize/2 + 7"
          class="star"
        >⭐</text>
        <!-- 皇冠icon (当前关卡) -->
        <text
          v-if="isCurrent(i)"
          :x="levelPos(i).x + boxSize/2"
          :y="levelPos(i).y + 25"
          class="crown"
        >👑</text>
        <!-- 关卡数字 -->
        <text
          :x="levelPos(i).x + boxSize/2"
          :y="levelPos(i).y + boxSize/2 + (level.passed ? 32 : 10)"
          :class="['level-num', { 'hidden': level.passed || !isUnlocked(i) }]"
        >{{ i + 1 }}</text>
      </g>
    </svg>
    <button class="pass-btn" @click="goPass">通关演示跳转</button>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// --- 响应式状态定义 ---
const levels = reactive([
  { passed: true },   // 1
  { passed: true },   // 2
  { passed: false },  // 3
  { passed: false },  // 4
  { passed: false },  // 5
  { passed: false },  // 6
  { passed: false },  // 7
])
const currentLevelIndex = ref(2)

// --- 布局常量 ---
const boxSize = 82 // 微调尺寸
const gap = 60    // 微调间距

// --- 计算属性 ---
const svgWidth = computed(() => {
  return boxSize * levels.length + gap * (levels.length - 1) + 80
})
const svgHeight = computed(() => boxSize + 60) // 增加高度给皇冠和动画留出空间

// 动态生成连接路径
const pathData = computed(() => {
  if (levels.length < 2) return ''
  const start = `M ${levelPos(0).x + boxSize / 2},${svgHeight.value / 2}`
  const points = []
  for (let i = 1; i < levels.length; i++) {
    points.push(`L ${levelPos(i).x + boxSize / 2},${svgHeight.value / 2}`)
  }
  return `${start} ${points.join(' ')}`
})

// --- 颜色变量 ---
const levelColors = { start: '#67e8ff', end: '#7a6fff' }
const currentLevelColors = { start: '#ffe97a', end: '#ffb84c' }

// --- 方法 ---
const isCurrent = (i) => i === currentLevelIndex.value
const isUnlocked = (i) => levels[i].passed || isCurrent(i)

function levelPos(i) {
  return {
    x: 40 + i * (boxSize + gap),
    y: 30 // 往下移一点，给皇冠留空间
  }
}

function handleLevelClick(i) {
  if (isUnlocked(i)) {
    console.log(`跳转到关卡 ${i + 1}`)
    router.push({ name: 'LearnPython' })
  }
}

function goPass() {
  router.push({ name: 'LearnPython' })
}
</script>

<style scoped>
/* 使用CSS变量进行统一样式管理 */
:root {
  --box-size: 82px;
  --border-radius: 22px;
  --glow-color: #fff;
  --primary-glow-color: #ffe97a;
  --primary-glow-shadow: #ffe97a88;
  --level-grad-start: #67e8ff;
  --level-grad-end: #7a6fff;
  --current-grad-start: #ffe97a;
  --current-grad-end: #ffb84c;
  --bg-dark: #181937;
  --bg-light: #2c2d6e;
}

.level-map-bg {
  max-width: 900px;
  width: 100%;
  margin: 40px auto;
  background: radial-gradient(ellipse 100% 90% at 50% 30%, var(--bg-light) 0%, var(--bg-dark) 100%);
  border-radius: 24px;
  box-shadow: 0 10px 30px 0 rgba(24, 25, 55, 0.4);
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
  overflow-x: auto; /* 允许在小屏幕上水平滚动 */
}

.level-map-title {
  color: var(--glow-color);
  font-size: 26px;
  font-family: 'Poppins', 'Segoe UI', Arial, sans-serif;
  font-weight: 700;
  margin-bottom: 24px;
  letter-spacing: 3px;
  text-shadow: 0 4px 20px rgba(37, 36, 66, 0.6);
  user-select: none;
}

.level-map-svg {
  display: block;
  width: 100%;
  min-width: 860px; /* 保证SVG内容不会被压缩 */
  height: auto;
}

/* 关卡组入场动画 */
.level-group {
  animation: pop-in 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  opacity: 0;
  transform-origin: center;
}

/* 为每个关卡设置不同的动画延迟 */
.level-group:nth-child(2) { animation-delay: 0.1s; }
.level-group:nth-child(3) { animation-delay: 0.2s; }
.level-group:nth-child(4) { animation-delay: 0.3s; }
.level-group:nth-child(5) { animation-delay: 0.4s; }
.level-group:nth-child(6) { animation-delay: 0.5s; }
.level-group:nth-child(7) { animation-delay: 0.6s; }


@keyframes pop-in {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}


.level-block {
  transition: transform 0.3s ease, filter 0.3s ease;
}

.level-block.unlocked {
  cursor: pointer;
  filter: url(#white-glow);
}

.level-block.unlocked:hover,
.level-block.unlocked:focus {
  transform: translateY(-8px) scale(1.05);
  filter: url(#white-glow) drop-shadow(0 0 20px var(--primary-glow-shadow));
}

.level-block.unlocked:active {
  transform: translateY(-2px) scale(0.98);
}


.level-block.current {
  filter: url(#white-glow) drop-shadow(0 0 22px var(--primary-glow-shadow));
  animation: current-level-pulse 2s infinite;
}

.level-block.locked {
  opacity: 0.7;
}

@keyframes current-level-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}


.star, .crown, .level-num, .lock-icon {
  text-anchor: middle;
  font-family: 'Segoe UI Emoji', 'Poppins', sans-serif;
  pointer-events: none;
  user-select: none;
}

.star {
  font-size: 36px;
  fill: var(--primary-glow-color);
  animation: star-bounce 2s ease-in-out infinite;
}

.crown {
  font-size: 30px;
  fill: var(--primary-glow-color);
  transform-origin: bottom center;
  animation: crown-sway 2.5s ease-in-out infinite;
}

@keyframes crown-sway {
  0%, 100% { transform: rotate(-8deg); }
  50% { transform: rotate(8deg); }
}

.lock-icon {
  font-size: 32px;
}


.level-num {
  font-size: 32px;
  fill: var(--glow-color);
  font-weight: bold;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.7);
  transition: opacity 0.3s ease;
}

.level-num.hidden {
  opacity: 0;
}

@keyframes star-bounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-8px) scale(1.15); }
}

.pass-btn {
  margin-top: 32px;
  padding: 14px 40px;
  font-size: 1.2rem;
  border-radius: 30px;
  border: none;
  background: linear-gradient(95deg, var(--current-grad-start), var(--current-grad-end));
  color: #333;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 5px 20px -5px var(--primary-glow-shadow);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pass-btn:hover {
  background-position: 100% 0;
  box-shadow: 0 8px 25px -5px #ffb84c88;
  transform: translateY(-4px) scale(1.02);
}

.pass-btn:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 2px 10px -3px #ffb84c55;
}

/* 响应式设计 */
@media (max-width: 920px) {
  .level-map-bg {
    max-width: 100vw;
    border-radius: 0;
    margin: 0;
    padding: 24px 10px;
  }
}

@media (max-width: 700px) {
  .level-map-title {
    font-size: 22px;
    margin-bottom: 16px;
  }
}
</style>
