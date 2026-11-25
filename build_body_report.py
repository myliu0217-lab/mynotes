from io import BytesIO
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TEMPLATE = Path(r"C:\Users\12508\Downloads\正文模板.docx")
SOURCE = Path(r"D:\lmy-graduate\workspace\docs\mynotes\annual_source_1120_readonly.docx")
OUTPUT = Path(r"D:\lmy-graduate\workspace\docs\mynotes\课题四2026年度科技报告正文_按模板.docx")

src = Document(SOURCE)
doc = Document(TEMPLATE)
for name in ("Title", "Heading 1", "Heading 2", "Caption"):
    if name not in doc.styles:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]

# Keep the reference styles, header/footer parts, and final section geometry.
body = doc._element.body
for child in list(body):
    if child.tag != qn("w:sectPr"):
        body.remove(child)

def style_run(run, size=12, bold=False, name="宋体"):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

def add_text(text, indent=True):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.first_line_indent = Cm(0.74) if indent else Cm(0)
    style_run(p.add_run(text))
    return p

def heading(text, level=1, numbered=False):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(13 if level == 1 else 9)
    p.paragraph_format.space_after = Pt(8 if level == 1 else 6)
    p.paragraph_format.keep_with_next = True
    style_run(p.add_run(text), size=15 if level == 1 else 13, bold=True, name="黑体")
    if numbered:
        p.style = doc.styles["Heading 1" if level == 1 else "Heading 2"]
    return p

def add_page_field(footer):
    for p in list(footer.paragraphs):
        p._element.getparent().remove(p._element)
    p = footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    p._p.append(fld)
    return p

def page_number_type(section, fmt, start):
    sectPr = section._sectPr
    pg = sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        sectPr.append(pg)
    pg.set(qn("w:fmt"), fmt)
    pg.set(qn("w:start"), str(start))

