clc; clear; close all;

% Генерация последовательности Голда
X = [0 1 1 0 1];
Y = [1 0 1 0 0];
L = 31;
g = zeros(1, L);

for i = 1:L
    g(i) = xor(X(end), Y(end));
    newX = xor(X(4), X(5));
    newY = xor(Y(2), Y(5));
    X = [newX X(1:end-1)];
    Y = [newY Y(1:end-1)];
end

disp('Последовательность Голда:');
fprintf('%d ', g);
fprintf('\n\n');

% Таблица автокорреляции 
for s = 0:L-1
    fprintf('%2d | ', s);
    
    % Вывод сдвинутой последовательности
    for i = 1:L
        idx = mod(i-1 + s, L) + 1;
        fprintf('%d ', g(idx));
    end
    
    % Вычисление автокорреляции
    matches = 0;
    mismatches = 0;
    for i = 1:L
        idx = mod(i-1 + s, L) + 1;
        if g(i) == g(idx)
            matches = matches + 1;
        else
            mismatches = mismatches + 1;
        end
    end
    
    diff = matches - mismatches;
    fprintf('| %d/31 (%.4f)\n', diff, diff/L);
end

% Преобразование для xcorr()
g_pm = 2*g - 1;

% График 1: Автокорреляция через xcorr()
[R_xc, lags_xc] = xcorr(g_pm, 'normalized');

figure('Name', 'Графики автокорреляции', 'Position', [100, 100, 1200, 500]);

subplot(1,3,1);
stem(lags_xc, R_xc, 'filled', 'MarkerSize', 4);
xlabel('Задержка (lag)');
ylabel('Автокорреляция');
title('xcorr() - нормализованная');
grid on;
xlim([-30, 30]);
hold on;
plot([0, 0], [-0.2, 1.1], 'r--', 'LineWidth', 0.5);

% График 2: Автокорреляция по формуле
R_formula = zeros(1, L);
for s = 0:L-1
    matches = 0;
    mismatches = 0;
    for i = 1:L
        idx = mod(i-1 + s, L) + 1;
        if g(i) == g(idx)
            matches = matches + 1;
        else
            mismatches = mismatches + 1;
        end
    end
    R_formula(s+1) = (matches - mismatches) / L;
end

subplot(1,3,2);
stem(0:L-1, R_formula, 'filled', 'MarkerSize', 4);
xlabel('Задержка (lag)');
ylabel('Автокорреляция');
title('По формуле из методички');
grid on;
xlim([0, 30]);
hold on;
plot([0, 30], [0, 0], 'k-', 'LineWidth', 0.5);

% График 3: Сравнение
subplot(1,3,3);
hold on;
stem(0:L-1, R_formula, 'b', 'filled', 'MarkerSize', 4, 'DisplayName', 'Формула');
[R_biased, lags] = xcorr(g_pm, 'biased');
stem(lags(lags>=0), R_biased(lags>=0), 'r', 'filled', 'MarkerSize', 3, 'DisplayName', 'xcorr(biased)');
xlabel('Задержка (lag)');
ylabel('Автокорреляция');
title('Сравнение методов');
legend('Location', 'best');
grid on;
xlim([0, 30]);
