# CMU 11-768 AI Agents 自学教学网站

纯静态站点：用浏览器打开 `index.html`，或在仓库根目录起一个静态服务器。讲次正文在 `data/lectures/L01.js` … `L15.js`，每个讲次页只加载自己的那一篇。

推荐：

```bash
cd cmu-11768-learn
python3 -m http.server 8765
```

然后访问 http://127.0.0.1:8765/

## 学习体验

- 首页集中显示继续学习与全部讲次；学习路径页选择系统学习 / 工程实践 / 产品与交付三条路线。
- 实践中心进入课程作业、综合项目、机制实验与源码对照；论文、术语和搜索在资源菜单中。
- `learning-lab.html` 提供采样与验证、工具反馈、GRPO 优势三个自编交互实验，无需 API。
- 讲次页通过学习指南进入阅读、实验、自测和实践；阅读进度与阶段交付物分别记录在浏览器中。

- 官方课程站与课表来源：https://www.cmu-agents.com
- 中文讲义素材仓库：https://github.com/xbsheng/cmu-agents
- 自编练习/自测/闪卡/综合项目均标注「自编」
- Pyodide 代码运行需能访问 jsDelivr CDN（本地 server 模式）

## 幻灯配图来源与版权

本站讲次页中的幻灯缩略图来自 **CMU 11-768 AI Agents** 官方公开幻灯（PDF 逐页渲染为 ≤1344px WebP），仅供个人学习与复习。

- 版权归原作者 / 授课方（CMU 11-768 / Daniel Fried / Graham Neubig）。
- 每张配图附信用语「CMU 11-768 课程幻灯 · 版权归原作者」，并链回官方 slides PDF。
- 请勿二次分发为商业素材；如需正式课件请以官方渠道为准。
