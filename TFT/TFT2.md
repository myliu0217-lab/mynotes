# IGZO 2T 漏极侧选通电流/TIA 架构的尺寸优化与 SmartSpice 仿真

## 1 研究对象与结论边界

本文只分析已经选定的第二种架构，并将两只晶体管均改为 IGZO TFT：

- 传感晶体管 $T_S$：栅极连接电极，漏极连接内部节点 $v_x$，源极连接 TIA 求和节点；
- 选通晶体管 $T_R$：位于 $T_S$ 的漏极供电侧，漏极接正电源，源极接内部节点 $v_x$，栅极由 ROW 控制；
- TIA 在闭环有效频带内将 $T_S$ 源极维持在虚地附近，并把源端电流转换成输出电压。

信号路径为：

$$
v_E\rightarrow T_S\text{ 的跨导电流}
\rightarrow \text{TIA}\rightarrow v_{\mathrm{out}}.
$$

需要首先说明：在没有给出目标偏置电流、工作电压、允许噪声、列电容、行选通时间、TIA 参数、版图最小尺寸及实测 IGZO 噪声数据之前，不存在可信的唯一“最优 $W/L$ 数值”。本文给出的结果是严格的优化条件、仿真网表和从仿真数据中选出最优尺寸的方法，而不是预先猜测一个固定尺寸。

## 2 小信号尺寸优化依据

### 2.1 有效跨导

令 TIA 求和节点小信号电压为零，$T_R$ 在选通状态下的等效小信号导纳为：

$$
g_{mR}+g_{dsR}.
$$

传感晶体管的有效跨导为：

$$
\boxed{
\frac{I_{\mathrm{sig}}}{v_E}
=
\frac{g_{mS}(g_{mR}+g_{dsR})}
{g_{mR}+g_{dsR}+g_{dsS}}
}.
$$

如果希望选通晶体管造成的跨导损失不超过 $\varepsilon_g$，则：

$$
\frac{g_{mR}+g_{dsR}}
{g_{mR}+g_{dsR}+g_{dsS}}
\geq1-\varepsilon_g,
$$

从而：

$$
\boxed{
g_{mR}+g_{dsR}
\geq
\frac{1-\varepsilon_g}{\varepsilon_g}g_{dsS}
}.
$$

若允许损失为 $5\%$：

$$
g_{mR}+g_{dsR}\geq19g_{dsS}.
$$

因此，$T_R$ 的最优尺寸不是越大越好，而是满足上述条件、压降裕量和建立时间的最小可靠尺寸。

### 2.2 输入参考噪声

两只 IGZO TFT 与 TIA 的输入参考噪声为：

$$
\begin{aligned}
S_{v,\mathrm{in}}(f)
={}&S_{eE}(f)
+\frac{S_{iS}(f)}{g_{mS}^2}
+\frac{g_{dsS}^2}
{g_{mS}^2(g_{mR}+g_{dsR})^2}S_{iR}(f)\\
&+\frac{(g_{mR}+g_{dsR}+g_{dsS})^2}
{g_{mS}^2(g_{mR}+g_{dsR})^2}
\left[
S_{iA}(f)+\frac{4kT}{R_F}+S_{i,\mathrm{other}}(f)
\right]\\
&+\frac{(g_{mR}+g_{dsR}+g_{dsS})^2}
{g_{mS}^2(g_{mR}+g_{dsR})^2}
\left|
\frac{1}{R_F}+j2\pi fC_F+Y_P(j2\pi f)
\right|^2S_{eA}(f).
\end{aligned}
$$

由该式可以直接得到尺寸趋势：

1. 增大 $T_S$ 的 $g_{mS}$ 会降低几乎所有后端噪声的输入参考值；
2. 增大 $T_S$ 面积 $W_SL_S$ 通常降低 IGZO 陷阱主导的低频噪声；
3. 但增大 $W_S$ 会增加 $C_{gsS}$、$C_{gdS}$ 和 TIA 求和节点导纳 $Y_P$，从而放大运放电压噪声并降低相位裕量；
4. 增大 $g_{mR}+g_{dsR}$ 可减小 $T_R$ 噪声耦合和跨导损失，但过大的 $W_R$ 会增加漏极节点电容、ROW 馈通和开关注入。

### 2.3 IGZO TFT 的特殊约束

IGZO 尺寸优化必须额外考虑：

- 接触电阻 $R_C$ 可能主导总电阻，使增大 $W/L$ 的收益提前饱和；
- 界面态和体陷阱引起的 $1/f$ 噪声通常不能由简单硅 MOSFET 公式准确预测；
- 正偏压应力会引起 $V_T$ 漂移；
- 关断漏电和器件间离散性可能随短沟道设计恶化；
- 栅漏重叠电容会直接增加 TIA 求和节点电容或内部节点电容。

固定偏置电流下，尺寸趋势可用下式作初步理解：

$$
g_{mS}\propto\sqrt{\frac{W_S}{L_S}},
\qquad
S_{v_g,1/f}\propto\frac{1}{W_SL_S},
$$

