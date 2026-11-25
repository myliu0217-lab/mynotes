from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = r"D:\lmy-graduate\workspace\docs\mynotes\课题四2026年度重要进展及成果.docx"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.3), Cm(2.2)
sec.left_margin, sec.right_margin = Cm(2.6), Cm(2.6)

styles = doc.styles
normal = styles['Normal']
normal.font.name = '宋体'
normal.font.size = Pt(11)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
normal.paragraph_format.line_spacing = 1.35
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.first_line_indent = Cm(0.74)

for name, size, before, after in [('Title', 16, 0, 13), ('Heading 1', 13, 9, 7), ('Heading 2', 11.5, 8, 5), ('Heading 3', 11, 6, 3)]:
    st = styles[name]
    st.font.name = '黑体' if name != 'Title' else '黑体'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    st.paragraph_format.first_line_indent = Cm(0)
    st.paragraph_format.keep_with_next = True

# Word's built-in Title style can carry a theme-colored bottom border.
for el in list(styles['Title']._element.pPr):
    if el.tag == qn('w:pBdr'):
        styles['Title']._element.pPr.remove(el)

p = doc.add_paragraph(style='Title')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('课题四 2026年度重要进展及成果')

doc.add_heading('五、本年度取得的重要进展及成果', 1)

doc.add_heading('1. 项目年度重要进展及成果总结', 2)
doc.add_paragraph('课题四围绕任务书指标6.1及2026年9月至2027年2月阶段任务，推进柔性高通量植入式皮层脑电（ECoG）电极和微丝神经电极的材料筛选、阵列设计、基础工艺开发与原型器件试制。ECoG电极方面，对铟镓锌氧化物（IGZO）与多晶硅开展对比表征，综合结果显示IGZO更适合作为本阶段有源器件的沟道材料，已据此确定材料方案，并开展阵列结构与制备工艺设计及原型试制。微丝电极方面，完成256通道柔性阵列的单列、双列位点方案及18步制备工艺流程设计，明确了聚酰亚胺（PI）绝缘层、金属互连、位点开窗和焊盘封装等关键工艺环节。上述工作形成了后续原型表征、工艺稳定性验证及电极定型的技术基础。')

doc.add_heading('2. 项目年度重要进展及成果详细介绍', 2)
doc.add_heading('（1）柔性高通量ECoG电极', 3)
doc.add_paragraph('材料选择与表征。针对大面积、高通量柔性ECoG阵列的器件需求，对IGZO和多晶硅两种沟道材料进行对比表征，重点考察与阵列制备相关的电学特性、器件一致性及工艺适配性。综合对比结果，IGZO方案表现更优，确定采用IGZO开展后续器件设计与工艺开发。具体测试条件、样本量及量化对比数据待补充。')
doc.add_paragraph('结构设计与工艺开发。围绕柔性基底上的有源阵列集成，开展电极位点、走线、寻址单元和连接区域的结构设计，梳理薄膜沉积、图形化、绝缘保护、位点开窗及柔性器件释放等工艺环节，并针对高密度互连与器件一致性开展版图和工艺参数优化。器件结构图、层间材料与关键尺寸待补充。')
doc.add_paragraph('原型器件试制与表征。推进IGZO方案的原型器件试制，围绕薄膜晶体管转移特性、阈值电压、开关比、器件均一性，以及电极界面阻抗、噪声、柔性弯折和浸泡稳定性等项目开展表征与工艺反馈。原型数量、测试方法及各项实测结果待补充；达到任务书规定的ECoG通道数、覆盖面积、厚度和信号质量要求，仍需以完成后的专项测试结果为依据。')

p = doc.add_heading('（2）256通道柔性微丝神经电极', 3)
doc.add_paragraph('阵列结构设计。完成单列和双列两种位点版本的256通道微丝电极阵列设计。每版设置8根植入微丝（shank），每根布置32个位点；单列版采用8×1×32布局，位点中心距60 μm，双列版采用8×2×16布局，轴向投影节距约29.9 μm。植入段几何长度分别约为10.125 mm和10.127 mm。电极以PI为柔性绝缘材料，设计厚度小于5 μm，与任务书中微丝电极厚度要求相衔接。')
doc.add_paragraph('高密度互连优化。将连接焊盘等间距排列为连续阵列，优化扇出区与植入段之间的走线布局。走线线宽和线间距均设计为1.5 μm；256条走线在转角处汇成约0.77 mm宽的线束，再分成8组，每组32条进入对应的shank。该布局在保持256通道规模的同时，为后续版图制备与焊盘连接提供明确的几何约束。')
doc.add_paragraph('基础工艺流程开发。形成覆盖衬底与牺牲层、底部PI、焊盘、互连、顶部PI与开窗、顶电极及封装的18步工艺流程。首先在衬底上沉积SiO₂，并通过光刻、磁控溅射和剥离形成Ni牺牲层；随后旋涂底部PI，在焊盘区域形成Ti/Ni/Au接触焊盘，在互连区域形成Ti/Au/Ti金属走线。完成顶部PI覆盖后，采用厚胶掩膜与反应离子刻蚀开出电极位点和焊盘位点，再以Ti/Au形成顶电极，并在焊盘区域规划PCB键合封装。各金属层均采用磁控溅射结合剥离实现图形化。')
doc.add_paragraph('阶段性成果与后续验证。已形成256通道单列、双列设计方案、关键参数表及完整工艺流程图，为原型器件制备和工艺稳定性测试提供了可执行的设计输入。微丝电极的实际厚度、通道导通率、界面阻抗、尖峰记录信噪比等性能，需在完成试制和测试后据实报告；本阶段不将设计参数等同于实测达标结果。')

doc.add_heading('3. 项目社会效益和经济效益', 2)
doc.add_paragraph('本年度工作聚焦高通量柔性电极的前期研发，形成了ECoG电极材料选择和原型试制方案，以及256通道微丝电极阵列设计与制备工艺流程。相关技术积累有助于推进高通量神经信号采集关键部件的自主研发，并为后续电极性能验证、系统集成和汉语言脑机接口应用研究提供基础。现阶段成果主要体现为技术储备；专利、标准、成果转化及经济效益情况应在形成相应证明材料后据实填报。')

doc.add_heading('六、项目年度组织实施中的重大问题及建议', 1)
doc.add_paragraph('课题四由材料与版图设计转入原型试制及性能验证阶段后，需重点关注两类问题：一是ECoG电极的材料对比结果、器件结构与原型表征数据尚需按统一测试口径汇总，以支撑材料方案和工艺参数的进一步确定；二是256通道微丝电极采用1.5 μm线宽与线间距，高密度走线、位点开窗及焊盘键合等环节对加工一致性和良率提出较高要求，需通过实际试制和重复测试验证工艺稳定性。建议建立材料、版图、工艺和测试结果的对应记录，优先完成原型器件的界面阻抗、通道导通率、噪声及柔性稳定性测试，并依据测试结果迭代设计，为下一阶段电极定型和封装工艺优化提供依据。')

doc.add_heading('七、任务书中有特殊约定或其他需要说明的事项', 1)
doc.add_paragraph('课题任务书“需要约定的其他内容”填写为“无”。')

doc.save(OUT)
print(OUT)
