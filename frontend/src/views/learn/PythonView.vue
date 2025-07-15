<template>
  <div class="python-main">
    <div class="python-toolbar">
      <h1>Python闯关 - 第二关</h1>
      <span class="level-desc">引入循环while的思想，可以在此处引入“重复执行...直到终点”的动作。</span>
    </div>
    <div class="python-content">
      <!-- 左侧 Blockly 拖拽区 -->
      <div class="python-blocks-panel">
        <div class="blocks-header">
          <span>编程区</span>
          <button @click="initBlockly" class="init-btn">重新初始化</button>
        </div>
        <div ref="blocklyDiv" class="python-blocks-div"></div>
      </div>
      <!-- 右侧地图舞台区 -->
      <div class="python-stage-panel">
        <div class="stage-toolbar">
          <button class="flag-btn" @click="runCode">运行</button>
          <span class="stage-mode">拖拽积木并运行，骑士将自动到达终点</span>
        </div>
        <div class="stage-area">
          <h3>关卡地图</h3>
          <div class="map-row">
            <span v-for="(cell, idx) in mapData[0]" :key="idx" :class="cellClass(cell)">{{ cellSymbol(cell, idx) }}</span>
          </div>
          <div class="map-desc">
            <span class="start">🏇 起点</span>
            <span class="end">🏁 终点</span>
            <span class="empty">⬜ 路径</span>
          </div>
        </div>
        <div v-if="showFeedback" class="run-feedback">🎉 恭喜你，骑士已到达终点！</div>
      </div>
    </div>
    <div v-if="showIntro" class="intro-modal">
      <div class="intro-content">
        <h2>第二关：while循环闯关</h2>
        <h3>教学目标</h3>
        <ul>
          <li>理解并掌握 while 循环的基本用法</li>
          <li>学会用循环让骑士自动前进直到终点</li>
          <li>体验拖拽式编程，感受编程乐趣</li>
        </ul>
        <h3>关卡规则</h3>
        <ul>
          <li>骑士初始在起点（🏇），目标是到达终点（🏁）</li>
          <li>每次只能前进一格</li>
          <li>请用“重复执行直到到达终点”+“骑士向前移动一步”完成闯关</li>
        </ul>
        <h3>编程提示</h3>
        <ul>
          <li>拖拽“循环”积木和“动作”积木到编程区</li>
          <li>点击右侧“运行”按钮，观察骑士自动前进</li>
          <li>如遇问题可点击“重新初始化”重置编程区</li>
        </ul>
        <button class="intro-confirm" @click="showIntro = false">我已了解，开始闯关</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as Blockly from 'blockly'
import 'blockly/javascript'

const mapData = ref([[1,0,0,0,0,0,0,0,0,2]])
const knightPos = ref(0) // 骑士当前位置
const blocklyDiv = ref(null)
let workspace = null
const showFeedback = ref(false)
const showIntro = ref(true)
const blockTip = ref('请拖拽"while循环"和"移动一步"积木到编程区，然后点击右侧"运行"按钮。')

function cellSymbol(cell, idx) {
  if (idx === knightPos.value) return '🏇'
  switch(cell) {
    case 2: return '🏁'
    case -1: return '🧱'
    case -4: return '❌'
    case -2: return '🌫️'
    default: return '⬜'
  }
}

function cellClass(cell, idx) {
  let baseClass = ''
  switch(cell) {
    case 1: baseClass = 'start'; break;
    case 2: baseClass = 'end'; break;
    case -1: baseClass = 'obstacle1'; break;
    case -4: baseClass = 'unreachable'; break;
    case -2: baseClass = 'fog'; break;
    default: baseClass = 'empty';
  }
  
  // 如果是骑士当前位置，添加特殊样式
  if (idx === knightPos.value) {
    baseClass += ' knight-position'
  }
  
  return baseClass
}

