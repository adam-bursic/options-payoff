% Alex Kind (2025) Lecture: QAM, HSG

function value = CallEurTree1(sigma, r, K, S0, div, T, n)

% parameters for binominal tree
dt = T/n;
u = exp(sigma*sqrt(dt));
d = 1/u;
p = (exp((r-div)*dt)-d)/(u-d);
q = 1-p;
sMat = zeros(n+1,n+1);
opMat = zeros(n+1,n+1);

% stock tree
sMat(1,1) = S0;
for j = 2:n+1
    for i = 1:j-1
        sMat(i,j) = sMat(i,j-1)*u;
    end
    sMat(i+1,j) = sMat(i,j-1)*d;
end

% matrix for option values; insert terminal values
opMat(:,1+n) = max(sMat(:,n+1)-K, 0);

% value call by backward induction
disc = exp(-r*dt);
for j = n:-1:1
    for i = j:-1:1
        opMat(i,j) = disc*(p*opMat(i,j+1)+q*opMat(i+1,j+1));
    end
end

value = opMat(1,1);