<template>
  <div class="scratch-main">
    <!-- 顶部工具栏 -->
    <div class="scratch-toolbar">
      <input class="project-title" v-model="projectTitle" />
      <el-button size="small" type="primary" class="toolbar-btn">取消分享</el-button>
      <div class="toolbar-right">
        <span class="user-center">我的作品</span>
        <span class="logo">Test01</span>
      </div>
    </div>
    <div class="scratch-content">
      <!-- 左侧：Blockly 拖拽区 -->
      <div class="scratch-blocks-panel">
        <div class="blocks-header">
          <span>编程区</span>
          <button @click="initBlockly" class="init-btn">重新初始化</button>
        </div>
        <!-- 新增引导提示 -->
        <div class="guide-tip">
          请拖拽“画笔”积木到编程区，然后点击右侧“运行”按钮，看看舞台会发生什么！
        </div>
        <div ref="blocklyDiv" class="scratch-blocks-div"></div>
        <!-- 在Blockly区 guide-tip 下方添加 -->
        <button class="rainbow-demo-btn" @click="insertRainbowDemo">一键生成彩虹示例</button>
      </div>
      <!-- 右侧：舞台区 -->
      <div class="scratch-stage-panel">
        <div class="stage-toolbar">
          <el-button icon="el-icon-caret-right" size="small" type="success" class="flag-btn" @click="runCode">运行</el-button>
          <span class="stage-mode">点击“运行”绘制你的彩虹</span>
          <el-button size="small" class="bg-toggle-btn" @click="toggleBg">
            切换背景
          </el-button>
        </div>
        <div class="stage-area">
          <img v-if="stageBg" class="stage-bg" :src="stageBg" />
          <canvas ref="stageCanvas" width="480" height="360" class="stage-canvas"></canvas>
        </div>
        <!-- 角色信息栏和舞台信息栏放在舞台下方 -->
        <div class="sprite-panel">
          <div class="sprite-info">
            <span>角色</span>
            <input class="sprite-name" v-model="spriteName" />
            <span>x</span><input class="sprite-xy" v-model.number="spriteX" />
            <span>y</span><input class="sprite-xy" v-model.number="spriteY" />
            <span>大小</span><input class="sprite-size" v-model.number="spriteSize" />
            <span>方向</span><input class="sprite-dir" v-model.number="spriteDir" />
          </div>
          <div class="sprite-list">
            <div class="sprite-item">
              <img :src="rainbowImg" class="sprite-thumb" />
              <span>{{ spriteName }}</span>
            </div>
          </div>
        </div>
        <div class="stage-bg-panel">
          <span>舞台</span>
          <img :src="stageBg" class="bg-thumb" />
        </div>
        <!-- 反馈提示保持在最下方 -->
        <div v-if="showFeedback" class="run-feedback">
          🎉 恭喜你，舞台已经根据你的积木绘制出彩虹啦！
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
declare global {
  interface Window {
    Blockly: any
    drawArc: any
  }
}
import { ref, onMounted, nextTick } from 'vue'
import bg from '@/assets/bgs/bg2.png'
import role1 from '@/assets/role/role1.png'
import * as Blockly from 'blockly'
window.Blockly = Blockly


const projectTitle = ref('画彩虹')
const spriteName = ref('彩虹')
const spriteX = ref(0)
const spriteY = ref(0)
const spriteSize = ref(100)
const spriteDir = ref(90)
const stageBg = ref(bg)
const rainbowImg = ref(role1)
const isWhiteBg = ref(false)

const blocklyDiv = ref<HTMLDivElement | null>(null)
const stageCanvas = ref<HTMLCanvasElement | null>(null)
let workspace: any = null

