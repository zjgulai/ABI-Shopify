# -*- coding: utf-8 -*-
import os, matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
P=os.path.dirname(os.path.abspath(__file__))+os.sep
fm.fontManager.addfont(P+"NotoSansSC-Regular.ttf")
fm.fontManager.addfont(P+"NotoSansSC-Bold.ttf")
FP=fm.FontProperties(fname=P+"NotoSansSC-Regular.ttf")
FPB=fm.FontProperties(fname=P+"NotoSansSC-Bold.ttf")
plt.rcParams["font.family"]=FP.get_name()
plt.rcParams["axes.unicode_minus"]=False

INK="#0B1F3A"; NAVY="#13294B"; GREEN="#008060"; LIME="#95BF47"; MINT="#DCF0E6"
INDIGO="#5C6AC4"; LAV="#E7E9F8"; AMBER="#C98A00"; AMBERBG="#FBEFD2"; CORAL="#D9543B"
TEAL="#0E7C86"; TEALBG="#D7EEF0"; BLUE="#2D6CDF"; BLUEBG="#DCE8FB"
BG="#F4F7FB"; CARD="#FFFFFF"; GREY="#62718A"; LINE="#CBD7E6"

def box(ax,x,y,w,h,fc=CARD,ec=LINE,lw=1.4,r=0.02,z=2,alpha=1):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",
        fc=fc,ec=ec,lw=lw,zorder=z,alpha=alpha,mutation_aspect=1); ax.add_patch(p); return p
def txt(ax,x,y,s,size=11,color=INK,bold=False,ha="center",va="center",z=5,italic=False,rot=0):
    fp=FPB if bold else FP
    return ax.text(x,y,s,fontsize=size,color=color,ha=ha,va=va,zorder=z,
        fontproperties=fp,rotation=rot,fontstyle=("italic" if italic else "normal"))
def arrow(ax,x1,y1,x2,y2,color=GREY,lw=1.8,style="-|>",mut=13,ls="-",z=1,rad=0.0):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=mut,color=color,lw=lw,
        linestyle=ls,zorder=z,connectionstyle=f"arc3,rad={rad}"); ax.add_patch(a); return a
def fig(w=16,h=10):
    f,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,160); ax.set_ylim(0,160*h/w)
    ax.axis("off"); f.patch.set_facecolor(BG); ax.set_facecolor(BG); return f,ax
def save(f,name):
    out=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/_diagrams/"
    f.savefig(out+name+".png",dpi=200,bbox_inches="tight",facecolor=f.get_facecolor(),pad_inches=0.3)
    f.savefig(out+name+".pdf",bbox_inches="tight",facecolor=f.get_facecolor(),pad_inches=0.3)
    plt.close(f); print("saved",name)
