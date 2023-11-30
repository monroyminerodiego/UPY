/*
Instructions:
- Implement a Prolog program that defines a family tree with at least three generations. Include rules to determine sibling relationships and ancestors.

Development:
- Set of names {
    alejandra
    alejandro
    angel
    angela
    arantza
    armando
    aylin
    belen
    claudia
    carolina
    daniela
    diego
    elba
    eduardo
    fernanda
    gabriela
    isaac
    jose_luis
    jazmin
    javier
    jose
    laura
    luis
    leonardo
    miguel
    mayeli
    melissa
    marcial
    mia
    octavio
    oscar
    rocio
    sofia
    spanki
    tania
    valeria
    victor
}
*/

% FACTS
is_mother_of(luisa,claudia).
is_mother_of(luisa,laura).
is_mother_of(luisa,alejandra).
is_mother_of(luisa,rocio).
is_mother_of(luisa,angela).
is_mother_of(luisa,marcial).
is_mother_of(luisa,jose).
is_mother_of(luisa,oscar).
is_mother_of(claudia,javier).
is_mother_of(claudia,diego).
is_mother_of(claudia,eduardo).
is_mother_of(laura,miguel).
is_mother_of(laura,aylin).
is_mother_of(laura,mayeli).
is_mother_of(mayeli,luis).
is_mother_of(mayeli,melissa).
is_mother_of(mayeli,valeria).
is_mother_of(belen,armando).
is_mother_of(belen,daniela).
is_mother_of(belen,fernanda).
is_mother_of(elba,alejandro).
is_mother_of(elba,leonardo).
is_mother_of(arantza,sofia).
is_father_of(gonzalo,oscar).
is_father_of(gonzalo,rocio).
is_father_of(gonzalo,alejandra).
is_father_of(gonzalo,laura).
is_father_of(gonzalo,angela).
is_father_of(gonzalo,claudia).
is_father_of(gonzalo,marcial).
is_father_of(gonzalo,jose).
is_father_of(jose,victor).
is_father_of(jose,carolina).
is_father_of(jose,gabriela).
is_father_of(jose,elba).
is_father_of(jose,jose_luis).
is_father_of(marcial,spanki).
is_father_of(marcial,octavio).
is_father_of(abel,eduardo).
is_father_of(abel,jazmin).
is_father_of(abel,isaac).
is_father_of(villedas,belen).
is_father_of(villedas,tania).
is_father_of(villedas,javier).
is_father_of(villedas,diego).
is_father_of(villedas,angel).
is_father_of(jose_luis,arantza).
is_father_of(octavio,mia).


% RULES
% Tipo Propiedades
is_father(A):-
    is_father_of(A,_);
    is_mother_of(A,_).

is_granny(A):-
    is_father(A),
    (is_mother_of(A,B);is_father_of(A,B)),
    is_father(B).

% Tipo Verificacion
is_grandson_of(A,B):-
    (is_mother_of(C,A); is_father_of(C,A)),
    is_son_of(C,B).

is_son_of(A,B):-
    is_father_of(B,A);
    is_mother_of(B,A).    

is_brother_of(A,B):-
    is_father_of(C,A),is_father_of(C,B);
    is_mother_of(C,A),is_mother_of(C,B).    

is_cousin_of(A,B):-
    ((is_mother_of(C,A), is_mother_of(D,B));
    (is_father_of(C,A), is_father_of(D,B));
    (is_mother_of(C,A), is_father_of(D,B));
    (is_father_of(C,A), is_mother_of(D,B))),
    is_brother_of(C,D).

is_auncle_of(A,B):-
    (is_father_of(C,B);is_mother_of(C,B)),
    is_brother_of(A,C).

is_nephew_of(A,B):-
    (is_mother_of(C,A);is_father_of(C,A)),
    is_brother_of(C,B).

is_granny_de(A,B):-
    (is_father_of(C,B);is_mother_of(C,B)),
    is_son_of(C,A).

is_related_with(A,B):-
    is_grandson_of(A,B);
    is_son_of(A,B);
    is_brother_of(A,B);
    is_cousin_of(A,B);
    is_auncle_of(A,B);
    is_nephew_of(A,B);
    is_granny_de(A,B).

% Copy before execute:
% consult('c:/Users/diego/OneDrive/PROGRAMACION/UPY/3rd_quarter/Programming_Paradigms/Notebook/Prolog/Assignment1_Task1_U4.pl').