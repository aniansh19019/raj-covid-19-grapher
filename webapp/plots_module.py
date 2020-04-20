import matplotlib.pyplot as plt
import matplotlib.animation as animation 
# import numpy as np
from webapp.covid19 import *
import webapp.covid19 as cov
# import tkinter as tk
# import geo_data as gd
import os
import time
# matplotlib.use('agg')
plt.switch_backend('Agg')

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


class Plot:

    
    data_keys=[('days', 'Days'), ('Confirmed.cases', 'No. of Confirmed Cases'), ('Confirmed.new_cases', 'New Confirmed Cases'), ('Confirmed.rate', 'Daily Growth Rate of Confirmed Cases'), ('Deaths.cases', 'No. of Deaths'), ('Deaths.new_cases', 'New deaths'), ('Deaths.rate', 'Daily Growth Rate of Deaths'), ('Recovered.cases', 'No. of Recoveries'), ('Recovered.new_cases', 'New Recoveries'), ('Recovered.rate', 'Daily Growth Rate of Recoveries'), ('closed_death_rate', 'Death Rate in Closed Cases'), ('death_rate', 'Death Rate for All Cases'), ('closed_recovered_rate', 'Recovery Rate in Closed Cases'), ('recovered_rate', 'Recovery Rate in all Cases')]
    data_dict={'days':'Days', 'Confirmed.cases':'No. of Confirmed Cases', 'Confirmed.new_cases':'New Confirmed Cases', 'Confirmed.rate':'Daily Growth Rate of Confirmed Cases', 'Deaths.cases':'No. of Deaths', 'Deaths.new_cases':'New deaths', 'Deaths.rate':'Daily Growth Rate of Deaths', 'Recovered.cases':'No. of Recoveries', 'Recovered.new_cases':'New Recoveries', 'Recovered.rate':'Daily Growth Rate of Recoveries', 'closed_death_rate':'Death Rate in Closed Cases', 'death_rate':'Death Rate for All Cases', 'closed_recovered_rate':'Recovery Rate in Closed Cases', 'recovered_rate':'Recovery Rate in all Cases'}
    colors=["black", "darkgrey", "rosybrown","darkred", "red", "magenta", "orange", "gold", "olive", "lime", "palegreen", "green", "aqua", "blue", "teal", "darkblue", "blueviolet", "violet", "indigo"]*15#verify
    x_field=''
    y_field=''
    video=False
    image=False
    leg=True
    image_ext=".png"
    res=150#dpi
    #scale, linear or log
    yplot_scale="linear"
    xplot_scale="linear"
    line_width=1
    
    countries=["US"]
    
    #averaging
    smoothness=0
    
    start="1/23/20"
    end="4/16/20"
    
    frame_rate=10#fps export
    
    y_label="Cases"
    x_label="Days"
    title=""

    X=[]
    Y=[]
    N=0

    Xdata=[]
    Ydata=[]

    lines = []

    fig=None
    ax=None

    ylimit=0
    xlimit=0


    def set_data():#no days on y axis


        Plot.x_label=Plot.data_dict[Plot.x_field]
        Plot.y_label=Plot.data_dict[Plot.y_field]
        yfunc=None
        if Plot.y_field.find('.')!=-1:
            dot=Plot.y_field.index('.')
            obj_str=Plot.y_field[:dot]
            func_str=Plot.y_field[dot+1:]
            yfunc=getattr(getattr(cov,obj_str),func_str)
        else:
            yfunc=getattr(cov,Plot.y_field)


        for i in range(Plot.N):
            Plot.Y[i]=smooth(yfunc(Plot.countries[i], Plot.start, Plot.end),Plot.smoothness)




        if Plot.x_field=='days':
            for i in range(1,len(Plot.Y[0])+1):
                for j in range(Plot.N):
                    Plot.X[j].append(i)
        else:

            xfunc=None
            if Plot.x_field.find('.')!=-1:
                dot=Plot.x_field.index('.')
                obj_str=Plot.x_field[:dot]
                func_str=Plot.x_field[dot+1:]
                xfunc=getattr(getattr(cov,obj_str),func_str)
            else:
                xfunc=getattr(cov,Plot.x_field)

            for i in range(Plot.N):
                Plot.X[i]=smooth(xfunc(Plot.countries[i], Plot.start, Plot.end),Plot.smoothness)





    def __init__(self):
        Plot.X=[]
        Plot.Y=[]
        Plot.N=0
    
        Plot.Xdata=[]
        Plot.Ydata=[]
    
        Plot.lines = []
    
        Plot.fig=None
        Plot.ax=None
    
        Plot.ylimit=0
        Plot.xlimit=0








        # print("plot init run!")
        Plot.title=""
        Plot.N=len(Plot.countries)
    
    
        for i in range(Plot.N):
            Plot.title+=Plot.countries[i]
            if i!=Plot.N-1:
                if i<=2:
                    Plot.title+=", "
            if i>2 and Plot.N>4:
                Plot.title+=" & others"
                break

        for i in range(Plot.N):
            Plot.X.append([])
            Plot.Y.append([])
    
        #Assigning Plot.Y values:
        
        
        
        #Assigning Plot.X values:
        
        Plot.set_data()
        
        
        # for i in range(Plot.N):
        #     Plot.X[i]=smooth(Confirmed.cases(Plot.countries[i],Plot.start,Plot.end),Plot.smoothness)
        
        
        # Plot.X=[smooth(gd.geo_x,Plot.smoothness)]
        # Plot.Y=[smooth(gd.geo_y,Plot.smoothness)]
        
        # print("survived!")
        # print(list(map(max, Plot.Y)))
        # print(list(map(max, Plot.X)))
        Plot.ylimit=max(map(max, Plot.Y))
        Plot.xlimit=max(map(max, Plot.X))

        # max_x=[]
        # max_y=[]
        # for x in Plot.X:
        #     maximum=0
        #     for a in x:
        #         if maximum>a:
        #             maximum=a
        #     max_x.append(maximum)
        # for y in Plot.Y:
        #     maximum=0
        #     for a in y:
        #         if maximum>a:
        #             maximum=a
        #     max_y.append(maximum)
        # Plot.xlimit=max(max_x)
        # Plot.ylimit=max(max_y)





    
    
    
    
        for i in range(Plot.N):
            Plot.Xdata.append([])
            Plot.Ydata.append([])
        
        if Plot.leg:
            legends = plt.legend()
    
        # create a figure, axis and Plot element 
        Plot.fig = plt.figure()
        Plot.ax = plt.axes(xlim=(1, Plot.xlimit), ylim=(1,Plot.ylimit), yscale=Plot.yplot_scale, xscale=Plot.xplot_scale)
        # Plot.ax = plt.axes(xlim=(-90, Plot.xlimit), ylim=(0,Plot.ylimit), yscale=Plot.yplot_scale, xscale=Plot.xplot_scale)####change!!!!
        # Plot.ax.set_yscale("log")
        # line, = Plot.ax.Plot([], [], lw=Plot.line_width)
        plt.xlabel(Plot.x_label)
        plt.ylabel(Plot.y_label)
        plt.title(Plot.title) 
        # plt.legend()
        # plotlays, Plot.colors = [2], ["black","red"]
    # labels=[country1,country2]

        for index in range(Plot.N):
            lobj = Plot.ax.plot([],[],lw=Plot.line_width,color=Plot.colors[index])[0]
            Plot.lines.append(lobj)

    def init():
        for line in Plot.lines:
            line.set_data([],[])
    
        return Plot.lines

    def animate(i):
    
        # legends = plt.legend()
    
    
        # xdata1.append(x1[i])
        # xdata2.append(x2[i])
        # ydata1.append(y1[i])
        # ydata2.append(y2[i])
    
        for j in range(Plot.N):
            Plot.Xdata[j].append(Plot.X[j][i])
            Plot.Ydata[j].append(Plot.Y[j][i])
    
        # xlist = [xdata1, xdata2]
        # ylist = [ydata1, ydata2]
    
        #for index in range(0,1):
        for lnum,line in enumerate(Plot.lines):
            line.set_data(Plot.Xdata[lnum], Plot.Ydata[lnum]) # set data for each line separately.
            line.set_label(Plot.countries[lnum])
        # legends.remove()
        if Plot.leg:
            legends = plt.legend()
            return Plot.lines + [legends]
        else:
            return Plot.lines

    def img_plot():
        for i in range(Plot.N):
            plt.plot(Plot.X[i],Plot.Y[i], label=Plot.countries[i], color=Plot.colors[i], lw=Plot.line_width)
            plt.yscale=Plot.yplot_scale
            plt.xscale=Plot.xplot_scale
            # plt.hist(Plot.Y[i],bins=180)
            # Plot.ax.bar(Plot.X[i],Plot.Y[i], width=1)
            if Plot.leg:
                plt.legend()

    # if Plot.video:
    #     # call the animator 
    #     anim = animation.FuncAnimation(Plot.fig, animate, init_func=init, frames=len(Plot.Y[0]), interval=300, blit=True) 
    #     # save the animation as mp4 Plot.video file 
    #     anim.save(Plot.title+".mp4", writer = 'ffmpeg', fps = Plot.frame_rate, dpi=Plot.res) 
        
        
    
    
    # if Plot.image:
    #     if not Plot.video:
    #         img_plot()
    #     plt.savefig(Plot.title+Plot.image_ext,dpi=Plot.res)
    
    
    
    
    def generate_plot(self):
        t=time.time()
        # os.system("rm webapp/static/img/*")
        Plot.img_plot()
        plt.savefig("webapp/static/img/graph"+str(t)+Plot.image_ext,dpi=300)
        return t

    def generate_anim(self):
        t=time.time()
        # os.system("rm webapp/static/vid/*")
        anim = animation.FuncAnimation(Plot.fig, Plot.animate, init_func=Plot.init, frames=len(Plot.Y[0]), interval=1, blit=True) 
        anim.save("webapp/static/vid/anim"+str(t)+".mp4", writer = 'ffmpeg', fps = Plot.frame_rate, dpi=200)
        return t






