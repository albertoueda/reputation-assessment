"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import matplotlib.ticker as tkr

def func(x, pos):  # formatter function takes tick label and tick position
   s = '{:0,d}'.format(int(x))
   return s

y_format = tkr.FuncFormatter(func)  # make formatter  

# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
rc('axes', axisbelow=True)

N = 20

ind = np.arange(N)  # the x locations for the groups
width = 0.5       # the width of the bars

# order = ["Computer vision","Speech recognition","Human-computer interaction","Theoretical computer science","Machine learning","Database","Artificial intelligence","Computer network","Computer graphics","Natural language processing","Algorithm","Parallel computing","Data mining","Information retrieval","Computer security","Bioinformatics","Distributed computing","World Wide Web","Programming language","Operating system"]
# order = ["CV","SR","HCI","TCS","ML","DB","AI","CN","CG","NLP","Alg","PC","DM","IR","CS","Bio","DC","WWW","PL","OS"]
order = ["Computer vision","Database","Theoretical computer science","Machine learning","Computer network","Human-computer interaction","Artificial intelligence","Speech recognition","Computer graphics","Data mining","Natural language processing","Algorithm","Parallel computing","Computer security","Information retrieval","Bioinformatics","World Wide Web","Distributed computing","Programming language","Operating system"]
order_br_sort = ['Parallel computing','Information retrieval','Computer graphics','World Wide Web','Data mining','Database','Algorithm','Computer vision','Bioinformatics','Artificial intelligence','Computer network','Human-computer interaction','Natural language processing','Machine learning','Distributed computing','Theoretical computer science','Operating system','Programming language','Speech recognition','Computer security']

# order_paper = ["Database","Computer network","Machine learning","Computer vision","Theoretical computer science","Artificial intelligence","Data mining","Computer security","Human-computer interaction","Computer graphics","Parallel computing","Natural language processing","Algorithm","Operating system","World Wide Web","Programming language","Speech recognition","Bioinformatics","Distributed computing","Information retrieval"]
# order_paper_br = ["Parallel computing","Information retrieval","Data mining","World Wide Web","Computer graphics","Database","Bioinformatics","Algorithm","Computer vision","Artificial intelligence","Computer network","Machine learning","Human-computer interaction","Natural language processing","Operating system","Distributed computing","Theoretical computer science","Programming language","Computer security","Speech recognition"]

# total_us = [1252292.7328569388, 1021260.4926421765, 852153.80684788246, 829249.55802103411, 616026.49732629501, 612384.76030401315, 534171.67885084485, 531694.53628993186, 357599.54853169608, 323760.82697246427, 310876.97964190744, 274286.54233161738, 243269.0530571983, 174143.66910835635, 157919.46541756098, 118608.77963955689, 87025.375617219237, 78760.70093440557, 68766.413947488356, 41646.143647047953]
# total_br = [4096.3121314959335, 485.43827521548468, 2580.1795659578979, 640.7689332627051, 1162.431581760238, 3607.9739642206423, 3437.9871664439615, 2600.2551071851753, 9317.2574085038013, 1588.9374624043337, 4083.7755115828213, 14205.091590003683, 4636.2949456969563, 6887.171313770009, 46.696084638639313, 3853.964311631968, 943.54166798602569, 5341.0996647240954, 255.64510859175917, 291.38121940701018]
total_us_scale = [105423.1946,58634.98469,55920.04233,52920.19329,45795.48904,40856.34937,35534.92187,22781.17311,16892.57378,15244.30117,14434.91775,13140.62578,12746.27171,8116.542447,3678.582179,2560.980551,2078.685753,1873.655532,1658.11875,1434.504997]
total_br_scale = [196.2315619,324.4262332,5.713402205,24.28324988,87.05236389,51.10323295,116.6361283,0.7935608477,871.7543617,561.8927663,24.60148448,197.2224852,1924.011082,0.1337758108,913.036624,189.687257,613.0302691,8.522709108,2.082062815,3.769768176]
total_br_scale_sort = [1924.011082,913.036624,871.7543617,613.0302691,561.8927663,324.4262332,197.2224852,196.2315619,189.687257,116.6361283,87.05236389,51.10323295,24.60148448,24.28324988,8.522709108,5.713402205,3.769768176,2.082062815,0.7935608477,0.1337758108]