function defineCustomBlocks() {
  // 单步前进
  if (!Blockly.Blocks['move_step']) {
    Blockly.Blocks['move_step'] = {
      init: function () {
        this.appendDummyInput().appendField('骑士向前移动一步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向前移动一格')
      }
    }
    Blockly.JavaScript['move_step'] = function () {
      return 'moveStep();\n'
    }
  }
  // 多步前进
  if (!Blockly.Blocks['move_steps']) {
    Blockly.Blocks['move_steps'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('骑士向前移动')
          .appendField(new Blockly.FieldNumber(2, 1, 20), 'STEPS')
          .appendField('步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向前移动多步')
      }
    }
    Blockly.JavaScript['move_steps'] = function (block) {
      const steps = block.getFieldValue('STEPS')
      return `moveSteps(${steps});\n`
    }
  }
  // while循环
  if (!Blockly.Blocks['while_not_end']) {
    Blockly.Blocks['while_not_end'] = {
      init: function () {
        this.appendStatementInput('DO').appendField('重复执行直到到达终点')
        this.setColour('#FFAB19')
        this.setTooltip('while循环，直到骑士到达终点')
      }
    }
    Blockly.JavaScript['while_not_end'] = function (block) {
      var branch = Blockly.JavaScript.statementToCode(block, 'DO')
      return 'whileNotEnd(async () => {\n' + branch + '});\n'
    }
  }
  // 判断是否到终点
  if (!Blockly.Blocks['is_at_end']) {
    Blockly.Blocks['is_at_end'] = {
      init: function () {
        this.appendDummyInput().appendField('是否到达终点?')
        this.setOutput(true, 'Boolean')
        this.setColour('#FFD700')
        this.setTooltip('判断骑士是否到达终点')
      }
    }
    Blockly.JavaScript['is_at_end'] = function () {
      return ['isAtEnd()', Blockly.JavaScript.ORDER_NONE]
    }
  }
  // 输出提示
  if (!Blockly.Blocks['show_tip']) {
    Blockly.Blocks['show_tip'] = {
      init: function () {
        this.appendDummyInput().appendField('输出提示').appendField(new Blockly.FieldTextInput('继续加油！'), 'TIP')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#8BC34A')
        this.setTooltip('在页面上输出提示')
      }
    }
    Blockly.JavaScript['show_tip'] = function (block) {
      const tip = block.getFieldValue('TIP')
      return `showTip('${tip}');\n`
    }
  }
}

onMounted(() => {
  nextTick(() => {
    defineCustomBlocks()
    setTimeout(() => {
      initBlockly()
    }, 300)
  })
})

function initBlockly() {
  console.log('开始初始化 Blockly...')
  console.log('blocklyDiv.value:', blocklyDiv.value)
  console.log('Blockly:', Blockly)
  
  if (blocklyDiv.value && Blockly) {
    try {
      defineCustomBlocks();
      if (workspace) workspace.dispose()
      workspace = Blockly.inject(blocklyDiv.value, {
        toolbox: `
          <xml>
            <category name="循环" colour="#FFAB19">
              <block type="while_not_end"></block>
            </category>
            <category name="动作" colour="#4C97FF">
              <block type="move_step"></block>
              <block type="move_steps"></block>
            </category>
            <category name="判断" colour="#FFD700">
              <block type="is_at_end"></block>
            </category>
            <category name="提示" colour="#8BC34A">
              <block type="show_tip"></block>
            </category>
          </xml>
        `,
        trashcan: true,
        zoom: { controls: true, wheel: true, startScale: 1.0, maxScale: 2, minScale: 0.5, scaleSpeed: 1.2 },
        grid: { spacing: 20, length: 3, colour: '#ccc', snap: true }
      })
      console.log('Blockly 初始化成功:', workspace)
    } catch (error) {
      console.error('Blockly 初始化失败:', error)
    }
  } else {
    console.log('重试初始化...')
    setTimeout(() => { initBlockly() }, 500)
  }
}

