# 实验五 触发器电路分析与应用（Quartus 工程）

本目录是《数字电子技术基础实验（I）》实验五的完整 Quartus 工程，按讲义（`../实验5/讲义.pdf`）的图 5.9、5.12、5.14、5.15、5.16、5.19 实现了全部必做任务和选做任务，并在本机用 Quartus Prime 19.1 Lite 验证编译通过（Analysis & Synthesis / Fitter / Assembler 均为 0 error）。

## 开发环境

| 项目 | 说明 |
| --- | --- |
| EDA 工具 | Quartus Prime Lite 19.1（讲义写 17.0/18.1，19.1 亦可） |
| 器件 | MAX 10 `10M50DAF484C7G`（DE10-Lite） |
| 工程文件 | `exp5.qpf` / `exp5.qsf`（默认顶层 `exp5_top`） |
| 设计方式 | 原理图 BDF + VHDL 子模块（层次设计：子模块编译后生成 `.bsf` 符号，顶层 BDF 调用） |

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `exp5_t1_7474.bdf` | 任务 1：74LS74 D 触发器逻辑功能测试（Sd1/Rd1 经非门接 PRN/CLRN，D1→1D，clk1→1CLK，Q1/Q1N 输出） |
| `exp5_t2_74112.bdf` | 任务 2：74LS112 J-K 触发器逻辑功能测试（Sd1、Rd1、J1、K1、clk1 与 Q1/Q1N） |
| `keyin.bdf` / `keyin.bsf` | 任务 3：按键去抖动模块（2 个 DFF + 2 个非门 + 三输入与门，另引出 Q0/Q1/Q2 便于观察） |
| `fenpin.vhd` / `fenpin.bsf` | 任务 3：50 MHz 分频模块，输出 5M、500k、10k、5k、500、50、1 Hz |
| `rising_edge_detect.vhd` / `.bsf` | 任务 3：按键脉冲计数模块，4 位十进制 BCD 输出 `D[15..0]` |
| `seg_show.vhd` / `seg_show.bsf` | 任务 3：显示接口，16 位 BCD → 4 组七段码 `HEX0~HEX3[7..0]`（共阳，低电平点亮） |
| `exp5_top.bdf` | 任务 3 顶层：KEY0 经去抖、KEY1 直接（经非门）→ 或门 → 计数 → 数码管显示 |
| `exp5_t4_jk2d.bdf` | 选做：J-K 触发器转 D 触发器（J=D，K=/D） |
| `exp5_t4_jk2t.bdf` | 选做：J-K 触发器转 T 触发器（J=K=T） |
| `exp5_t1_7474.vwf`、`exp5_t2_74112.vwf`、`keyin.vwf` | 对应的仿真激励波形 |
| `tools/` | 生成 BDF/BSF/VWF 与预习报告的脚本（可重复生成设计文件） |

## 任务与引脚

### 任务 1：74LS74 测试（`exp5_t1_7474`）

| 端口 | clk1 | Sd1 | Rd1 | D1 | Q1 | Q1N |
| --- | --- | --- | --- | --- | --- | --- |
| 引脚 | PIN_F15 | PIN_A7 | PIN_B8 | PIN_A14 | PIN_A8 | PIN_A9 |

### 任务 2：74LS112 测试（`exp5_t2_74112`）

| 端口 | clk1 | Sd1 | Rd1 | J1 | K1 | Q1 | Q1N |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 引脚 | PIN_F15 | PIN_A7 | PIN_B8 | PIN_C11 | PIN_C10 | PIN_A8 | PIN_A9 |

### 任务 3：按键去抖动与脉冲计数（`exp5_top`）

| 端口 | CLK_50M | KEY0 | KEY1 |
| --- | --- | --- | --- |
| 引脚 | PIN_P11 | PIN_W5 | PIN_AA15 |

数码管按表 5.9 分配（`HEX0[7]…HEX0[0]` = D15、C17、D17、E16、C16、C15、E15、C14；`HEX1` = A16、B17、A18、A17、B16、E18、D18、C18；`HEX2` = A19、B22、C22、B21、A21、B19、A20、B20；`HEX3` = D22、E17、D19、C20、C19、E21、E22、F21），全部写在 `exp5.qsf` 中。

## 使用方法

1. 用 Quartus Prime 打开 `exp5.qpf`。
2. 在 **Project Navigator → Files** 中右键需要验证的 `.bdf`，选择 **Set as Top-Level Entity**（或修改 `exp5.qsf` 里的 `TOP_LEVEL_ENTITY`）。
3. 执行 **Processing → Start Compilation**，通过 **Programmer** 下载 `output_files/exp5.sof`。
4. 仿真：**Tools → Run Simulation Tool → RTL Simulation**，或直接用对应的 `.vwf` 波形文件设置激励后运行。

> 任务 1、2 与任务 3 的引脚互不冲突，可以共用一个 `.qsf`；切换顶层后才对相应引脚生效。

## 电路要点

- **按键去抖动**：`k_in` 经非门后串入两个由 50 Hz 时钟（反相后下降沿触发）的 D 触发器，与门输出 `k_out = Q1·/Q2·clk`，每次按键只输出一个宽度约 10 ms 的单脉冲。
- **脉冲计数**：`rising_edge_detect` 以 `KEY_IN` 的上升沿为计数时钟，4 位 BCD 级联，实现 0000~9999 计数。
- **显示**：`SEG_show` 把 4 位 BCD 译成共阳七段码（`0` 点亮），小数点 `HEXx[7]` 恒为高（熄灭）。
- **对比通路**：KEY0 经过 `keyin` 去抖，KEY1 只经非门直连或门；按一次 KEY1 会因抖动多计数。
