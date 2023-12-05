/*
instructions:
- Utilize collections to represent a simple database of books. Implement queries to find books by a specific author or within a certain genre.

Made By
Diego Monroy
*/


% List
categories([
    fantasy,
    science,
    mistery,
    romance,
    thriller]).
authors([
    author1_fantasy, author2_fantasy,
    author1_science, author2_science,
    author1_mistery, author2_mistery,
    author1_romance, author2_romance,
    author1_thriller,author2_thriller]).
books([
    book1_author1_fantasy, book2_author1_fantasy, book1_author2_fantasy, book2_author2_fantasy,
    book1_author1_science, book2_author1_science, book1_author2_science, book2_author2_science,
    book1_author1_mistery, book2_author1_mistery, book1_author2_mistery, book2_author2_mistery,
    book1_author1_romance, book2_author1_romance, book1_author2_romance, book2_author2_romance,
    book1_author1_thriller,book2_author1_thriller,book1_author2_thriller,book2_author2_thriller]).

% Rules
is_category(X):-
    categories(Categories),
    member(X,Categories).

is_author(X):-
    authors(Authors),
    member(X,Authors).

is_book(X):-
    books(Books),
    member(X,Books).

in(SubString, String) :-
    sub_string(String, _, _, _, SubString).

books_by_author(Book,Author):-
    is_book(Book),
    in(Author,Book).

books_by_category(Book,Category):-
    is_book(Book),
    in(Category,Book).

% Copy before execute
% consult('UPY/3rd_quarter/Programming_Paradigms/Notebook/Prolog/Assignment_1/Task2_U4.pl').