window.moveStep = function () {
  if (knightPos.value < mapData.value[0].length - 1) {
    knightPos.value++
  }
}
window.moveSteps = function (steps) {
  for (let i = 0; i < steps; i++) {
    if (knightPos.value < mapData.value[0].length - 1) {
      knightPos.value++
    }
  }
}
window.whileNotEnd = async function (fn) {
  while (knightPos.value < mapData.value[0].length - 1) {
    await fn()
    await new Promise(r => setTimeout(r, 300))
  }
}
window.isAtEnd = function () {
  return knightPos.value === mapData.value[0].length - 1
}
window.showTip = function (tip) {
  alert(tip)
}

async function runCode() {
  knightPos.value = 0
  showFeedback.value = false
  
  if (workspace) {
    try {
      const code = Blockly.JavaScript.workspaceToCode(workspace)
      console.log('生成的代码:', code)
      if (code.trim()) {
        eval(code)
      } else {
        // 如果没有代码，默认演示
        const steps = mapData.value[0].length - 1
        for (let i = 0; i < steps; i++) {
          await new Promise(r => setTimeout(r, 300))
          knightPos.value++
        }
      }
    } catch (error) {
      console.error('代码执行出错:', error)
      // 出错时也执行默认演示
      const steps = mapData.value[0].length - 1
      for (let i = 0; i < steps; i++) {
        await new Promise(r => setTimeout(r, 300))
        knightPos.value++
      }
    }
  } else {
    // 没有 workspace 时执行默认演示
    const steps = mapData.value[0].length - 1
    for (let i = 0; i < steps; i++) {
      await new Promise(r => setTimeout(r, 300))
      knightPos.value++
    }
  }
  
  showFeedback.value = true
  setTimeout(() => { showFeedback.value = false }, 2000)
}
</script>

<style scoped>
.python-main {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  font-family: 'Comic Sans MS', 'Arial', sans-serif;
  position: relative;
}

/* 添加动态背景装饰 */
.python-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.2) 0%, transparent 50%);
  pointer-events: none;
}

.python-toolbar {
  display: flex;
  align-items: center;
  background: linear-gradient(45deg, #4c97ff, #667eea);
  padding: 0 24px;
  height: 60px;
  color: #fff;
  justify-content: space-between;
  margin-top: 80px;
  box-shadow: 0 4px 20px rgba(76, 151, 255, 0.3);
  border-radius: 0 0 20px 20px;
  position: relative;
  overflow: hidden;
}

.python-toolbar::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.python-toolbar h1 {
  font-size: 24px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  position: relative;
  z-index: 1;
}

.level-desc {
  font-size: 16px;
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

/* 主内容区优化布局 */
.python-content {
  display: flex;
  gap: 32px;
  padding: 32px 0;
  justify-content: center;
  align-items: flex-start;
  position: relative;
  z-index: 1;
}

.python-blocks-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    0 0 0 1px rgba(255,255,255,0.2);
  width: 600px;
  min-width: 400px;
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 2px solid rgba(76, 151, 255, 0.2);
  transition: all 0.3s ease;
}

.python-blocks-panel:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 15px 40px rgba(0,0,0,0.15),
    0 0 0 1px rgba(255,255,255,0.3);
}

.blocks-header {
  padding: 16px 24px;
  font-weight: bold;
  color: #4c97ff;
  border-bottom: 2px solid rgba(76, 151, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(76, 151, 255, 0.1), rgba(102, 126, 234, 0.1));
  border-radius: 20px 20px 0 0;
  font-size: 18px;
}

.init-btn {
  background: linear-gradient(45deg, #4c97ff, #667eea);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(76, 151, 255, 0.3);
  font-weight: 600;
}

.init-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 151, 255, 0.4);
  background: linear-gradient(45deg, #667eea, #4c97ff);
}

.python-blocks-div {
  flex: 1;
  min-height: 520px;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 0 0 20px 20px;
  height: 100%;
  position: relative;
}

