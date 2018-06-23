-module(myLib).
%-export([for/3, qsort/1, area/1, pythag/1, perm/1, max/2, f/1, 
%        sum/1, calc/3, startCalc/3, autoCalc/2, sqrt/1 ]).
-compile(export_all).

area( {rect, Width, Ht} ) -> Width * Ht;
area( {circle, R} )       -> 3.1415 * R * R.

for( Max, Max, F )  -> [ F(Max) ];
for( I, Max, F )    -> [ F(I) | for( I+1, Max, F ) ].

qsort([]) -> [];
qsort([Pivot|T]) ->
    qsort([X || X<-T, X<Pivot ])
    ++ [Pivot] ++
    qsort([X || X<-T, X>=Pivot ]).

pythag(N) ->
    [ {A,B,C} ||
        A <- lists:seq(1,N),
        B <- lists:seq(1,N),
        C <- lists:seq(1,N),
        A+B+C =< N,
        A*A+B*B =:= C*C
    ].

perm([])    -> [ [] ];
perm(L)     -> [ [H|T] || H<-L, T<-perm(L--[H]) ].

max(X, Y) when X>Y -> X;
max(_, Y) -> Y.

f(X) when (X==0) orelse (X/1)>0 -> hello;
f(_) -> bye.

sum(L)  -> sum(L, 0).

sum([], N)  -> N;
sum([H|T], N)   -> sum( T, H+N ).


autoCalc( A, B ) ->
    [ catch(calc(A, B, X)) || X <- ['+', '-', '*', '/'] ].

startCalc( A, B, Op ) ->
    try calc(A, B, Op)

    catch
        exit:X  -> {caught, X};
        throw:X when X == 'div' -> 'DIVIDE';
        throw:X when X == 'sum' -> 'SUM';
        throw:X -> {X, caught}
    end.

calc(A, B, Op) when is_integer(A), is_integer(B) ->
    case Op of
        '+' -> throw('sum');
        '-' -> exit('Exit');
        '*' -> erlang:error('Erl Error');
        '/' when A>B -> throw('div');
        _ -> throw(shit)
    end.

sqrt( X ) ->
    if
        X < 0   -> erlang:error( {'SqRootNeg', X, erlang:get_stacktrace()} );
        true    -> math:sqrt(X)
    end.
