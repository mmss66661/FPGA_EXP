"""Fill the experiment-5 pre-lab report, answering with the lecture-note wording."""
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "实验5", "实验五 预习报告.docx")
DST = os.path.join(ROOT, "..", "实验5", "实验五 预习报告（已完成）.docx")

RPR = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" '
       'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="21"/>'
       '<w:szCs w:val="21"/></w:rPr>')


def para(text, indent=True):
    ppr = '<w:pPr><w:ind w:firstLineChars="%d"/>%s</w:pPr>' % (200 if indent else 0, RPR)
    return ('<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (ppr, RPR, text))


ANSWERS = {
    9: [
        "本实验的目的如下：",
        "（1）掌握 Quartus II 中基于原理图的 EDA 设计流程与设计方法；",
        "（2）掌握 Quartus II 中工程的设计、文件的创建、元件符号的调用、波形仿真等；",
        "（3）理解基本 D 和 JK 触发器的逻辑功能并掌握测试方法；",
        "（4）实现按键去抖动电路的设计、仿真和硬件验证；",
        "（5）掌握 Quartus II 中层次设计方法，并用该方法实现实验；",
        "（6）掌握用 FPGA 开发硬件系统的方法，利用硬件电路进行验证。",
    ],
    16: [
        "扩展板通过 2×20（40 芯）排针与 DE10-Lite 的 GPIO 口相连，主要有：",
        "（1）2×20 GPIO 接口（P1）：GPIO9、GPIO18~GPIO26 等通用 IO；",
        "（2）按键：KEY1~KEY8；",
        "（3）DAC 通路：DADB0~DADB7、DACLOCK，DAC 芯片、DAC 信号接口及 DAC 信号测试点；",
        "（4）ADC 通路：ADD0~ADD7、ADCLOCK，ADC 芯片、ADC 信号接口、ADC 信号测试点和输入信号测试点；",
        "（5）音频接口（AUX）；",
        "（6）电源与地：VCC5V、3.3V、GND，以及地信号测试点（GND_TP）。",
    ],
    21: [
        "本次实验任务：",
        "（1）74LS74 D 触发器逻辑功能测试：设计 74LS74 D 触发器逻辑功能测试电路（图 5.9）→ 电路仿真（图 5.10）→ 按表 5.3 完成管脚配置并下载测试（表 5.4、表 5.5）；",
        "（2）74LS112 J-K 触发器逻辑功能测试：设计测试电路（图 5.12）→ 电路仿真（图 5.13）→ 按表 5.6 完成管脚配置并下载测试（表 5.7、表 5.8）；",
        "（3）实现基于 D 触发器的按键去抖动电路并测试：设计按键去抖动电路（图 5.16）、设计脉冲计数电路（图 5.19），仿真（图 5.20、图 5.21），按表 5.9 完成管脚配置并下载测试；",
        "（4）选做：触发器之间的相互转换电路设计和测试（J-K 转 D、J-K 转 T，图 5.14、图 5.15）。",
    ],
    26: [
        "任何按键在触点接触和断开时都会产生机械抖动，如果不进行处理，每一次按键都有可能产生若干次的响应，从而影响电路的正常功能。本实验使用 FPGA 设计一个按键去抖动电路，保证每次按键只产生一次响应。",
        "电路由 D 触发器和与门组成，CLK 为工作时钟，以同步方式输入给串接的 D 触发器，输入的按键信号以位移串行方式向右传递。必须在 D 触发器输出端 Q 都同时为 1 时与门才输出高电平；由于抖动信号是多个时间宽度狭窄的随机信号，很难十分整齐地使与门输出为 1，而只有正常的按键信号才有足够的时间宽度通过此电路，从而起到“滤波”的作用。增加 D 触发器的多少，决定了“滤波”的时间宽度门限。",
        "本实验（图 5.16）用 2 个 D 触发器和 1 个三输入与门：按键产生的抖动时间一般小于 10 ms，当 clk 端输入 50 Hz 时钟信号时，输出信号就能得到宽度固定为 10 ms 的单脉冲信号，因此 clk 端通常接一个频率低于 100 Hz 的方波。",
    ],
    27: [
        "（1）主要包括的模块：按键去抖动模块 keyin（k_in、clk 输入，k_out 输出）；分频模块 fenpin（将 50 MHz 时钟信号分频，其中 50 Hz 用作按键去抖动电路的输入时钟，其他分频信号留作后用）；按键计数模块 rising_edge_detect（对 KEY_IN 的上升沿计数，每输入一个按键脉冲计数值加 1，输出 D[3:0]、D[7:4]、D[11:8]、D[15:12] 分别为十进制个、十、百、千位）；显示接口模块 SEG_show（将计数值译码后输出给数码管显示）；以及二输入或门、顶层电路。",
        "（2）生成模块符号的方法：步骤一，设计原理图并通过编译；步骤二，选择 File → Create/Update → Create Symbol Files for Current File，在弹窗中点击 Save，将符号文件保存在工程路径中；步骤三，在电路图文件（bdf）中调用元件，检查和调用模块。",
        "（3）两路按键通路的主要区别：KEY0 的信号经过了按键去抖动处理（经 keyin 模块），而 KEY1 的信号未经过按键去抖动处理，直接（经非门）送入或门；同一时间只有 1 个键按下，相应信号经或门输入给计数器。",
    ],
}


def main():
    zin = zipfile.ZipFile(SRC)
    xml = zin.read("word/document.xml").decode("utf-8")
    spans = [(m.start(), m.end(), m.group(0))
             for m in re.finditer(r"<w:p[ >].*?</w:p>", xml, re.S)]

    def text_of(p):
        return "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)).strip()

    ops = []          # (start, end, replacement)
    for idx, texts in ANSWERS.items():
        start, end, _ = spans[idx]
        ops.append((end, end, "".join(para(t, indent=not t.startswith("（")) for t in texts)))
        # drop the blank writing-space paragraphs that follow this question
        j = idx + 1
        while j < len(spans) and text_of(spans[j][2]) == "":
            ops.append((spans[j][0], spans[j][1], ""))
            j += 1

    out = xml
    for start, end, repl in sorted(ops, reverse=True):
        out = out[:start] + repl + out[end:]

    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = out.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    print("written", os.path.basename(DST))


main()
