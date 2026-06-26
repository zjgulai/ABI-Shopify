# -*- coding: utf-8 -*-
import diag_common as d
from diag_common import txt,box,arrow
f,ax=d.fig(18,10); H=160*10/18  # 88.9
txt(ax,4,H-4,"横向流程蓝图 · 建站 → 全自动运营",size=22,color=d.INK,bold=True,ha="left")
txt(ax,4,H-8.3,"每个节点:目标 · 关键 AI/Shopify 能力 · 人审点",size=11.5,color=d.GREEN,ha="left",bold=True)

G={"b":(d.BLUEBG,d.BLUE),"g":(d.MINT,d.GREEN),"i":(d.LAV,d.INDIGO),"t":(d.TEALBG,d.TEAL),"a":(d.AMBERBG,d.AMBER)}
S=[("00","战略定位","b","卖给谁·凭什么赢","Catalog 可见性·竞品数据","赛道 / 红线"),
("01","选品调研","b","验证做什么产品","Helium10·Trends·Catalog","终审选品"),
("02","建站基建","g","立技术底座","AI Toolkit·Dev MCP·Hydrogen·Functions","支付 / 合规"),
("03","上架Listing","g","被搜到·被打动","Magic·Catalog·多语言","卖点 / 措辞"),
("04","内容素材","g","规模化造素材","Sidekick 出图·视频流·ElevenLabs","调性 / 版权"),
("05","营销引流","i","多渠道获客","Campaign Autopilot·Klaviyo·红人","预算 / 合规"),
("06","转化CRO","i","流量变订单","Pulse·Functions·AB 测试","实验上线"),
("07","数据归因","t","装仪表盘","GA4/GTM·UTM·BQ·看板","指标口径"),
("08","履约供应链","t","库存到交付","Flow·库存同步·海外仓","异常 / 退款"),
("09","会员运营","t","留住客户","Store AI·MCP·VOC/舆情","高危工单"),
("10","自动化编排","a","串成 AI 流水线","Agent·MCP·Flow·UCP","不可逆写")]
n=len(S); x0=3; gap=0.9; w=(154-(n-1)*gap)/n
ytop=72; cardh=46
# trigger band
box(ax,3,ytop+3,154,5,fc="#EDF2F8",ec=d.LINE,r=0.4,z=2)
txt(ax,5,ytop+5.5,"触发",size=9.5,color=d.GREY,ha="left",bold=True)
txt(ax,82,ytop+5.5,"定时 / 趋势异动  ·  选品定档  ·  上新 / 促销  ·  流量进入  ·  下单  ·  售后 / 复购",size=9,color=d.INK,ha="center")
for i,(num,name,g,goal,cap,rev) in enumerate(S):
    x=x0+i*(w+gap); fc,ec=G[g]
    # header
    box(ax,x,ytop-9,w,8.4,fc=ec,ec=ec,r=0.4,z=4)
    txt(ax,x+w/2,ytop-3.6,num,size=13,color="#FFFFFF",bold=True,z=5)
    txt(ax,x+w/2,ytop-7.2,name,size=7.6,color="#FFFFFF",z=5)
    # body
    box(ax,x,ytop-cardh,w,cardh-10,fc=fc,ec=ec,lw=1.4,r=0.3,z=3)
    yy=ytop-13
    txt(ax,x+w/2,yy,"目标",size=6.6,color=ec,bold=True,z=5); 
    txt(ax,x+w/2,yy-3.4,goal,size=6.7,color=d.INK,z=5)
    txt(ax,x+w/2,yy-9,"关键能力",size=6.6,color=ec,bold=True,z=5)
    for k,part in enumerate(cap.split("·")):
        txt(ax,x+w/2,yy-12.2-k*3.0,part.strip(),size=6.3,color=d.INK,z=5)
    # human review chip at bottom
    box(ax,x,ytop-cardh-0.2,w,4.6,fc="#FFF4E8",ec=d.AMBER,lw=1,r=0.3,z=4)
    txt(ax,x+w/2,ytop-cardh+2.1,"审  ·  "+rev,size=6.4,color="#9A6A00",z=5)
    if i<n-1: arrow(ax,x+w,ytop-cardh/2,x+w+gap,ytop-cardh/2,color=d.GREY,lw=1.2,mut=7,z=4)
# feedback
arrow(ax,x0+9*(w+gap)+w/2,ytop-cardh-0.2,x0+1*(w+gap)+w/2,ytop-cardh-0.2,color=d.CORAL,lw=1.5,ls="--",mut=10,rad=-0.18,z=2)
txt(ax,82,ytop-cardh-6.5,"复购 / VOC 数据回流 → 选品 & 营销(自驱动闭环)",size=9,color=d.CORAL,italic=True)
# crosscut footer
box(ax,3,5,154,6,fc=d.NAVY,ec=d.NAVY,r=0.4,z=2)
txt(ax,82,8,"横切层贯穿全程:  90 AI 能力地图   ·   91 合规与风控   ·   92 组织与 SOP   ·   人审兜底 + 异常回滚",size=9.5,color="#FFFFFF",ha="center",bold=True)
d.save(f,"02_横向流程蓝图_horizontal")
