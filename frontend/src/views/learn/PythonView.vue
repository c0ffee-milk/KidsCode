<template>
  <div class="python-main">
    <div class="python-toolbar">
      <h1>Python闯关 - {{ levels[currentLevel].name }}</h1>
      <span class="level-desc">{{ levels[currentLevel].desc }}</span>
    </div>
    <div class="python-content">
      <!-- 左侧 Blockly 拖拽区 -->
      <div class="python-blocks-panel">
        <div v-if="loadingBlockly" class="blockly-loading">
          <span>正在加载编程区，请稍候...</span>
        </div>
        <div class="blocks-header">
          <span>编程区</span>
          <div class="header-buttons">
            <button @click="initBlockly" class="init-btn">重新初始化</button>
          </div>
        </div>
        <div ref="blocklyDiv" class="python-blocks-div"></div>
      </div>
      <!-- 右侧地图舞台区 -->
      <div class="python-stage-panel">
        <div class="stage-toolbar">
          <button class="flag-btn" @click="runCode">运行</button>
          <span class="stage-mode">拖拽积木并运行，骑士将自动到达终点</span>
          <button v-if="currentLevel < levels.length - 1" @click="nextLevel" class="init-btn">下一关</button>
        </div>
        <div class="stage-area">
          <h3>关卡地图 - {{ levels[currentLevel].name }}</h3>
          <div v-for="(row, rowIdx) in mapData" :key="rowIdx" class="map-row">
            <span
              v-for="(cell, idx) in row"
              :key="idx"
              :class="cellClass(cell, idx, rowIdx)"
            >
              {{ cellSymbol(cell, idx, rowIdx) }}
            </span>
          </div>
          <div class="map-desc">
            <span class="start">🏇 起点</span>
            <span class="end">🏁 终点</span>
            <span class="empty">⬜ 路径</span>
            <span style="color:#b71c1c;">🧱 障碍</span>
          </div>
        </div>
        <div v-if="showFeedback" class="run-feedback">🎉 恭喜你，骑士已到达终点！</div>
      </div>
    </div>
    <div v-if="showIntro" class="intro-modal">
      <div class="intro-content">
        <h2>{{ levels[currentLevel].intro.title }}</h2>
        <h3>教学目标</h3>
        <ul>
          <li v-for="goal in levels[currentLevel].intro.goals" :key="goal">{{ goal }}</li>
        </ul>
        <h3>关卡规则</h3>
        <ul>
          <li v-for="rule in levels[currentLevel].intro.rules" :key="rule">{{ rule }}</li>
        </ul>
        <h3>编程提示</h3>
        <ul>
          <li v-for="tip in levels[currentLevel].intro.tips" :key="tip">{{ tip }}</li>
        </ul>
        <button class="intro-confirm" @click="showIntro = false">我已了解，开始闯关</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, inject } from 'vue'
import { useRoute } from 'vue-router'
import * as Blockly from 'blockly'
import 'blockly/javascript'

// 注入 AI 助手方法
const showAIError = inject('showAIError')

