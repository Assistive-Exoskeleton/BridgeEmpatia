clear all
close all
clc

%%
% 
filename = '20180705_1905.h5';
h5disp(filename);
Record = h5read(filename,'/Record');

figure
plot(Record.J_des(1,:))
hold on
plot(Record.J_current(1,:))
legend('Desired angle','Actual angle');

figure
plot(Record.J_des(2,:))
hold on
plot(Record.J_current(2,:))
legend('Desired angle','Actual angle');

figure
plot(Record.J_des(3,:))
hold on
plot(Record.J_current(3,:))
legend('Desired angle','Actual angle');

figure
plot(Record.J_des(4,:))
hold on
plot(Record.J_current(4,:))
legend('Desired angle','Actual angle');

figure
plot(Record.p0(1,:))
hold on
plot(Record.p0(2,:))
plot(Record.p0(3,:))


% data = h5read('earray1.h5','/array_c');
% h5disp('earray1.h5')

% 
% data.timestamp = data.timestamp';

% dt = datetime( data.timestamp, 'ConvertFrom', 'posixtime' );
% datestr( dt )

% data

