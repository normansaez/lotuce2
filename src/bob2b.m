%% A data sample from LOTUCE2 laboratory tests 
%Data taken on April 14th, 2014




% reading bob2 files
%
clear all; close all; fclose all; clc;

thedirectory='data';

fitfile=dir([thedirectory '\*.fits']);
N_files=length(fitfile);


%first file
I1=fitsread([thedirectory '\' fitfile(1).name]);
[sizeH sizeV]=size(I1);
%separate the Mantas
I76=I1(1:sizeH/2,:);
I77=I1(sizeH/2+1:end,:);
%1D PSFs
PSF77H=sum(I77,1);
PSF77V=sum(I77,2);
PSF76H=sum(I76,1);
PSF76V=sum(I76,2);
%centroid positions

pos77H=sum((1:sizeV).*PSF77H) / sum(PSF77H);
pos77V=sum((1:sizeH/2).*PSF77V') / sum(PSF77V);
pos76H=sum((1:sizeV).*PSF76H) / sum(PSF76H);
pos76V=sum((1:sizeH/2).*PSF76V') / sum(PSF76V);

% NOTE: use also the logistic function to fit the cumsum of the 1D PSF

%simple Gaussian fit (not the other one)
f77H = fit( (1:sizeV)', PSF77H','gauss1');
f77V = fit( (1:sizeH/2)', PSF77V,'gauss1');
f76H = fit( (1:sizeV)', PSF76H','gauss1');
f76V = fit( (1:sizeH/2)', PSF76V,'gauss1');


%representations
fontsize=7;


%% MANTA77 full frame with spot position using centroid and Gauss fitting

figure(1)
subplot(3,3,[2 3]),
plot(PSF77H,'k','linewidth',0.5),hold on,
plot(f77H.a1*exp(-(((1:sizeV)-f77H.b1)/f77H.c1).^2),'m','linewidth',0.5),hold off
xlim([1 sizeV]),
set(gca,'FontSize',fontsize);
subplot(3,3,[4 7])
plot(PSF77V,1:sizeH/2,'k','linewidth',0.5),hold on,
plot(f77V.a1*exp(-(((1:sizeH/2)-f77V.b1)/f77V.c1).^2),1:sizeH/2,'m','linewidth',0.5),hold off
axis ij
set(gca,'XDir','reverse'),
ylim([1 sizeH/2]),
set(gca,'FontSize',fontsize);
subplot(3,3,[5 6 8 9])
imagesc(sqrt(I77)),colormap(CubeHelix(256,0.5,-1.5,1.2,1.0)),
set(gca,'FontSize',fontsize);

%% MANTA76 full frame with spot position using centroid and Gauss fitting


figure(2)
subplot(3,3,[2 3]),
plot(PSF76H,'k','linewidth',0.5),hold on,
plot(f76H.a1*exp(-(((1:sizeV)-f76H.b1)/f76H.c1).^2),'m','linewidth',0.5),hold off
xlim([1 sizeV]),
set(gca,'FontSize',fontsize);
subplot(3,3,[4 7])
plot(PSF76V,1:sizeH/2,'k','linewidth',0.5),hold on,
plot(f76V.a1*exp(-(((1:sizeH/2)-f76V.b1)/f76V.c1).^2),1:sizeH/2,'m','linewidth',0.5),hold off
axis ij
set(gca,'XDir','reverse'),
ylim([1 sizeH/2]),
set(gca,'FontSize',fontsize);
subplot(3,3,[5 6 8 9])
imagesc(sqrt(I76)),colormap(CubeHelix(256,0.5,-1.5,1.2,1.0)),
set(gca,'FontSize',fontsize);



%let's take just 77 for now




%cropping and thresholding

limits77V=[floor(f77V.b1-5*f77V.c1) ceil(f77V.b1+5*f77V.c1)];
limits77H=[floor(f77H.b1-5*f77H.c1) ceil(f77H.b1+5*f77H.c1)];
Icrop=I77(limits77V(1):limits77V(2),limits77H(1):limits77H(2));
sizeH0=sizeH;sizeV0=sizeV;
[sizeH sizeV]=size(Icrop);
%thresholding later


%% MANTA77 sub-window frame to be applied to the whole sequence
%This is part of the real-time acquisition and pre-processing procedure

figure(3)
mesh(Icrop);box on;set(gca,'FontSize',fontsize);






%Now, we do the rest of the images, only for 77 for now

H77centroid=[];
V77centroid=[];
H77gauss=[];
V77gauss=[];


pause(0.2);

tic;
p = ProgressBar(N_files); 


for i_f=1:N_files
filename1=fitfile(i_f).name;
I=fitsread([thedirectory '\' fitfile(i_f).name]);
I77=I(sizeH0/2+1:end,:);
Icrop=I77(limits77V(1):limits77V(2),limits77H(1):limits77H(2));
%we work with the windowed (cropped) matrix

PSF77H=sum(Icrop,1);
PSF77V=sum(Icrop,2);
%PSF76H=sum(I76,1);
%PSF76V=sum(I76,2);
%centroid positions

pos77H=sum((1:sizeV).*PSF77H) / sum(PSF77H);
pos77V=sum((1:sizeH).*PSF77V') / sum(PSF77V);
%pos76H=sum((1:sizeV).*PSF76H) / sum(PSF76H);
%pos76V=sum((1:sizeH/2).*PSF76V') / sum(PSF76V);

%NOTE: use also the logistic function to fit the cumsum of the 1D PSF

%simple Gaussian fit (not the other one)
f77H = fit( (1:sizeV)', PSF77H','gauss1');
f77V = fit( (1:sizeH)', PSF77V,'gauss1');
%f76H = fit( (1:sizeV)', PSF76H','gauss1');
%f76V = fit( (1:sizeH/2)', PSF76V,'gauss1');

H77centroid=[H77centroid pos77H];
V77centroid=[V77centroid pos77V];
H77gauss=[H77gauss f77H.b1];
V77gauss=[V77gauss f77V.b1];

p.progress;

end; %i_f

p.stop;

%% Time-Frequency analysis display of the vertical fluctuations from MANTA77

[base nu_dsp spetro]=MEMS(V77gauss-mean(V77gauss),256,10,44.8149144035);



toc;