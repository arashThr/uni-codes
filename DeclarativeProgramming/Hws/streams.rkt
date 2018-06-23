#lang racket
(require racket/stream)

(define (prime? x)
  (define (iter i)
    (cond ((> i (sqrt x)) #t)
          ((= 0 (remainder x i)) #f)
          (else (prime? (+ i 1)))))
  (iter 2))

(define (display-stream s)
  (stream-for-each display-line s))
(define (display-line x) (newline) (display x))

; Enum generator
(define (stream-enum low high)
  (if (> low high)
      '()
      (stream-cons low
                   (stream-enum (+ low 1) high))))

(define (show x)
  (display x)
  x)
(define x
  (stream-map show (stream-enum 0 10)))
(define sum 0)
(define (accum x) (set! sum (+ x sum)) sum)
(define seq
  (stream-map accum
              (stream-enum 1 20)))
(define y (stream-filter even? seq))
(define z
  (stream-filter (lambda (x) (= (remainder x 5) 0))
                 seq))
;(stream-ref y 7)
;(display sum)
;(display-stream z)

; Natural numbers
(define (int-from-n n)
  (stream-cons
   n
   (int-from-n (+ n 1))))
(define natural (int-from-n 1))

(define (div? x y) (= 0 (remainder x y)))
(define (sevens start)
  (stream-filter (λ(x) (div? x 7)) (int-from-n start)))

(define (fibgen a b) (stream-cons a (fibgen b (+ a b))))
(define fibs (fibgen 0 1))

; Seive
(define (seive s)
  (stream-cons
   (stream-first s)
   (seive (stream-filter
           (λ(x) (not (div? x (stream-first s))))
           (stream-rest s)))))
(define primes (seive natural))

(define (map-s p . args)
  (if (stream-empty? args)
      empty-stream
      (stream-cons
       (apply p (map stream-first args))
       (apply map-s p (map stream-rest args)))))

; Top n elements in stream
(define (top n s)
  (cond ((= n 0) 'done)
        (else 
         (display (stream-first s))
         (newline)
         (top (- n 1) (stream-rest s)))))

; Implicit creation of streams : add
(define (stream-add a b)
  (map-s + a b))
(define ones (stream-cons 1 ones))
(define ints (stream-cons 1 (stream-add ones ints)))

; implicit fibs
(define imp-fib
  (stream-cons
   0
   (stream-cons 
    1
    (stream-add imp-fib (stream-rest imp-fib)))))

(define sprime
  (stream-cons
   2
   (stream-filter prime? (int-from-n 3))))

(define (stream-mul a b)
  (map-s * a b))
(define fact
  (stream-cons
   1
   (stream-mul fact natural)))

; Partial sum
; Notice that in here we have taken our function as stream
(define (par-sum s)
  (stream-cons
   (stream-first s)
   (stream-add (par-sum s) (stream-rest s))))

(define (scale-stream s factor)
  (stream-map (λ(x) (* x factor)) s))

; 3:58 Merging
(define (merge s1 s2)
  (cond ((stream-empty? s1) s2)
        ((stream-empty? s2) s1)
        (else
         (let ((s1car (stream-first s1))
               (s2car (stream-first s2)))
           (cond ((< s1car s2car)
                  (stream-cons
                   s1car
                   (merge (stream-rest s1) s2)))
                 ((> s1car s2car)
                  (stream-cons
                   s2car
                   (merge s1 (stream-rest s2))))
                 (else
                  (stream-cons
                   s1car
                   (merge (stream-rest s1)
                          (stream-rest s2)))))))))
(define hamming
  (stream-cons
   1
   (merge
    (scale-stream natural 2)
    (merge
     (scale-stream natural 3)
     (scale-stream natural 5)))))

(define (expand num den radix)
  (stream-cons
   (quotient (* num radix) den)
   (expand (remainder (* num radix) den) den radix)))

(define (elem? x set)
  (cond((null? set) #f)
       ((equal? x (car set)) #t)
       (else (elem? x (cdr set)))))

(define (join x set)
  (if (elem? x set)
      set
      (cons x set)))

(define (f x)
  (define (even? n) (if (= n 0) true
                        (odd?
                         (- n 1))))
  (define (odd? n)
    (if (= n 0) false (even? (- n 1))))
  even?)

(define (integrate-series s)
  (map-s * (map-s / ones ints) s))
(define exp-series
  (stream-cons 1 (integrate-series exp-series)))