但最终必须以模型或实测结果为准。

## 3 最优尺寸的判据

对每组 $(W_S,L_S,W_R,L_R)$，至少计算以下指标：

1. 直流漏极电流 $I_D$；
2. $T_S$ 的 $g_{mS}$、$g_{dsS}$、$V_{DS,S}$；
3. $T_R$ 的 $g_{mR}$、$g_{dsR}$、$V_{DS,R}$；
4. 有效跨导；
5. TIA 低频增益、带宽和相位裕量；
6. 目标频带内输入参考积分噪声；
7. ROW 选通后的建立时间；
8. 两只晶体管总面积、求和节点电容和内部节点电容；
9. $V_T$、温度、迁移率和接触电阻变化下的最差结果。

建议设置硬约束：

$$
\frac{g_{mR}+g_{dsR}}
{g_{mR}+g_{dsR}+g_{dsS}}
\geq0.95,
$$

$$
t_{\mathrm{set}}\leq t_{\mathrm{row}},
\qquad
\mathrm{PM}\geq60^{\circ},
$$

$$
V_{DS,S}\geq V_{DS,S,\min},
\qquad
V_{DS,R}\text{ 满足选通区要求}.
$$

在满足全部硬约束的候选中，以输入参考积分噪声为主目标：

$$
v_{n,\mathrm{in,rms}}
=\sqrt{
\int_{f_L}^{f_H}S_{v,\mathrm{in}}(f)\,df
}.
$$

若多个候选噪声接近，例如差别小于 $5\%$，优先选择面积更小、输入电容更小、建立更快且对 $V_T$ 漂移更鲁棒的尺寸。

## 4 模型卡使用前必须确认的问题

指定库文件实际包含 `W7L7`、`W14L7`、`W21L7`、`W28L7`、`W35L7`、`W63L7`、`W105L7`、`W154L7`、`W203L7`、`W420L7` 和 `W840L7` 等按几何尺寸分别拟合的模型。下面按照要求另外定义 `MY_W600L10`，并通过实例参数 $W$、$L$ 扫描尺寸。

这隐含了一个重要假设：`MY_W600L10` 的参数对其他 $W$、$L$ 具有可缩放性。若该参数集本质上只拟合了一个尺寸，那么扫描得到的只能作为趋势初筛，最终候选必须用对应几何的实测模型重新验证。尤其是 `RD=100`、`RS=100`、`MU0`、`LAMBDA` 和陷阱相关参数未必能随实例宽度自动正确缩放。

另外，给定模型设置了：

```text
CAPMOD = 0
CGSO   = 1.31e-13
CGDO   = 1.31e-13
```

并且没有显式给出常见的 $1/f$ 噪声拟合参数。因此：

- 必须检查 SmartSpice 输出的 $C_{gs}$、$C_{gd}$ 是否与实测一致；
- 必须检查 `.NOISE` 是否真正包含 LEVEL 36 IGZO 模型的低频噪声；
- 如果 `.NOISE` 只给出热噪声或噪声为零，必须用实测 $S_{iS}(f)$、$S_{iR}(f)$ 后处理，不能据此宣称某个尺寸噪声最优。

## 5 SmartSpice 主仿真网表

下面的网表严格以指定内容开头。它采用理想有限增益 TIA 进行尺寸初筛；最终稳定性和绝对噪声必须换成实际运放宏模型。