// 自定义画弧线积木
function defineCustomBlocks() {
  // @ts-ignore
  if (window.Blockly && !window.Blockly.Blocks['pen_arc']) {
    // 画弧线
    window.Blockly.Blocks['pen_arc'] = {
      init: function () {
        this.appendDummyInput()
          .appendField("画弧线 半径")
          .appendField(new window.Blockly.FieldNumber(100, 10, 240), "RADIUS")
          .appendField("起始角")
          .appendField(new window.Blockly.FieldNumber(0, 0, 360), "START")
          .appendField("结束角")
          .appendField(new window.Blockly.FieldNumber(180, 0, 360), "END")
          .appendField("颜色")
          .appendField(new window.Blockly.FieldColour("#FF0000"), "COLOR")
          .appendField("线宽")
          .appendField(new window.Blockly.FieldNumber(10, 1, 50), "WIDTH");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour("#0FBD8C");
        this.setTooltip("画一个彩虹弧线");
      }
    }
    window.Blockly.JavaScript['pen_arc'] = function (block: any) {
      const radius = block.getFieldValue('RADIUS')
      const start = block.getFieldValue('START')
      const end = block.getFieldValue('END')
      const color = block.getFieldValue('COLOR')
      const width = block.getFieldValue('WIDTH')
      return `drawArc(${radius}, ${start}, ${end}, "${color}", ${width});\n`
    }
  }
  // @ts-ignore
  if (window.Blockly && !window.Blockly.Blocks['pen_moveto']) {
    window.Blockly.Blocks['pen_moveto'] = {
      init: function () {
        this.appendDummyInput()
          .appendField("移动画笔到 x")
          .appendField(new window.Blockly.FieldNumber(240, 0, 480), "X")
          .appendField("y")
          .appendField(new window.Blockly.FieldNumber(180, 0, 360), "Y");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour("#0FBD8C");
        this.setTooltip("移动画笔到指定位置");
      }
    }
    window.Blockly.JavaScript['pen_moveto'] = function (block: any) {
      const x = block.getFieldValue('X')
      const y = block.getFieldValue('Y')
      return `moveTo(${x}, ${y});\n`
    }
  }
}

onMounted(() => {
  nextTick(() => {
    defineCustomBlocks() 
    setTimeout(() => {
      initBlockly()
    }, 500)
  })
})

function initBlockly() {
  if (blocklyDiv.value && window.Blockly) {
    try {
      if (workspace) {
        workspace.dispose()
      }
      
      workspace = window.Blockly.inject(blocklyDiv.value, {
        toolbox: `
          <xml>
            <category name="画笔" colour="#0FBD8C">
              <block type="pen_moveto"></block>
              <block type="pen_arc"></block>
            </category>
            <category name="控制" colour="#FFAB19">
              <block type="controls_repeat_ext"></block>
              <block type="controls_for"></block>
            </category>
            <category name="数学" colour="#4C97FF">
              <block type="math_number"></block>
              <block type="math_arithmetic"></block>
            </category>
          </xml>
        `,
        trashcan: true,
        zoom: { controls: true, wheel: true, startScale: 1.0, maxScale: 3, minScale: 0.3, scaleSpeed: 1.2 },
        grid: { spacing: 20, length: 3, colour: '#ccc', snap: true }
      })
      console.log('Blockly 初始化成功')
    } catch (error) {
      console.error('Blockly 初始化失败:', error)
    }
  } else {
    setTimeout(() => { initBlockly() }, 500)
  }
}

const showFeedback = ref(false)

function runCode() {
  if (workspace && stageCanvas.value) {
    const ctx = stageCanvas.value.getContext('2d')
    if (!ctx) return
    ctx.clearRect(0, 0, stageCanvas.value.width, stageCanvas.value.height)
    // 定义画弧线函数
    let centerX = 240
    let centerY = 180
    window.moveTo = function (x: number, y: number) {
      centerX = x
      centerY = y
    }
    window.drawArc = function (radius: number, start: number, end: number, color: string, width: number) {
      ctx.save()
      ctx.beginPath()
      ctx.strokeStyle = color
      ctx.lineWidth = width
      ctx.arc(centerX, centerY, radius, (start * Math.PI) / 180, (end * Math.PI) / 180)
      ctx.stroke()
      ctx.restore()
    }
    const code = window.Blockly.JavaScript.workspaceToCode(workspace)
    //若用户不写相关代码 提示用户
    if(!code.includes('drawArc')&&!code.includes('moveTo')) {
      alert('请拖拽画笔积木到编程区，并编写相关代码！')
      return
    }

    try {
      // eslint-disable-next-line no-eval
      eval(code)
      // 运行成功后显示反馈
      showFeedback.value = true
      setTimeout(() => {
        showFeedback.value = false
      }, 2000)
    } catch (e) {
      alert('代码执行出错：' + e)
    }
  }
}
// 一键生成彩虹示例函数
function insertRainbowDemo() {
  if (workspace) {
    workspace.clear()
    const xml = `
      <xml>
        <block type="pen_moveto" x="10" y="10">
          <field name="X">240</field>
          <field name="Y">180</field>
          <next>
            <block type="pen_arc">
              <field name="RADIUS">100</field>
              <field name="START">0</field>
              <field name="END">180</field>
              <field name="COLOR">#FF0000</field>
              <field name="WIDTH">12</field>
              <next>
                <block type="pen_arc">
                  <field name="RADIUS">88</field>
                  <field name="START">0</field>
                  <field name="END">180</field>
                  <field name="COLOR">#FF7F00</field>
                  <field name="WIDTH">12</field>
                  <next>
                    <block type="pen_arc">
                      <field name="RADIUS">76</field>
                      <field name="START">0</field>
                      <field name="END">180</field>
                      <field name="COLOR">#FFFF00</field>
                      <field name="WIDTH">12</field>
                      <next>
                        <block type="pen_arc">
                          <field name="RADIUS">64</field>
                          <field name="START">0</field>
                          <field name="END">180</field>
                          <field name="COLOR">#00FF00</field>
                          <field name="WIDTH">12</field>
                          <next>
                            <block type="pen_arc">
                              <field name="RADIUS">52</field>
                              <field name="START">0</field>
                              <field name="END">180</field>
                              <field name="COLOR">#0000FF</field>
                              <field name="WIDTH">12</field>
                              <next>
                                <block type="pen_arc">
                                  <field name="RADIUS">40</field>
                                  <field name="START">0</field>
                                  <field name="END">180</field>
                                  <field name="COLOR">#4B0082</field>
                                  <field name="WIDTH">12</field>
                                  <next>
                                    <block type="pen_arc">
                                      <field name="RADIUS">28</field>
                                      <field name="START">0</field>
                                      <field name="END">180</field>
                                      <field name="COLOR">#9400D3</field>
                                      <field name="WIDTH">12</field>
                                    </block>
                                  </next>
                                </block>
                              </next>
                            </block>
                          </next>
                        </block>
                      </next>
                    </block>
                  </next>
                </block>
              </next>
            </block>
          </next>
        </block>
      </xml>
    `
    const xmlDom = Blockly.utils.xml.textToDom(xml)
    Blockly.Xml.domToWorkspace(xmlDom, workspace)
    // 自动运行
    setTimeout(() => {
      runCode()
    }, 300)
  }
}

