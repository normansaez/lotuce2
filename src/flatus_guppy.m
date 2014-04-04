fitfile=dir([thedirectory '\' subset '\*.fits']);


%Area of Interest limits
X1=20;
X2=100;
Y1=60;
Y2=100;

I_mean=zeros(X2-X1+1,Y2-Y1+1);
%I_mean=zeros(1080,1920);
%I_var=zeros(201,201);
sigma2_S=0;





N_files=length(fitfile);

for i_f=1:N_files
filename1=fitfile(i_f).name;    
I1=fitsread([thedirectory '\' subset '\' filename1]);
I=I1(X1:X2,Y1:Y2);
I_mean=I_mean+double(I)./N_files;
end;
S=mean(I_mean(:)); %mean signal



for i_f=1:N_files-1
filename1=fitfile(i_f).name;
I1=fitsread([thedirectory '\' subset '\' filename1]);
I=I1(X1:X2,Y1:Y2);


for i_f2=i_f+1:N_files
filename2=fitfile(i_f2).name;
I1=fitsread([thedirectory '\' subset '\' filename2]);
I2=I1(X1:X2,Y1:Y2);


Iv=I2-I;

sigma2_S=sigma2_S+var(Iv(:))/sum(1:N_files-1);

end;
end;