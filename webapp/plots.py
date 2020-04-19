import matplotlib.pyplot as plt
import matplotlib.animation as animation 
# import numpy as np
from covid19 import *
# import tkinter as tk
# import geo_data as gd

def smooth(list,level=1):
    retlist=[]
    for i in range(len(list)):
        sum=list[i]
        counter=1
        for j in range(1,level+1):
            if i<j:
                sum+=list[i+j]
                counter+=1

            elif i>=len(list)-j:
                sum+=list[i-j]
                counter+=1
            else:
                sum+=list[i+j]
                sum+=list[i-j]
                counter+=2
        avg=sum/counter
        retlist.append(avg)
    return retlist







colors=["black", "darkgrey", "rosybrown","darkred", "red", "magenta", "orange", "gold", "olive", "lime", "palegreen", "green", "aqua", "blue", "teal", "darkblue", "blueviolet", "violet", "indigo"]*15#verify
# country1="India"
# country2="Nepal"



video=True
image=False
leg=True
image_ext=".png"
res=600#dpi
# countries=list(Recovered.dict.keys());
# print(len(countries))
# print(countries)
# countries=["Brazil","India", "Pakistan", "US", "Italy", "Korea, South"]
# countries=["All Countriesss"]
countries=["Brazil","India", "Pakistan", "China", "Italy", "Spain", "France", "Germany", "US", "Korea, South", "Japan", "United Kingdom"]
#plot scale, linear or log
yplot_scale="linear"
xplot_scale="linear"
line_width=1.5

#averaging
smoothness=4

start="1/23/20"
end="4/16/20"

frame_rate=10#fps export

y_label="Death Rate"
x_label="Days"

title=y_label+" vs "+x_label+" for "




n=len(countries)


for i in range(n):
    title+=countries[i]
    if i!=n-1:
        if i<=3:
            title+=", "
    if i>3 and n>5:
        title+=" & others"
        break





#make x, y lists
# x1=[]
# y1=[]
# x2=[]
# y2=[]

X=[]
Y=[]
for i in range(n):
    X.append([])
    Y.append([])



# y1=Confirmed.cases(country1,"1/23/20","4/2/20")
# y2=Confirmed.cases(country2,"1/23/20","4/2/20")
# y=Confirmed.global_rate("1/23/20","4/2/20")
# print(y1)



#Assigning Y values:

for i in range(n):
    Y[i]=smooth(closed_death_rate(countries[i], start, end),smoothness)

#Assigning X values:

for i in range(1,len(Y[0])+1):
    for j in range(n):
        X[j].append(i)


# for i in range(n):
#     X[i]=smooth(Confirmed.cases(countries[i],start,end),smoothness)


# X=[smooth(gd.geo_x,smoothness)]
# Y=[smooth(gd.geo_y,smoothness)]



ylimit=max(map(max, Y))
xlimit=max(map(max, X))


Xdata=[]
Ydata=[]

for i in range(n):
    Xdata.append([])
    Ydata.append([])

if leg:
    legends = plt.legend()







# create a figure, axis and plot element 
fig = plt.figure()
ax = plt.axes(xlim=(1, xlimit), ylim=(1,ylimit), yscale=yplot_scale, xscale=xplot_scale)
# ax = plt.axes(xlim=(-90, xlimit), ylim=(0,ylimit), yscale=yplot_scale, xscale=xplot_scale)####change!!!!
# ax.set_yscale("log")
# line, = ax.plot([], [], lw=line_width)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title) 
# plt.legend()
# plotlays, colors = [2], ["black","red"]
# labels=[country1,country2]
lines = []
for index in range(n):
    lobj = ax.plot([],[],lw=line_width,color=colors[index])[0]
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([],[])

    return lines



def animate(i):

	# legends = plt.legend()


    # xdata1.append(x1[i])
    # xdata2.append(x2[i])
    # ydata1.append(y1[i])
    # ydata2.append(y2[i])

    for j in range(n):
        Xdata[j].append(X[j][i])
        Ydata[j].append(Y[j][i])

    # xlist = [xdata1, xdata2]
    # ylist = [ydata1, ydata2]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(Xdata[lnum], Ydata[lnum]) # set data for each line separately.
        line.set_label(countries[lnum])
    # legends.remove()
    if leg:
        legends = plt.legend()
        return lines + [legends]
    else:
        return lines
	


def img_plot():
    for i in range(n):
        plt.plot(X[i],Y[i], label=countries[i], color=colors[i], lw=line_width)
        plt.yscale=yplot_scale
        plt.xscale=xplot_scale
        # plt.hist(Y[i],bins=180)
        # ax.bar(X[i],Y[i], width=1)
        if leg:
            plt.legend()














if video:
    # call the animator 
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(Y[0]), interval=300, blit=True) 
    # save the animation as mp4 video file 
    anim.save(title+".mp4", writer = 'ffmpeg', fps = frame_rate, dpi=res) 
    
    


if image:
    if not video:
        img_plot()
    plt.savefig(title+image_ext,dpi=res)

# show the plot 
# plt.show()




