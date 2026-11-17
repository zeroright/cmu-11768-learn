/* CMU 11-768 learning routes: 4 phases / 3 tracks derived from cmu-agents notes. */
(function () {
  const lessons = {
    L01: ['建立 Agent 的坐标系','用 Russell-Norvig 定义说清 agent = 模型 + 工具 + 环境 + 循环，并列出 6 项能力。',[],'react_loop.py'],
    L02: ['把 token 变成动作','解释 tool call 如何经 chat template 成 token、harness 如何执行、结果如何回写。',['L01'],'tool_call_parse.py'],
    L03: ['管理长上下文','比较无损压缩 / ReSum / KV cache 三种策略在长任务中的取舍。',['L02'],'context_compact.py'],
    L04: ['设计技能与记忆','区分 memory（过程性/事实性）与 skill，并说明何时用哪一种。',['L03'],'memory_skill_router.py'],
    L05: ['拆解规划与多 Agent','比较 plan-and-execute 与 ReAct，列出多 agent 协调的接口成本。',['L04'],'plan_and_act.py'],
    L06: ['理解 Coding Agent 循环','追踪 locate → edit → test → iterate 的反馈闭环，指出 harness 的关键作用。',['L05'],'swe_patch_loop.py'],
    L07: ['评估 Computer Use','说明 DOM/截图/VNC 三种接入方式的优缺点与 grounding 难度。',['L05'],'cua_step_log.py'],
    L08: ['理解 SFT 在 Agent 里的作用','区分 imitation SFT 与 rejection sampling 产生的演示数据。',['L06','L07']],
    L09: ['建立 RL 的最低词汇','说清 state/action/reward/trajectory 在 agent 语境下的含义。',['L08'],'grpo_advantage.py'],
    L10: ['构建 Deep Research 流程','把 question → sub-question → retrieval → synthesis 画成可控流水线。',['L05','L06']],
    L11: ['读懂高级 RL 算法','比较 PPO / GRPO / DPO 在 agent 任务中的奖励稀疏问题。',['L09']],
    L12: ['理解 RL 系统开销','说清 rollout 与 train 的资源不匹配如何影响吞吐。',['L11']],
    L13: ['识别 Agent 失效模式','用「能力 ≠ 安全」的视角列出 sandbox/凭证/监控/策略四层漏洞。',['L01','L06']],
    L14: ['拆解 OpenHands 工程结构','定位 agent loop / sandbox / observation / skill 的实现位置。',['L06','L13']],
    L15: ['把 Agent 工程化上线','写出编排、重试、监控、成本四个 SLO 维度。',['L13','L14']]
  };
  const phases = [
    {title:'理解 Agent 的本质', ids:['L01','L02'], output:'用四要素定义你自己的 Agent 用例；列出 agent ≠ chatbot 的证据。', work:'playground.html?ex=tool_call_parse.py', label:'运行 tool_call 解析示例'},
    {title:'掌握能力与上下文', ids:['L03','L04','L05'], output:'给出长任务下上下文、记忆、规划三层的设计取舍。', work:'playground.html?ex=context_compact.py', label:'运行上下文压缩示例'},
    {title:'领域 + 训练两条腿', ids:['L06','L07','L08','L09','L10','L11','L12'], output:'为 Coding / GUI / Research 各画一张闭环图，并说明奖励信号来源。', work:'playground.html?ex=swe_patch_loop.py', label:'运行 SWE 反馈环示例'},
    {title:'安全与工程化', ids:['L13','L14','L15'], output:'提交一份「上线前清单」：sandbox、凭证、监控、回退、成本。', work:'homework.html#hw3', label:'对照课程项目验收'}
  ];
  const tracks = {
    full:{title:'系统学习', duration:'8 周参考节奏', intro:'适合要把 Agent 从概念做到工程落地的学习者。15 讲全量，含训练与上线两条线。', ids:phases.flatMap(p=>p.ids), outcome:'3 个领域闭环图 + 一份上线前检查清单', phases},
    builder:{title:'工程实践', duration:'4 周参考节奏', intro:'重点是 harness、工具、上下文、领域闭环与上线；训练讲次可后置。', ids:['L01','L02','L03','L04','L05','L06','L07','L10','L13','L14','L15'], outcome:'一个可运行 Agent + 一份监控/成本方案', phases:[
      {title:'Agent 骨架',ids:['L01','L02'],output:'跑通 ReAct 循环并说明 harness 角色。',work:'playground.html?ex=react_loop.py',label:'运行 ReAct 示例'},
      {title:'上下文与技能',ids:['L03','L04'],output:'设计上下文压缩与记忆接口。',work:'playground.html?ex=memory_skill_router.py',label:'运行记忆路由示例'},
      {title:'领域落地',ids:['L05','L06','L07','L10'],output:'为一个领域写出工具集与评测指标。',work:'playground.html?ex=swe_patch_loop.py',label:'运行 SWE 示例'},
      {title:'安全与上线',ids:['L13','L14','L15'],output:'提交 sandbox + 监控 + 成本预算。',work:'assignments.html',label:'选综合项目'}]},
    pm:{title:'产品与交付', duration:'按项目推进', intro:'面向 AI 产品 / 解决方案：重点在能力边界、用户体验、验收与成本，训练讲次仅需 L01、L13。', ids:['L01','L02','L04','L05','L10','L13','L15'], outcome:'一页产品方案 + 验收指标 + 成本预估', phases:[
      {title:'定义 Agent 边界',ids:['L01','L02'],output:'写出用户任务、可验证的成功条件、权限边界。',work:'playground.html?ex=tool_call_parse.py',label:'运行调用解析示例'},
      {title:'用户体验与编排',ids:['L04','L05','L10'],output:'画出人机介入点、计划展示、研究溯源的产品形态。',work:'homework.html#hw3',label:'对照课程项目要求'},
      {title:'安全与验收',ids:['L13','L15'],output:'提交验收指标、监控指标、成本上限。',work:'assignments.html',label:'选业务延伸项目'}]}
  };
  window.LEARNING = {lessons,tracks,midterms:[],
    source(id){return SITE_META.lectures[id].youtube?'视频教案 · YT':'Slides 补读';},
    coverage(p,k){return 1-Math.pow(1-p,k);},
    advantages(rewards){const mean=rewards.reduce((a,b)=>a+b,0)/rewards.length;const sd=Math.sqrt(rewards.reduce((s,r)=>s+(r-mean)**2,0)/rewards.length);return rewards.map(r=>sd?(r-mean)/sd:0);}
  };
})();
