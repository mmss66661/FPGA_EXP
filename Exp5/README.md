# 实验五 触发器电路分析与应用（Quartus 工程）

《数字电子技术基础实验（I）》实验五的完整 Quartus 工程，按讲义（`../实验5/讲义.pdf`）图 5.9、5.12、5.14、5.15、5.16、5.19 实现全部必做任务与选做任务。

已验证：Quartus Prime Lite **19.1** 下 6 个顶层（任务 1、任务 2、任务 3、keyin、两个选做）Analysis & Synthesis 均为 **0 error**；`exp5_top` 完整流程（Map/Fit/Assemble/Timing）通过并生成 `output_files/exp5.sof`。

## 环境

| 项目 | 说明 |
| --- | --- |
| EDA 工具 | Quartus Prime Lite 19.1（讲义写 17.0/18.1，19.1 亦可） |
| 器件 | MAX 10 `10M50DAF484C7G`（DE10-Lite 开发板 + 功能扩展板） |
| 工程文件 | `exp5.qpf` / `exp5.qsf`，默认顶层 `exp5_top` |
| 设计方式 | 原理图 BDF + VHDL 子模块（层次设计：子模块编译后生成 `.bsf` 符号，顶层 BDF 调用） |

## 快速开始

1. 用 Quartus Prime 打开 `exp5.qpf`。
2. **Project Navigator → Files** 里右键要测的 `.bdf`，选 **Set as Top-Level Entity**（或改 `exp5.qsf` 的 `TOP_LEVEL_ENTITY`）。
3. **Processing → Start Compilation** 编译，**Tools → Programmer** 下载 `output_files/exp5.sof`。

## 任务与文件对照

| 任务 | 顶层实体 | 主要文件 | 说明 |
| --- | --- | --- | --- |
| 任务 1：74LS74 D 触发器测试 | `exp5_t1_7474` | `exp5_t1_7474.bdf`、`exp5_t1_7474.vwf` | Sd1/Rd1 直接接低有效的 `1PRN/1CLRN`，D1→`1D`，clk1→`1CLK`，输出 Q1、Q1N |
| 任务 2：74LS112 J-K 触发器测试 | `exp5_t2_74112` | `exp5_t2_74112.bdf`、`exp5_t2_74112.vwf` | Sd1/Rd1 直接接低有效的 `1PRN/1CLRN`，J1→`1J`，K1→`1K`，clk1→`1CLK` |
| 任务 3：按键去抖动模块 | `keyin` | `keyin.bdf`、`keyin.bsf`、`keyin.vwf` | 2×DFF + 2×NOT + AND3，`k_out = Q1·/Q2·clk`，另引出 Q0/Q1/Q2 便于观察 |
| 任务 3：脉冲计数顶层 | `exp5_top` | `exp5_top.bdf` + `fenpin.vhd`、`rising_edge_detect.vhd`、`seg_show.vhd` 及其 `.bsf` | KEY0 去抖、KEY1 直通 → 或门 → 计数 → 4 位数码管显示 |
| 选做：J-K → D | `exp5_t4_jk2d` | `exp5_t4_jk2d.bdf` | J=D，K=/D |
| 选做：J-K → T | `exp5_t4_jk2t` | `exp5_t4_jk2t.bdf` | J=K=T，T=1 即 T′ |
| 工具脚本 | — | `tools/*.py` | 生成 BDF/BSF/VWF、写引脚约束、填写预习报告、导出网表检查 |

> 工程目录用 ASCII 名 `Exp5/`：Quartus 对中文文件名支持不佳（`exp3.qsf` 里那条乱码 BDF 引用就是例子），课程资料仍放在 `../实验5/`。

## 引脚分配

全部写在 `exp5.qsf` 中，与讲义表 5.3、5.6、5.9 一致。

### 任务 1（74LS74）

| 端口 | clk1 | Sd1 | Rd1 | D1 | Q1 | Q1N |
| --- | --- | --- | --- | --- | --- | --- |
| 引脚 | PIN_F15 | PIN_A7 | PIN_B8 | PIN_A14 | PIN_A8 | PIN_A9 |

### 任务 2（74LS112）

| 端口 | clk1 | Sd1 | Rd1 | J1 | K1 | Q1 | Q1N |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 引脚 | PIN_F15 | PIN_A7 | PIN_B8 | PIN_C11 | PIN_C10 | PIN_A8 | PIN_A9 |

### 任务 3（脉冲计数）

| 端口 | CLK_50M | KEY0 | KEY1 |
| --- | --- | --- | --- |
| 引脚 | PIN_P11 | PIN_W5 | PIN_AA15 |

| 数码管 | [7] DP | [6] g | [5] f | [4] e | [3] d | [2] c | [1] b | [0] a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HEX0 | D15 | C17 | D17 | E16 | C16 | C15 | E15 | C14 |
| HEX1 | A16 | B17 | A18 | A17 | B16 | E18 | D18 | C18 |
| HEX2 | A19 | B22 | C22 | B21 | A21 | B19 | A20 | B20 |
| HEX3 | D22 | E17 | D19 | C20 | C19 | E21 | E22 | F21 |

