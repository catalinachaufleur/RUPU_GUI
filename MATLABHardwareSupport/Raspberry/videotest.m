while(1)
for ii = 1:10
img = snapshot(cam);
    imagesc(img);
    drawnow;
end
end

% [imagedata,ts] = readFrame(myraspi,8);
% record(cam,'myvideo.h264',10)
% stop(cam)
% getFile(myraspi,'myvideo.h264','C:\MATLAB')
% deleteFile(myraspi,'myvideo.h264')