
# coding: utf-8

# ### Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---
# 
# *Note: The data given for this assignment is not the same as the data used in the article and as a result the visualizations may look a little different.*

# In[1]:

# Use the following data for this assignment:

import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df


# In[2]:

get_ipython().magic('matplotlib notebook')

import matplotlib.gridspec as grid
import matplotlib.pyplot as plt

fign = plt.figure()
gspec = grid.GridSpec(6,6)
gspec.update(wspace = 0,hspace = 0)

barchart = plt.subplot(gspec[0:5,1:],zorder = 10)
left_plot = plt.subplot(gspec[0:5,0:1],sharey = barchart,zorder = 12)
bottom_plot = plt.subplot(gspec[5:,1:])
square_plot = plt.subplot(gspec[5:6,0:1])
all_plot = [bottom_plot,square_plot]
for plot in all_plot:
    plot.axes.get_xaxis().set_visible(False)
    plot.axes.get_yaxis().set_visible(False)
    
barchart.axes.get_yaxis().set_visible(False)
left_plot.yaxis.tick_right()
left_plot.tick_params(axis='y',direction = 'in',pad = -40)
left_plot.xaxis.set_visible(False)


# In[3]:

import scipy.stats as stats
# Get color palette
palette = plt.get_cmap('Set2')
RdBu = plt.get_cmap('RdBu')
Reds = plt.get_cmap('Reds')

# Set parameters
year = ['1992','1993','1994','1995']
average = pd.Series(round(df.mean(axis = 1),2))
se = pd.Series(round((df.std(axis = 1))/(len(df.columns))**(1/2),2))
z_score = stats.norm.ppf(.975)
x_pos = [i for i, _ in enumerate(year)]
yerr = se*z_score
CI = pd.DataFrame(None)
CI['upperbound'] = round(average + yerr,1)
CI['lowerbound'] = round(average - yerr,1)


# Plot barchart
allbars = barchart.bar(x_pos,average,yerr = yerr,capsize = 10,linewidth = 1,width = 1.0,edgecolor = 'k',align = 'center',color = 'whitesmoke')
allbars[3].set_facecolor('red')
barchart.set_xlim([-1,4.5])
barchart.set_xticks(x_pos)
barchart.set_xticklabels(year)
barchart.tick_params(axis = 'x',bottom = False)


# Set the loc of tick label 'o' numerically
import matplotlib.transforms as transforms
trans = transforms.Affine2D().translate(30,0)
labelzero = left_plot.get_yticklabels()[0]
labelzero.set_transform(labelzero.get_transform() + trans)

plt.gcf().canvas.draw()


# In[4]:

# spanselector
from matplotlib.widgets import SpanSelector

xloc = .2 # location for text of spanselector min and max
yedge = 1
colscaler = 2.4 # since 240 shades of Reds

# def a select function
def span_on_select(min_span,max_span):
    global minSpan,maxSpan
    minSpan = min_span
    maxSpan = max_span
    # clear plot & set tick label loc again
    left_plot.cla()
    trans = transforms.Affine2D().translate(30,0)
    labelzero = left_plot.get_yticklabels()[0]
    labelzero.set_transform(labelzero.get_transform() + trans) # Set the location of tick label '0' numerically 
    # It is not necessary. But due to my misunderstanding of the original plot ...
    
    # show values 
    text_min = left_plot.text(s = '{}'.format(round(min_span,1)),x = xloc,y = min_span - yedge,visible = True)
    text_min.set_bbox(dict(facecolor = 'beige',alpha = .75,edgecolor = 'white')) # set facecolor etc. of box
    text_max = left_plot.text(s = '{}'.format(round(max_span,1)),x = xloc,y = max_span + yedge,visible = True)
    text_max.set_bbox(dict(facecolor = 'beige',alpha =.75, edgecolor = 'white'))

    
    # update color
    overlap = []
    for i in np.arange(len(allbars)):
        # function to calculate proportion of overlap
        def span_overlap(minSpan,maxSpan):
            return max(0,min(maxSpan,CI.iloc[i]['upperbound']) - max(minSpan,CI.iloc[i]['lowerbound']))
        if span_overlap(minSpan,maxSpan) == 0:
            overlap.append(0) 
        else: overlap.append(100*span_overlap(minSpan,maxSpan)/(yerr.values[i]*2))
        allbars[i].set_facecolor(Reds(int(round(overlap[i]*2.4,0))))
        
    return min_span,max_span
    
# make a span selector
spanBar = SpanSelector(barchart,onselect=span_on_select,direction= 'vertical',minspan=1000,
                       useblit=True,button=1,
                       span_stays = True,
                       rectprops={'facecolor':'beige','alpha':.25,'edgecolor':'gray'})


# Add a ColorBar
import numpy as np
from matplotlib.cm import ScalarMappable # Because it is a standalone colorbar
import matplotlib

norm = matplotlib.colors.Normalize(vmin=0,vmax =1) # It can actually be omitted
sm = ScalarMappable(cmap= Reds) # Map number to colors; Perhaps should map proportion in this way
sm.set_array([])
cbaxes = fign.add_axes([.915, 0.11, 0.03, 0.77],zorder = 10) # new axis to posit colorbar
cb = fign.colorbar(sm,norm = norm,ticks = np.arange(0,1.1,.1),
             cax = cbaxes)
cb.ax.tick_params(labelsize = 8) # set size of ticklabels

plt.gcf().canvas.show()

