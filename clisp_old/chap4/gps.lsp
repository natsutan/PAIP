(load "c:/home/Dropbox/clisp/mylib/paip.lsp")

(defvar *state* nil)
(defvar *ops* nil)

(defstruct op "An operation"
	   (action nil)
	   (preconds nil)
	   (add-list nil)
	   (del-list nil))

(defun GPS (*state* goals *ops*)
  (if (every #'achieve goals) 'solved))

(defun achieve (goal)
  (print "----- in achieve -----")
  (print goal)
  (print *state*)
  (or (member goal *state*)
      (some #'apply-op
	     (find-all goal *ops* :test #'appropriate-p))))

(defun appropriate-p (goal op)
  (member goal (op-add-list op)))

(defun apply-op (op)
  (when (every #'achieve (op-preconds op))
    (print (list 'execute (op-action op)))
    (setf *state* (set-difference *state* (op-del-list op)))
    (setf *state* (union *state* (op-add-list op)))
    t))


(defparameter *school-ops*
  (list 
   (make-op 
    :action 'drive-son-to-school
    :preconds '(son-at-home car-works)
    :add-list '(son-at-school)
    :del-list '(son-at-home))
   (make-op
    :action 'shop-installs-battery
    :preconds '(car-needs-battery shop-knows-problem shop-has-money)
    :add-list '(car-works))
   (make-op
    :action 'tell-shop-problem
    :preconds '(in-communication-with-shop)
    :add-list '(shop-knows-problem))
   (make-op
    :action 'telephon-shop
    :preconds '(know-phone-number)
    :add-list '(in-communication-with-shop))
   (make-op
     :action 'look-up-number
     :preconds '(have-phone-book)
     :add-list '(know-phone-number))
    (make-op
     :action 'give-shop-money
     :preconds '(have-money)
     :add-list '(shop-has-money)
     :del-list '(have-money))))

; -> SOLVED
(gps '(son-at-home car-needs-battery have-money have-phone-book)
     '(son-at-school)
     *school-ops*)


; -> Solved
(gps '(son-at-home car-needs-battery have-money have-phone-book)
     '(have-money son-at-school) *school-ops*)

; -> SOLVED
(gps '(son-at-home car-works)
     '(son-at-school)
     *school-ops*)

(print "new problem")

(trace achieve)
(trace appropriate-p)
(trace every)
(trace apply-op)
(trace gps)

(untrace achieve)
(untrace appropriate-p)
(untrace every)
(untrace apply-op)
(untrace gps)
