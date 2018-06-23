;; Quiz 3 Solutions

;; Problem 1

;; (a)

(define (square x) (* x x))

(define (square-tree tree)
  (cond ((null? tree) '())
        ((pair? (car tree))
         (cons (square-tree (car tree))
               (square-tree (cdr tree))))
         (else (cons (square (car tree))
                     (square-tree (cdr tree)))))) 
;; (b)

(define (square-tree tree)
  (map (lambda (t)
         (if (pair? t)
             (square-tree t)
             (square t)))
       tree))

;; Or, we can define a more general tree-map procedure:

(define (tree-map proc tree)
  (map (lambda (t)
         (if (pair? t)
             (tree-map proc t)
             (proc t)))
       tree))

(define (square-tree tree)
  (tree-map square tree))

(square-tree
 (list 1
       (list 2 (list 3 4) 5)
       (list 6 7)))               

;; Problem 2

;; Using the imperative style:

(define (unique-pairs n)
  (define (outer-loop i pairs)
    (define (inner-loop j ps)
      (if (< j 1)
          ps
          (inner-loop (- j 1) (cons (list i j) ps))))
    (if (> i n)
        pairs
        (append (inner-loop (- i 1) '())
                (outer-loop (+ i 1) pairs))))
  (outer-loop 2 '()))


;; The solution can be expressed more elegantly using map and fold:

;; foldr is the same as accumulate in the book
;; range is similar to enumerate-interval in the book

(define (unique-pairs n)
  (foldr
   append '() (map (lambda (i)
                     (map (lambda (j) (list i j))
                          (range 1 i)))
                   (range 1 (+ n 1)))))

;; Problem 3

(define (union-set s1 s2)
  (cond ((null? s1) s2)
        ((null? s2) s1)
        (else 
         (let ((e1 (car s1))
               (e2 (car s2)))
           (cond ((< e1 e2) (cons e1 (union-set (cdr s1) s2)))
                 ((> e1 e2) (cons e2 (union-set s1 (cdr s2))))
                 (else (cons e1 (union-set (cdr s1) (cdr s2)))))))))

(union-set '(1 2 3 4) '(2 4 6 7))

;; Problem 4

(define (make-monitored f)
  (let ((count 0)) 
    (define (mf msg)      
      (cond ((eq? msg 'how-many-calls?) count)
            ((eq? msg 'reset-count) (set! count 0))
            (else (set! count (+ 1 count))
                  (f msg))))
  mf))

(define g (make-monitored square))