def list_entry(text, number=1, indent=0):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.1
    tabs = p.paragraph_format.tab_stops
    tabs.add_tab_stop(Cm(14.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    style_run(p.add_run(text), size=10.5)
    style_run(p.add_run("\t" + str(number)), size=10.5)
    return p

def figure(index, caption, width_cm):
    image_para = src.paragraphs[index]
    vml = [x for x in image_para._element.iter() if x.tag.endswith("imagedata")]
    if len(vml) != 1:
        raise ValueError(f"Expected one source image at paragraph {index}, got {len(vml)}")
    rid = vml[0].get(qn("r:id"))
    blob = src.part.related_parts[rid].blob
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(BytesIO(blob), width=Cm(width_cm))
    c = doc.add_paragraph(style="Caption")
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.first_line_indent = Cm(0)
    c.paragraph_format.space_after = Pt(9)
    c.paragraph_format.line_spacing = 1.2
    style_run(c.add_run(caption), size=10.5)

def process_table():
    source_table = src.tables[0]
    p = doc.add_paragraph(style="Caption")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    style_run(p.add_run("表 1 微丝电极工艺阶段与对应步骤"), size=10.5)
    t = doc.add_table(rows=len(source_table.rows), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for j,w in enumerate([Cm(1.5),Cm(2.6),Cm(8.4),Cm(2.1)]):
        t.columns[j].width = w
    for i,row in enumerate(source_table.rows):
        trPr = t.rows[i]._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        for j,cell in enumerate(row.cells):
            target=t.cell(i,j)
            target.width=t.columns[j].width
            target.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            target.text=cell.text.replace("Contact pad", "接触焊盘")
            for cp in target.paragraphs:
                cp.paragraph_format.space_after=Pt(0)
                cp.paragraph_format.line_spacing=1.1
                for r in cp.runs:
                    style_run(r,size=9.5,bold=(i==0))
            pr=target._tc.get_or_add_tcPr()
            mar=OxmlElement("w:tcMar")
            for side in ("top","left","bottom","right"):
                el=OxmlElement("w:"+side)
                el.set(qn("w:w"),"80")
                el.set(qn("w:type"),"dxa")
                mar.append(el)
            pr.append(mar)
            if i==0:
                shade=OxmlElement("w:shd")
                shade.set(qn("w:fill"),"EAEAEA")
                pr.append(shade)
            borders=OxmlElement("w:tcBorders")
            for side in ("top","left","bottom","right"):
                e=OxmlElement("w:"+side)
                e.set(qn("w:val"),"single")
                e.set(qn("w:sz"),"4")
                e.set(qn("w:color"),"D9D9D9")
                borders.append(e)
            pr.append(borders)

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(2.54)
sec.left_margin = sec.right_margin = Cm(3.175)
page_number_type(sec, "upperRoman", 1)
add_page_field(sec.footer)

# Front matter. Page numbers are updated after a first render.
heading("目录", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
toc = [
    ("引言",0,1),
    ("1 柔性高通量ECoG电极",0,1),
    ("1.1 材料选择与表征",1,1),
    ("1.2 结构设计与工艺开发",1,2),
    ("1.3 原型器件试制与表征",1,2),
    ("2 256通道柔性微丝神经电极",0,3),
    ("2.1 阵列结构设计",1,3),
    ("2.2 高密度互连优化",1,4),
    ("2.3 基础工艺流程开发",1,5),
    ("3 阶段进展与后续工作",0,6),
    ("结论",0,6),
]
for title, level, page in toc:
    list_entry(title,page,0.55*level)
doc.add_page_break()

heading("插图清单",1).alignment = WD_ALIGN_PARAGRAPH.CENTER
figlist = [
    "图 1 Ln-IZO与多晶硅晶体管转移特性曲线",
    "图 2 Ln-IZO有源器件及互连结构工艺流程",
    "图 3 Ln-IZO晶体管表征结果",
    "图 4 256通道微丝电极总览",
    "图 5 微丝电极位点局部放大",
    "图 6 256通道柔性微丝神经电极工艺流程",
]
for name, page in zip(figlist,[1,2,3,4,4,5]):
    list_entry(name,page)
doc.add_page_break()

heading("附表清单",1).alignment = WD_ALIGN_PARAGRAPH.CENTER
list_entry("表 1 微丝电极工艺阶段与对应步骤",5)

# Restart the body page count as in the reference template.
bodysec = doc.add_section(WD_SECTION_START.NEW_PAGE)
bodysec.page_width, bodysec.page_height = Cm(21), Cm(29.7)
bodysec.top_margin = bodysec.bottom_margin = Cm(2.54)
bodysec.left_margin = bodysec.right_margin = Cm(3.175)
bodysec.footer.is_linked_to_previous = False
page_number_type(bodysec, "decimal", 1)
add_page_field(bodysec.footer)

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(14)
style_run(title.add_run("课题四 2026年度柔性高通量植入式电极研究进展"),size=16,bold=True,name="黑体")
title_ppr = doc.styles["Title"]._element.pPr
if title_ppr is not None:
    for el in list(title_ppr):
        if el.tag==qn("w:pBdr"):
            title_ppr.remove(el)

heading("引言",1)
add_text("课题四围绕面向汉语言脑机接口的全植入硬件系统研发需求，开展柔性高通量植入式皮层脑电（ECoG）电极与微丝神经电极研究。本阶段重点推进材料筛选、阵列设计、基础工艺开发和原型器件试制，对应任务书指标6.1的前期研发工作。")
add_text("ECoG电极方面，对掺镧铟锌氧化物（Ln-IZO）与多晶硅沟道材料进行对比表征，确定Ln-IZO器件方案并开展结构设计与试制。微丝电极方面，形成256位点单列、双列阵列设计及18步制备工艺流程，为后续性能验证和电极定型提供设计输入。")

heading("1 柔性高通量ECoG电极",1,True)
heading("1.1 材料选择与表征",2,True)
add_text(src.paragraphs[86].text.replace("材料选择与表征：", "", 1))
figure(87,"图 1 晶体管转移特性曲线：（a）Ln-IZO晶体管，Vds = 0.1 V；（b）多晶硅晶体管，Vds = −0.1 V。",14.2)
add_text("图1展示两类器件在相应偏置条件下的转移特性。Ln-IZO器件表现出较低的关态漏电流和明显的开关特性；结合材料与柔性工艺适配性，确定以Ln-IZO开展后续有源器件设计。噪声和工艺成本等指标仍需结合专项测试及工艺评估进一步确认。")

heading("1.2 结构设计与工艺开发",2,True)
add_text(src.paragraphs[90].text.replace("结构设计与工艺开发：", "", 1))
figure(90,"图 2 Ln-IZO有源器件及互连结构工艺流程示意",14.2)

heading("1.3 原型器件试制与表征",2,True)
add_text("推进Ln-IZO薄膜晶体管单元的原型试制，围绕转移特性、输出特性、沟道电容及在PBS溶液中的阻抗等项目开展表征。图3给出不同器件尺寸和偏置条件下的测试结果，其中40个宽长比为600/10（μm/μm）的器件在Vgs = 6 V时的阻抗为20.6 ± 1.7 kΩ。")
figure(93,"图 3 Ln-IZO晶体管表征结果：（a）不同Vds下的转移特性；（b）不同宽长比的转移特性；（c）40个器件的转移特性及阻抗分布；（d）输出特性；（e）1 kHz沟道电容；（f）PBS溶液中的阻抗与相位。",14.2)

heading("2 256通道柔性微丝神经电极",1,True)
heading("2.1 阵列结构设计",2,True)
add_text(src.paragraphs[97].text.replace("阵列结构设计：", "", 1))
figure(99,"图 4 256通道微丝电极总览：上为双列版，下为单列版；自左至右依次为焊盘阵列、扇出与柔性互连、shank及尖端位点区。",13.8)
figure(101,"图 5 位点局部放大：（a）单列；（b）双列。",9.2)

heading("2.2 高密度互连优化",2,True)
add_text(src.paragraphs[104].text.replace("高密度互连优化：", "", 1).replace("保持256通道规模", "保持256位点规模"))

heading("2.3 基础工艺流程开发",2,True)
add_text(src.paragraphs[105].text.replace("基础工艺流程开发：", "", 1))
figure(106,"图 6 256通道柔性微丝神经电极工艺流程：每步左图为电极区域，右图为焊盘区域。",14.2)
process_table()

heading("3 阶段进展与后续工作",1,True)
add_text(src.paragraphs[112].text.replace("阶段性成果与后续验证：", "", 1))
add_text("ECoG部分形成了沟道材料选择、器件工艺及晶体管单元表征结果；微丝电极部分形成256位点阵列设计、关键几何参数和18步制备流程。下一阶段需完成原型器件试制、工艺稳定性测试以及电极界面和信号质量验证，并据实评估任务书规定的通道数、厚度、覆盖面积等指标。")

heading("结论",1)
add_text("本阶段围绕柔性高通量ECoG和微丝神经电极开展了材料筛选、结构设计和工艺开发，获得Ln-IZO晶体管单元的初步表征结果，完成256位点微丝电极单列、双列版图及制备流程设计。现有微丝电极尺寸和位点规模为设计参数，完整电极的性能及工艺稳定性仍需通过试制和测试确认。上述工作为后续电极优化、系统集成和汉语言脑机接口应用研究提供了基础。")

doc.save(OUTPUT)
print(OUTPUT)
