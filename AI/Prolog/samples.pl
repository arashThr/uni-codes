bigger( elephant, horse ).
bigger( horse, donkey ).
bigger( donkey, dog ).

/* Hello */
is_bigger( X, Y ) :- bigger(X, Y ) .
is_bigger( X, Y ) :- bigger(X, Z ), bigger(Z, Y ).

female(mary).
female(sandra).
female(juliet).
female(lisa).
male(peter).
male(paul).
male(dick).
male(bob).
male(harry).
parent(bob, lisa).
parent(bob, paul).
parent(bob, mary).
parent(juliet, lisa).
parent(juliet, paul).
parent(juliet, mary).
parent(peter, harry).
parent(lisa, harry).
parent(mary, dick).
parent(mary, sandra).

father( X, Y ) :- parent(X, Y), male(X).

mother( X, Y ) :- parent(X, Y), female(X).

sister( X, Y ) :- 
  father(Z, X),
  father(Z, Y),
  mother(M, X),
  mother(M, Y),
  female(X),
  X\=Y .
/*sister( X, Y ) :- parent(Z, X), parent(Z, Y), female(X), X\=Y .*/

grMoth( X, Y ) :- 
  parent(Z, Y),
  parent(X, Z),
  female(X).

/* Not correct ! */
cousin( X, Y ) :- 
  mother(A, X),
  mother(B, Y),
  parent(Z, A),
  parent(Z, B),
  X \= Y.

conc( [], List, List ).
conc( [Elm|List1], List2, [Elm|List3] ) :- conc( List1, List2, List3 ).

leng( [], 0 ).
leng( [_|List], Len ) :- leng( List, Len1 ), Len is Len1+1.

memb( _, [] ) :- false.
memb( X, X ) :- true.
memb( X, [Elm|_] ) :- memb( X, Elm ).
memb( X, [_|List] ) :- memb( X, List).

copy_list( [], [] ).
copy_list( [Elm|List1], [Elm|List2] ) :- remove_dup( List1, List2 ).

analys_list( [] ) :- write('An empty list').
analys_list( X, [] ) :- 
  write( 'Head :' ), write(X), nl,
  write( 'Tail is empty' ).
analys_list( X, Y ) :-
  write( 'Head :' ), write(X), nl,
  write( 'Tail :' ), write(Y).
get_list( [Elm|List] ) :- 
  analys_list( Elm, List ).

/* Remove duplicate, first checke */
%check( _, [] ) :- false.
check( X, X ) :- true.
check( X, [Elm|_] ) :- check(X, Elm).
check( X, [_|List] ) :- check( X, List ).

remove_dup( [], [] ).
remove_dup( [Elm|Rest], List ) :- member(Elm, Rest), remove_dup( Rest, List ).
remove_dup( [Elm|Rest], [Elm|List] ) :- not(member(Elm, Rest)),remove_dup( Rest, List ).

/* Reverse ( there is also another solution, look in wikibook */
rev( [], [] ).
rev( [H|T], List ) :- rev( T, List1 ), append( List1, [H], List ) .

/* who am i exercise */
whoami( [] ).
whoami( [ _, _ | Rest ] ) :- whoami( Rest ).

/* Last */
last1( [H|[]], H ).
last1( [_|T], X ) :- last1( T, X ).
/* Vary celever :) */
last2( List, Last ) :- append( _, [Last], List ).

/* Replace */
replace( [], _, _, [] ) :- !.
replace( [X|T], X, Y, [Y|R] ) :- replace( T, X, Y, R ), !.
replace( [Z|T], X, Y, [Z|R] ) :- replace( T, X, Y, R ).

/* Power */
power( X, 1, X ) :- !.
power( X, N, Res ) :- power( X, N-1, Tmp ), Res is Tmp * Res .

/* Union of tow sets */
union( [], X, X ).
union( [H|T], X, List ) :- member( H, X ), union( T, X, List ), !.
union( [H|T], X, [H|List] ) :- union( T, X, List ).

/* Power set ! */
pset( [], [] ).
pset( [X|T], [X|R] ) :- pset( T, R ).
pset( [_|T], R ) :- pset( T, R ).
/* Astonishing ! */

/* Distance */
dist( (A1,A2), (B1,B2), X ) :- X is sqrt( (A1-B1)**2 + (A2-B2)**2 ).

/* Sqaure */
printStar( 0, _ ).
printStar( N, Char ) :- N > 0, 0 is N mod 5, nl, N1 is N-1, printStar(N1, Char).
printStar( N, Char ) :- N >0, write( Char ), N1 is N-1, printStar(N1, Char).
square( N, Char ) :- N1 is N**2, printStar( N1, Char ).

/* Fibo */
fibo( 1, 1 ).
fibo( 2, 1 ).
fibo( N, X ) :- N>= 3, N1 is N-1, N2 is N-2, fibo(N1, X1), fibo(N2, X2), X is X1+X2.

