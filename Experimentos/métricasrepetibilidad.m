clear all
datos = readtable('datos_repetibilidad.xlsx');

vel_exp_1 = datos{:, 1};  
vel_exp_2 = datos{:, 2};
vel_exp_3 = datos{:, 3};

[dtw_12_matlab, ix_12, iy_12]= dtw(vel_exp_1, vel_exp_2);
[dtw_13_matlab, ix_13, iy_13]= dtw(vel_exp_1, vel_exp_3);

%Distancia Euclideana calculada a mano usando la forma generica
euc_12_before_dtw = sqrt(sum((vel_exp_1 - vel_exp_2).^2));
euc_12_after_dtw =  sqrt(sum((vel_exp_1(ix_12) - vel_exp_2(iy_12)).^2));

%la distancia entregada por dtw efectivamente corresponde a la "minima suma
%entre la distancia euclideana de los puntos individuales a lo largo del
%path de alineamiento optimo". Basicamente, comparando el resultado de
%dtw_12_local con el dtw_12_matlab deberia dar lo mismo

dtw_12_local = (sum(sqrt((vel_exp_1(ix_12) - vel_exp_2(iy_12)).^2)));

%Para calcular la suma de la distancia euclidiana original sigo la
%estructura del dtw_local
sum_eucl_12_before = (sum(sqrt((vel_exp_1 - vel_exp_2).^2)));


euc_13_before_dtw = sqrt(sum((vel_exp_1 - vel_exp_3).^2));
euc_13_after_dtw =  sqrt(sum((vel_exp_1(ix_13) - vel_exp_3(iy_13)).^2));

dtw_13_local = (sum(sqrt((vel_exp_1(ix_13) - vel_exp_3(iy_13)).^2)));
sum_eucl_13_before = (sum(sqrt((vel_exp_1 - vel_exp_3).^2)));


%% Métricas

%Error cuadrático medio
ECM_12_before=immse(vel_exp_1,vel_exp_2);
ECM_12_after=immse(vel_exp_1(ix_12),vel_exp_2(iy_12));

ECM_13_before=immse(vel_exp_1,vel_exp_3);
ECM_13_after=immse(vel_exp_1(ix_13),vel_exp_3(iy_13));

%raiz del error cuadrático
RMSE_12_before=rmse(vel_exp_1,vel_exp_2);
RMSE_12_after=rmse(vel_exp_1(ix_12),vel_exp_2(iy_12));

RMSE_13_before=rmse(vel_exp_1,vel_exp_3);
RMSE_13_after=rmse(vel_exp_1(ix_13),vel_exp_3(iy_13));

%normalizado al promedio
NRMSE_12_before=rmse(vel_exp_1,vel_exp_2);
NRMSE_12_after=rmse(vel_exp_1(ix_12),vel_exp_2(iy_12))/mean(vel_exp_1);

NRMSE_13_before=rmse(vel_exp_1,vel_exp_3);
NRMSE_13_after=rmse(vel_exp_1(ix_13),vel_exp_3(iy_13))/mean(vel_exp_1);

%%
Metricas = ["Suma Dist.Eucl";"ECM";"RECM";"RECMN"];
Experimento12 = [dtw_12_local; ECM_12_after; RMSE_12_after; NRMSE_12_after];
Experimento13 = [dtw_13_local; ECM_13_after; RMSE_13_after; NRMSE_13_after]; 

tablametricas = table(Metricas, Experimento12, Experimento13)