// 每关的标准错误类型数据
const levelErrors = [
  // 第一关
  [
    {
      type: 'out_of_map',
      position: [0, 10],
      message: '🚫 骑士走出地图右边界（第0行第10列），应该停止并往左走。'
    },
    {
      type: 'not_arrive_end',
      message: '⚠️ 骑士还没有到达终点（第0行第9列），请继续往右走。'
    },
    {
      type: 'wrong_steps',
      message: '💡 提示：本关需要9步才能到达终点，请检查步数设置。'
    }
  ],
  // 第二关
  [
    {
      type: 'out_of_map',
      position: [0, 11],
      message: '🚫 骑士走出地图右边界（第0行第11列），应该停止并往左走。'
    },
    {
      type: 'not_arrive_end',
      message: '⚠️ 骑士还没有到达终点（第0行第10列），请继续往右走。'
    },
    {
      type: 'wrong_steps',
      message: '💡 提示：本关需要10步才能到达终点，建议使用"骑士向前移动N步"积木。'
    }
  ],
  // 第三关
  [
    {
      type: 'hit_obstacle',
      position: [2, 3],
      message: '🧱 骑士撞到障碍物（第2行第3列），建议往上或下绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [0, 2],
      message: '🧱 骑士撞到障碍物（第0行第2列），建议往下绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [0, 6],
      message: '🧱 骑士撞到障障碍物（第0行第6列），建议往下或左绕开。'
    },
    {
      type: 'wrong_path',
      message: '🤔 路径规划错误，需要使用判断语句绕过障碍物。'
    }
  ],
  // 第四关
  [
    {
      type: 'hit_obstacle',
      position: [2, 3],
      message: '🧱 骑士撞到障碍物（第2行第3列），建议往上走。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 1],
      message: '🧱 骑士撞到障碍物（第1行第1列），建议往下或右绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [0, 9],
      message: '🧱 骑士撞到障障碍物（第0行第9列），建议往下或左绕开。'
    },
    {
      type: 'complex_path',
      message: '🔄 障碍物较多，建议使用while循环+if判断组合进行路径规划。'
    }
  ],
  // 第五关
  [
    {
      type: 'hit_obstacle',
      position: [2, 3],
      message: '🧱 骑士撞到障碍物（第2行第3列），建议往上或下绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 4],
      message: '🧱 骑士撞到障碍物（第1行第4列），建议往下或左绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 7],
      message: '🧱 骑士撞到障碍物（第1行第7列），建议绕开障碍群。'
    },
    {
      type: 'ultimate_challenge',
      message: '🏆 终极挑战！地图更大障碍更多，需要灵活运用循环、判断和变量。'
    }
  ],
  // 第六关
  [
    {
      type: 'hit_obstacle',
      position: [2, 6],
      message: '🧱 骑士撞到障碍物（第2行第6列），建议往上或左绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 1],
      message: '🧱 骑士撞到障碍物（第1行第1列），建议往下或右绕开。'
    },
    {
      type: 'branch_choice',
      message: '🛤️ 分岔路线选择：有多条路线可选，需要用if判断选择最优路线。'
    }
  ],
  // 第七关
  [
    {
      type: 'hit_obstacle',
      position: [0, 1],
      message: '🧱 骑士撞到障碍物（第0行第1列），建议往下或右绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 2],
      message: '🧱 骑士撞到障碍物（第1行第2列），建议往上或下绕开。'
    },
    {
      type: 'nested_loop',
      message: '🔄 障碍物分布复杂，建议使用嵌套循环解决路径问题。'
    }
  ],
  // 第八关
  [
    {
      type: 'hit_fog',
      position: [0, 1],
      message: '🌫️ 骑士走进迷雾（第0行第1列），建议尝试其它方向绕开迷雾。'
    },
    {
      type: 'hit_fog',
      position: [0, 5],
      message: '🌫️ 骑士走进迷雾（第0行第5列），建议尝试其它方向绕开迷雾。'
    },
    {
      type: 'hit_fog',
      position: [2, 4],
      message: '🌫️ 骑士走进迷雾（第2行第4列），建议尝试其它方向绕开迷雾。'
    },
    {
      type: 'fog_challenge',
      message: '🌫️ 迷雾挑战：部分区域不可见，需要多尝试不同路线！'
    }
  ],
  // 第九关
  [
    {
      type: 'hit_obstacle',
      position: [0, 2],
      message: '🧱 骑士撞到障碍物（第0行第2列），建议往下绕开。'
    },
    {
      type: 'hit_obstacle',
      position: [1, 7],
      message: '🧱 骑士撞到障碍物（第1行第7列），建议绕开障碍群。'
    },
    {
      type: 'global_planning',
      message: '🗺️ 全局规划：终点隐藏在角落，需要先分析地图再编程！'
    }
  ],
  // 第十关
  [
    {
      type: 'hit_obstacle',
      position: [0, 2],
      message: '🧱 骑士撞到障碍物（第0行第2列），建议往下绕开。'
    },
    {
      type: 'hit_fog',
      position: [0, 1],
      message: '🌫️ 骑士走进迷雾（第0行第1列），建议尝试其它方向。'
    },
    {
      type: 'hit_fog',
      position: [2, 4],
      message: '🌫️ 骑士走进迷雾（第2行第4列），建议绕开迷雾区域。'
    },
    {
      type: 'ultimate_maze',
      message: '🎯 终极迷宫：障碍、迷雾、分岔全部出现，综合运用所有编程知识！'
    }
  ]
]

