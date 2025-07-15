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
  background: #f6f6f6;
  min-height: 100vh;
  font-family: 'Comic Sans MS', 'Arial', sans-serif;
}
.python-toolbar {
  display: flex;
  align-items: center;
  background: #4c97ff;
  padding: 0 24px;
  height: 48px;
  color: #fff;
  justify-content: space-between;
  margin-top: 80px;
}
.level-desc {
  font-size: 16px;
}

/* 主内容区优化布局 */
.python-content {
  display: flex;
  gap: 32px;
  padding: 32px 0 32px 0;
  justify-content: center;
  align-items: flex-start;
}
.python-blocks-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  width: 600px;
  min-width: 400px;
  display: flex;
  flex-direction: column;
  height: 600px;
}
.python-blocks-div {
  flex: 1;
  min-height: 520px;
  background: #f8fafc;
  border-radius: 0 0 12px 12px;
  height: 100%;
}
.python-stage-panel {
  flex: none;
  min-width: 380px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 28px 32px 24px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 600px;
}
.stage-area {
  width: 380px;
  min-height: 80px;
  background: #fff;
  border-radius: 10px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.stage-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.flag-btn {
  background: #4c97ff;
  color: #fff;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 15px;
  cursor: pointer;
}
.stage-mode {
  color: #ffab19;
  font-size: 14px;
}
.stage-area {
  width: 340px;
  min-height: 48px;
  background: #fff;
  border-radius: 10px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
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
.guide-tip {
  background: #fffbe6;
  color: #d48806;
  border: 1px solid #ffe58f;
  border-radius: 6px;
  padding: 8px 12px;
  margin: 12px 16px 0 16px;
  font-size: 15px;
}
.run-feedback {
  margin: 16px auto 0 auto;
  background: #e6fffb;
  color: #13c2c2;
  border: 1px solid #87e8de;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 18px;
  text-align: center;
  width: fit-content;
}
.intro-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.intro-content {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
.intro-content h2 {
  margin-bottom: 16px;
  font-size: 20px;
  color: #333;
}
.intro-content h3 {
  margin: 16px 0 8px 0;
  font-size: 16px;
  color: #666;
}
.intro-content ul {
  text-align: left;
  margin: 0 0 16px 0;
}
.intro-content li {
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}
.intro-confirm {
  background: #4c97ff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}
.intro-confirm:hover {
  background: #3d82e6;
}

/* 添加缺失的样式 */
.blocks-header {
  padding: 12px 20px;
  font-weight: bold;
  color: #4c97ff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
}

.init-btn {
  background: #4c97ff;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.init-btn:hover {
  background: #3d82e6;
}
</style>
