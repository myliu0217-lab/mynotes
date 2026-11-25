from copy import deepcopy
from pathlib import Path
import shutil

from docx import Document
from docx.text.paragraph import Paragraph


source = Path(r"C:\Users\12508\Downloads\正文模板.docx")
target = Path(r"D:\lmy-graduate\workspace\docs\mynotes\正文模板_引言正文扩充及参考文献.docx")
shutil.copy2(source, target)
doc = Document(target)
p = list(doc.paragraphs)


def set_text(paragraph, value):
    runs = paragraph.runs
    if not runs:
        paragraph.add_run(value)
    else:
        runs[0].text = value
        for run in runs[1:]:
            run.text = ""


def insert_after(anchor, prototype, value):
    element = deepcopy(prototype._element)
    anchor._element.addnext(element)
    para = Paragraph(element, anchor._parent)
    set_text(para, value)
    return para


def remove(paragraph):
    paragraph._element.getparent().remove(paragraph._element)


# 仅插入正文内容，沿用模板正文段落的样式、缩进、字体和行距。
intro = [
    "脑机接口需要从神经活动中提取与运动、感觉和语言相关的信息。皮层脑电（ECoG）电极可在皮层表面记录较大范围的局部场电位；较密集的位点有助于表征皮层活动的空间差异。早期人类皮层记录研究已揭示语音感知和发音过程中具有空间分布特征的神经活动，为语言相关信号的解码提供了依据[1-3]。面向汉语言脑机接口，电极需兼顾覆盖范围、空间分辨率、柔性贴附性及与植入式采集系统的连接能力。",
    "随着位点数量增加，逐点独立引出的走线和焊盘占用面积增大，成为柔性阵列扩展的重要约束。将薄膜晶体管等有源器件集成于电极阵列，可通过寻址与复用减少外围互连需求。已有柔性有源皮层阵列和可贴附皮层表面的薄型电极研究，为高密度信号记录及器件集成提供了技术参考[4-5]。这些公开结果说明相关路线具有可行性，但具体材料、工艺与信号质量仍需针对本课题器件单独验证。",
    "微丝神经电极可进入皮层内部，记录更局部的神经活动，与表面ECoG电极形成空间尺度和信号类型上的互补。早期柔性网状电子学和超柔性神经探针研究表明，植入结构的机械柔顺性与组织界面稳定性值得在器件设计中重点考虑[6-7]。本课题据此并行开展柔性高通量ECoG电极与微丝神经电极研究，为后续场电位及Spikes信号采集提供器件基础。",
]
anchor = p[19]
for paragraph in intro:
    anchor = insert_after(anchor, p[20], paragraph)

set_text(
    p[20],
    "根据课题任务书，课题四指标6.1的中期目标为：ECoG电极采集通道数不少于256、覆盖面积不少于4 cm²、厚度小于30 μm；微丝电极通道数不少于256、厚度小于5 μm。后续还需验证场电位采样率与噪声、Spikes采样率与信噪比等系统性能。本报告对应2026年9月至2027年2月年度任务，重点记录材料筛选、结构设计、基础工艺开发和原型器件试制进展。",
)
set_text(
    p[21],
    "ECoG电极方面，对掺镧铟锌氧化物（Ln-IZO）与多晶硅沟道器件进行对比表征，确定Ln-IZO作为后续有源阵列的研究方案，并开展工艺开发与晶体管单元试制。微丝电极方面，形成256位点单列、双列阵列设计及18步制备工艺流程。以下分别说明两类电极的阶段工作，并区分已获得的器件测试结果与仍待实测验证的电极指标。",
)

