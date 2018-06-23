#lang racket

; 3.1 : Accumulator
(define (accum init-val)
  (let ((sum init-val))
    (λ(x)
      (set! sum (+ x sum))
      sum)))

; 3.2 : Procedure call counter
(define (sqrt x) (* x x))
(define (proc-counter proc)
  (let ((counter 0))
    (define (call-proc x) (proc x))
    (define (print-counter) counter)
    (define (reset-counter) (set! counter 0))
    (define (dispatch m)
      (cond ((eq? m 'how-many?) (print-counter))
            ((eq? m 'reset) (reset-counter))
            (else
             (set! counter (+ counter 1))
             (call-proc m))))
    dispatch))

; 3.3 : Password
(define (acc-pass new-pass proc)
  (let ((pass new-pass))
    (define (check-pass entered-pass value)
      (if (eq? entered-pass pass)
          (proc value)
          (error "Bad pass")))
    check-pass))

; checking refrential transparency
(define (rt x)
  (let ((init x))
    (λ(y)
      (display x)
      (set! x y)
      x)))

; 3.7 : Joint accounts -> Intresting question

; 3.8 : Order of evaluation
(define (g init)
  (define (f x)
    (let ((val init))
      (let ((old-val val))
        (set! val x)
        old-val)))
  f)

(define f 
  (let ((init (- 1))) 
    (lambda (x) (if (= init (- 1)) 
                    (set! init x) 
                    0)))) 