total_us_paper = [1829.410743,1645.65687,1641.348536,1608.455667,1288.430586,1271.02265,1197.290231,982.0060929,916.0524773,902.5632497,887.8865062,851.8611188,807.6185156,658.1214654,504.2640996,460.6998137,426.2047995,412.5420536,411.3605373,403.6003697]
total_br_paper = [47.09613,17.53465652,10.94137897,25.0904512,4.670098095,17.76893898,63.47680175,1.500478499,10.37363819,49.00480749,70.94081658,8.10937085,25.29456522,6.776192573,60.11514366,4.265687073,0.8562071871,25.77882511,4.730959542,69.43524383]
total_br_paper_order = [70.94081658,69.43524383,63.47680175,60.11514366,49.00480749,47.09613,25.77882511,25.29456522,25.0904512,17.76893898,17.53465652,10.94137897,10.37363819,8.10937085,6.776192573,4.730959542,4.670098095,4.265687073,1.500478499,0.8562071871]

# order_5 = ["Computer vision", "Human-computer interaction", "Speech recognition", "Theoretical computer science", "Machine learning", "Computer network", "Database", "Artificial intelligence", "Natural language processing", "Computer graphics", "Data mining", "Parallel computing", "Algorithm", "Computer security", "Information retrieval", "Bioinformatics", "World Wide Web", "Distributed computing", "Programming language", "Operating system"]
total_us_5 = [518089.9705,473429.2135,287143.511,265381.8413,259367.6934,223027.855,211922.573,158208.3462,154609.2912,133043.715,107319.5702,87412.99432,85729.74239,79685.99126,69765.16956,46113.99104,38295.75233,31657.45723,22230.17836,9665.621646]
n_publ_top_5 = [58677,73915,34094,42158,60652,24826,43488,60099,31978,69954,38066,53574,37832,30942,18048,33780,69508,37654,22675,19087]

n_publ_top_5_usa = []

fig, ax = plt.subplots()

# rects1 = ax.bar(ind, total_us, color='r')
ax.bar(ind, total_us_scale, width=0.7, color='indianred', hatch='\\', alpha=0.65, align='center')

# add some text for labels, title and axes ticks
# ax.set_ylabel('Accumulated Pscore')
ax.set_ylabel(r'Accumulated \textit{weighted-P-score}')
# ax.set_xlabel(r'Subareas')
ax.set_title(r'CS Subareas -- US')
# ax.set_title('CS Subareas')
# ax.set_xticks(ind + width / 2)

ax.set_xticks(ind)
ax.set_xticklabels(order, fontsize = 10)
ax.set_ylim([0,110000])
# ax.invert_yaxis()  # labels read top-to-bottom
# ax.set_xlabel('Performance')
# ax.set_title('How fast do you want to go today?')

# ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
ax.set_axisbelow(True)

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

# autolabel(rects1)

fig.autofmt_xdate()
ax.margins(0.03,0)
plt.grid(True)
# plt.show()
plt.savefig('chart_usa_scaled.eps', dpi=1000, format='eps', bbox_inches='tight')
# plt.savefig('chart_top-10_conf.eps', dpi=1000, format='eps', bbox_inches='tight')
plt.savefig('chart_usa_scaled.pdf', dpi=1000, format='pdf', bbox_inches='tight')
# plt.savefig('chart_top-10_conf.pdf', dpi=1000, format='pdf', bbox_inches='tight')



fig, ax = plt.subplots()
rects1 = ax.bar(ind, total_br_scale, width=0.7, color='seagreen', hatch='//', alpha=0.65, align='center')

# add some text for labels, title and axes ticks
ax.set_ylabel(r'Accumulated \textit{weighted-P-score}')
# ax.set_xlabel(r'Subareas')
ax.set_title(r'CS Subareas -- Brazil')
# ax.set_xticks(ind + width / 2)

ax.set_xticks(ind)
ax.set_xticklabels(order, fontsize = 10)
ax.set_ylim([0,2100])

fig.autofmt_xdate()
ax.margins(0.03,0)
plt.grid(True)
plt.savefig('chart_br_scaled.eps', dpi=1000, format='eps', bbox_inches='tight')
plt.savefig('chart_br_scaled.pdf', dpi=1000, format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
rects1 = ax.bar(ind, total_br_scale_sort, width=0.7, color='seagreen', hatch='//', alpha=0.65, align='center')

# add some text for labels, title and axes ticks
ax.set_ylabel(r'Accumulated \textit{weighted-P-score}')
# ax.set_xlabel(r'Subareas')
ax.set_title(r'CS Subareas -- Brazil')
# ax.set_xticks(ind + width / 2)

ax.set_xticks(ind)
ax.set_xticklabels(order_br_sort, fontsize = 10)
ax.set_ylim([0,2100])

fig.autofmt_xdate()
ax.margins(0.03,0)
plt.grid(True)
plt.savefig('chart_br_scaled_sorted.eps', dpi=1000, format='eps', bbox_inches='tight')
plt.savefig('chart_br_scaled_sorted.pdf', dpi=1000, format='pdf', bbox_inches='tight')
