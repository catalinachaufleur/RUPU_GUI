clear all
%myraspi=raspi('192.168.1.17')
myraspi=raspi('192.168.1.18','pi','raspberry')
cam = cameraboard(myraspi,"Resolution","1280x720")
image = snapshot(cam);
image = snapshot(cam);%Snapshot entrega el último, y yo quiero el actual

%Store Image
filelocation = "C:\Users\56979\OneDrive - Universidad Técnica Federico Santa María (1)\ELO308";
filename = "AppDesignerPic.png";
fullFilename = fullfile(filelocation, filename);
imwrite(image, fullFilename, "png");

%Show image
imageData = imread(fullFilename);
f = figure;
ax = axes(f);
imshow(imageData, "Parent", ax);