```spice
* 导入 TFT 工艺库 
.LIB 'C:\Users\12508\Documents\xwechat_files\wxid_ncy6a4tna08y11_7cd8\msg\file\2026-06\NVO_TFT Modelcard.LIB' NVOTFT

* 修改模型参数
.MODEL MY_W600L10 NTFT (
+LAMBDA   = 0.0497989      LEVEL    = 36             VERSION  = 2
+TNOM     = 27             TOX      = 1.03577e-07 
+VTO      = 10           
*<--- 【在这里把 VTO 修改成你想要的数值，比如 5.0】
+VFB      = 0              VON      = 0              DVT      = 0
+VKINK    = 10             VSI      = 6.24934        VST      = 10
+MU1      = 0.1            MMU      = 1.02429        MU0      = 21.2225
+MK       = 2              MUS      = 2              RD       = 100
+RS       = 100            BT       = 5.82535e-05    BLK      = 1e-08
+DD       = 2.93579e-06    DELTA    = 2.8843         DG       = 6.43138e-07
+EB       = 0.640753       ETA      = 1.65606        I0       = 17.2082
+I00      = 10             ASAT     = 1.6111         AT       = 6.17753e-09
+DASAT    = 0              LASAT    = 3.16543e-06    LKINK    = 1e-09
+DVTO     = 0              DMU1     = 0              CAPMOD   = 0
+CGSO     = 1.31e-13       CGDO     = 1.31e-13       ETAC00   = 0
+MC       = 3              RDX      = 0              RSX      = 0
+ZEROC    = 0              ME       = 2.5            MSS      = 1.5
+THETA    = 0              ISUBMOD  = 0              INTSDNOD = 0
+SCALERPI = 0 )

************************************************************
* IGZO 2T 漏极侧选通 + TIA 尺寸扫描
************************************************************
.OPTIONS POST=2 LIST NODECK NOMOD ACCURATE SAVEMEASUREOUT
.TEMP 27

* ---------- 可修改的系统参数 ----------
.PARAM VDDVAL = 12
.PARAM VROWON = 20
.PARAM VECM   = 0
.PARAM VREFVAL = -5.2
.PARAM DVIN   = 10m

.PARAM WS = 600u
.PARAM LS = 10u
.PARAM WR = 600u
.PARAM LR = 10u

.PARAM RFB = 330k
.PARAM CFB = 1n
.PARAM CIN = 20p
.PARAM A0  = 1e6
.PARAM ROUTOP = 10
.PARAM RLOAD  = 1meg

* ---------- 电源、ROW 与电极输入 ----------
VDD    VDD   0  DC='VDDVAL'

* DC/AC 使用 VROWON；TRAN 使用 PULSE 波形
VROW   GROW  0  DC='VROWON'
+ PULSE(0 'VROWON' 1m 1u 1u 8m 12m)

* DC 工作点为 VECM；AC 幅值为 1 V；TRAN 叠加 DVIN 阶跃
VELEC  GE    0  DC='VECM' AC=1
+ PULSE('VECM' 'VECM+DVIN' 3m 1u 1u 20m 40m)

* TIA 虚地参考；实测仿真中 -12 V 会造成过大的静态电流和输出饱和
VREF   VREF  0  DC='VREFVAL'

* ---------- 2T pixel ----------
* 本机 SmartSpice LEVEL 36 NTFT 使用三端格式：漏极 栅极 源极 模型
MTR    VDD   GROW  VX  MY_W600L10 W='WR' L='LR'
MTS    VX    GE    VS  MY_W600L10 W='WS' L='LS'

* ---------- TIA ----------
* VOUT = A0*(VREF - VS)，使 VS 形成 VREF 附近的低阻虚地
EOP    NDRV  0     VREF VS  'A0'
ROUT1  NDRV  VOUT  'ROUTOP'
RFBK   VOUT  VS    'RFB'
CFBK   VOUT  VS    'CFB'

* 求和节点总寄生电容；应替换为版图/实测值
CINP   VS    0     'CIN'
RLOUT  VOUT  0     'RLOAD'

* ---------- 工作点与输出 ----------
.OP
.PRINT OP V(VX) V(VS) V(VOUT)
+ I(VDD) @MTS[CD] @MTS[GM] @MTS[GDS]
+ @MTR[CD] @MTR[GM] @MTR[GDS]

* ---------- DC 电极共模扫描 ----------
.DC VELEC -2 8 0.1
.PRINT DC V(VX) V(VS) V(VOUT) I(VDD)
+ @MTS[CD] @MTS[GM] @MTS[GDS]
+ @MTR[CD] @MTR[GM] @MTR[GDS]

* ---------- AC 增益与带宽 ----------
.AC DEC 40 0.1 10MEG
.PRINT AC VM(VOUT) VP(VOUT) VM(VS) VM(VX)

.MEASURE AC AV10HZ FIND VM(VOUT) AT=10
.MEASURE AC F3DB WHEN VM(VOUT)='AV10HZ*0.70710678'

* 低频时 Gm_eff 约等于 |VOUT|/RFB
.MEASURE AC GMEFF10 PARAM='AV10HZ/RFB'

* ---------- 噪声 ----------
.NOISE V(VOUT) VELEC DEC 40 0.1 100K
.PRINT NOISE INOISE ONOISE

* ---------- ROW 选通与电极阶跃瞬态 ----------
.TRAN 2u 20m
.PRINT TRAN V(GROW) V(GE) V(VX) V(VS) V(VOUT) I(VDD)

.MEASURE TRAN VOUT_FINAL FIND V(VOUT) AT=19m
.MEASURE TRAN VOUT_RMS RMS V(VOUT) FROM=10m TO=19m

.END
```

### 5.1 该网表的偏置必须先检查

当前示例使用：

$$
V_{DD}=12\ \mathrm{V},\qquad
V_{ROW}=20\ \mathrm{V},\qquad
V_{E,CM}=0\ \mathrm{V},\qquad
V_{\mathrm{REF}}=-5.2\ \mathrm{V},
$$

这是本机实际扫描后用于尺寸比较的偏置。原有 $V_{\mathrm{REF}}=-12\ \mathrm{V}$ 在 $W_S=W_R=600\ \mu\mathrm{m}$、$L_S=L_R=10\ \mu\mathrm{m}$ 时产生约 $1.507\ \mathrm{mA}$ 静态电流和约 $-509.4\ \mathrm{V}$ 的理想 TIA 输出，实际运放必然饱和；改为 $V_{\mathrm{REF}}=-5.2\ \mathrm{V}$ 后，静态电流约为 $8.39\ \mu\mathrm{A}$，输出约为 $-7.97\ \mathrm{V}$。这些数值仍需根据实际运放供电与目标电流修改。运行后必须确认：

