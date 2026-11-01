# 重庆大学《电子技术基础》实验 —— FPGA 代码

本仓库是重庆大学《电子技术基础》课程实验的 FPGA 设计源码，包含实验三、实验四以及若干 74 系列芯片的验证电路。设计使用 **Quartus Prime** 完成，图形部分采用 **Block Diagram/Schematic（.bdf）** 原理图输入，模块部分采用 **VHDL** 描述，并配有 ModelSim 仿真波形与脚本。

## 开发环境

| 项目 | 说明 |
| --- | --- |
| EDA 工具 | Quartus Prime Lite 17.0 / 19.1（Intel/Altera） |
| 目标器件 | MAX 10 `10M50DAF484C7G`（DE10-Lite 开发板） |
| 设计输入 | 原理图 BDF + VHDL |
| 仿真 | ModelSim / Questa（`.vwf` 波形、`.do` 脚本） |
| 工程文件 | `exp3.qpf`（工程）、`exp3.qsf`（引脚与顶层配置） |

> 引脚分配（见 `exp3.qsf`）：`clk = PIN_P11`（50 MHz 时钟）；`hex00~hex06` 与 `hex10~hex16` 对应开发板的 HEX0~HEX5 七段数码管；`qia~qid`、`qoa~qod` 对应拨码开关/输出。

## 目录结构

```
Exp3/
├── exp3.qpf / exp3.qsf        # Quartus 工程与约束文件
├── *.bdf                      # 原理图设计（各实验主电路）
├── *.bsf / *.vhd              # VHDL 模块及其原理图符号
├── *.vwf                      # 仿真波形文件
└── simulation/qsim/           # ModelSim 仿真输出与脚本
```

> 每次编译生成的 `db/`、`incremental_db/`、`output_files/`、`simulation/qsim/` 等均为中间/生成文件，已在 `.gitignore` 中排除。

## 各文件逐一说明

### 工程与配置文件

| 文件 | 意义与作用 |
| --- | --- |
| `exp3.qpf` | Quartus 工程文件，记录工程名、软件版本和修订版本（`exp3`）。是打开本工程的入口，双击即可用 Quartus Prime 打开整个项目 |
| `exp3.qsf` | Quartus 设置（约束）文件，是本工程的核心配置：目标器件 `MAX 10 10M50DAF484C7G`、默认顶层实体 `exp4-3`、输出目录 `output_files`、引脚分配（`clk=P11`、`hex00~hex06`/`hex10~hex16` 数码管、`qia~qid`/`qoa~qod` 开关与输出），以及加入工程的全部 `.bdf`/`.vwf` 文件清单 |
| `exp3_assignment_defaults.qdf` | Quartus 导出的全局赋值默认值文件，保存器件、时序等默认约束（`exp3.qsf` 顶部会引用它），一般由软件自动生成，无需手工修改 |
| `exp3_description.txt` | 实验说明文本的模板文件，用于填写本次实验的描述，当前内容为空 |
| `.gitignore` | Git 忽略规则，把编译/仿真产生的中间文件（`db/`、`output_files/`、`simulation/qsim/` 等）和临时文件排除在版本管理之外 |

### VHDL 模块及其原理图符号

每个 VHDL 文件都配有一个同名的 `.bsf` 文件，即该模块的原理图符号，供 `.bdf` 原理图以“元件”的方式调用。

| 文件 | 意义与作用 |
| --- | --- |
| `divm.vhd` / `divm.bsf` | 时钟分频器（VHDL）。常数 `m = 25 000 000`，把 50 MHz 输入时钟分频为约 1 Hz 输出 |
| `divm1.vhd` / `divm1.bsf` | 参数与 `divm` 相同的分频器（`m = 25 000 000`），作为独立元件供原理图多次例化使用 |
| `divm5.vhd` / `divm5.bsf` | 时钟分频器，`m = 5 000 000`，输出约 5 Hz 方波，用于产生较快的观察时钟 |
| `divm10.vhd` / `divm10.bsf` | 时钟分频器，`m = 2 500 000`，输出约 10 Hz 方波 |
| `hex7seg.vhd` / `hex7seg.bsf` | 4 位二进制 → 七段显示译码器（共阴，输入 `D3~D0`，输出 `S[6..0]`）。把计数器输出转换为数码管段码，供 `exp4.bdf` 例化 |

