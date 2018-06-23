
1392

(quote a)

(define x 3)

(define x 2) (set! x 3) x

(define x 2) (+ x x)

(define (f x) (* 2 x)) (f 5)

(+ 2 2 2)

(define (g x y) (* x y)) (g 4 10)

(define h (lambda (x) (* x x))) (h 7)

(define (min a b) (if (< a b) a b)) (min 3 4)

(define (f x) (+ x x) (* x x)) (f 7)
 
((lambda (x) (+ x x) (* x x)) 7)

(define (min a b) (cond ((< a b) a ) ((= a b)  0) (else b))) (min 5 4)

(define (f x) (define y 0) (set! y 2) y) (f 5)

(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1))))) (factorial 5)

(define (f x) (begin (+ x x) (* x x))) (f 7)

(begin (+ 2 2) (* 3 4))

(if (< 1 1) 2 3)

(g 10 20)

(define (make-account balance)
  (define (withdraw amount)
    (if (< amount balance)
        (begin (set! balance (- balance amount))
               balance)
        (quote Insufficient_funds)))
  (define (deposit amount)
    (set! balance (+ balance amount))
    balance)
  (define (dispatch m) 
    (cond ((= m (quote withdraw)) withdraw)
          ((= m (quote deposit)) deposit)
          (else (quote Unknown_request))))                       
  dispatch)

(define acc (make-account 50))
((acc (quote deposit)) 40)
((acc (quote withdraw)) 10)
((acc (quote withdraw)) 110)
(define acc2 (make-account 100))

