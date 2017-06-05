% ASSUMPTIONS
% 1. Data is already sorted according to the ping number.
% 2. Since all the packet numbers are zero, the are all assumed to be
% valid.
% 3. Since all the Data Validity header values contain 65,44, They are
% assumed to valid data. 
% 4. The total time for the ping is 15.36ms and each reading is taken after
% an interval of 10microSeconds. 
% 5. Assuming only along or across data is present. Also, assuming that the
% data is collected in a single path
% 6. Using the previous year's chirp_user.mat data as the trasmitter data.

numberOfPings=input(' enter the number of pings ');
numberOfArrayElements=input(' enter the number of array elements in the hydrophone array ');
load('NIOT_DATA.mat');
% seatrial_data has all the data.

[m n]=size(seatrial_data);
 
% m contains number of rows, n contains the number of columns


% ############ Extract Useful data ###################
actualData=zeros(46080,numberOfPings);
k=1;i=1;
for j=1:1536
    actualData((j-1)*30+i:(j-1)*30+i+30-1,:)=seatrial_data((j-1)*32+k+32:(j-1)*32+k+32-1-1-1+32,:);
end

% ############ Extract Useful data ends ##############

% ########### Normalization ##########################
minOfData=min(double(actualData(:)));
maxOfData=max(double(actualData(:)));

if(minOfData<0)
    minOfData=minOfData*(-1.0);
end
if(minOfData>maxOfData)
    maxOfData=minOfData;
end


actualData=actualData./maxOfData;
%actualData(1,1);
% ########### Normalization Ends #####################

% ########### Check if Along Map and across Map data. ######
summedData=zeros(1536,n);
for i=1:n
    for t=1:1536
        summedData(t,i)=sum(actualData((t-1)*30+1:(t-1)*30+30,i));
    end
end


% ############# Taking the transform #################
finalMat=transform_g(summedData,n);
finalMat=ind2rgb(finalMat(:,:),jet(256));
figure(1)
imshow(finalMat,[])