/* Element at */
elmAt( [H|_], 0, H ).
elmAt( [_|T], Index, Var ) :- Tmp is Index-1, elmAt( T, Tmp, Var ).

/* Mean */
sum( [], 0 ).
sum( [H|T], X ) :- sum( T, Tmp ), X is Tmp+H .
mean( List, Result ) :- sum(List, SumVal ), length(List, Len), Len>0, Result is SumVal/Len.

/* Range */
range( X, X, [X] ).
range( X, Y, [X|T] ) :- X<Y, Tmp is X+1, range( Tmp, Y, T ).

/* Polynomial Sum */

/* Kth element */
kthElm( [X|_], 0, X ).
kthElm( [_|T], K, X ) :- K1 is K-1, kthElm( T, K1, X ).

/* Palindrom */
pal( [X,_,X] ).
pal( [X, X] ).
pal( [H|T] ) :- append( Mid, [Last], T ), Last = H, pal( Mid ).

/* Flatten a list : [a, [b,c] ] -> [a, b, c] */
flat( [], [] ).
flat( [H|T], [H|Rest] ) :- not( is_list(H) ), flat( T, Rest ), !.
flat( [H|T], Rest ) :- flat( H, Rest1 ), flat( T, Rest2 ), append( Rest1, Rest2, Rest ).

/* elminate consecutive duplication */
consDup( [], [] ).
consDup( [A|T], Rest ) :- [A|_] = T, consDup( T, Rest ), !. % If the next one is the same
consDup( [A|T], [A|Rest] ) :- consDup( T, Rest ).

/* Duplicate elements */
dupli( [], [] ).
dupli( [H|T], [H,H|Rest] ) :- dupli( T, Rest ).

/* Init list ( list but the last ) */
initList( List, X ) :- append( X, [_], List ).

/* Swap head with kth element */
chgKthElm( [_|T], 0, Val, [Val|T] ).
chgKthElm( [H|T], K, Val, [H|List] ) :- K1 is K-1, chgKthElm( T, K1, Val, List ).

swap( List, K, X ) :- 
  kthElm( List, K, Val ),
  [H|T] = List,
  Tmp = [Val|T],
  chgKthElm( Tmp, K, H, X ).

/* Permutation */
perm([H|T],Perm):-
    perm(T,SP),insert(H,SP,Perm). 
perm([],[]). 
  
insert(X,T,[X|T]). 
insert(X,[H|T],[H|NT]):-
    insert(X,T,NT). 

/* Pack as a list */
% retrive sublist, and remaning of the list
% Elm : Input, subList, remaining
giveList( [], [], [] ).
giveList( [H], [H], [] ).
giveList( [H| [H|T] ], [H|Rest], Rem ) :- giveList( [H|T], Rest, Rem ).
giveList( [H1,H2|T], [H1], [H2|T] ) :- H1 \= H2 .

% create list
packElm( [], [] ) :- !.
packElm( List, Result ) :- giveList( List, SubList, Rem ), packElm( Rem, OtherResults ), append( [SubList], OtherResults, Result ).

/* Length in form [[Len,Char]...] using Pack */
packLen( [], [] ) :- !.
packLen( List, Result ) :- 
  giveList( List, SubList, Rem ),
  packLen( Rem, OtherResults ),
  length(SubList, Len),
  [Char|_] = SubList,
  append( [ [Len,Char] ] , OtherResults, Result ).

/* Length in form [[Len,Char]...] using Pack BUT
single elements -> just themselves */
packLenDup( [], [] ) :- !.
packLenDup( List, Result ) :- 
  giveList( List, SubList, Rem ),
  packLenDup( Rem, OtherResults ),
  length(SubList, Len),
  [Char|_] = SubList,
  addToList( Result, OtherResults, Char, Len ).

addToList( Result, List, Char, 1 ) :-
  append( [Char] , List, Result ).
addToList( Result, List, Char, Len ) :-
  Len =\= 1 ,
  append( [ [Len, Char] ] , List, Result ).

/* Decode packed list - Problem 12 */
unPack( [], [] ).

unPack( [ [Len,Char] | T ], Result ) :-
  unPack( T, MidResult ),
  dupChar( Char, Len, DupList ),
  append( DupList, MidResult, Result ).

unPack( [H|T], Result ) :-
  \+is_list( H ),
  unPack( T, MidResult ),
  append( [H], MidResult, Result ).

dupChar( _, 0, [] ) :- !.
dupChar( Char, Len, [Char|Result] ) :- NewLen is Len-1, dupChar( Char, NewLen, Result ).

/* Another reverse, Using accumlator */
myReverse( X, Y ) :- myRev( X, Y, [] ).

myRev( [], L1, L1 ).
myRev( [X|Xs], L1, Acc ) :- myRev( Xs, L1, [X|Acc] ).

/* Remove Nth element */
remNth( [_|T], 0, T ).
remNth( [H|T], N, [H|Rest] ) :- N > 0, N1 is N-1, remNth( T, N1, Rest ).