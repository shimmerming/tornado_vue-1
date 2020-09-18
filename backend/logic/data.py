# [[i for i in item.split("|")] for item in x.split("\n") if item]

华信鼎成服务器产品目录 = """
平台系列|主推型号|平台型号描述|应单型号
2U通用服务器|R2308 i1| CXSail R2308 i1 2U/8盘位双路机架式服务器，支持两个二代英特尔®至强®可扩展处理器，支持CPU TDP205W TDP,提供24个DDR4 ECC RDIMM/LRDIMM内存插槽，支持12个英特尔® 傲腾™ 持久内存模组，每CPU支持6个，提供8个PCIE3.0扩展，提供2个10GbE RJ45网络接口,提供1300W冗余电源，机架导轨ｘ1付。|R2312 i1   R2224i1

3U存储服务器|R3316 i1|CXSail R3316 i1 3U/16盘位双路机架存储服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP140W，提供8个DDR4 ECC RDIMM/LRDIMM内存插槽，提供2个 PCI-E 3.0 x16,3个 PCI-E 3.0 x8,1个 PCI-E 3.0 x4 (in x8 slot)提供2个1GbE RJ45网络接口，提供800W冗余电源，机架导轨机架导轨ｘ1付|"平台如果需要205W TDP支持，4 个PCI-E 3.0 x16, 2 个PCI-E 3.0 x8，成本增加500元"

4U存储服务器|R4324 i1|CXSail R4324 i1 4U/24盘位双路机架存储服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP140W，提供8个DDR4 ECC RDIMM/LRDIMM内存插槽，提供2个 PCI-E 3.0 x16,3个 PCI-E 3.0 x8,1个 PCI-E 3.0 x4 (in x8 slot)。提供2个1GbE RJ45网络接口，提供800W冗余电源，机架导轨机架导轨ｘ1付|"平台如果需要205W TDP支持，4 个PCI-E 3.0 x16, 2 个PCI-E 3.0 x8，成本增加500元"


4U存储服务器| R4336 i1|CXSail R4336 i1 4U/36盘位双路机架存储服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP140W ,提供8个DDR4 ECC RDIMM/LRDIMM内存插槽，提供2个 PCI-E 3.0 x16,3个 PCI-E 3.0 x8,1 个PCI-E 3.0 x4 (in x8 slot)提供2个1GbE RJ45网络接口，提供1200W冗余电源，机架导轨机架导轨ｘ1付|"平台如果需要205W TDP支持，4 个PCI-E 3.0 x16, 2 个PCI-E 3.0 x8，成本增加500元"


2U双节点|T2208  i1|CXSail T2208 i1 2U双节点超算服务器，提供192个计算核心，全模块化风冷设计，每节点提供24个 DDR4 2933 MT/s DIMMS,提供2个M.2 SATA/NVMe SSDs和2个U.2 NVMe 热插拔SSD盘位，2个1GbE RJ45接口,4个 PCI-E 3.0 x16扩展槽,整个系统提供3组热交换2100W冗余铂金级电源

2U四节点|F2312 i1|CXSail F2312 i1 2U四节点超算服务器，全模块化风冷设计，每节点支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持高达CPU TDP 165W,每节点提供16个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s,支持英特尔® 傲腾™ 持久内存（2代处理器），提供3个3.5寸兼容2.5寸热插拔盘位，每节点提供1个M.2 SATA/PCIeｘ4连接，同时提供提个1个M.2 PCIeｘ4扩展连接，,提供2个 PCI-E 3.0 x16扩展槽,提供2个10GbE RJ45网络接口，整系统提供2130W冗余电源|  F2224 I1

四路企业级服务器|M2224 i4|CXSail M2224 i4四路数据中心级服务器，支持4颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP 70-165W, 选配配件最高可以支持205W TDP.提供48个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s，提供24个SAS/SATA 2.5寸热插拔盘位，提供5个 PCI-E 3.0 x8 插槽,  6个 PCI-E 3.0 x16 插槽，提供4个1GbE RJ45网络接口，提供1600W钛金级冗余电源（https://www.supermicro.org.cn/zh_cn/products/system/2U/2049/SYS-2049U-TR4.cfm）|M4324 I 4

八路企业级服务器|  M7216 i8|"CXSail M7216 i8八路数据中心级服务器，支持8颗英特尔® 至强®1代或者2代可扩展处理器，支持 CPU TDP 70-205W，提供96个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s，提供16个2.5寸 SAS热插拔盘位，内部提供8个2.5""或者6个3.5"" 盘位，提供23个 PCI-E 3.0 插槽， 提供4个10GbE RJ45网络接口，提供5组(N+2)1600W钛金级冗余电源(https://www.supermicro.org.cn/zh_cn/products/system/7U/7089/SYS-7089P-TR4T.cfm)"

GPU服务器|G4308 i4|CXSail G4308 i4机架塔式互转GPU服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP 70-205W,提供16个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s,提供8个3.5寸热插拔盘位，提供 4个 PCI-E 3.0 x16 (双宽) 插槽，2个 PCI-E 3.0 x16 (单宽) 插槽，2x 10GBase-T 网络接口，2200W钛金级冗余电源（https://www.supermicro.org.cn/zh_cn/products/system/4U/7049/SYS-7049GP-TRT.cfm）

GPU服务器| G2210 i6  |CXSail G2210 i6 2U机架式GPU服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP 70-205W，提供16个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s,提供10个2.5寸热插拔盘位， 提供6 PCI-E 3.0 x16 插槽 (全高全长),2000W铂金级冗余电源。（https://www.supermicro.org.cn/zh_cn/products/system/2U/2029/SYS-2029GP-TR.cfm）

GPU服务器|  G4224 i8|CXSail G4224 i8 4U机架式GPU服务器，支持2颗英特尔® 至强®1代或者2代可扩展处理器，支持CPU TDP 70-205W，提供24个DDR4 ，RDMM/LRDMM内存插槽，高达2933MT/s,提供24个2.5寸热插拔盘位，提供8 PCI-E 3.0 x16 插槽 (双宽GPU),提供2个 RJ45 10GBase-T 网络端口，提供2000W（2+2）钛金级冗余电源。（https://www.supermicro.org.cn/zh_cn/products/system/4U/4029/SYS-4029GP-TRT.cfm）
"""

