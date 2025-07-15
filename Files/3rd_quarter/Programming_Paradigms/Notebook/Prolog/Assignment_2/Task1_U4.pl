/*
Instuctions by teacher:
- Develop a Prolog program that solves a Sudoku puzzle using logic programming principles. Use relations and constraints to ensure a valid solution.

Made by
Diego Monroy Minero
*/

sudoku_table(row) :-
    length(row, 9), maping(same_length(row), row),
    append(row, Vs), Vs ins 1..9,
    maping(all_distinct, row),
    transpose(row, column),
    maping(not_same, column),
    row = [Ar,Br,Cr,Dr,Er,Fr,Gr,Hr,Ir],
    section(Ar, Br, Cr),
    section(Dr, Er, Fr),
    section(Gr, Hr, Ir).
section([], [], []).
section([C1,C2,C3|Cr1], [C4,C5,C6|Cr2], [C7,C8,C9|Cr3]) :-
    not_same([C1,C2,C3,C4,C5,C6,C7,C8,C9]),
    section(Cr1, Cr2, Cr3).
sudoku_game(1, [[_,_,_,_,_,_,_,_,_,],
    [_,_,_,_,_,3,_,8,5],
    [_,_,1,_,2,_,_,_,_],
    [_,_,_,5,_,7,_,_,_],
    [_,_,4,_,_,_,1,_,_],
    [_,9,_,_,_,_,_,_,_],
    [5,_,_,_,_,_,_,7,3],
    [_,_,2,_,1,_,_,_,_],
    [_,_,_,_,4,_,_,_,9]]).

% Copy before execute
% consult('UPY/3rd_quarter/Programming_Paradigms/Notebook/Prolog/Assignment_2/Task1_U4.pl').