function toggleBg() {
  isWhiteBg.value = !isWhiteBg.value
  stageBg.value = isWhiteBg.value ? '' : bg
}
</script>

<style scoped>
.scratch-main {
  background: #f4f7fb;
  min-height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}
.scratch-toolbar {
  display: flex;
  align-items: center;
  background: #4c97ff;
  padding: 0 24px;
  height: 48px;
  color: #fff;
  justify-content: space-between;
  margin-top: 100px;
}
.project-title {
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 16px;
  margin-right: 12px;
  width: 120px;
}
.toolbar-btn {
  margin-left: 12px;
}
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 24px;
}
.user-center {
  font-size: 15px;
  cursor: pointer;
}
.logo {
  font-weight: bold;
  font-size: 16px;
  color: #ffd500;
}
.scratch-content {
  display: flex;
  gap: 16px;
  padding: 24px;
}
.scratch-blocks-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  width: 420px;
  min-width: 320px;
  display: flex;
  flex-direction: column;
}
.blocks-header {
  padding: 12px 20px;
  font-weight: bold;
  color: #4c97ff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
.scratch-blocks-div {
  flex: 1;
  min-height: 500px;
  background: #f8fafc;
  border-radius: 0 0 12px 12px;
}
.scratch-stage-panel {
  flex: 1;
  min-width: 500px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
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
}
.stage-mode {
  color: #ffab19;
  font-size: 14px;
}
.stage-area {
  position: relative;
  width: 480px;
  height: 360px;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}
.stage-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  left: 0; top: 0;
  z-index: 1;
  pointer-events: none; /* 防止遮挡canvas事件 */
}
.stage-canvas {
  position: absolute;
  left: 0; top: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}
.rainbow {
  position: absolute;
  left: 60px;
  top: 30px;
  width: 360px;
  height: 180px;
  z-index: 3;
}
.sprite-panel {
  background: #f8fafc;
  border-radius: 8px;
  padding: 8px 12px;
  margin-top: 220px;
  margin-bottom: 8px;
}
.sprite-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin-bottom: 8px;
}
.sprite-name, .sprite-xy, .sprite-size, .sprite-dir {
  width: 40px;
  border: 1px solid #e0e7ef;
  border-radius: 4px;
  padding: 2px 4px;
  margin: 0 2px;
}
.sprite-list {
  display: flex;
  align-items: center;
  gap: 8px;
}
.sprite-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  border-radius: 6px;
  padding: 2px 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.sprite-thumb {
  width: 32px;
  height: 16px;
  object-fit: contain;
}
.stage-bg-panel {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border-radius: 8px;
  padding: 6px 12px;
}
.bg-thumb {
  width: 40px;
  height: 30px;
  object-fit: cover;
  border-radius: 4px;
}
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
.rainbow-demo-btn {
  background: #69c0ff;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin: 12px 0;
}
.rainbow-demo-btn:hover {
  background: #40a9ff;
}
</style>