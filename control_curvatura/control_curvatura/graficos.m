i=1;
x=table2array(vel);
y=table2array(vel_ref);
w=table2array(d);
z=table2array(d_ref);
while i<=length(x)
    Value = x(i);
    t=linspace(0,i,i);
    figure(1)
    set(plot(t,x(1:i),'linewidth',2,'Color','blue'))
    hold on
    set(plot(t,y(1:i),'linewidth',1,'Color','red','LineStyle','--'))
    grid on
     if i<=50
        axis([0,t(i),min(x),max(x)])
    else
        axis([t(i-50),t(i),min(x),max(x)])
    end
    
    drawnow;
    figure(2)
    set(plot(t,w(1:i),'linewidth',2,'Color','blue'))
    hold on
    set(plot(t,z(1:i),'linewidth',1,'Color','red','LineStyle','--'))
    grid on
    if i<=50
        axis([0,t(i),min(x),max(x)])
    else
        axis([t(i-50),t(i),min(x),max(x)])
    end
    
    drawnow;
    i= i+1;
end