.python-stage-panel {
  flex: none;
  min-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    0 0 0 1px rgba(255,255,255,0.2);
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 600px;
  border: 2px solid rgba(255, 183, 77, 0.2);
  transition: all 0.3s ease;
}

.python-stage-panel:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 15px 40px rgba(0,0,0,0.15),
    0 0 0 1px rgba(255,255,255,0.3);
}

.stage-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  width: 100%;
  justify-content: center;
}

.flag-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 30px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.flag-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
  background: linear-gradient(45deg, #ff8e53, #ff6b6b);
}

.stage-mode {
  color: #ffab19;
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 171, 25, 0.1);
  padding: 8px 12px;
  border-radius: 15px;
  border: 1px solid rgba(255, 171, 25, 0.3);
}

.stage-area {
  width: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
  border-radius: 15px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 24px;
  border: 2px solid rgba(76, 151, 255, 0.1);
  box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
}

.stage-area h3 {
  color: #4c97ff;
  margin-bottom: 16px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.map-row {
  display: flex;
  gap: 4px;
  margin-bottom: 16px;
}

.map-row span {
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6em;
  border-radius: 12px;
  border: 3px solid #ddd;
  background: #fff;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.map-row span:hover {
  transform: scale(1.15) rotate(5deg);
  z-index: 10;
}

/* 骑士动画效果 */
.map-row span:has-text('🏇') {
  animation: knight-bounce 1s ease-in-out infinite alternate;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-color: #2196f3;
  box-shadow: 
    0 4px 20px rgba(33, 150, 243, 0.4),
    0 0 20px rgba(33, 150, 243, 0.2);
  transform: scale(1.1);
}

/* 使用CSS选择器来匹配包含骑士emoji的元素 */
.map-row span[style*="🏇"] {
  animation: knight-bounce 1s ease-in-out infinite alternate;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-color: #2196f3;
  box-shadow: 
    0 4px 20px rgba(33, 150, 243, 0.4),
    0 0 20px rgba(33, 150, 243, 0.2);
  transform: scale(1.1);
}

@keyframes knight-bounce {
  0% { 
    transform: scale(1.1) translateY(0px); 
    box-shadow: 0 4px 20px rgba(33, 150, 243, 0.4);
  }
  100% { 
    transform: scale(1.15) translateY(-3px); 
    box-shadow: 0 8px 25px rgba(33, 150, 243, 0.6);
  }
}

.start { 
  background: linear-gradient(135deg, #b3e5fc, #81d4fa);
  border-color: #4fc3f7;
  box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
}

.end { 
  background: linear-gradient(135deg, #ffe082, #ffd54f);
  border-color: #ffca28;
  box-shadow: 0 4px 15px rgba(255, 202, 40, 0.3);
  animation: end-glow 2s infinite alternate;
}

@keyframes end-glow {
  0% { 
    box-shadow: 0 4px 15px rgba(255, 202, 40, 0.3);
    transform: scale(1);
  }
  100% { 
    box-shadow: 0 4px 30px rgba(255, 202, 40, 0.8);
    transform: scale(1.05);
  }
}

.empty { 
  background: linear-gradient(135deg, #fff, #f8fafc);
  border-color: #e2e8f0;
  transition: all 0.3s ease;
}

.empty:hover {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-color: #0ea5e9;
}

/* 地图描述区域美化 */
.map-desc {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 20px;
}

.map-desc span {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
  padding: 8px 16px;
  border-radius: 20px;
  border: 2px solid rgba(76, 151, 255, 0.2);
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.map-desc span:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(76, 151, 255, 0.3);
  border-color: rgba(76, 151, 255, 0.4);
}

.map-desc span.start {
  border-color: #4fc3f7;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
}

.map-desc span.end {
  border-color: #ffca28;
  background: linear-gradient(135deg, #fff3e0, #ffe082);
}

.map-desc span.empty {
  border-color: #e2e8f0;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}

/* 添加闪烁效果给特殊元素 */
.map-row span:nth-child(1) {
  animation: start-pulse 3s ease-in-out infinite;
}

@keyframes start-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* 为地图整体添加一些装饰 */
.stage-area::before {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  background: linear-gradient(45deg, #4c97ff, #667eea, #764ba2, #ff6b6b);
  border-radius: 20px;
  z-index: -1;
  opacity: 0.1;
  animation: rotate-border 4s linear infinite;
}

@keyframes rotate-border {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 运行反馈优化 */
.run-feedback {
  margin: 20px auto 0;
  background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
  color: #2e7d32;
  border: 3px solid #4caf50;
  border-radius: 25px;
  padding: 20px 30px;
  font-size: 20px;
  text-align: center;
  width: fit-content;
  font-weight: bold;
  box-shadow: 
    0 8px 25px rgba(76, 175, 80, 0.3),
    inset 0 2px 0 rgba(255,255,255,0.3);
  animation: success-celebration 0.8s ease-out;
  position: relative;
}

.run-feedback::before {
  content: '✨';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24px;
  animation: sparkle 1s ease-in-out infinite alternate;
}

.run-feedback::after {
  content: '✨';
  position: absolute;
  right: -10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24px;
  animation: sparkle 1s ease-in-out infinite alternate 0.5s;
}

@keyframes success-celebration {
  0% { 
    transform: scale(0.8) translateY(20px) rotate(-5deg); 
    opacity: 0; 
  }
  50% { 
    transform: scale(1.1) translateY(-5px) rotate(2deg); 
  }
  100% { 
    transform: scale(1) translateY(0) rotate(0deg); 
    opacity: 1; 
  }
}

@keyframes sparkle {
  0% { 
    transform: translateY(-50%) scale(1) rotate(0deg); 
    opacity: 0.7; 
  }
  100% { 
    transform: translateY(-50%) scale(1.2) rotate(10deg); 
    opacity: 1; 
  }
}

.knight-position {
  animation: knight-bounce 1s ease-in-out infinite alternate !important;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb) !important;
  border-color: #2196f3 !important;
  box-shadow: 
    0 4px 20px rgba(33, 150, 243, 0.4),
    0 0 20px rgba(33, 150, 243, 0.2) !important;
  transform: scale(1.1) !important;
  z-index: 5;
}

/* 骑士移动时的轨迹效果 */
.knight-position::after {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border: 2px solid #2196f3;
  border-radius: 12px;
  opacity: 0.3;
  animation: knight-trail 0.8s ease-out infinite;
}

@keyframes knight-trail {
  0% { 
    transform: scale(1); 
    opacity: 0.5; 
  }
  100% { 
    transform: scale(1.3); 
    opacity: 0; 
  }
}

.intro-modal {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  background: rgba(0, 0, 0, 0.8) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 1000 !important;
}

.intro-content {
  background: #fff;
  border-radius: 18px;
  padding: 36px 40px 28px 40px;
  min-width: 340px;
  max-width: 90vw;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18), 0 1.5px 0 rgba(76,151,255,0.08);
  color: #333;
  text-align: left;
  font-size: 18px;
  line-height: 1.7;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.intro-content h2 {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 18px;
  color: #4c97ff;
}

.intro-content h3 {
  font-size: 20px;
  margin: 18px 0 8px 0;
  color: #ffab19;
}

.intro-content ul {
  margin: 0 0 10px 18px;
  padding: 0;
}

.intro-content li {
  margin-bottom: 4px;
}

.intro-confirm {
  margin-top: 18px;
  background: linear-gradient(45deg, #4c97ff, #667eea);
  color: #fff;
  border: none;
  border-radius: 22px;
  padding: 10px 28px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(76, 151, 255, 0.18);
  transition: background 0.2s, transform 0.2s;
}
.intro-confirm:hover {
  background: linear-gradient(45deg, #667eea, #4c97ff);
  transform: translateY(-2px) scale(1.04);
}
</style>
