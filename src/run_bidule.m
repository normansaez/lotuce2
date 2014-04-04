cum_S=[];
cum_Sigma2=[];


%thedirectory='guppyimagesdark02122013';
%thedirectory='darkguppy';
thedirectory='guppy_imagesdark4';

subdirectories=dir([thedirectory]);

tic;
p = ProgressBar(length(subdirectories)); 


for i_s=3:length(subdirectories)
    
    subset=subdirectories(i_s).name;
    
    %darkus_pike;
    %flatus_pike3;
    flatus_guppy;

    cum_S=[cum_S S];
    cum_Sigma2=[cum_Sigma2 sigma2_S/2];
    
    %time bidule
    p.progress;


    
end;



%reorganize results (sorting according to intensity)

results=[cum_S' cum_Sigma2'];


plot(results(:,2),results(:,1),'.'),
xlabel('\sigma^2_S [ADU^2]'),ylabel('S [ADU]'),box on,

N1=1;N2=100;plot(results(N1:N2,2),results(N1:N2,1),'.'),
DD1=1000;DD2=1000;

figure
scattercloud((cum_Sigma2(N1:N2))/DD1,(cum_S(N1:N2))/DD2,25,5,'k+','cold');
hold on,
scattercloud((cum_Sigma2(N1:N2))/DD1,(cum_S(N1:N2))/DD2,25,5,'ko','cold');
scattercloud((cum_Sigma2(N1:N2))/DD1,(cum_S(N1:N2))/DD2,25,5,'k.','cold');
hold off
xlabel('\sigma^2_S/10^3 [ADU^2]'),ylabel('S/10^3 [ADU]'),box on,

%time bidule
p.stop;
toc;