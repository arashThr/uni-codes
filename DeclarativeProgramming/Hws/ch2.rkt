#lang scheme

; 2.1
(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))

(define (make-rat n d)
  (let ((g (gcd n d)))
    (let (
          (n (/ n g))
          (d (/ d g)))
      (if (negative? d)
          (cons (- n) (- d))
          (cons n d)))))

(define (print-rat rat-num)
  (display (car rat-num))
  (display "/")
  (display (cdr rat-num)))

; 2.2 Point
(define (make-seg p1 p2)
  (cons p1 p2))
(define (start-seg p)
  (car p))
(define (end-seg p)
  (cdr p))

(define (make-point x y)
  (cons x y))
(define x-point car)
(define y-point cdr)

(define (print-point p)
  (display (x-point p))
  (display ",")
  (display (y-point p))
  (newline))

(define (mid-point line)
  (let(( x1 (x-point (start-seg line)) )
       ( x2 (x-point (end-seg line)) )
       ( y1 (x-point (start-seg line)) )
       ( y2 (x-point (end-seg line)) ))
    (make-point (/ (+ x1 x2) 2)
                (/ (+ y1 y2) 2))))

(define (cons1 x y)
  (lambda (m) (m x y))) 
; Return val is a procedure which takes an input
; This input it gives a function which chooses either x or y
(define (car1 z)
  (z (lambda (p q) p)))
; Gives input to returned procedure from cons
; Btween it's two input, it returns the first one
(define (cdr1 z)
  (z (λ(p q) q)))

; 2.5
(define (cons2 x y)
  (* (expt 2 x)
     (expt 3 y)))

(define (reduce num base)
  (define (iter num base counter)
    (if (= 0 (remainder num base))
        (iter (/ num base) base (+ counter 1))
        counter))
  (iter num base 0))

(define (car2 c)
  (reduce c 2))
(define (cdr2 c)
  (reduce c 3))

; 2.6 
(define zero (lambda (f) (lambda (x) x)))
(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))

; Length of list
(define (len l)
  (if (null? l)
      0
      (+ (len (cdr l)) 1)))

; Append
(define (app l1 l2)
  (if (null? l1)
      l2
      (cons (car l1) (app (cdr l1) l2))))

; 2.17 Last element of the list as a list
(define (last l)
  (if (null? (cdr l))
      l
      (last (cdr l))))

; 2.18 Reverse a list
(define (rev l)
  (if (null? l)
      null
      ; replace app with cons and see what happens
      (app (rev (cdr l)) (list (car l)) )))
(define (iter-rev l)
  (define (iter l res)
    (if (null? l)
        res
        (iter (cdr l) (cons (car l) res))))
  (iter l null))

; 2.19 Coin change
(define (no-more? lst) (null? lst))
(define (except-first-denomination coins) (cdr coins))
(define (first-denomination coins) (car coins))
(define (cc amount coin-values)
  (cond ((= amount 0) 1)
        ((or (< amount 0) (no-more? coin-values)) 0)
        (else
         (+ (cc amount
                (except-first-denomination
                 coin-values))
            (cc (- amount
                   (first-denomination
                    coin-values))
                coin-values)))))

; 2.20 Dotter-tail-notation
(define (parity x . l )
  (let ( (p (remainder x 2)))
    (define (create-list rest result)
      ( if(null? rest)
          result
          (if (= p (remainder (car rest) 2))
              (create-list (cdr rest) (app result (list (car rest))))
              ; OR : (create-list (cdr rest) (cons (car rest) result))
              ; but it will be in reverse order
              (create-list (cdr rest) result))))
    (create-list l (list x) )))

(define (sum a b . l)
  (define (iter l)
    (if (null? l)
        0
        (+ (car l) (iter (cdr l)))))
  (+ (iter l) a b))

; 2.21 Map
(define (map-square l)
  (map (λ(x) (* x x)) l))

; 2.22 Square
(define (square x)(* x x))
(define (square-list items)
  (define (iter things answer)
    (if (null? things)
        answer
        (iter (cdr things)
              (cons (square (car things))
                    answer))))
  (iter items null))

; 2.23
(define (print x)
  (display x)(newline))
(define (for-each lst action)
  (cond ((null? lst) #t)
        (else (action (car lst))
              (for-each (cdr lst) action))))

; Trees
(define (count-leaves lst)
  (cond((null? lst) 0)
       ((not (list? lst)) 1)
       (else (+ (count-leaves (car lst))
                (count-leaves (cdr lst))))))

(define l1 (list 1 3 (list 5 7) 9))

; 2.26
(define x1 (list 1 2 3))
(define y1 (list 4 5 6))

; 2.27 Deep reverse
(define (deep-rev l)
  (if (null? l)
      null
      (if (not (list? (car l)))
          (append (deep-rev (cdr l)) (list (car l)))
          (append (deep-rev (cdr l)) (list (deep-rev (car l)))))))

; 2.28 Flatting list
(define (fringe l)
    (cond((null? l) null)
         ((not(list? (car l))) (cons (car l) (fringe (cdr l))))
         (else (append (fringe (car l)) (fringe (cdr l))))))

(define my-tree (list 1 (list 2 (list 3 4) (list 5 6)) (list 7 (list 8))))

; eq in list
(define (memq sym l)
  (cond((null? l) false)
      ((eq? sym (car l)) (cdr l))
      (else (memq sym (cdr l)))))