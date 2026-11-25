from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SOURCE = r"D:\lmy-graduate\workspace\docs\mynotes\report_review_20261121.docx"
OUTPUT = r"D:\lmy-graduate\workspace\docs\mynotes\专项2026年度执行情况报告_微丝电极修订.docx"

doc = Document(SOURCE)

def replace_paragraph(index, expected_start, new_text):
    p = doc.paragraphs[index]
    if not p.text.startswith(expected_start):
        raise RuntimeError(f"段落定位失效：{index}: {p.text[:40]}")
    p.runs[0].text = new_text
    for run in p.runs[1:]:
        run.text = ""
    return p

replace_paragraph(
    97,
    "阵列结构设计：",
    "阵列结构设计：在原4根植入微丝（shank）方案基础上，将阵列扩展至8根shank，单根仍布置32个位点，完成每版256位点的单列和双列两种设计。单列版采用8×1×32布局，位点中心距60 μm；双列版采用8×2×16布局，轴向投影节距约29.9 μm。植入段几何长度单列约10.125 mm、双列约10.127 mm。电极以聚酰亚胺（PI）为柔性绝缘材料，设计厚度小于5 μm。",
)
replace_paragraph(
    103,
    "高密度互连优化：",
    "高密度互连优化：将连接焊盘等间距排列为连续阵列，中间不留空隙，并优化扇出区与植入段之间的走线布局。走线线宽和线间距均设计为1.5 μm；256条走线在转角处汇成约0.77 mm宽的线束，再分成8组，每组32条进入对应的shank。该布局在保持256位点规模的同时，为后续版图制备与焊盘连接提供明确的几何约束。",
)
replace_paragraph(
    104,
    "基础工艺流程开发：",
    "基础工艺流程开发：形成覆盖衬底与牺牲层、底部PI、焊盘、互连、顶部PI与开窗、顶电极及封装的18步工艺流程。各金属层均采用磁控溅射结合剥离的方式实现图形化，具体步骤如下图和下表所示。",
)
replace_paragraph(
    111,
    "阶段性成果与后续验证：",
    "阶段性成果与后续验证：已形成256位点单列、双列设计方案、关键设计参数及完整工艺流程图，为原型器件制备和工艺稳定性测试提供了可执行的设计输入。上述位点数、尺寸和厚度均为设计参数，实际性能仍需通过试制与测试验证。",
)

doc.save(OUTPUT)
print(OUTPUT)
