clc; clear; close all;

% Генерация двух последовательностей Голда
X1 = [0 1 1 0 1];
Y1 = [1 0 1 0 0];
X2 = [0 1 1 1 0];   % x = x+1 = 14
Y2 = [0 1 1 1 1];   % y = y-5 = 15

L = 31;
g1 = zeros(1, L);
g2 = zeros(1, L);

% Первая последовательность
X1_temp = X1; Y1_temp = Y1;
for i = 1:L
    g1(i) = xor(X1_temp(5), Y1_temp(5));
    newX1 = xor(X1_temp(4), X1_temp(5));
    newY1 = xor(Y1_temp(2), Y1_temp(5));
    
    for j = 5:-1:2
        X1_temp(j) = X1_temp(j-1);
        Y1_temp(j) = Y1_temp(j-1);
    end
    X1_temp(1) = newX1;
    Y1_temp(1) = newY1;
end

% Вторая последовательность  
X2_temp = X2; Y2_temp = Y2;
for i = 1:L
    g2(i) = xor(X2_temp(5), Y2_temp(5));
    newX2 = xor(X2_temp(4), X2_temp(5));
    newY2 = xor(Y2_temp(2), Y2_temp(5));
    
    for j = 5:-1:2
        X2_temp(j) = X2_temp(j-1);
        Y2_temp(j) = Y2_temp(j-1);
    end
    X2_temp(1) = newX2;
    Y2_temp(1) = newY2;
end

% Взаимная корреляция по формуле из методички
matches = 0;
mismatches = 0;
for i = 1:L
    if g1(i) == g2(i)
        matches = matches + 1;
    else
        mismatches = mismatches + 1;
    end
end

diff = matches - mismatches;
fprintf('Взаимная корреляция (формула): %d/31 = %.6f\n\n', diff, diff/L);

% Взаимная корреляция через xcorr()
g1_pm = 2*g1 - 1;  % 0→-1, 1→+1
g2_pm = 2*g2 - 1;

[R12, lags12] = xcorr(g1_pm, g2_pm, 'normalized');
fprintf('Взаимная корреляция (xcorr): %.6f при lag=0\n', R12(lags12 == 0));

% График взаимной корреляции
figure;
stem(lags12, R12, 'filled', 'MarkerSize', 4);
xlabel('Задержка (lag)');
ylabel('Взаимная корреляция');
title('Взаимная корреляция двух последовательностей Голда');
grid on;
xlim([-30, 30]);
hold on;
plot([0, 0], [-0.5, 1.1], 'r--', 'LineWidth', 0.5);
plot(0, R12(lags12 == 0), 'ro', 'MarkerSize', 8, 'LineWidth', 2);