任务 1/2 与任务 3 的引脚互不冲突，共用一个 `.qsf`；切换顶层后只对相应引脚生效。

## 层次设计（模块与符号）

子模块 `keyin`、`fenpin`、`rising_edge_detect`、`seg_show` 都有同名 `.bsf` 符号文件。修改子模块后需要重新生成符号：

1. 打开子模块文件（BDF 或 VHDL），编译通过；
2. 执行 **File → Create/Update → Create Symbol Files for Current File**，保存为 `.bsf`；
3. 回到顶层 BDF，双击空白处（或点 Symbol 工具）选择该符号调用。

## 仿真波形（.vwf）怎么看

| 波形文件 | 对应顶层 |
| --- | --- |
| `exp5_t1_7474.vwf` | `exp5_t1_7474` |
| `exp5_t2_74112.vwf` | `exp5_t2_74112` |
| `keyin.vwf` | `keyin` |

1. 先把对应 `.bdf` 设为顶层，否则波形里的信号与顶层对不上。
2. **File → Open…** 选中 `.vwf`，Quartus 用**波形编辑器（Waveform Editor）**打开：左侧是信号名，右侧是时间轴上的电平，可直接看到 `clk1`、`Sd1`、`Rd1`、`D1` 等激励。
   任务 1/2 的 `Sd1`、`Rd1` 按实物按键极性设置：平时为 `1`，按下为 `0`。
3. 想看输出真正跳变：编译后点 **Tools → Run Simulation Tool → RTL Simulation**，ModelSim 会用该 `.vwf` 生成测试平台并显示 `Q1/Q1N`、`k_out/Q0~Q2` 的仿真结果；未跑仿真前输出显示 `X` 属正常。
4. `.vwf` 本质是文本，也可以用记事本/VSCode 打开，但可读性差，建议用波形编辑器。

## 电路要点

- **任务 1/2 的按键极性**：DE10-Lite 的 KEY0/KEY1（`PIN_A7`、`PIN_B8`）按下为低电平，74LS74/74LS112 的 `PRN`、`CLRN` 也是低有效，因此按键应直接接到对应引脚，不要再串非门。按下 `Sd1` 置位（Q=1），按下 `Rd1` 复位（Q=0）；两个按键不能同时按下。
- **按键去抖动**：`k_in` 经非门后串入两个由 50 Hz 时钟（反相后下降沿触发）采样的 D 触发器，与门输出 `k_out = Q1·/Q2·clk`；只有按键电平连续稳定两个采样周期才输出一个宽约 10 ms 的单脉冲，窄的抖动被滤除。
- **脉冲计数**：`rising_edge_detect` 以 `KEY_IN` 上升沿为计数时钟，4 位 BCD 级联，实现 0000~9999 计数。
- **显示**：`seg_show` 把 4 位 BCD 译成共阳七段码（`0` 点亮），小数点 `HEXx[7]` 恒为高（熄灭）。
- **对比通路**：KEY0 经 `keyin` 去抖，KEY1 只经非门直连或门；按一次 KEY1 会因抖动多计数。

## 验证记录

- 6 个顶层 `quartus_map`：全部 0 error（任务 1/2 各有 2 条寄存器等效转换类 warning，属 74 系列异步控制端在 MAX 10 上的正常提示）。
- `exp5_t1_7474`、`exp5_t2_74112` 全流程：Map / Fit / Assembler 均 0 error。
- `exp5_top` 全流程：Fitter / Assembler / Timing Analyzer 均成功，生成 `output_files/exp5.sof`。
- 网表核对（`tools/check_net.py`）：
  - `exp5_t1_7474`：`Sd1→1PRN`、`Rd1→1CLRN`、`D1→1D`、`clk1→1CLK`，置位/复位按键不再经非门。
  - `exp5_t2_74112`：`Sd1→1PRN`、`Rd1→1CLRN`、`J1→1J`、`K1→1K`、`clk1→1CLK`。
  - `keyin`：`k_in→NOT→DFF0.D`，`DFF0.Q→DFF1.D/AND3.IN1`，`DFF1.Q→NOT→AND3.IN2`，`clk→NOT→两 DFF 时钟`、`clk→AND3.IN3`，`AND3.OUT→k_out`，PRN/CLRN 接 VCC。
  - `exp5_top`：`KEY0→keyin`、`KEY1→NOT→OR2`、`OR2.OUT→KEY_sig/rising_edge_detect`、`D[15:0]→KD/SEG_show`、`HEX0~3[7:0]→引脚`、`fenpin.clk_50→keyin.clk`。

## 相关文件

- 预习报告：`../实验5/实验五 预习报告（已完成）.docx`（原模板保留未改）。
- 讲义与课件：`../实验5/讲义.pdf`、`../实验5/PPT.pdf`。
