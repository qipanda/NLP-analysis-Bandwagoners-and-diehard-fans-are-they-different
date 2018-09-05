import matplotlib.pyplot as plt
import numpy as np

def create_H2_plot(df, rg, ax, y_ticks_off, y_label_on, y_label_print, right_y_axis, right_string, left_team_mention):
    '''
    INPUTS:
        df  - dataframe of a given context
        rg  - rank group
        ax - axes object of whole matplotlib figure
    '''

    width = 0.35
    ind = np.arange(2)

    # set the title
    ttl = ax.set_title("{} Rank Group (RG)".format(rg), size=8)
    ttl.set_position([0.5, 0.85])

    # low lg
    low = ax.bar(
        x=ind,
        height=df.loc[(df["Rank Group"]==rg) & (df["Loyalty Group"]=="low"), "s"].values,
        yerr=df.loc[(df["Rank Group"]==rg) & (df["Loyalty Group"]=="low"), "UB_95"].values,
        width=width,
        color='C0',
        error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=1, elinewidth=1),
        label="High LG"
    )
    # high lg
    high = ax.bar(
        x=ind + width,
        height=df.loc[(df["Rank Group"]==rg) & (df["Loyalty Group"]=="high"), "s"].values,
        yerr=df.loc[(df["Rank Group"]==rg) & (df["Loyalty Group"]=="high"), "UB_95"].values,
        width=width,
        color='C1',
        error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=1, elinewidth=1),
        label="Low LG"
    )

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(("Loss", "Win"))
    ax.set_ylim(0.05, 0.30)

    if y_ticks_off:
        ax.set_yticklabels([""]*6)
    if y_label_on:
        if y_label_print == "True":
            ax.set_ylabel("Mentioned", color="g", size=13)
        else:
            ax.set_ylabel("Not Mentioned", color="r", size=13)
    if right_y_axis:
        # ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.set_ylabel(right_string, rotation=270, labelpad=-155)
    if left_team_mention:
        ax.text(x=-1.10, y=0.08, s="Self Team Mention (f)", size=15, rotation=90)

    # ax.legend()
    ax.yaxis.grid()

    return high, low
