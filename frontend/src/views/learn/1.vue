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
      <!-- 左侧：积木区 -->
      <div class="scratch-blocks-panel">
        <div class="blocks-header">
          <span>编程区</span>
        </div>
        <div ref="scratchBlocksDiv" class="scratch-blocks-div"></div>
      </div>
      <!-- 右侧：舞台区 -->
      <div class="scratch-stage-panel">
        <div class="stage-toolbar">
          <el-button icon="el-icon-caret-right" size="small" circle class="flag-btn" />
          <span class="stage-mode">打开加速模式</span>
        </div>
        <div class="stage-area">
          <img class="stage-bg" :src="stageBg" />
          <img
            class="rainbow"
            :src="rainbowImg"
            :style="{
              left: spriteX + 200 + 'px',
              top: spriteY + 90 + 'px',
              width: spriteSize * 1.2 + 'px',
              height: 'auto',
              transform: 'rotate(' + (spriteDir - 90) + 'deg)',
              transition: 'all 0.3s'
            }"
          />
        </div>
        <div class="sprite-panel">
          <div class="sprite-info">
            <span>角色</span>
            <input class="sprite-name" v-model="spriteName" />
            <span>x</span><input class="sprite-xy" v-model="spriteX" />
            <span>y</span><input class="sprite-xy" v-model="spriteY" />
            <span>大小</span><input class="sprite-size" v-model="spriteSize" />
            <span>方向</span><input class="sprite-dir" v-model="spriteDir" />
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
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import bg1 from '@/assets/bgs/bg1.png'
import role1 from '@/assets/role/role1.png'

const projectTitle = ref('画彩虹')
const spriteName = ref('彩虹')
const spriteX = ref(0)
const spriteY = ref(0)
const spriteSize = ref(100)
const spriteDir = ref(90)
const stageBg = ref(bg1)
const rainbowImg = ref(role1)

const scratchBlocksDiv = ref<HTMLDivElement | null>(null)

onMounted(() => {
  // 延迟初始化，确保 ScratchBlocks 完全加载
  setTimeout(() => {
    initScratchBlocks()
  }, 100)
})

function initScratchBlocks() {
  // @ts-ignore
  if (scratchBlocksDiv.value && window.ScratchBlocks) {
    try {
      // @ts-ignore
      window.ScratchBlocks.inject(scratchBlocksDiv.value, {
        toolbox: `
          <xml>
            <category name="事件" colour="#FFD500">
              <block type="event_whenflagclicked"></block>
              <block type="event_whenkeypressed"></block>
            </category>
            <category name="动作" colour="#4C97FF">
              <block type="motion_movesteps"></block>
              <block type="motion_turnright"></block>
              <block type="motion_turnleft"></block>
              <block type="motion_goto"></block>
              <block type="motion_gotoxy"></block>
              <block type="motion_glideto"></block>
              <block type="motion_pointindirection"></block>
              <block type="motion_changexby"></block>
              <block type="motion_setx"></block>
              <block type="motion_changeyby"></block>
              <block type="motion_sety"></block>
            </category>
            <category name="外观" colour="#9966FF">
              <block type="looks_sayforsecs"></block>
              <block type="looks_say"></block>
              <block type="looks_thinkforsecs"></block>
              <block type="looks_think"></block>
              <block type="looks_switchcostumeto"></block>
              <block type="looks_nextcostume"></block>
              <block type="looks_changeeffectby"></block>
              <block type="looks_seteffectto"></block>
              <block type="looks_cleargraphiceffects"></block>
              <block type="looks_show"></block>
              <block type="looks_hide"></block>
            </category>
            <category name="控制" colour="#FFAB19">
              <block type="control_wait"></block>
              <block type="control_repeat"></block>
              <block type="control_forever"></block>
              <block type="control_if"></block>
              <block type="control_if_else"></block>
              <block type="control_wait_until"></block>
              <block type="control_repeat_until"></block>
              <block type="control_stop"></block>
            </category>
            <category name="运算" colour="#40BF4A">
              <block type="operator_add"></block>
              <block type="operator_subtract"></block>
              <block type="operator_multiply"></block>
              <block type="operator_divide"></block>
              <block type="operator_random"></block>
              <block type="operator_gt"></block>
              <block type="operator_lt"></block>
              <block type="operator_equals"></block>
              <block type="operator_and"></block>
              <block type="operator_or"></block>
              <block type="operator_not"></block>
              <block type="operator_join"></block>
              <block type="operator_letter_of"></block>
              <block type="operator_length"></block>
              <block type="operator_mod"></block>
              <block type="operator_round"></block>
              <block type="operator_mathop"></block>
            </category>
            <category name="变量" colour="#FF8C1A" custom="VARIABLE"></category>
            <category name="画笔" colour="#0FBD8C">
              <block type="pen_clear"></block>
              <block type="pen_stamp"></block>
              <block type="pen_pendown"></block>
              <block type="pen_penup"></block>
              <block type="pen_setpencolortocolor"></block>
              <block type="pen_changepencolorby"></block>
              <block type="pen_setpensizeto"></block>
              <block type="pen_changepensizeby"></block>
            </category>
          </xml>
        `,
        trashcan: true,
        zoom: { controls: true, wheel: true }
      })
      console.log('ScratchBlocks 初始化成功')
    } catch (error) {
      console.error('ScratchBlocks 初始化失败:', error)
      // 如果还是失败，重试
      setTimeout(() => {
        initScratchBlocks()
      }, 500)
    }
  } else {
    console.log('ScratchBlocks 还未加载，等待重试...')
    // 如果 ScratchBlocks 还未加载，继续等待
    setTimeout(() => {
      initScratchBlocks()
    }, 200)
  }
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
  background: #e0e7ef;
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
}
.rainbow {
  position: absolute;
  left: 60px;
  top: 30px;
  width: 360px;
  height: 180px;
  z-index: 2;
}
.sprite-panel {
  background: #f8fafc;
  border-radius: 8px;
  padding: 8px 12px;
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
</style>