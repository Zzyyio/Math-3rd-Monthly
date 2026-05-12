import pandas as pd
import matplotlib
from matplotlib.ticker import MaxNLocator, FixedLocator
import color

def process(df,tgtstr):
    IB24G10 = df[df["Grade"] == "IB24G10"]
    IB23G11 = df[df["Grade"] == "IB23G11"]
    IB22G12 = df[df["Grade"] == "IB22G12"]
    IB24G10_processed = IB24G10.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB23G11_processed = IB23G11.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB22G12_processed = IB22G12.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    return IB24G10_processed,IB23G11_processed,IB22G12_processed


def page_process(df,tgtstr,bins,labels):
    # 5️⃣ 分页统计
    df = df[df['pages'] > 50]
    df['pages_range'] = pd.cut(df['pages'], bins=bins, labels=labels, right=False)

    IB24G10 = df[df["Grade"] == "IB24G10"]
    IB23G11 = df[df["Grade"] == "IB23G11"]
    IB22G12 = df[df["Grade"] == "IB22G12"]
    IB24G10_processed = IB24G10.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB23G11_processed = IB23G11.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB22G12_processed = IB22G12.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    return IB24G10_processed,IB23G11_processed,IB22G12_processed


def price_process(df,tgtstr,bins,labels):
    # 5️⃣ 分页统计
    df = df[df['price'] > 50]
    df['prices_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)

    IB24G10 = df[df["Grade"] == "IB24G10"]
    IB23G11 = df[df["Grade"] == "IB23G11"]
    IB22G12 = df[df["Grade"] == "IB22G12"]
    IB24G10_processed = IB24G10.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB23G11_processed = IB23G11.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    IB22G12_processed = IB22G12.groupby([tgtstr, "Circulation Type"]).size().unstack(fill_value=0).reset_index()
    return IB24G10_processed,IB23G11_processed,IB22G12_processed

def show(g10,g11,g12,g10_data,g11_data,g12_data,x_label,y_label):
    g10.bar(g10_data[x_label],g10_data[y_label])
    g11.bar(g11_data[x_label],g11_data[y_label])
    g12.bar(g12_data[x_label],g12_data[y_label])

def page_show(g10,g11,g12,g10_data,g11_data,g12_data,bins,y_label,width,alpha):
    g10.bar(bins,g10_data[y_label],color=color.bar_color1,width=width,label=y_label,alpha=alpha)
    g11.bar(bins,g11_data[y_label],color=color.bar_color1,width=width,alpha=alpha)
    g12.bar(bins,g12_data[y_label],color=color.bar_color1,width=width,alpha=alpha)

    g10.bar(bins,g10_data["续借"],bottom=g10_data[y_label],color=color.bar_color2,width=width,alpha=alpha,label="续借")
    g11.bar(bins,g11_data["续借"],bottom=g11_data[y_label],color=color.bar_color2,width=width,alpha=alpha)
    g12.bar(bins,g12_data["续借"],bottom=g12_data[y_label],color=color.bar_color2,width=width,alpha=alpha)

    g10.set_xlabel('Page Intervals')
    g10.xaxis.set_major_locator(MaxNLocator(21))
    g11.set_xlabel('Page Intervals')
    g11.xaxis.set_major_locator(MaxNLocator(21))
    g12.set_xlabel('Page Intervals')
    g12.xaxis.set_major_locator(MaxNLocator(21))

    g10.set_ylabel('Borrowings/Renewals')
    g11.set_ylabel('Borrowings/Renewals')
    g12.set_ylabel('Borrowings/Renewals')
    g11.set_ylim(0, 250)
    g12.set_ylim(0, 250)
    g10.set_ylim(0, 250)

    g10.set_title("G10")
    g11.set_title("G11")
    g12.set_title("G12")


def price_show(g10,g11,g12,g10_data,g11_data,g12_data,mid_bins,y_label,width,alpha,bins):
    g10.bar(mid_bins, g10_data[y_label], color=color.bar_color1, width=width, label=y_label, alpha=alpha)
    g11.bar(mid_bins, g11_data[y_label], color=color.bar_color1, width=width, alpha=alpha)
    g12.bar(mid_bins, g12_data[y_label], color=color.bar_color1, width=width, alpha=alpha)

    g10.bar(mid_bins, g10_data["续借"], bottom=g10_data[y_label], color=color.bar_color2, width=width, alpha=alpha, label="续借")
    g11.bar(mid_bins, g11_data["续借"], bottom=g11_data[y_label], color=color.bar_color2, width=width, alpha=alpha)
    g12.bar(mid_bins, g12_data["续借"], bottom=g12_data[y_label], color=color.bar_color2, width=width, alpha=alpha)

    g10.set_xlabel('Page Intervals')
    g10.xaxis.set_major_locator(FixedLocator(bins))
    g11.set_xlabel('Page Intervals')
    g11.xaxis.set_major_locator(FixedLocator(bins))
    g12.set_xlabel('Page Intervals')
    g12.xaxis.set_major_locator(FixedLocator(bins))



    g10.set_ylabel('Borrowings/Renewals')
    g11.set_ylabel('Borrowings/Renewals')
    g12.set_ylabel('Borrowings/Renewals')
    # g11.set_ylim(0, 800)
    # g12.set_ylim(0, 800)
    # g10.set_ylim(0, 800)

    g10.set_title("G10(Scaled)")
    g11.set_title("G11(Scaled)")
    g12.set_title("G12(Scaled)")