insert_after(
    p[29], p[29],
    "两类器件的测试偏置条件不同，图1主要用于观察各自的开关行为，不宜据此直接给出迁移率、噪声或阵列良率的定量优劣结论。后续需在统一测试条件和样本统计基础上，进一步比较批间一致性、柔性基底上的工艺适配性及长期工作稳定性。相关金属氧化物薄膜电子学在柔性皮层阵列中的应用已有报道，可为本课题器件评估提供参照[8]。",
)
insert_after(
    p[31], p[31],
    "工艺路线按栅极及绝缘层制备、有源层沉积与图形化、源漏电极形成、层间绝缘和外部连接等环节组织（图2）。版图设计需同时考虑阵列寻址、器件单元尺寸和互连密度；工艺优化则重点关注薄膜均匀性、图形边界及层间对准，以减少后续阵列扩展时的器件差异。现阶段形成的是薄膜晶体管单元工艺基础，完整ECoG阵列的覆盖面积和总厚度尚需在集成样机上测量。",
)
insert_after(
    p[38], p[35],
    "图3分别从转移与输出特性、沟道电容及电解质环境下的阻抗反映器件工作状态。其中40个器件的阻抗结果可用于初步判断同一尺寸样本在所列偏置条件下的分布情况；该结果不能替代完整阵列的通道一致性、输入噪声或长期浸泡稳定性测试。下一阶段应在统一测试频率、偏置及液体环境条件下补充统计，并结合阵列互连与读出电路开展系统级评价。",
)
insert_after(
    p[41], p[41],
    "单列与双列方案保留相同的总位点数和单根shank位点数，区别主要体现在位点排布及轴向采样间距。两种版图可用于比较位点密度与走线、开窗工艺之间的匹配关系。柔性高密度植入式阵列及其连接方式已有相关研究[9-10]，可供后续集成验证参考。当前厚度小于5 μm为设计约束，尚不能视为成品电极的实测厚度；植入段的机械完整性和位点暴露情况也需在样品制备后检查。",
)
insert_after(
    p[46], p[46],
    "高密度互连的实现依赖细线宽图形转移、转角过渡及层间绝缘质量。扇出区将密集走线逐步引至连续焊盘阵列，便于与后续连接工艺衔接；植入段则需控制相邻导线间距和位点开窗的位置误差。版图参数已明确，但走线连续性、相邻通道绝缘性及焊盘连接良率仍需通过制备样品逐项验证。",
)
insert_after(
    p[48], p[48],
    "工艺安排中，牺牲层用于后续柔性结构释放；上下PI层承担支撑与绝缘作用；金属互连、焊盘和顶电极分别通过光刻、磁控溅射及剥离形成。顶部PI开窗采用反应离子刻蚀（RIE），使电极位点与焊盘按设计区域暴露。试制阶段应重点检查金属图形完整性、开窗对准和柔性释放后的结构状态，并通过批次统计评价流程稳定性。",
)
set_text(
    p[55],
    "对照本年度计划，ECoG部分已完成沟道材料对比、Ln-IZO晶体管单元工艺路线及初步电学表征；微丝电极部分已完成256位点单列、双列版图、关键几何参数和18步制备流程设计。上述工作覆盖材料筛选、设计与基础工艺开发，形成了原型试制的技术输入。当前报告中的微丝位点数、线宽、长度与厚度属于设计参数，ECoG测试数据来自晶体管单元，均需与成品电极实测指标区分。",
)
set_text(
    p[56],
    "后续工作应围绕原型器件试制及工艺稳定性测试展开：ECoG阵列需补充有效采集通道数、覆盖面积、总厚度、场电位采样率和噪声的测试；微丝电极需补充成品厚度、有效通道数、位点阻抗、Spikes采样率和单神经元尖峰记录信噪比的验证。还应记录各批次制备和封装结果，明确失效环节，为电极定型、系统集成及第三方检测准备可追溯的测试依据。",
)
set_text(
    p[58],
    "本阶段完成了柔性高通量ECoG电极的材料方案选择与Ln-IZO晶体管单元初步表征，形成了256位点柔性微丝电极的单列、双列版图和制备流程。已有结果证明了所选器件单元与设计方案的阶段可行性，为下一阶段阵列试制提供了基础。任务书规定的成品电极通道数、覆盖面积、厚度及采集性能，仍需通过原型器件与系统测试据实确认。",
)

# 去除模板中与本报告无关的参考文献示例及附录样例，仅替换内容。
for para in p[60:]:
    remove(para)

references = [
    "[1] CHANG E F. Towards large-scale, human-based, mesoscopic neurotechnologies[J]. Neuron, 2015, 86: 68-78.",
    "[2] PASLEY B N, DAVID S V, MESGARANI N, et al. Reconstructing speech from human auditory cortex[J]. PLoS Biology, 2012, 10(1): e1001251. DOI: 10.1371/journal.pbio.1001251.",
    "[3] BOUCHARD K E, MESGARANI N, JOHNSON K, et al. Functional organization of human sensorimotor cortex for speech articulation[J]. Nature, 2013, 495: 327-332. DOI: 10.1038/nature11911.",
    "[4] VIVENTI J, KIM D H, VIGELAND L, et al. Flexible, foldable, actively multiplexed, high-density electrode array for mapping brain activity in vivo[J]. Nature Neuroscience, 2011, 14: 1599-1605. DOI: 10.1038/nn.2973.",
    "[5] KHODAGHOLY D, GELINAS J N, THESEN T, et al. NeuroGrid: recording action potentials from the surface of the brain[J]. Nature Neuroscience, 2015, 18: 310-315. DOI: 10.1038/nn.3905.",
    "[6] LIU J, FU T M, CHENG Z, et al. Syringe-injectable electronics[J]. Nature Nanotechnology, 2015, 10: 629-636. DOI: 10.1038/nnano.2015.115.",
    "[7] LUAN L, WEI X, ZHAO Z, et al. Ultraflexible nanoelectronic probes form reliable, glial scar-free neural integration[J]. Science Advances, 2017, 3: e1601966. DOI: 10.1126/sciadv.1601966.",
    "[8] LONDOÑO-RAMÍREZ H, HUANG X, COOLS J, et al. Multiplexed surface electrode arrays based on metal oxide thin-film electronics for high-resolution cortical mapping[J]. Advanced Science, 2024, 11: 2308507. DOI: 10.1002/advs.202308507.",
    "[9] SEO K J, HILL M, RYU J, et al. A soft, high-density neuroelectronic array[J]. npj Flexible Electronics, 2023, 7: 40. DOI: 10.1038/s41528-023-00271-2.",
    "[10] ZHAO E T, HULL J M, MINTZ HEMED N, et al. A CMOS-based highly scalable flexible neural electrode interface[J]. Science Advances, 2023, 9: eadf9524. DOI: 10.1126/sciadv.adf9524.",
]
anchor = p[59]
for entry in references:
    anchor = insert_after(anchor, p[64], entry)
    anchor.paragraph_format.keep_together = True

doc.save(target)
print(target)
print("paragraphs", len(doc.paragraphs), "images", len(doc.inline_shapes), "tables", len(doc.tables))
