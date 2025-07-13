<template>
  <div class="scratch-main">
    <h2>Blockly 编程测试</h2>
    
    <!-- 积木区 -->
    <div class="test-blocks-panel">
      <div class="blocks-header">
        <span>积木区</span>
        <button @click="testBlockly">初始化积木</button>
      </div>
      <div ref="blocklyDiv" class="scratch-blocks-div"></div>
    </div>
    
    <!-- 调试信息 -->
    <div class="debug-info">
      <p>Blockly 状态: {{ blocklyStatus }}</p>
      <p>错误信息: {{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const blocklyDiv = ref<HTMLDivElement | null>(null)
const blocklyStatus = ref('未初始化')
const errorMessage = ref('')

function testBlockly() {
  blocklyStatus.value = '正在测试...'
  errorMessage.value = ''
  
  // @ts-ignore
  if (window.Blockly) {
    blocklyStatus.value = 'Blockly 已加载'
    
    try {
      // @ts-ignore
      window.Blockly.inject(blocklyDiv.value, {
        toolbox: `
          <xml>
            <category name="逻辑" colour="#5C81A6">
              <block type="controls_if"></block>
              <block type="logic_compare"></block>
              <block type="logic_operation"></block>
              <block type="logic_negate"></block>
              <block type="logic_boolean"></block>
            </category>
            <category name="循环" colour="#5CA65C">
              <block type="controls_repeat_ext"></block>
              <block type="controls_for"></block>
              <block type="controls_whileUntil"></block>
            </category>
            <category name="数学" colour="#5C68A6">
              <block type="math_number"></block>
              <block type="math_arithmetic"></block>
              <block type="math_single"></block>
              <block type="math_trig"></block>
              <block type="math_constant"></block>
            </category>
            <category name="文本" colour="#5CA68D">
              <block type="text"></block>
              <block type="text_join"></block>
              <block type="text_append"></block>
              <block type="text_length"></block>
            </category>
            <category name="变量" colour="#A55B5B" custom="VARIABLE"></category>
            <category name="函数" colour="#9A5BA5" custom="PROCEDURE"></category>
          </xml>
        `,
        trashcan: true,
        zoom: {
          controls: true,
          wheel: true,
          startScale: 1.0,
          maxScale: 3,
          minScale: 0.3,
          scaleSpeed: 1.2
        },
        grid: {
          spacing: 20,
          length: 3,
          colour: '#ccc',
          snap: true
        }
      })
      blocklyStatus.value = '✅ 初始化成功！'
    } catch (error) {
      blocklyStatus.value = '❌ 初始化失败'
      errorMessage.value = String(error)
    }
  } else {
    blocklyStatus.value = '❌ Blockly 未加载'
    errorMessage.value = '请检查 index.html 中的 script 标签'
  }
}

onMounted(() => {
  // 等待 1 秒后自动初始化
  setTimeout(() => {
    testBlockly()
  }, 1000)
})
</script>

<style scoped>
.scratch-main {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.test-blocks-panel {
  background: #fff;
  border: 2px solid #ddd;
  border-radius: 8px;
  margin: 20px 0;
  overflow: hidden;
}

.blocks-header {
  background: #4c97ff;
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.blocks-header button {
  background: #fff;
  color: #4c97ff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.blocks-header button:hover {
  background: #f0f0f0;
}

.scratch-blocks-div {
  height: 500px;
  background: #f8fafc;
}

.debug-info {
  background: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.debug-info p {
  margin: 5px 0;
  font-family: monospace;
}
</style>