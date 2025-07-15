/*
Instuctions by teacher:
- Implement a logical system to model a scheduling problem. Define constraints related to time, resources, and dependencies to find an optimal solution.

Made by
Diego Monroy Minero
*/

%Fact: Tasks to do
task('to_do1', 3).
task('to_do2', 2).
task('to_do', 4).
task('to_do', 1).

%Fact: Resources
resources('resource_1').
resources('resource_2').
resources('resource_3').

%Rules to restrict
restriction('to_do2', 'to_do1').
restriction('to_do3', 'to_do2').
restriction('to_do4', 'to_do1').

%Restriction by resource
resource_rest('to_do1', 'resource_1').
resource_rest('to_do2', 'resource_2').
resource_rest('to_do3', 'resource_3').
resource_rest('to_do4', 'resource_1').

%Defining schedule
my_schedule(tasks, schedule):-
	mix(tasks, schedule),
	ok_schedule(schedule).
%Defining restrictions for the OK schedule
ok_schedule([]).
ok_schedule([main_task | nothing):-
	ok_schedule(main_task, nothing),
	ok_schedule(nothing).
ok_task(_, []).
ok_task(main_task, [next_main_task | nothing]):-
	\+ restriction(next_main_task, main_task),
	\+ restriction(main_task, next_main_task),
	\+ resource_rest(main_task, main_resource),
	\+ resource_rest(next_main_task, main_resource),
	ok_task(main_task, nothing).

% Copy before execute
% consult('UPY/3rd_quarter/Programming_Paradigms/Notebook/Prolog/Assignment_2/Task2_U4.pl').