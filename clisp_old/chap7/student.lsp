

(defstruct (rule (:type list)) pattern response)
(defstruct (exp (:type list)
                (:constructor mkexp (lhs op rhs)))
  op lhs rhs)

(defun exp-p (x)
  (consp x))

(defun exp-args (x)
  (rest x))

(pat-match-abbrev '?x* '(?* ?x))
(pat-match-abbrev '?y* '(?* ?y))

(defparameter *student-rules*
  (mapcar #'expand-pat-match-abbrev
          '(((?x* |.|) ?x)
            ((?x* |.|) (?x ?Y))
            ((if ?x* |,| then ?y*) (?x ?y))
            ((if ?x* then ?y*) (?x ?y))
            ((if ?x* |,| ?y*) (?x ?y))
            ((if ?x* |,| and ?y*) (?x ?y))
            ((?x* |,| and ?y*) (?x ?y))
            ((find ?x* and ?y*) ((= to-find-l ?x) (= to-find-2 ?y)))
            ((find ?x*) (= tofind ?x))
            ((?x* equals ?y*) (= ?x ?y))
            ((?x same as ?y*) (= ?x ?y))
            ((?x* = ?y*) (= ?x ?y))
            ((?x* is equal to ?y*) (= ?x ?y))
            ((?x* is ?y*) (= ?x ?y))
            ((?X* - ?y*) (- ?x ?y))
            ((?x* minus ?y*) (- ?x ?y))
            ((difference between ?x* and ?y*) (- ?y ?x))
            ((differnce ?x* and ?y*) (- ?y ?x))
            ((?x* + ?y*) (+ ?x ?y))
            ((?x* plus ?y*) (+ ?x ?y))
            ((sum ?x* and ?y*) (+ ?x ?y))
            ((product ?x* and ?y*) (* ?x ?y))
            ((?x* * ?y*) (* ?x *y))
            ((?x* times *?y) (* ?x ?y))
            ((?x* / ?y*) (/ ?x ?y))
            ((?x per ?y*) (/ ?x ?y))
            ((?x divided by ?y*) (/ ?x ?y))
            ((half ?x*) (/ ?x 2))
            ((one half ?x*) (/ ?x 2))
            ((twice ?x*) (* 2 ?x))
            ((square ?x*) (* ?x ?x))
            ((?x* % less than ?y*) (* ?y (/ (- 100 ?x) 100)))
            ((?x* % more than ?y*) (* ?y (/ (+ 100 ?x) 100)))
            ((?x % ?y*) (* (/ ?x 100) ?y)))))



(defun student (words)
  "Solve certain Algebra Word Problems."
  (solove-equations
   (create-lis-ob-equation
    (translate-to-expression (remove-if #noise-word-p words)))))

;(noise-word-p 'a) =>  (A AN THE THIS NUMBER OF $)
;(noise-word-p 'b) =>  NIL
(defun noise-word-p (word)
  "Is this a low-content word that can be safely igonored?"
  (member word '(a an the this number of $)))
             

(defun tranlate-to-expression (words)
  "Translate an English phrase into an equation or expresssion"
  (or (rule-based-translator
       words *student-rules*
       :rule-if #'rule-pattern :rule-then #'rule-response
       :action #'(lambda (bindings response)
                   (sublis (mapcar #'translate-pair bindings)
                           response)))
      (make-variable words)))