1. $T_S$ 已导通但没有超过允许电流；
2. 内部节点 $v_x$ 给 $T_S$ 留有足够 $V_{DS,S}$；
3. $T_R$ 处于目标选通工作区；
4. TIA 输出没有超过实际运放电源范围；
5. 若将 $VTO$ 改为 $5\ \mathrm{V}$，必须同步重新选择 $V_{ROW}$、$V_{E,CM}$ 和 $V_{DD}$。

## 6 尺寸扫描网表

### 6.1 第一阶段：固定 $L_S=L_R=10\ \mu\mathrm{m}$ 扫描宽度

先在主网表中把原 `.AC` 行替换为：

```spice
.AC DEC 30 0.1 10MEG
+ SWEEP WS LIST 6 100u 200u 400u 600u 800u 1000u
+ SWEEP WR LIST 6 50u 100u 200u 400u 600u 800u
```

把 `.TRAN` 行替换为：

```spice
.TRAN 2u 20m
+ SWEEP WS LIST 6 100u 200u 400u 600u 800u 1000u
+ SWEEP WR LIST 6 50u 100u 200u 400u 600u 800u
```

SmartSpice 官方示例支持在 AC 和 TRAN 分析后使用 `SWEEP ... LIST` 或多重 sweep。为避免输出文件过大，建议 AC、TRAN 和 NOISE 分成三个网表分别运行，而不是一次扫描所有分析。

### 6.2 第二阶段：扫描沟道长度

从第一阶段保留噪声与面积表现最好的 3 到 5 组宽度，再扫描：

```spice
.AC DEC 30 0.1 10MEG
+ SWEEP LS LIST 4 5u 10u 15u 20u
+ SWEEP LR LIST 4 5u 10u 15u 20u
```

但必须注意：给定自定义模型的名称是 `MY_W600L10`，其参数可能只对接近 $L=10\ \mu\mathrm{m}$ 的器件可信。若没有其他长度的测量数据，$L=5\ \mu\mathrm{m}$ 或 $20\ \mu\mathrm{m}$ 的结果只能作为数学外推。

### 6.3 使用 `.DATA` 明确列出候选尺寸

为了避免多重扫描生成过多无效组合，推荐用 `.DATA` 列出候选：

```spice
.DATA GEOM WS LS WR LR
+ 200u 10u 100u 10u
+ 400u 10u 100u 10u
+ 400u 10u 200u 10u
+ 600u 10u 200u 10u
+ 600u 10u 400u 10u
+ 800u 10u 400u 10u
+ 800u 10u 600u 10u
.ENDDATA

.AC DEC 30 0.1 10MEG SWEEP DATA=GEOM
```

瞬态分析同理：

```spice
.TRAN 2u 20m SWEEP DATA=GEOM
```

若所安装的 SmartSpice 版本不接受 `.NOISE ... SWEEP DATA=GEOM`，应为每个候选修改四个 `.PARAM` 后分别运行 `.NOISE`，不要用不受版本支持的语法强行批处理。

## 7 建议分成四个仿真任务

### 7.1 任务 A：DC 工作点和偏置裕量

目的：淘汰不能正确偏置的尺寸。

操作：

1. 打开 SmartSpice，新建输入文件；
2. 粘贴第 5 节完整网表；
3. 确认 `.LIB` 路径存在；
4. 先只保留 `.OP` 和 `.DC`，注释 `.AC`、`.NOISE`、`.TRAN`；
5. Source 网表并 Run；
6. 在日志中读取 `@MTS[CD]`、`@MTS[GM]`、`@MTS[GDS]`、`@MTR[CD]`、`@MTR[GM]`、`@MTR[GDS]`；
7. 若当前版本的 LEVEL 36 模型使用不同的工作点变量名，先使用 `.PRINT OP @MTS[*] @MTR[*]` 或在 SmartView 中查看器件 operating-point 列表，再替换名称；
8. 淘汰 TIA 输出超限、$T_S$ 漏极裕量不足或电流过大的组合。

对每组尺寸，由工作点数据计算：

$$
G_{m,\mathrm{eff}}
=\frac{g_{mS}(g_{mR}+g_{dsR})}
{g_{mR}+g_{dsR}+g_{dsS}},
$$

以及：

$$
\eta_R
=\frac{g_{mR}+g_{dsR}}
{g_{mR}+g_{dsR}+g_{dsS}}.
$$

只保留 $\eta_R\geq0.95$ 的组合。

### 7.2 任务 B：AC 增益、带宽和 TIA 稳定性

目的：检查跨导增益和输入电容代价。

理想 TIA 初筛时：

