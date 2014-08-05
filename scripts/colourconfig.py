#####
# Colours as defined in the PP template
#####
green_lighter = '#edf3d2'
green_light = '#cadd7a'
green = '#a0bb2f'
green_dark = '#788c23'

yellow_lighter = '#fdf2cb'
yellow_light = '#f9d863'
yellow = '#eab808'
yellow_dark = '#af8a05'

red_light = '#ea657b'
red = '#c31a35'
red_dark = '#951327'

orange_light = '#ebaa70'
orange = '#d2731d'
orange_dark = '#9d5615'

blue_light = '#2fe4ff'
blue = '#0090a5'
blue_dark = '#006b7b'

blue_text = '#004b54'

#####
# Colours defined for usages
#####
c_text = blue_text
c_plotlines = blue_text
c_highlight_line = red

c_face_1 = yellow
c_edge_1 = yellow_dark

c_face_2 = green
c_edge_2 = green_dark

c_face_3 = red
c_edge_3 = red_dark

c_face_4 = orange
c_edge_4 = orange_dark

c_face_5 = blue
c_edge_5 = blue_dark

#####
# Function to manipulate objects
#####
def set_figure_style(figure):
    "Change colours and more of figure elements."
    import matplotlib
    ax = figure.add_subplot(1, 1, 1)
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color(c_plotlines)
    ax.tick_params(axis='x', colors=c_text, labelsize=25)
    ax.tick_params(axis='y', colors=c_text, labelsize=25)
    
    return ax
    
def set_min_figure_style(figure):
    "Change colours of figure elements."
    import matplotlib
    ax = figure.add_subplot(1, 1, 1)
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color(c_plotlines)
    ax.tick_params(axis='x', colors=c_text)
    ax.tick_params(axis='y', colors=c_text)
    
    return ax

def set_boxplot_style(layout):
    "Change colours and more of boxplot elements."
    for box in layout['boxes']:
        box.set_facecolor(c_face_1)
        box.set_edgecolor(c_edge_1)
        box.set_linewidth(2)
    for whisker in layout['whiskers']:
        whisker.set_color(c_edge_1)
        whisker.set_linewidth(2)
    for median in layout['medians']:
        median.set_color(c_highlight_line)
        median.set_linewidth(2)
    for cap in layout['caps']:
        cap.set_color(c_edge_1)
        cap.set_linewidth(2)
    for flier in layout['fliers']:
        flier.set(marker='o', color=c_face_2, alpha=1)
        flier.set_markersize(10)
        flier.set_markeredgecolor(c_edge_2)
        