### 原理图设计文件（.bdf）

| 文件 | 意义与作用 |
| --- | --- |
| `74151_test.bdf` | 74151（8 选 1 数据选择器）功能验证电路：输入 `GN`（使能）、地址 `C/B/A`、数据 `D0~D7`（接 VCC/GND 作为固定电平），输出 `Y` |
| `74138_test.bdf` | 74138（3-8 线译码器）功能验证电路：输入地址 `A/B/C`、使能 `G1=1`、`G2A/G2B=0`，输出低有效译码结果 `Y0N~Y7N` |
| `74138_test2.bdf` | 用 74138 + 7420（双 4 输入与非门）实现 1 位全加器：输入 `A`、`B`、`CI`，输出和 `S` 与进位 `CO`。原理是用译码器输出对应真值表的最小项，再用与非门组合出 `S` 和 `CO` |
| `2-4.bdf` | 用门电路（`NOT` + `NAND3`）搭建的 2-4 线译码器：输入低有效使能 `ST_N` 与地址 `A0`、`A1`，输出低有效 `N_Y0~N_Y3`，体现用基本门实现译码功能 |
| `16-4.bdf` | 两片 74148（8-3 优先编码器）级联 + 与门构成的 16-4 线优先编码器：输入 `A[15..0]`，输出编码 `Y[3..0]` 与标志 `YEX`。高 8 位与低 8 位各用一片，用与门扩展级联位 |
| `eight.bdf` | 74151 与 74138 的组合电路：输入数据 `D0~D7`、地址 `A/B/C`、使能 `G1`，输出 `Y0N~Y7N`，实现“选择 + 译码”的组合逻辑 |
| `frequency.bdf` | 实验三主电路：由 `divm1/divm5/divm10` 产生不同频率时钟，经 74151 多路选择、再由 74138 译码输出。输入 `clk50M` 及数据/地址输入，输出 `Y0N~Y7N`，用于观察不同分频时钟的选择结果 |
| `frequency2.bdf` | `frequency.bdf` 的简化版，只保留 74151 多路选择部分，输出 `Y`，便于单独观察分频时钟的选择输出；对应 `frequency2.vwf` 仿真 |
| `exp4.bdf` | 实验四电路之一：两片 74161（4 位二进制计数器）+ `hex7seg` 显示译码，用 `divm` 提供慢时钟，计数结果经 `hex7seg` 输出 `S6[6..0]`、`S10[6..0]`，并给出 `OA~OD` |
| `exp4-2.bdf` | 两片 74161 级联构成的计数器（扩展计数位宽）：输入 `pin_name9`（时钟），输出 `pin_name1~pin_name8` |
| `exp4-3.bdf` | 实验四综合电路，当前工程默认顶层：两片 74161 级联构成 **00~11（十二进制，模 12）计数器**，`divm` 提供 1 Hz 时钟，两片 7447 译码后驱动两位数码管。输入 `clk`；输出 `qia~qid`（个位计数）、`qoa~qod`（十位计数）以及 `hex00~hex06`（个位段码）、`hex10~hex16`（十位段码） |

#### `exp4-3.bdf` 电路结构

| 器件 | 连线 | 作用 |
| --- | --- | --- |
| `inst1`（74161） | 时钟接 `divm` 的 1 Hz 输出 | **个位**计数（0~9） |
| `inst`（74161） | 时钟接 `inst5` 的输出 | **十位**计数（0~1） |
| `inst5`（7400 与非门） | `NAND(inst1.QB, inst1.QD) → inst.CLK` | 个位进位脉冲：个位计到 10 时该信号变低，个位清零后回升，这个上升沿送给十位时钟 |
| `inst4`（7400 与非门） | `NAND(inst.QA, inst1.QB) → inst.CLRN` 与 `inst3.IN1` | 十二进制译码：十位为 1 且个位为 2（即计数到 12）时输出低电平 |
| `inst3`（AND2） | `inst.CLRN ∧ inst.CLK → inst1.CLRN` | 个位清零：计到 10 时由 `inst5` 清零（个位取模 10），计到 12 时由 `inst4` 清零，两者相与后接到个位 `CLRN` |
| `inst8`（7447） | `A←inst1.QA, B←inst1.QB, C←inst1.QC, D←inst1.QD` | 个位 BCD 七段译码，输出到 `hex00~hex06` |
| `inst7`（7447） | `A←inst.QA, B←inst.QB, C←inst.QC, D←inst.QD` | 十位 BCD 七段译码，输出到 `hex10~hex16` |
| `inst2`、`inst9`（VCC） | 计数器的 `ENP/ENT/LDN` 与 7447 的 `LTN/RBIN/BIN` 均为高电平 | 计数器始终允许计数、不预置；数码管正常显示（熄灭测试/消隐关闭） |

