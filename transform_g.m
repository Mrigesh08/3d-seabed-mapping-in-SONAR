%%%%%%%%%%%%%% Performs Signal Processing %%%%%%%%%%%%%

function mat=transform_g(x,m)
    
    mat=zeros(1536,m);
    for p=drange(1:m)
        rx = fft(x(:,p));%fft
        % V_MF = H.*rx;%match filtering
        % b = real(ifft(V_MF));%i fft
        b = real(ifft(rx));
        h=abs(hilbert(b));%hilbert

        vdata=uint8(abs((((h-min(h))/(max(h)-min(h)))*255)));
         %mat(1:800,p)=255-vdata(267:1066,1); % case filter
 
        mat(:,p)=255-vdata(:,1);
    end
end
