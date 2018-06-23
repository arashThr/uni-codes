;;;;;;;;;   Final Exam Solutions


;; Problem 1

;(define (make-time hr mn cat) (list hr mn cat)) 
;(define hour car) 
;(define minute cadr) 
;(define category caddr) 

;; part a

(define (print-time time)
  (newline)
  (display (hour time))
  (display ":")
  (if (< (minute time) 10)
      (display "0")
      (display ""))
  (display (minute time))
  (display (category time)))

;; part b

(define (24-hour time)
  (+ (* (hour time) 100)
     (minute time)
     (if (equal? (category time) 'pm) 1200 0)))

;; part c

(define (make-time hr min cat)
  (+ (* hr 100)
     min
     (if (equal? cat 'pm) 1200 0)))

(define (hour time)
  (if (>= time 1200)
      (- (quotient time 100) 12)
      (quotient time 100)))

(define (minute time)
  (remainder time 100))

(define (category time)
  (if (>= time 1200) 'pm 'am))



; Problem 2

(define (compose f g)
  (λ (x)
    (f (g x))))


(define (locate value struct)
  (cond ((equal? value struct) (lambda (x) x))
        ((pair? struct)
         (let ((left (locate value (car struct))))
           (if left
               (compose left car)
               (let ((right (locate value (cdr struct))))
                 (if right
                     (compose right cdr)
                     #f)))))
        (else #f)))


;; Problem 3

(define (merge! a b)
  (cond ((null? a) b)
        ((null? b) a)
        ((<= (car a) (car b))
         (set-cdr! a (merge! (cdr a) b))
         a)
        (else
         (set-cdr! b (merge! a (cdr b)))
         b)))


;; Problem 4

(define all-integers
  (cons-stream 0 (interleave integers
                             (scale-stream -1 integers))))


;; Problem 5

(define (plus x y)
  (let ((tx (type x))
        (ty (type y)))
    (if (eq? tx ty)
        (attach-tag tx (+ (contents x) (contents y)))
        (let ((gxy (get tx ty))
              (gyx (get ty tx)))
          (cond ((number? gxy)
                 (attach-tag ty (+ (* gxy (contents x)) (contents y))))
                ((number? gyx)
                 (attach-tag tx (+ (contents x) (* gyx (contents y)))))
                (else (error "You can't add apples and oranges.")))))))


;; Problem 6 

(define (make-rat num den)
  (define (dispatch msg)
    (cond
      ((eq? msg 'numer) num)
      ((eq? msg 'denom) den)
      ((eq? msg 'type) 'rational)
      ((eq? msg 'raise) (make-real (/ num den)))
      (else ((dispatch 'raise) msg)) ))
  dispatch)

(define (type r) (r 'type))

(define (raise r) (r 'raise))

;; Problem 7

;; Ask Google!