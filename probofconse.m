prob = 0;
for i = 2:82
    prob = prob + numberofconse(i)*0.097^i*0.903^(82-i);
end