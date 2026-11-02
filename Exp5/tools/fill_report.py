import os
import re
import shutil
import zipfile

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "..", "实验5", "实验五 预习报告.docx")
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "..", "实验5", "实验五 预习报告（已完成）.docx")

RPR = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" '
       'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="21"/>'
       '<w:szCs w:val="21"/></w:rPr>')


def para(text, indent=True, bold=False):
    rpr = RPR.replace("<w:rPr>", "<w:rPr><w:b/>" if bold else "<w:rPr>")
    ppr = '<w:pPr>%s<w:ind w:firstLineChars="%d"/>%s</w:pPr>' % (
        "", 200 if indent else 0, rpr)
    return ('<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (ppr, rpr, text))


ANSWERS = {
    9: [
        "本实验以触发器电路为对象，通过 Quartus 的原理图（BDF）设计流程完成“设计—仿真—引脚分配—下载验证”的完整过程，具体目的如下：",
        "（1）掌握 Quartus II/Prime 中基于原理图的 EDA 设计流程与设计方法；",
        "（2）掌握工程和设计文件的创建、元件符号的调用、波形（.vwf）仿真等基本操作；",
        "（3）理解基本 D 触发器（74LS74，上升沿触发）和 J-K 触发器（74LS112，下降沿触发）的逻辑功能，并掌握其功能测试方法；",
        "（4）实现基于 D 触发器的按键去抖动电路的设计、仿真与硬件验证；",
        "（5）掌握 Quartus 的层次设计方法：先设计并编译子模块，生成 .bsf 符号文件，再在顶层 BDF 中调用；",
        "（6）掌握用 FPGA 开发硬件系统的方法，利用 DE10-Lite 开发板上的按键、开关、数码管等完成硬件验证。",
    ],
    16: [
        "本实验使用的功能扩展板通过 2×20（40 芯）通用 IO 插座 P1 与 DE10-Lite 的 GPIO 口（JP1，GPIO[0]~GPIO[35]）对接，板上主要包括以下接口和测试点：",
        "（1）通用 IO 接口：2×20 排针 P1，引脚包括 8 个按键、16 路 GPIO（GPIO18~GPIO26 等）、DAC/ADC 数据线与控制线；",
        "（2）按键：KEY1~KEY8，共 8 个独立按键，本实验的 KEY0、KEY1 即取自扩展板按键，经 GPIO 口引入 FPGA；",
        "（3）DAC 通路：DADB0~DADB7 数据线、DACLOCK 控制线、DAC 芯片、DAC 信号接口及 DAC 信号测试点；",
        "（4）ADC 通路：ADD0~ADD7 数据线、ADCLOCK 控制线、ADC 芯片、ADC 信号接口（ADC 输入）、ADC 信号测试点与输入信号测试点；",
        "（5）音频接口（AUX）以及电源与地：VCC5V、3.3V、GND，板上设有地信号测试点（GND_TP），便于示波器接地与测量。",
    ],
    21: [
        "本次实验共包括三个必做任务和一个选做任务：",
        "任务 1：74LS74 D 触发器逻辑功能测试。在 Quartus 中新建 BDF，按图 5.9 搭接测试电路（Sd1、Rd1 经非门接 PRN、CLRN，D1 接 1D，clk1 接 1CLK，输出 Q1、Q1N），编译后用 .vwf 仿真，并按表 5.3 分配引脚（clk1=PIN_F15、Sd1=PIN_A7、Rd1=PIN_B8、D1=PIN_A14、Q1=PIN_A8、Q1N=PIN_A9），下载后完成表 5.4（直接置位/复位）和表 5.5（D 与 CP）的测试。",
        "任务 2：74LS112 J-K 触发器逻辑功能测试。按图 5.12 搭接电路（增加 J1=PIN_C11、K1=PIN_C10），完成仿真与硬件测试，记录表 5.7（直接置位/复位）和表 5.8（J、K、CP 功能，含保持、置 0、置 1、翻转）。",
        "任务 3：基于 D 触发器的按键去抖动电路及脉冲计数电路的设计与测试。先设计去抖动模块 keyin（2 个 D 触发器 + 三输入与门）并生成符号；再设计分频模块 fenpin、按键计数模块 rising_edge_detect、显示接口模块 SEG_show，在顶层中把 KEY0（经去抖）与 KEY1（未经去抖）经或门送入计数器，用 4 个数码管显示计数值，完成仿真（图 5.20、5.21）并下载验证。",
        "选做任务：触发器之间的相互转换，包括 J-K 触发器转 D 触发器（J=D、K=/D）和 J-K 触发器转 T/T′ 触发器（J=K=T，T=1 时即为 T′），并写出 T 触发器的功能表。",
    ],
    26: [
        "机械按键在触点闭合和断开瞬间会产生持续时间很短（一般小于 10 ms）的随机抖动，若直接作为计数脉冲，按一次键可能被识别成多次，因此必须去抖动。",
        "去抖动电路的基本思想是“延时采样 + 宽度判别”：用较低频率的时钟（本实验为 50 Hz，周期 20 ms）对按键信号连续采样，只有连续若干个时钟周期都保持同一电平，才认为按键状态真正改变，宽度小于一个采样周期的抖动脉冲会被自然滤除。",
        "本实验采用 2 个串接的 D 触发器加 1 个三输入与门实现：按键信号 k_in 先经非门，再串行送入两个由同一时钟（经非门后为下降沿）触发的 D 触发器，得到 Q1、Q2；与门输出 k_out = Q1·/Q2·clk。",
        "由于 Q1、Q2 是逐级传递的，只有当 k_in 稳定地保持新电平、使 Q1 已更新而 Q2 尚未更新时，k_out 才会在 clk 为高电平的半个周期内输出一个宽度固定为 10 ms 的高脉冲；随后 Q2 跟上，k_out 自动回零。因此按键按下（或释放）一次只产生一个脉冲，抖动被完全消除。",
        "增加串接 D 触发器的级数（如图 5.7 中的 4 级 + 四输入与门）可以提高“滤波”的时间门限，抗干扰能力更强，但响应更慢。",
    ],
    27: [
        "（1）测试电路中主要包括的模块：①去抖动模块 keyin（输入 k_in、clk，输出 k_out，内部含 2 个 DFF、2 个非门和 1 个三输入与门，并引出 Q0、Q1、Q2 便于观察）；②分频模块 fenpin，把 50 MHz 时钟分频为 5 M、500 k、10 k、5 k、500、50 Hz 和 1 Hz，其中 50 Hz 作为去抖动电路的采样时钟；③按键计数模块 rising_edge_detect，对 KEY_IN 的上升沿计数，输出 4 位十进制数的 D[15..0]（D[3..0]、D[7..4]、D[11..8]、D[15..12] 分别为个、十、百、千位）；④显示接口模块 SEG_show，把 16 位 BCD 码译成 4 组七段码 HEX0~HEX3；⑤二输入或门，把两路按键信号合并（同一时刻只有一个键按下）；⑥顶层电路 exp5_top 以及输入输出引脚。",
        "（2）生成模块符号的方法：先完成子模块的 BDF（或 VHDL）设计并编译通过；执行 File → Create/Update → Create Symbol Files for Current File，在弹出的对话框中保存，Quartus 会在工程目录下生成同名的 .bsf 符号文件；在顶层 BDF 中双击空白处（或点击 Symbol 工具）打开符号库，选择该符号即可像标准元件一样调用，并可用引脚工具连线。",
        "（3）两路按键通路在电路上的主要区别：KEY0 通道先经过 keyin 去抖动模块，输出的是宽度固定、与抖动无关的干净单脉冲；KEY1 通道只经过一个非门（把“按下为 0”变成正脉冲）就直接送入或门，没有经过任何去抖动处理。因此按一次 KEY0，计数只加 1；而按一次 KEY1，由于其抖动信号全部进入计数器，计数值会一次跳动多个数，这正是用来对比去抖动效果的两条通路。",
        "（4）本预习对应的电路文件：Quartus 工程 exp5.qpf 位于仓库的 Exp5 目录，包含 exp5_t1_7474.bdf（任务 1）、exp5_t2_74112.bdf（任务 2）、keyin.bdf（去抖动模块）、exp5_t4_jk2d.bdf / exp5_t4_jk2t.bdf（选做）、exp5_top.bdf（任务 3 顶层），以及 fenpin.vhd、rising_edge_detect.vhd、seg_show.vhd 三个子模块和对应的 .bsf 符号、.vwf 仿真波形文件。",
    ],
}


def main():
    zin = zipfile.ZipFile(SRC)
    xml = zin.read("word/document.xml").decode("utf-8")
    spans = [(m.start(), m.end(), m.group(0))
             for m in re.finditer(r"<w:p[ >].*?</w:p>", xml, re.S)]

    inserts = []
    for idx, texts in ANSWERS.items():
        start, end, _ = spans[idx]
        block = "".join(para(t, indent=not t.startswith("（")) for t in texts)
        inserts.append((end, block))

    out = xml
    for pos, block in sorted(inserts, reverse=True):
        out = out[:pos] + block + out[pos:]

    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = out.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    print("written", DST)


main()