// 显示当前关卡的所有标准错误
function showCurrentLevelErrors() {
  const errors = levelErrors[currentLevel.value] || []
  if (errors.length === 0) {
    showAIError && showAIError(`😅 第${currentLevel.value + 1}关暂无标准错误数据`)
    return
  }
  
  // 发送关卡介绍
  showAIError && showAIError(`🎮 第${currentLevel.value + 1}关 - ${levels[currentLevel.value].name} 标准错误分析：`)
  
  // 逐个发送错误信息
  errors.forEach((error, index) => {
    setTimeout(() => {
      showAIError && showAIError(error.message)
    }, (index + 1) * 500) // 每0.5秒发送一条
  })
  
  // 最后发送总结
  setTimeout(() => {
    showAIError && showAIError(`💡 以上是第${currentLevel.value + 1}关的常见错误，遇到问题时可以参考这些提示哦！`)
  }, (errors.length + 1) * 500)
}

// 根据错误类型显示具体错误
function showStandardError(type, row, col) {
  const errors = levelErrors[currentLevel.value] || []
  let msg = ''
  
  // 查找匹配的错误
  if (type === 'hit_obstacle' || type === 'hit_fog' || type === 'out_of_map') {
    const err = errors.find(e => e.type === type && e.position && e.position[0] === row && e.position[1] === col)
    if (err) msg = err.message
  } else {
    const err = errors.find(e => e.type === type)
    if (err) msg = err.message
  }
  
  // 如果没找到匹配的，使用默认提示
  if (!msg) {
    if (type === 'hit_obstacle') msg = `🧱 骑士撞到了障碍物（第${row}行第${col}列），请尝试其它方向绕开。`
    if (type === 'hit_fog') msg = `🌫️ 骑士走进了迷雾（第${row}行第${col}列），请尝试其它方向绕开。`
    if (type === 'out_of_map') msg = `🚫 骑士走出了地图边界（第${row}行第${col}列），请回到地图内。`
    if (type === 'not_arrive_end') msg = `⚠️ 骑士还没有到达终点，请继续寻路。`
  }
  
  showAIError && showAIError(msg)
}

// 暴露给全局使用
window.showCurrentLevelErrors = showCurrentLevelErrors

