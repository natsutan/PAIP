(load "c:/home/Dropbox/clisp/PAIP/chap6/tools.lsp")

(setf (get '?is 'single-match) 'match-is)
(setf (get '?or 'single-match) 'match-or)
(setf (get 'and 'single-match) 'match-and)
(setf (get 'not 'single-match) 'match-not)

(setf (get '?* 'segment-match) 'segment-match)
(setf (get '?+ 'segment-match) 'segment-match+)
(setf (get '?? 'segment-match) 'segment-match?)
(setf (get '?if 'segment-match) 'match-if)


(defun pat-match (pattern input &optional (bindings no-bindings))
  (cond ((eq bindings fail) fail)
        ((variable-p pattern)
         (match-variable pattern input bindings))
        ((eql pattern input) bindings)
        ((segment-pattern-p pattern)
         (segment-matcher pattern input bindings))
        ((single-pattern-p pattern)
         (single-matcher pattern input binidngs))
        ((and (consp pattern) (rest input))
         (pat-match (rest pattern) (rest input)
                    (pat-match (first pattern) (first input) bindings)))
        (t fail)))

(defconstant fail nil "Indicates pat-match failure")

(defconstant no-bindings '((t . t))
  "Indicates pat-match success, with no variables.")

; (variable-p 'abc)  => NIL
; (variable-p '?*?x) => T
(defun variable-p (x)
  "Is x a variable (a symbol beginninng with '?')?"
  (and (symbolp x) (equal (char (symbol-name x) 0) #\?)))

; (get-binding  'c '((a . b) (c . d) (e . f) (g . h))) => (c . d)
; (get-binding  'd '((a . b) (c . d) (e . f) (g . h))) => NIL
(defun get-binding (var bindings)
  "Find a (variable . value) pair in a binding list."
  (assoc var bindings))

; (binding-var '(?x . 'hello)) => ?X 
(defun binding-var (binding)
  "Get the variable part of a single binding."
  (car binding))

; (binding-val '(?x . ?hello)) => 'HELLO
(defun binding-val (binding)
  "Get the variable part of a single binding."
  (cdr binding))

; (make-binding '?x 'hello) => (?X . HELLO)
(defun make-binding (var val)
  (cons var val))


; (lookup  'c '((a . b) (c . d) (e . f) (g . h))) => D
; (lookup  'd '((a . b) (c . d) (e . f) (g . h))) => NIL
(defun lookup (var bindings)
  "Get the value part (for var) from binding list."
  (binding-val (get-binding var bindings)))


; (extend-bindings  '?x 'hello '((a . b) (c . d) (e . f) (g . h)))
; => ((?X . HELLO) (A . B) (C . D) (E . F) (G . H))
(defun extend-bindings (var val bindings)
  "Add a (var . value) pair to a binding list."
  (cons (make-binding var val)
        ; Once we add a "real" binding. we can get rid of the dummy no-binding
        (if (eq bindings no-bindings)
          nil
          bindings)))


; (match-variable  'a 'b '((a . b) (c . d) (e . f) (g . h)))
; => ((A . B) (C . D) (E . F) (G . H))
; (match-variable  'x 'hello '((a . b) (c . d) (e . f) (g . h)))
; => => ((X . HELLO) (A . B) (C . D) (E . F) (G . H))
(defun match-variable (var input bindings)
  "Does VAR match input? Uses (or updates) and returns bindings"
  (let ((binding (get-binding var bindings)))
    (cond ((not binding)
           (extend-bindings var input bindings))
          ((equal input (binding-val binding))
           bindings)
          (t fail))))

;(setf (get '?* 'segment-match) 'segment-match)
; (segment-pattern-p  '((?* var). pat)) => segment-match
; (segment-pattern-p  '((?** var). pat)) => nil
(defun segment-pattern-p (pattern)
  "Is this a segment-maching pattern like ((?* var) . pat)?"
  (and (consp pattern) (consp (first pattern))
       (symbolp (first (first pattern)))
       (segment-match-fn (first (first pattern)))))

;(setf (get '?* 'segment-match) 'segment-match)
;(setf (get '?+ 'segment-match) 'segment-match+)
;(segment-match-fn '?* ) => 'segment-match
;(segment-match-fn '?+ ) => 'segment-match+
;(segment-match-fn '?a ) => nil
(defun segment-match-fn (x)
  "Get the segment-match function for x"
  (when (symbolp x)
    (get x 'segment-match)))

;(setf (get '?is 'single-match) 'match-is)
;(single-pattern-p  '(?is . pat)) => MATCH-IS
;(single-pattern-p  '(?nand . pat)) => NIL
(defun single-pattern-p (pattern)
  "Is this a single matching pattern?
   E.g. (?is x predicate) (?and . patterns) (?or . patterns)."
  (and (consp pattern)
       (single-match-fn (first pattern))))

;(setf (get '?is 'single-match) 'match-is)
;(setf (get '?or 'single-match) 'match-or)
;(single-match-fn '?is) => MATCH-IS
;(single-match-fn '?or) => MATCH-OR
;(single-match-fn '?nand) => NIL
(defun single-match-fn (x)
  "Get the segmetn-match function for x"
  (when (symbolp x)
    (get x 'single-match)))


(defun segment-matcher (pattern input bindings)
  "Call the right function for this kind of segment pattern"
  (funcall (segment-match-fn (first (first pattern)))
           pattern input bindings))


(defun single-matcher (pattern input bindings)
  "Call the right function for this kind of single pattern"
  (funcall (single-match-fn (first pattern))
           (rest pattern) input bindings))

;; Individual matching function
;; (setf (get '?is 'single-match) 'match-is)
;; (defun eq_hello (x) (eq x 'hello))
;; (match-is '(x  eq_hello) 'hello '((a . b) (c . d) (e . f) (g . h))) = NIL

(defun match-is (var-and-pred input bindings)
  "Succeed and bind var if the input satifies pred,
   Where var-and-pred it the list (var . pred)"
  (let* ((var (first var-and-pred))
         (pred (second var-and-pred))
         (new-bindings (pat-match var input bindings)))
    (if (or (eq new-bindings fail)
            (not (funcall pred input)))
      fail
      new-bindings)))

(defun segment-match (pattern input bindings &optioanal (start 0))
  "Match the segment pattern ((?* var) . pat) against input"
  (let ((var (second (first pattern))
             (pat (rest pattern))))
    (if (null pat)
      (match-variable var input bindings)
      (let ((pos (first-match-pos (first pat) input start)))
        (if (null pos)
          fail
          (let ((b2 (pat-match
                     pat  (subseq input pos)
                     (match-variable var (subseq input 0 pos)
                                     bindings))))
            ;; if this match failed, try another longer one
            (if (eq b2 fail)
              (segment-match pattern input bindings (+ pos 1))
              b2)))))))



(defun eliza ()
  (interactive-interpreter 'eliza_a>
                           #'(lambda (x) (flatten (use-eliza-rules x)))))

;;(eliza)
;; (pat-match '(a (?* ?x) d) '(a b c d))
;; => ((?x b c))
;; (pat-match '(a (?* ?x) (?* ?y) d) '(a b c d))
;; => ((?Y B X) (?x))