$$
|G_{m,\mathrm{eff}}|
\approx\frac{|v_{\mathrm{out}}|}{R_F|v_E|}
$$

适用于：

$$
f\ll\frac{1}{2\pi R_FC_F}.
$$

操作：

1. 运行 AC 尺寸扫描；
2. 在 SmartView 中分别绘制 `VM(VOUT)`、`VP(VOUT)`、`VM(VS)`；
3. $|v_s|$ 必须远小于 $|v_E|$，否则虚地假设失效；
4. 用实际运放宏模型替换 `EOP` 与 `ROUT1` 后重新运行；
5. 检查闭环增益、$-3\ \mathrm{dB}$ 带宽、相位裕量和增益峰化；
6. 若增大 $W_S$ 后带宽下降或峰化增加，说明求和节点电容已经成为限制。

理想受控源没有真实运放的有限增益带宽和噪声，因此不能用它确定最终的 $C_F$ 或相位裕量。

### 7.3 任务 C：噪声

官方 SmartSpice 示例采用：

```spice
.NOISE V(VOUT) VELEC DEC 40 0.1 100K
.PRINT NOISE INOISE ONOISE
```

其中：

- `ONOISE` 是输出节点噪声谱；
- `INOISE` 是除以电极到输出信号增益后的输入参考噪声谱；
- 应在相同 $f_L$、$f_H$ 内比较所有尺寸；
- SmartSpice 日志或 SmartView 中应查看器件噪声贡献列表，确认 `MTS`、`MTR` 和 `RFBK` 是否出现。

运行顺序：

1. 先运行标称尺寸；
2. 检查 `MTS` 和 `MTR` 是否有非零噪声贡献；
3. 检查低频谱是否表现出符合实测的 $1/f^{\alpha}$ 斜率；
4. 若 LEVEL 36 模型没有正确低频噪声，导出每组尺寸的 $g_m$、$g_{ds}$ 和 AC 传递函数；
5. 使用实测的 $S_{iS}(f,W,L)$、$S_{iR}(f,W,L)$ 代入第 2.2 节公式进行后处理；
6. 对 `INOISE` 积分得到 $v_{n,\mathrm{in,rms}}$，再排序。

反馈电阻热噪声必须保留：

$$
S_{i,R_F}=\frac{4kT}{R_F}.
$$

实际运放的输入电流噪声与电压噪声必须来自其宏模型或数据手册。理想 `EOP` 不会自动产生这些噪声。

### 7.4 任务 D：ROW 选通与建立时间

瞬态波形中，ROW 在 $1\ \mathrm{ms}$ 处打开，电极在 $3\ \mathrm{ms}$ 处产生小阶跃。对每个候选尺寸：

1. 读取最终稳定输出 $V_{\mathrm{final}}$；
2. 计算误差带：

$$
V_{\mathrm{final}}\pm
\varepsilon_{\mathrm{set}}|V_{\mathrm{final}}-V_{\mathrm{initial}}|;
$$

3. 找到波形进入该误差带且不再离开的最早时间；
4. 计算 $t_{\mathrm{set}}$；
5. 推荐同时使用 $0.1\%$ 与 $1\%$ 两个误差标准；
6. 淘汰 $t_{\mathrm{set}}>t_{\mathrm{row}}$ 的尺寸。

若需要在网表中自动测量，并且已经知道目标电压，可加入标准 TRIG/TARG 测量，例如：

```spice
* 示例：目标输出从 0 V 变化到 -1 V，测量达到 -0.999 V 的时间
.MEASURE TRAN TSET
+ TRIG V(GE) VAL='VECM+0.5*DVIN' RISE=1
+ TARG V(VOUT) VAL=-0.999 CROSS=1
```

实际目标电压随尺寸变化，所以批量扫描时更推荐在 SmartView 或导出的 CSV 中根据每条曲线的最终值计算建立时间。

## 8 阈值漂移、温度和工艺角

指定模型的标称阈值为：

$$
V_{TO}=10\ \mathrm{V}.
$$

至少应分别将网表中的 `VTO` 修改为低、标称、高三个值后重复四类仿真，例如：

$$
V_{TO}\in\{8,10,12\}\ \mathrm{V}.
$$

该范围只是演示，最终范围应来自 IGZO 偏压应力和批次统计。还应扫描：

$$
T\in\{0,27,50,75\}^{\circ}\mathrm{C},
$$

以及 $MU0$、$RD$、$RS$ 和列电容。可用 `.ALTER` 分别建立工艺角，也可为每个角生成独立网表。最优尺寸必须在所有角落都满足硬约束，而不是只在 $27^{\circ}\mathrm{C}$ 标称点最优。

SmartSpice 支持 Monte Carlo/Variation 分析，但只有在参数统计分布已由实测确定时才有意义。没有分布数据时，不应随意假设高斯标准差并据此报告良率。

## 9 从仿真结果选出最终尺寸

建议建立结果表，每一行对应一组尺寸：

