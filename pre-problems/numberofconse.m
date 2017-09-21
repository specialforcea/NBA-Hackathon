function y = numberofconse(n)
if n<28
    sumit = 0;
    for i = 1:n+1
        sumit = sumit + nchoosek(82-2*n,i-1)*nchoosek(n+1,i);
    end
    y = nchoosek(82,n) - sumit;
elseif n<42
    sumit = 0;
    for i = 1:83-2*n
        sumit = sumit + nchoosek(82-2*n,i-1)*nchoosek(n+1,i);
    end
    y = nchoosek(82,n) - sumit;
else
    y = nchoosek(82,n);
end