const levels = [
  {
    name: '第一关',
    desc: '骑士直线前进，体验编程的乐趣。',
    map: [[1, 0, 0, 0, 0, 0, 0, 0, 0, 2]],
    intro: {
      title: '第一关：直线前进',
      goals: [
        '了解编程闯关的基本玩法',
        '让骑士从起点走到终点',
        '体验拖拽式编程'
      ],
      rules: [
        '骑士初始在起点（🏇），目标是到达终点（🏁）',
        '每次只能前进一格',
        '请用“骑士向前移动一步”完成闯关'
      ],
      tips: [
        '拖拽“动作”积木到编程区',
        '点击右侧“运行”按钮，观察骑士前进',
        '如遇问题可点击“重新初始化”重置编程区'
      ]
    }
  },
  {
    name: '第二关',
    desc: '本关引入多步移动，体验参数积木的用法。',
    map: [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]],
    intro: {
      title: '第二关：多步移动',
      goals: [
        '学会使用带参数的积木',
        '让骑士一次性前进多步到达终点'
      ],
      rules: [
        '骑士初始在起点（🏇），目标是到达终点（🏁）',
        '可以使用“骑士向前移动N步”积木',
        '本关无需循环'
      ],
      tips: [
        '拖拽“骑士向前移动”积木到编程区',
        '设置步数为正确的值',
        '点击“运行”按钮，骑士会直接到达终点'
      ]
    }
  },
  {
    name: '第三关',
    desc: '本关引入障碍物，需要用判断语句绕过障碍。',
    map: [
      [0, 0, -1, 0, 0, 0, -1, 0, 0, 2],
      [0, -1, 0, 0, -1, 0, 0, 0, 0, 0],
      [1, 0, 0, -1, 0, 0, -1, 0, 0, 0]
    ],
    intro: {
      title: '第三关：障碍物闯关',
      goals: [
        '掌握if判断',
        '学会绕过障碍'
      ],
      rules: [
        '有障碍物，不能直接前进'
      ],
      tips: [
        '用判断积木绕开障碍'
      ]
    }
  },
  {
    name: '第四关',
    desc: '本关需要用循环和判断结合，绕过多个障碍到达终点。',
    map: [
      [0, 0, -1, 0, 0, 0, 0, 0, 0, -1],
      [0, -1, 0, 0, -1, 0, 0, -1, 0, 2],
      [1, 0, 0, -1, 0, 0, -1, 0, 0, 0]
    ],
    intro: {
      title: '第四关：循环与判断结合',
      goals: [
        '理解循环与判断的配合',
        '掌握复杂路径的自动寻路'
      ],
      rules: [
        '障碍物更多，需要合理规划路线',
        '可以上下左右移动'
      ],
      tips: [
        '尝试用while循环+if判断组合',
        '注意每一步都要判断是否有障碍'
      ]
    }
  },
  {
    name: '第五关',
    desc: '终极挑战！地图更大，障碍更多，考验你的编程思维。',
    map: [
      [0, 0, -1, 0, 0, 0, -1, 0, 0, 2, 0, 0],
      [0, -1, 0, 0, -1, 0, 0, -1, -1, -1, 0, 0],
      [1, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0],
      [0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
    ],
    intro: {
      title: '第五关：终极挑战',
      goals: [
        '灵活运用循环、判断和变量',
        '解决更复杂的迷宫问题'
      ],
      rules: [
        '地图更大，障碍更多',
        '需要多次判断和循环'
      ],
      tips: [
        '多用循环和判断，分步调试',
        '遇到困难可以先画出路线'
      ]
    }
  },
  {
    name: '第六关',
    desc: '引入分岔路线，选择最优路径到达终点。',
    map: [
      [0, 0, -1, 0, 0, 0, 0, 0, 2],
      [0, -1, 0, -1, 0, -1, 0, -1, 0],
      [1, 0, 0, 0, 0, 0, -1, 0, 0]
    ],
    intro: {
      title: '第六关：分岔选择',
      goals: [
        '学会选择不同路线',
        '理解分支结构'
      ],
      rules: [
        '有多条路线可选，部分路线有障碍',
        '选择最优路线到达终点'
      ],
      tips: [
        '尝试用if判断选择路线',
        '多观察地图结构'
      ]
    }
  },
  {
    name: '第七关',
    desc: '地图变大，障碍更复杂，考验循环嵌套。',
    map: [
      [0, -1, 0, 0, 0, -1, 0, 0, 2, 0, 0],
      [0, 0, -1, 0, -1, 0, -1, 0, 0, -1, 0],
      [1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
      [0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0]
    ],
    intro: {
      title: '第七关：循环嵌套',
      goals: [
        '掌握循环嵌套结构',
        '解决更复杂的路径问题'
      ],
      rules: [
        '障碍物分布更复杂',
        '需要多层循环和判断'
      ],
      tips: [
        '尝试用嵌套循环',
        '每一步都要判断是否有障碍'
      ]
    }
  },
  {
    name: '第八关',
    desc: '引入“迷雾”区域，部分路径不可见。',
    map: [
      [0, -2, -1, 0, 0, -2, 0, 0, 2, 0, 0],
      [0, 0, -2, 0, -1, 0, -2, 0, 0, -1, 0],
      [1, 0, 0, -1, -2, 0, 0, -1, 0, 0, 0],
      [0, -1, 0, 0, -1, 0, 0, 0, -2, 0, 0]
    ],
    intro: {
      title: '第八关：迷雾挑战',
      goals: [
        '应对未知区域',
        '合理规划路径'
      ],
      rules: [
        '部分区域为迷雾（🌫️），不可见',
        '需要尝试多种方案'
      ],
      tips: [
        '多尝试不同路线',
        '遇到迷雾时要小心'
      ]
    }
  },
  {
    name: '第九关',
    desc: '地图更大，终点隐藏在角落，考验全局规划。',
    map: [
      [0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 2],
      [0, -1, 0, 0, -1, 0, 0, -1, -1, -1, 0, 0],
      [1, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0],
      [0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0],
      [0, 0, 0, -1, 0, 0, 0, -1, 0, 0, -1, 0]
    ],
    intro: {
      title: '第九关：全局规划',
      goals: [
        '学会全局思考',
        '合理利用循环和判断'
      ],
      rules: [
        '终点隐藏在地图角落',
        '需要全局规划路线'
      ],
      tips: [
        '先分析地图再编程',
        '多用循环和判断'
      ]
    }
  },
  {
    name: '第十关',
    desc: '终极迷宫，障碍、迷雾、分岔全部出现，挑战极限！',
    map: [
      [0, -2, -1, 0, 0, -2, 0, 0, 2, 0, 0, -1, 0],
      [0, 0, -2, 0, -1, 0, -2, 0, 0, -1, 0, 0, 0],
      [1, 0, 0, -1, -2, 0, 0, -1, 0, 0, 0, -2, 0],
      [0, -1, 0, 0, -1, 0, 0, 0, -2, 0, 0, 0, 0],
      [0, 0, 0, -1, 0, 0, 0, -1, 0, 0, -1, 0, 0]
    ],
    intro: {
      title: '第十关：极限挑战',
      goals: [
        '综合运用所有编程知识',
        '解决最复杂的迷宫'
      ],
      rules: [
        '障碍、迷雾、分岔全部出现',
        '需要多次尝试和优化'
      ],
      tips: [
        '多用循环、判断和变量',
        '遇到困难不要放弃，多尝试'
      ]
    }
  }
]

const route = useRoute()
const currentLevel = ref(0)
const mapData = ref(JSON.parse(JSON.stringify(levels[currentLevel.value].map)))
const knightPos = ref(0)
const knightRow = ref(2) // 添加行位置记录
const blocklyDiv = ref(null)
let workspace = null
const showFeedback = ref(false)
const showIntro = ref(true)
const loadingBlockly = ref(true)
let blocklyRetryCount = 0
const MAX_BLOCKLY_RETRY = 10

function cellSymbol(cell, idx, rowIdx) {
  // 在骑士当前位置显示骑士
  if (idx === knightPos.value && rowIdx === knightRow.value) return '🏇'
  switch(cell) {
    case 2: return '🏁'
    case -4: return '✅'
    case -1: return '🧱'
    case -2: return '🌫️'
    default: return '⬜'
  }
}

function cellClass(cell, idx, rowIdx) {
  let baseClass = ''
  switch(cell) {
    case 1: baseClass = 'start'; break;
    case 2: baseClass = 'end'; break;
    case -1: baseClass = 'obstacle1'; break;
    case -4: baseClass = 'unreachable'; break;
    case -2: baseClass = 'fog'; break;
    default: baseClass = 'empty';
  }
  // 在骑士当前位置加骑士样式
  if (rowIdx === knightRow.value && idx === knightPos.value) {
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
  // 向上移动
  if (!Blockly.Blocks['move_up']) {
    Blockly.Blocks['move_up'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('骑士向上移动')
          .appendField(new Blockly.FieldNumber(1, 1, 20), 'STEPS')
          .appendField('步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向上移动指定步数')
      }
    }
    Blockly.JavaScript['move_up'] = function (block) {
      const steps = block.getFieldValue('STEPS')
      return `moveUp(${steps});\n`
    }
  }
  // 向下移动
  if (!Blockly.Blocks['move_down']) {
    Blockly.Blocks['move_down'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('骑士向下移动')
          .appendField(new Blockly.FieldNumber(1, 1, 20), 'STEPS')
          .appendField('步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向下移动指定步数')
      }
    }
    Blockly.JavaScript['move_down'] = function (block) {
      const steps = block.getFieldValue('STEPS')
      return `moveDown(${steps});\n`
    }
  }
  // 向左移动
  if (!Blockly.Blocks['move_left']) {
    Blockly.Blocks['move_left'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('骑士向左移动')
          .appendField(new Blockly.FieldNumber(1, 1, 20), 'STEPS')
          .appendField('步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向左移动指定步数')
      }
    }
    Blockly.JavaScript['move_left'] = function (block) {
      const steps = block.getFieldValue('STEPS')
      return `moveLeft(${steps});\n`
    }
  }
  // 向右移动
  if (!Blockly.Blocks['move_right']) {
    Blockly.Blocks['move_right'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('骑士向右移动')
          .appendField(new Blockly.FieldNumber(1, 1, 20), 'STEPS')
          .appendField('步')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#4C97FF')
        this.setTooltip('骑士向右移动指定步数')
      }
    }
    Blockly.JavaScript['move_right'] = function (block) {
      const steps = block.getFieldValue('STEPS')
      return `moveRight(${steps});\n`
    }
  }

  // 判断当前位置是否是障碍
  if (!Blockly.Blocks['is_obstacle']) {
    Blockly.Blocks['is_obstacle'] = {
      init: function () {
        this.appendDummyInput().appendField('当前位置是否是障碍?')
        this.setOutput(true, 'Boolean')
        this.setColour('#FFD700')
        this.setTooltip('判断当前位置是否是障碍')
      }
    }
    Blockly.JavaScript['is_obstacle'] = function () {
      return ['isObstacle()', Blockly.JavaScript.ORDER_NONE]
    }
  }

  // 判断是否到达终点
  if (!Blockly.Blocks['is_at_end']) {
    Blockly.Blocks['is_at_end'] = {
      init: function () {
        this.appendDummyInput().appendField('当前位置是否为终点?')
        this.setOutput(true, 'Boolean')
        this.setColour('#FFD700')
        this.setTooltip('判断当前位置是否为终点')
      }
    }
    Blockly.JavaScript['is_at_end'] = function () {
      return ['isAtEnd()', Blockly.JavaScript.ORDER_NONE]
    }
  }

  // 显示提示
  if (!Blockly.Blocks['show_tip']) {
    Blockly.Blocks['show_tip'] = {
      init: function () {
        this.appendDummyInput().appendField('提示').appendField(new Blockly.FieldTextInput('继续加油！'), 'TIP')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour('#8BC34A')
        this.setTooltip('显示提示信息')
      }
    }
    Blockly.JavaScript['show_tip'] = function (block) {
      const tip = block.getFieldValue('TIP')
      return `showTip("${tip}");\n`
    }
  }

  // for循环
  if (!Blockly.Blocks['for_loop']) {
    Blockly.Blocks['for_loop'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('重复')
          .appendField(new Blockly.FieldNumber(3, 1, 100), 'TIMES')
          .appendField('次')
        this.appendStatementInput('DO').appendField('执行')
        this.setColour('#FFAB19')
        this.setTooltip('for循环，重复指定次数')
      }
    }
    Blockly.JavaScript['for_loop'] = function (block) {
      const times = block.getFieldValue('TIMES')
      const branch = Blockly.JavaScript.statementToCode(block, 'DO')
      return `for(let i=0;i<${times};i++){${branch}}\n`
    }
  }

  // do-while循环
  if (!Blockly.Blocks['do_while']) {
    Blockly.Blocks['do_while'] = {
      init: function () {
        this.appendStatementInput('DO').appendField('先执行')
        this.appendValueInput('COND').setCheck('Boolean').appendField('直到')
        this.setColour('#FFAB19')
        this.setTooltip('do-while循环，先执行再判断条件')
      }
    }
    Blockly.JavaScript['do_while'] = function (block) {
      const branch = Blockly.JavaScript.statementToCode(block, 'DO')
      const cond = Blockly.JavaScript.valueToCode(block, 'COND', Blockly.JavaScript.ORDER_NONE) || 'false'
      return `do{${branch}}while(!(${cond}));\n`
    }
  }
  // while_not_end 循环
  if (!Blockly.Blocks['while_not_end']) {
    Blockly.Blocks['while_not_end'] = {
      init: function () {
        this.appendDummyInput()
          .appendField('当未到终点时重复')
        this.appendStatementInput('DO').appendField('执行')
        this.setColour('#FFAB19')
        this.setTooltip('while循环，直到到达终点')
      }
    }
    Blockly.JavaScript['while_not_end'] = function (block) {
      const branch = Blockly.JavaScript.statementToCode(block, 'DO')
      return `while(!isAtEnd()){\n${branch}}\n`
    }
  }
}