| $W_S$ | $L_S$ | $W_R$ | $L_R$ | $I_D$ | $g_{mS}$ | $g_{dsS}$ | $g_{mR}+g_{dsR}$ | $\eta_R$ | $v_{n,\mathrm{in,rms}}$ | $f_{-3\mathrm{dB}}$ | $t_{\mathrm{set}}$ | 面积 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

筛选顺序如下：

1. 删除直流工作点不正确的组合；
2. 删除 $\eta_R<0.95$ 的组合；
3. 删除 TIA 输出超量程或相位裕量不足的组合；
4. 删除建立时间不合格的组合；
5. 删除最差 $V_T$、温度或接触电阻角落失效的组合；
6. 在剩余组合中选择输入参考积分噪声最小者；
7. 如果噪声接近，选择总面积与求和节点电容更小者。

推荐的实际优化方向是：

- $T_S$：先增加面积和 $W_S/L_S$，直到输入参考噪声不再明显下降，或 TIA 电压噪声、带宽、稳定性开始恶化；
- $T_R$：选择刚好满足 $g_{mR}+g_{dsR}\geq19g_{dsS}$、压降和建立时间要求的最小尺寸；
- 不应默认 $W_S=W_R$；通常 $T_S$ 由噪声—电容折中决定，$T_R$ 由选通能力决定；
- 如果接触电阻主导，应先优化接触工艺，否则继续增宽的收益有限。

## 10 SmartSpice 操作步骤

1. 启动 SmartSpice；
2. 新建文本输入文件，例如 `igzo_2t_nominal.in`；
3. 粘贴第 5 节完整网表；
4. 使用 Windows 文件资源管理器确认模型路径准确；
5. 在 SmartSpice 中 Source 输入文件；
6. 查看日志，首先确认 `.LIB ... NVOTFT` 成功载入且 `MY_W600L10` 没有重复定义；
7. 第一次只运行 `.OP`，修正所有模型、节点、工作点错误；
8. 再分别建立 `igzo_2t_dc.in`、`igzo_2t_ac.in`、`igzo_2t_noise.in` 和 `igzo_2t_tran.in`，每个文件只保留一种主要分析；
9. 在 SmartView 中打开 RAW 文件，绘制对应波形；
10. 打开 `flattened_sweep`，使参数扫描结果便于按尺寸绘图：

```spice
.CONTROL
SET FLATTENED_SWEEP=TRUE
SET PARAMETRIC_DATA_IN_RAW=TRUE
.ENDC
```

11. 查看 `.measure` 输出文件和主日志；
12. 将每个候选的工作点、噪声、带宽和建立时间整理到第 9 节的表格；
13. 用实际运放宏模型、实测列电容和实测 IGZO 噪声数据重新验证最终 3 到 5 组候选；
14. 对最终候选运行 $V_T$、温度、接触电阻和列电容角落；
15. 只在最差角落也满足全部指标后确定版图尺寸。

本机已确认可调用 `D:\sedatools\exe\smartspice.exe`，实际加载版本为 SmartSpice 4.32.4.R。第 12 节给出了本次真实运行结果。本机 LEVEL 36 `NTFT` 的实例语法为三端格式，且可输出 `GM`、`GDS`、电容和噪声结果。

## 11 官方语法参考

