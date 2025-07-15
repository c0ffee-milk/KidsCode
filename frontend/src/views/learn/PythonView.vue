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
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4em;
  border-radius: 8px;
  border: 2px solid #ddd;
  background: #fff;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.map-row span:hover {
  transform: scale(1.1);
  z-index: 10;
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
  animation: glow 2s infinite alternate;
}

@keyframes glow {
  from { box-shadow: 0 4px 15px rgba(255, 202, 40, 0.3); }
  to { box-shadow: 0 4px 25px rgba(255, 202, 40, 0.6); }
}

.empty { 
  background: linear-gradient(135deg, #fff, #f8fafc);
  border-color: #e2e8f0;
}

.map-desc {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #666;
  justify-content: center;
  flex-wrap: wrap;
}

.map-desc span {
  background: rgba(255, 255, 255, 0.8);
  padding: 6px 12px;
  border-radius: 15px;
  border: 1px solid rgba(0,0,0,0.1);
  font-weight: 600;
}

.run-feedback {
  margin: 20px auto 0;
  background: linear-gradient(135deg, #e6fffb, #b2dfdb);
  color: #00695c;
  border: 2px solid #4db6ac;
  border-radius: 20px;
  padding: 16px 24px;
  font-size: 18px;
  text-align: center;
  width: fit-content;
  font-weight: bold;
  box-shadow: 0 4px 20px rgba(77, 182, 172, 0.3);
  animation: success 0.6s ease-out;
}

@keyframes success {
  0% { transform: scale(0.8) translateY(20px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

.intro-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.intro-content {
  background: linear-gradient(135deg, #fff, #f8fafc);
  padding: 32px;
  border-radius: 20px;
  text-align: center;
  width: 90%;
  max-width: 500px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255,255,255,0.2);
  border: 2px solid rgba(76, 151, 255, 0.2);
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.intro-content h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #4c97ff;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.intro-content h3 {
  margin: 20px 0 12px 0;
  font-size: 18px;
  color: #667eea;
  font-weight: bold;
}

.intro-content ul {
  text-align: left;
  margin: 0 0 20px 0;
  background: rgba(76, 151, 255, 0.05);
  padding: 16px;
  border-radius: 10px;
  border-left: 4px solid #4c97ff;
}

.intro-content li {
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.intro-confirm {
  background: linear-gradient(45deg, #4c97ff, #667eea);
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 30px;
  font-size: 16px;
  cursor: pointer;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(76, 151, 255, 0.3);
}

.intro-confirm:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 30px rgba(76, 151, 255, 0.4);
  background: linear-gradient(45deg, #667eea, #764ba2);
}

/* 添加一些装饰性动画 */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.python-blocks-panel {
  animation: float 6s ease-in-out infinite;
}

.python-stage-panel {
  animation: float 6s ease-in-out infinite 3s;
}
</style>
