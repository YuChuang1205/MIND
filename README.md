<div align="center">
  <h1 style="border-bottom: none;">MIND: Multi-rationale INtegrated Discriminative Reasoning Framework for Multi-modal Large Models</h1>
</div>

<div align="center">
  <p>
    <a href="https://scholar.google.com/citations?user=Dd4_VW8AAAAJ&hl=zh-CN" target="_blank">Chuang Yu</a><sup>1,2</sup>,
    <a href="https://scholar.google.com/citations?user=3cBa6r4AAAAJ&hl=zh-CN" target="_blank">Jinmiao Zhao</a><sup>1,2</sup>,&nbsp
    <a>Mingxuan Zhao</a><sup>3</sup>,&nbsp
    <a>Yunpeng Liu</a><sup>1*</sup>,&nbsp
    <a>Xiujun Shu</a><sup>4</sup>,
    <br>
    <a>Yuanhao Feng</a><sup>4</sup>,&nbsp
    <a>Bo Wang</a><sup>4</sup>,&nbsp
    <a href="https://xyue.io/" target="_blank">Xiangyu Yue</a><sup>5*</sup>
  </p>
  <p>
    <sup>1</sup> Shenyang Institute of Automation, Chinese Academy of Sciences
     <br>
    <sup>2</sup> University of Chinese Academy of Sciences &nbsp;&nbsp;
     <br>
    <sup>3</sup> HKUST(GZ) &nbsp;&nbsp;
    <sup>4</sup> Tencent &nbsp;&nbsp;
    <sup>5</sup> MMLab, The Chinese University of Hong Kong
  </p>
</div>


## ✅ Abstract
Recently, multimodal large language models (MLLMs) have been widely applied to reasoning tasks. However, they suffer from limited multi-rationale semantic modeling, insufficient logical robustness, and are susceptible to misleading interpretations in complex scenarios. Therefore, we propose a **Multi-rationale INtegrated Discriminative (MIND) reasoning framework**, which is designed to endow MLLMs with human-like cognitive abilities of **“Understand → Rethink → Correct”**, and achieves a paradigm evolution from passive imitation-based reasoning to active discriminative reasoning. Specifically, we introduce a Rationale Augmentation and Discrimination (RAD) paradigm, which automatically and efficiently expands existing datasets by generating diverse rationales, providing a unified and extensible data foundation. Meanwhile, we design a Progressive Two-stage Correction Learning (P2CL) strategy. The first phase enhances multi-rationale positive learning, while the second phase enables active logic discrimination and correction. In addition, to mitigate representation entanglement in the multi-rationale semantic space, we propose a Multi-rationale Contrastive Alignment (MCA) optimization strategy, which achieves semantic aggregation of correct reasoning and boundary separation of incorrect reasoning. Extensive experiments demonstrate that the proposed MIND reasoning framework achieves state-of-the-art (SOTA) performance on multiple public datasets covering scientific, commonsense, and mathematical scenarios. It provides a new perspective for advancing MLLMs towards higher levels of cognitive intelligence.


<!-- <div align="center">
<br>
  <img width="80%" src="imgs/MIND-Understand-Rethink-Correct.png" alt="MIND-Understand-Rethink-Correct">
<br>
  <b><span style="font-size: 40px;">Understand → Rethink → Correct</span></b>
</div> -->

## 🚀 Overview
<div align="center">
<br>
  <img width="100%" src="imgs/MIND-Overview.png" alt="MIND Overview">
<br>
</div>



## ✅ TODO List
We are finalizing the release of the paper, dataset and code and aim to complete it as soon as possible. Please stay tuned! ⚡⚡⚡
- [ ] Release paper.
- [ ] Release training and inference code.
- [ ] Release ScienceQA-RAD, V-OKVQA-RAD, and M3CoT-RAD  datasets.
- [ ] Release model weights.