- [Silvaco SmartSpice `.NOISE` 分析示例](https://silvaco.com/examples/smartspice/section2/example17/index.html)
- [Silvaco SmartSpice 多参数 AC sweep 示例](https://silvaco.com/examples/smartspice/section2/example3/index.html)
- [Silvaco SmartSpice 多重 sweep 与 `.DATA` 示例](https://silvaco.com/examples/smartspice/section2/example9/index.html)
- [Silvaco SmartSpice 工作点参数扫描说明](https://silvaco.com/wp-content/uploads/content/appNotes/analog/1-015_Operation_point_analyses.pdf)
- [Silvaco SmartSpice Monte Carlo 工作点示例](https://silvaco.com/examples/smartspice/section2/example7/index.html)

## 12 本次 SmartSpice 实际仿真结果

### 12.1 仿真环境与文件

实际调用程序为：

```text
D:\sedatools\exe\smartspice.exe
```

SmartSpice 实际加载版本为 `4.32.4.R`。仿真输入和输出文件保存在：

```text
D:\lmy-graduate\workspace\docs\mynotes\TFT\smartspice_runs
```

主要文件为：

- `igzo_2t_nominal.in/.out/.raw`：标称工作点、偏置扫描、AC 和噪声；
- `igzo_2t_grid.in/.out/.raw`：宽度网格的 DC、AC、噪声和瞬态扫描；
- `igzo_2t_length.in/.out/.raw`：沟道长度外推扫描。

仿真采用：

$$
V_D=12\ \mathrm{V},\quad
V_{ROW}=20\ \mathrm{V},\quad
V_E=0\ \mathrm{V},\quad
V_{\mathrm{REF}}=-5.2\ \mathrm{V},
$$

$$
R_F=330\ \mathrm{k\Omega},\qquad
C_F=1\ \mathrm{nF},\qquad
T=27^{\circ}\mathrm{C}.
$$

### 12.2 偏置扫描结果

在 $W_S=W_R=600\ \mu\mathrm{m}$、$L_S=L_R=10\ \mu\mathrm{m}$ 时：

| $V_{\mathrm{REF}}$ | 静态电流 | 理想 TIA 输出 | 结论 |
|---:|---:|---:|---|
| $-12\ \mathrm{V}$ | $1.5072\ \mathrm{mA}$ | $-509.39\ \mathrm{V}$ | 实际必然饱和，不可用 |
| $-5.3\ \mathrm{V}$ | $11.086\ \mu\mathrm{A}$ | $-8.958\ \mathrm{V}$ | 可用于较高电流偏置 |
| $-5.2\ \mathrm{V}$ | $8.394\ \mu\mathrm{A}$ | $-7.970\ \mathrm{V}$ | 本次尺寸扫描采用 |
| $-5.0\ \mathrm{V}$ | $4.319\ \mu\mathrm{A}$ | $-6.425\ \mathrm{V}$ | 更低功耗候选 |

输出电压不仅包含 $-I_DR_F$，还以 $V_{\mathrm{REF}}$ 为基准：

$$
V_{\mathrm{out,DC}}
\approx V_{\mathrm{REF}}-I_DR_F.
$$

因此最终偏置必须同时满足静态电流、输入共模范围和运放输出摆幅要求。

### 12.3 宽度网格结果

固定：

$$
L_S=L_R=10\ \mu\mathrm{m},
$$

扫描：

$$
W_S\in\{200,400,600,800\}\ \mu\mathrm{m},
$$

$$
W_R\in\{100,200,400\}\ \mu\mathrm{m}.
$$

其中：

$$
\eta_R=
\frac{g_{mR}+g_{dsR}}
{g_{mR}+g_{dsR}+g_{dsS}}.
$$

实际结果如下。噪声为 SmartSpice 在 $1\ \mathrm{Hz}$ 至 $100\ \mathrm{kHz}$ 内给出的总等效输入积分噪声；建立时间采用 $10\ \mathrm{mV}$ 电极阶跃和 $0.1\%$ 误差带计算。

| $W_S$/$\mu$m | $W_R$/$\mu$m | $I_D$/$\mu$A | $g_{mS}$/$\mu$S | $\eta_R$ | $G_{m,\mathrm{eff}}$/$\mu$S | 输入噪声/$\mu$V rms | 建立时间/$\mu$s |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 200 | 100 | 2.778 | 7.998 | 0.98494 | 7.876 | 15.2280 | 2002 |
| 200 | 200 | 2.800 | 8.044 | 0.99177 | 7.976 | 15.1300 | 2762 |
| 200 | 400 | 2.812 | 8.069 | 0.99566 | 8.032 | 15.0770 | 1950 |
| 400 | 100 | 5.477 | 15.826 | 0.97373 | 15.407 | 9.8125 | 2380 |
| 400 | 200 | 5.554 | 15.989 | 0.98490 | 15.744 | 9.7253 | 2464 |
| 400 | 400 | 5.598 | 16.081 | 0.99173 | 15.944 | 9.6761 | 3310 |
| 600 | 100 | 8.112 | 23.513 | 0.96455 | 22.675 | 7.7508 | 2298 |
| 600 | 200 | 8.269 | 23.847 | 0.97895 | 23.340 | 7.6679 | 2326 |
| 600 | 400 | 8.361 | 24.041 | 0.98814 | 23.750 | 7.6203 | 2292 |
| 800 | 100 | 10.692 | 31.079 | 0.95664 | 29.725 | 6.6067 | 2088 |
| 800 | 200 | 10.948 | 31.626 | 0.97367 | 30.786 | 6.5259 | 2188 |
| 800 | 400 | 11.102 | 31.951 | 0.98483 | 31.459 | 6.4786 | 2208 |

所有候选均满足 $\eta_R\ge0.95$。在本次网格内：

- 绝对最低输入噪声出现在 $W_S=800\ \mu\mathrm{m}$、$W_R=400\ \mu\mathrm{m}$；
- 其输入参考积分噪声为 $6.4786\ \mu\mathrm{V}_{\mathrm{rms}}$；
- 将 $W_R$ 减小到 $100\ \mu\mathrm{m}$ 后，噪声为 $6.6067\ \mu\mathrm{V}_{\mathrm{rms}}$，仅增加约 $1.98\%$；
- $W_R=100\ \mu\mathrm{m}$ 时 $\eta_R=0.95664$，仍满足允许跨导损失小于 $5\%$ 的要求；
- 因而按照“噪声距最小值不超过 $5\%$ 时优先选更小面积”的规则，宽度推荐为：

$$
\boxed{
W_S=800\ \mu\mathrm{m},\qquad
W_R=100\ \mu\mathrm{m}
}.
$$

本次所有组合的 $-3\ \mathrm{dB}$ 频率都约为：

$$
f_{-3\mathrm{dB}}\approx482.6\ \mathrm{Hz},
$$

因为它主要由当前理想 TIA 的：

$$
R_FC_F=330\ \mu\mathrm{s}
$$

决定，而不是由 TFT 尺寸决定：

$$
\frac{1}{2\pi R_FC_F}\approx482.3\ \mathrm{Hz}.
$$

建立时间约为 $2.0$ 至 $3.3\ \mathrm{ms}$，同样主要受反馈时间常数限制。这里的细小非单调差异不应被解释为可靠的尺寸规律。

### 12.4 长度扫描结果及模型失效判断

在 $W_S=800\ \mu\mathrm{m}$、$W_R=100\ \mu\mathrm{m}$ 下，对 $L_S,L_R\in\{5,10,15,20\}\ \mu\mathrm{m}$ 进行了数学扫描。

结果出现明显的模型外推异常：

- 当 $L_S=5\ \mu\mathrm{m}$ 时，静态电流上升到约 $0.697$ 至 $1.581\ \mathrm{mA}$，理想 TIA 输出达到 $-235$ 至 $-527\ \mathrm{V}$，不满足输出摆幅约束；
- 当 $L_S\ge15\ \mu\mathrm{m}$ 时，模型给出的 $g_{mS}$ 接近零，电路几乎关断，等效输入噪声跳变到约 $0.834\ \mathrm{V}_{\mathrm{rms}}$；
- 这两种结果与标称 $L_S=10\ \mu\mathrm{m}$ 附近不连续，说明 `MY_W600L10` 不适合跨较大长度范围外推。

在唯一保持合理工作点的 $L_S=10\ \mu\mathrm{m}$ 组内：

| $L_S$/$\mu$m | $L_R$/$\mu$m | 静态电流/$\mu$A | $G_{m,\mathrm{eff}}$/$\mu$S | 输入噪声/$\mu$V rms | 结论 |
|---:|---:|---:|---:|---:|---|
| 10 | 5 | 11.175 | 31.783 | 6.4567 | 模型预测最好，但属于 $L_R$ 外推 |
| 10 | 10 | 10.692 | 29.726 | 6.6065 | 与模型标称长度一致，可信度最高 |
| 10 | 15 | 9.910 | 27.117 | 6.8605 | 跨导降低 |
| 10 | 20 | 9.229 | 25.461 | 7.0869 | 跨导与噪声更差 |

因此：

1. 若只按当前可缩放模型的数值结果，候选尺寸为：

$$
W_S/L_S=800/10\ \mu\mathrm{m},\qquad
W_R/L_R=100/5\ \mu\mathrm{m}.
$$

2. 但 `MY_W600L10` 是以 $L=10\ \mu\mathrm{m}$ 命名和拟合的模型，$L_R=5\ \mu\mathrm{m}$ 的改进不能作为流片结论；
3. 在没有 $L_R=5\ \mu\mathrm{m}$ 实测模型前，推荐的可制造标称尺寸应保守取：

$$
\boxed{
W_S/L_S=800/10\ \mu\mathrm{m},\qquad
W_R/L_R=100/10\ \mu\mathrm{m}
}.
$$

### 12.5 噪声结果的适用范围

SmartSpice 确实产生了非零 TFT 与电阻噪声，并成功输出 `INOISE` 和 `ONOISE`。但该模型卡没有显式给出经过实测拟合的 IGZO $1/f$ 噪声参数，因此上述积分噪声只能作为当前 LEVEL 36 默认噪声模型下的相对比较，不能当作最终绝对噪声预测。

在确定版图前，还必须完成：

1. 测量不同 $W,L$ 的 IGZO TFT 电流噪声谱；
2. 用实测 $S_{iS}(f)$、$S_{iR}(f)$ 校准模型；
3. 使用实际 TIA 运放宏模型加入 $e_n$、$i_n$、输入电容和输出摆幅限制；
4. 加入真实列电容、未选通单元漏电和 ROW 馈通；
5. 对 $V_T$、迁移率、接触电阻和温度做角落分析。

### 12.6 本次仿真的最终建议

在当前模型、偏置和 $1\ \mathrm{Hz}$ 至 $100\ \mathrm{kHz}$ 噪声带宽下：

$$
\boxed{
T_S:\ W_S/L_S=800/10\ \mu\mathrm{m}
}
$$

$$
\boxed{
T_R:\ W_R/L_R=100/10\ \mu\mathrm{m}
}
$$

是现阶段最稳妥的标称选择。若后续得到 $L_R=5\ \mu\mathrm{m}$ 的有效模型或实测数据，并确认关断漏电、阈值漂移、ROW 馈通和可靠性均合格，则可以进一步考虑：

$$
T_R:\ W_R/L_R=100/5\ \mu\mathrm{m}.
$$

该推荐是有条件的仿真结论，不是脱离偏置、TIA 和工艺统计后的通用最优尺寸。