onMounted(() => {
  nextTick(() => {
    defineCustomBlocks()
    setTimeout(() => {
      initBlockly()
      resetKnightToStart() // 加这一行
    }, 300)
  })
})

// 监听路由参数变化
watch(
  () => route.query.level,
  (newLevel) => {
    if (newLevel && !isNaN(Number(newLevel))) {
      const idx = Number(newLevel) - 1
      if (idx >= 0 && idx < levels.length) {
        currentLevel.value = idx
        mapData.value = JSON.parse(JSON.stringify(levels[idx].map))
        resetKnightToStart()
        showIntro.value = true
        loadingBlockly.value = true
        setTimeout(() => {
          initBlockly()
        }, 300)
      }
    }
  },
  { immediate: true }
)

function initBlockly() {
  if (blocklyDiv.value && Blockly) {
    try {
      defineCustomBlocks();
      if (workspace) workspace.dispose()
      workspace = Blockly.inject(blocklyDiv.value, {
        toolbox: `
          <xml>
            <category name="循环" colour="#FFAB19">
              <block type="while_not_end"></block>
              <block type="for_loop"></block>
              <block type="do_while"></block>
            </category>
            <category name="动作" colour="#4C97FF">
              <block type="move_step"></block>
              <block type="move_steps"></block>
              <block type="move_up"></block>
              <block type="move_down"></block>
              <block type="move_left"></block>
              <block type="move_right"></block>
            </category>
            <category name="判断" colour="#FFD700">
              <block type="is_at_end"></block>
              <block type="is_obstacle"></block>
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
      loadingBlockly.value = false
      blocklyRetryCount = 0
    } catch (error) {
      blocklyRetryCount++
      if (blocklyRetryCount < MAX_BLOCKLY_RETRY) {
        setTimeout(() => { initBlockly() }, 500)
      } else {
        alert('Blockly 初始化多次失败，请刷新页面重试。')
      }
    }
  } else {
    blocklyRetryCount++
    if (blocklyRetryCount < MAX_BLOCKLY_RETRY) {
      setTimeout(() => { initBlockly() }, 500)
    } else {
      alert('Blockly 初始化多次失败，请刷新页面重试。')
    }
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
window.moveUp = function (steps) {
  for (let i = 0; i < steps; i++) {
    if (knightRow.value > 0 && mapData.value[knightRow.value - 1][knightPos.value] !== -1) {
      knightRow.value--
    }
  }
}
window.moveDown = function (steps) {
  for (let i = 0; i < steps; i++) {
    if (knightRow.value < mapData.value.length - 1 && mapData.value[knightRow.value + 1][knightPos.value] !== -1) {
      knightRow.value++
    }
  }
}
window.moveLeft = function (steps) {
  for (let i = 0; i < steps; i++) {
    if (knightPos.value > 0 && mapData.value[knightRow.value][knightPos.value - 1] !== -1) {
      knightPos.value--
    }
  }
}
window.moveRight = function (steps) {
  for (let i = 0; i < steps; i++) {
    if (knightPos.value < mapData.value[0].length - 1 && mapData.value[knightRow.value][knightPos.value + 1] !== -1) {
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


function resetKnightPosition() {
  let startRow = mapData.value.length - 1
  let col = mapData.value[startRow].findIndex(cell => cell === 1)
  knightPos.value = col
  knightRow.value = startRow
}

function resetKnightToStart() {
  let startRow = mapData.value.length - 1
  let col = mapData.value[startRow].findIndex(cell => cell === 1)
  knightPos.value = col
  knightRow.value = startRow
}



async function runCode() {
  // 查找起点（值为1）在最后一行的位置
  let startRow = mapData.value.length - 1
  let col = mapData.value[startRow].findIndex(cell => cell === 1)
  knightPos.value = col
  knightRow.value = startRow // 初始化骑士行位置
  showFeedback.value = false

  // 立即刷新页面，显示骑士在起点
  await nextTick()

  const map = mapData.value

  // 广度优先搜索（BFS）自动寻路，允许上下左右移动，避开障碍
  const queue = []
  const visited = Array.from({ length: map.length }, () => Array(map[0].length).fill(false))
  const prev = Array.from({ length: map.length }, () => Array(map[0].length).fill(null))

  queue.push([startRow, col])
  visited[startRow][col] = true

  let found = false
  let target = null

  const directions = [
    [0, 1],   // 右
    [0, -1],  // 左
    [-1, 0],  // 上
    [1, 0]    // 下
  ]

  while (queue.length && !found) {
    const [curRow, curCol] = queue.shift()
    if (map[curRow][curCol] === 2) {
      found = true
      target = [curRow, curCol]
      break
    }
    for (const [dr, dc] of directions) {
      const nr = curRow + dr
      const nc = curCol + dc
      if (
        nr >= 0 && nr < map.length &&
        nc >= 0 && nc < map[0].length &&
        !visited[nr][nc] &&
        map[nr][nc] !== -1
      ) {
        queue.push([nr, nc])
        visited[nr][nc] = true
        prev[nr][nc] = [curRow, curCol]
      }
    }
  }
  if(!found) {
    alert('无法到达终点，请检查路径！')
    return
  }
  // 回溯路径
  let path = []
  if (found && target) {
    let [r, c] = target
    while (!(r === startRow && c === col)) {
      path.push([r, c])
      ;[r, c] = prev[r][c]
    }
    path.push([startRow, col])
    path.reverse()
  }

  // 显示最优路径（高亮）
  // 先清除旧的路径标记
  for (let r = 0; r < map.length; r++) {
    for (let c = 0; c < map[0].length; c++) {
      if (map[r][c] === -4) map[r][c] = 0
    }
  }
  // 标记最优路径（不包括起点和终点）
  for (let i = 1; i < path.length - 1; i++) {
    const [r, c] = path[i]
    if (map[r][c] === 0) map[r][c] = -4
  }

  // 动画移动骑士
  let curRow = startRow
  let curCol = col
  for (let i = 1; i < path.length; i++) {
    const [nextRow, nextCol] = path[i]
    curRow = nextRow
    curCol = nextCol
    
    // 更新骑士的完整位置
    knightRow.value = curRow
    knightPos.value = curCol
    
    await new Promise(r => setTimeout(r, 300))
  }

  // 检查是否到达终点
  let endRow = map.findIndex(row => row.includes(2))
  let endCol = map[endRow].findIndex(cell => cell === 2)
  showFeedback.value = (curRow === endRow && curCol === endCol)
  setTimeout(() => { showFeedback.value = false }, 2000)
}


function nextLevel() {
  if (currentLevel.value < levels.length - 1) {
    currentLevel.value++
    mapData.value = JSON.parse(JSON.stringify(levels[currentLevel.value].map))
    resetKnightToStart() // 加这一行
    showIntro.value = true
    loadingBlockly.value = true
    setTimeout(() => {
      initBlockly()
    }, 300)
  }
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

.header-buttons {
  display: flex;
  gap: 12px;
}

.ai-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  font-weight: 600;
}

.ai-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
  background: linear-gradient(45deg, #ff8e53, #ff6b6b);
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
.blockly-loading {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  z-index: 10;
  background: rgba(255,255,255,0.85);
  text-align: center;
  padding: 40px 0;
  font-size: 20px;
  color: #4c97ff;
  border-radius: 0 0 20px 20px;
}

/*AI模块 */
.header-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.ai-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  font-weight: 600;
}

.ai-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
  background: linear-gradient(45deg, #ff8e53, #ff6b6b);
}

</style>