### 仿真文件

| 文件 | 意义与作用 |
| --- | --- |
| `frequency.vwf` | Quartus 矢量波形文件，为 `frequency.bdf` 提供仿真激励：设置 `A/B/C/clk50M` 输入波形，观察 `Y0N~Y7N` 输出 |
| `frequency2.vwf` | Quartus 矢量波形文件，为 `frequency2.bdf` 提供仿真激励：设置 `A/B/C/clk50M`，观察输出 `Y` |

### 编译/仿真生成文件（默认不入库）

| 文件/目录 | 意义与作用 |
| --- | --- |
| `db/`、`incremental_db/` | 综合与布局布线产生的中间数据库，删除后重新编译即可重建 |
| `output_files/` | 编译输出：`.sof`/`.pof` 编程文件、`.pin` 引脚文件、各类 `.rpt` 报告等 |
| `simulation/qsim/` | ModelSim 仿真输出：网表（`.vo`）、测试平台、波形（`.vcd`）、工作库和脚本（`exp3.do`）等 |
| `exp3.qws` | Quartus 工作区/界面布局设置文件（窗口位置等个人偏好），已由 `.gitignore` 排除 |

## `exp4-3.bdf` 的修复说明

现象：十位数码管在“0、3”之间交替，而期望是“0、1”。问题出在**十位数码管 7447（`inst7`）的 BCD 输入接错**，不在计数逻辑：

- 原电路：`B←inst.QA`、`C←inst.QB`，而 `inst.QC` 悬空。于是 7447 收到的 4 位编码实际是 `QD·QB·QA·QA`——十位计数为 1 时被译码成 `3`，所以看到的是“0、3”而不是“0、1”。
- 现已改为标准接线：`A←QA、B←QB、C←QC、D←QD`（个位那一块原本就是对的）。

计数部分本来就是一十二进制计数器（个位 0~9、十位 0~1，计到 12 时两个计数器同时清零），修复后显示序列为 `00, 01, …, 09, 10, 11, 00, …`，十位在 `0` 与 `1` 之间循环，与实验要求的 00~11 一致。

如需改成其他进制，只改译码部分即可（注意十位的清零信号同时也要清个位）：

| 目标 | 改法 |
| --- | --- |
| 00~11（当前） | 十位清零 `NAND(inst.QA, inst1.QB)`：计数到 12 时清零；`AND2` 把该信号与个位进位脉冲相与后送个位 `CLRN` |
| 00~19 | 十位改成取模 2：`inst4` 的两个输入都接到 `inst.QB`，并把 `inst1.CLRN` 直接接到 `inst5.OUT` |
| 00~59 | 十位取模 6：`inst4` 的两个输入分别接 `inst.QB`、`inst.QC`，其余同 00~19 |

> `exp4-2.bdf` 是同一计数逻辑的早期版本（没有接 7447 译码，只引出计数输出），逻辑与 `exp4-3.bdf` 一致。

## 使用方法

1. 用 Quartus Prime 打开工程文件 `exp3.qpf`。
2. 在 **Project Navigator → Files** 中将需要验证的 `.bdf` 设为顶层（或直接修改 `exp3.qsf` 中的 `TOP_LEVEL_ENTITY`）。当前默认顶层为 `exp4-3`。
3. 执行 **Processing → Start Compilation** 进行综合、布局布线。
4. 通过 **Programmer** 将 `output_files/*.sof`（或 `.pof`）下载到 DE10-Lite 开发板验证功能。
5. 如需仿真，使用 **Tools → Run Simulation Tool → RTL Simulation**，或直接运行 `simulation/qsim/exp3.do`。

## 说明

- 本仓库仅存放课程实验源代码，用于学习与存档。
- 请使用与实验指导书一致的开发板与引脚约束，避免因器件/引脚不同导致编译或下载失败。
