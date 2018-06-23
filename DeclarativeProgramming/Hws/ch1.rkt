#lang scheme

; First a few neccessary functions and definitions
(define (square x)(* x x))
(define (inc x)(+ x 1))
(define tolerance 0.0001)

#! 1.4 : The if statments returns a function wich will be applied to a and b
(define (aPlusb a b )
  ( (if (> b 0 ) + - ) a b ))

; 1.5 : Scheme evaluates statments in applicative order.
; which means it tries to calculate the value of (p) and substitute it.
; But, since (p) defines itself, it falls into a finit loop and nerver terminates
(define (p) (p))
(define (test x y)
  (if (= x 0) 0 (p)))

; 1.31
(define (product term a next b )
  ( if (> a b)
       1
       ( * (term a)
           (product term (next a) next b))))

(define (fact a)
  (product ( λ(x) x ) 1 (λ(x)(+ x 1)) a))


; Iterative implimentation of product
(define (iter-product term a next b start-val)
  ( if (> a b)
        start-val
        (iter-product term (next a) next b (* start-val (term a)))))


; General case
( define (acc comb null-val term a next b )
   ( if (> a b )
        null-val
        (comb (term a)
              (acc comb null-val term (next a) next b ))))

(define (gcd a b)
  ( if (= b 0)
       a
       (gcd b (remainder a b))))

( define (scale items factor )
   ( if ( null? items )
        null
        ( cons ( * (car items) factor )
               (scale ( cdr items) factor))))

; 1.35
; We simply use fixed point functuion to determine the golden-ratio
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next)
          next
          (try next))))
  (try first-guess))

(define (golden-ratio)
  (fixed-point (lambda (x) (+ 1 (/ 1 x))) 2.0))


; 1.36
; QUESTION : DAMPING !!!
(define (fixed-point-print f first-guess)
  (define (close-enough? v1 v2)
    (< (abs (- v1 v2))
       tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (display "Next guess : ")
      (display next)
      (newline)
      (if (close-enough? guess next)
          next
          (try next))))
  (try first-guess))

(define (find-x)
  (fixed-point-print (λ(x) (/ (log 1000) (log x))) 2))


; 1.37 : Continued Fraction
(define (cont-frac n d k)
  (define (helper n d k i)
    (if (= i k)
        (/ (n i) (d i))
        (/ (n i) (+ (d i) (helper n d k (+ i 1) )))))
  (helper n d k 1))

; Testin cont-fraction by checking whethere it gives us 1/golden or not
(define (golden-rev k)
  (cont-frac (λ(i) 1.0)
             (λ(i) 1.0)
             k))

; Equevalent iterative procedure
(define (cont-frac-iter n d k)
  (define (helper n d k result)
    (if (= k 0)
        result
        (helper n d (- k 1) (/ (n k) (+ (d k) result)))))
  (helper n d k 0))

(define (golden-rev-iter k)
  (cont-frac-iter (λ(i) 1.0)
             (λ(i) 1.0)
             k))

; 1.39
; There's no need to rewrite this program
; We can use our cont-frac
(define (tan-cf1 x k)
  (define (square x) (* x x))
  (cont-frac-iter
   (λ(i) (if (= i 1) x (- (square x))))
   (λ(i) (- (* 2 i) 1))
   k))

; 1.40
; Cubic procedure : Returns a function that represents cubic functions
(define (cubic a b c)
  (λ(x) (+ (* x x x) (+ (* a (* x x)) (+ (* b x) c)))))
; OR
(define (other-cubic a b c)
  (λ(x)
    (+ (* x x x)
       (* a (* x x))
       (* b x)
       c)))

; 1.41 : Doubling functions
(define (double f)
  (λ(x) (f (f x))))

; 1.42 : Composition function
; Very intresting !
(define (compose f g)
  (λ(x) (f (g x))))

; 1.43
(define (rep-func f i)
  (if (= i 1)
      f
      (compose f (rep-func f (- i 1)))))

; 1.44 Smooth function
(define dx 0.0001)
(define (smooth f)
  (λ(x) (/ (+ (f (+ x dx))
              (f (- x dx))
              (f x)) 3)))

(define (n-fold-smooth f n)
  ((rep-func smooth n) f))
