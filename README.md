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

## 文件说明

### VHDL 模块

| 文件 | 功能 |
| --- | --- |
| `divm.vhd` | 时钟分频器，`m = 25 000 000`，把 50 MHz 时钟分频为约 1 Hz |
| `divm1.vhd` | 时钟分频器（同 `divm`，用于原理图例化） |
| `divm5.vhd` | 时钟分频器，`m = 5 000 000`，约 5 Hz |
| `divm10.vhd` | 时钟分频器，`m = 2 500 000`，约 10 Hz |
| `hex7seg.vhd` | 4 位二进制转七段显示译码器（共阴，输出 `S[6..0]`） |

每个 VHDL 文件都有对应的 `.bsf` 符号文件，可直接在原理图中作为元件调用。

### 原理图设计

| 文件 | 主要器件 | 功能说明 |
| --- | --- | --- |
| `74151_test.bdf` | 74151 | 8 选 1 数据选择器 74151 的功能验证 |
| `74138_test.bdf` | 74138 | 3-8 线译码器 74138 的功能验证 |
| `74138_test2.bdf` | 74138、7420 | 用译码器 + 与非门实现 1 位全加器（输入 A、B、CI，输出 S、CO） |
| `2-4.bdf` | 74 系列门电路 | 用与非门搭建带使能端（`ST_N`）的 2-4 译码器 |
| `16-4.bdf` | 2 × 74148、与门 | 两片 74148 级联实现 16-4 线优先编码器 |
| `eight.bdf` | 74151、74138 | 74151 与 74138 组合的数据选择/译码电路 |
| `frequency.bdf` | divm1/5/10、74151、74138 | 分频 + 数据选择 + 译码的输出实验电路 |
| `frequency2.bdf` | divm1/5/10、74151 | `frequency` 的简化版本，仅保留多路选择输出 Y |
| `exp4.bdf` | 2 × 74161、hex7seg | 74161 计数器 + 七段译码显示（计数结果经 `hex7seg` 显示） |
| `exp4-2.bdf` | 2 × 74161、7400 | 两片 74161 级联构成的计数器 |
| `exp4-3.bdf` | 2 × 74161、divm、7447 | 计数器 + 分频时钟 + 7447 译码，驱动数码管显示 |

### 仿真

| 文件 | 说明 |
| --- | --- |
| `frequency.vwf`、`frequency2.vwf` | Quartus 矢量波形文件（`.vwf`），用于仿真激励 |
| `simulation/qsim/exp3.do` | ModelSim 仿真脚本 |
| `simulation/qsim/*.vwf`、`*.v`、`*.vcd` | 仿真运行生成的波形与网表文件（生成文件，默认不提交） |

## 使用方法

1. 用 Quartus Prime 打开工程文件 `exp3.qpf`。
2. 在 **Project Navigator → Files** 中将需要验证的 `.bdf` 设为顶层（或直接修改 `exp3.qsf` 中的 `TOP_LEVEL_ENTITY`）。当前默认顶层为 `exp4-3`。
3. 执行 **Processing → Start Compilation** 进行综合、布局布线。
4. 通过 **Programmer** 将 `output_files/*.sof`（或 `.pof`）下载到 DE10-Lite 开发板验证功能。
5. 如需仿真，使用 **Tools → Run Simulation Tool → RTL Simulation**，或直接运行 `simulation/qsim/exp3.do`。

## 说明

- 本仓库仅存放课程实验源代码，用于学习与存档。
- 请使用与实验指导书一致的开发板与引脚约束，避免因器件/引脚不同导致编译或下载失败。
