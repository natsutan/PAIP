(load "C:\\home\\myproj\\PAIP\\cl\\common\\paip.lisp")

(defvar *dbg-ids* nil "Identfiers uset by dbg")

(defun dbg (id format-string &rest args)
  "Print debugging info if (DEBUG ID) has been specified"
  (when (member id *dbg-ids*)
    (fresh-line *debug-io*)
    (apply #'format *debug-io* format-string args)))

(defun debug2 (&rest ids)
  "Start dbg output on the given ids"
  (setf *dbg-ids* (union ids *dbg-ids*)))

(defun undebug (&rest ids)
  "Stop dbg on the ids. With no ids, stop dbg altogether."
  (setf *dbg-ids* (if (null ids) nil
                      (set-difference *dbg-ids* ids))))

(defun dbg-indent (id indent format-string &rest args)
  "Print indentd debugging info if (DEBUG ID) has been specified"
  (when (member id *dbg-ids*) 
    (fresh-line *debug-io*)
    (dotimes (i indent) (princ " " *debug-io*))
    (apply #'format *debug-io* format-string args)))


(defvar *ops* nil "A list of available operators")

(defstruct op "An operation"
  (action nil)
  (preconds nil)
  (add-list nil)
  (del-list nil))

(defun executing-p (x)
  "Is x of the form: (executing ...) ?"
  (starts-with x 'executing))

(defun starts-with (list x)
  "Is this a list whose first elemetnt is x?"
  (and (consp list) (eql (first list) x)))


(defun convert-op (op)
  (unless (some #'executing-p (op-add-list op))
    (push (list 'executing  (op-action op)) (op-add-list op)))
  op)

(defun op (action &key preconds add-list del-list)
  (convert-op 
   (make-op :action action
            :preconds preconds
            :add-list add-list
            :del-list del-list)))


(defun gps (state goals &optional (ops *ops*))
  "General Problem Solver: from state, achieve goals using *ops*."
  (let ((old-ops *ops*))
    (setf *ops* ops)
    (let ((result (remove-if #'atom (achieve-all (cons '(start) state) goals nil))))
      (setf *ops* old-ops)
      result)))

(defun achieve-all (state goals goal-stack)
  "Achieve each goal, and make sure they still hold at the end"
  (let ((current-state state))
    (if (and (every #'(lambda (g)
                        (setf current-state (achieve current-state g goal-stack)))
                    goals)
             (subsetp goals current-state :test #'equal))
        current-state)))

(defun achieve (state goal goal-stack)
  "A goal is achieed if it that is applicable"
  (dbg-indent :gps (length goal-stack) "Goal:~a" goal)
  (cond ((member-equal goal state) state)
        ((member-equal goal goal-stack) nil)
        (t (some #'(lambda (op) (apply-op state goal op goal-stack))
                 (find-all goal *ops* :test #'appropriate-p)))))

(defun member-equal (item list)
  (member item list :test #'equal))

(defun apply-op (state goal op goal-stack)
  "Return a new. transformed state if op is applicable."
  (dbg-indent :gps (length goal-stack) "Consider: ~a" (op-action op))
  (let ((state2 (achieve-all state (op-preconds op)
                             (cons goal goal-stack))))
    (unless (null state2)
      ;; Return an updated state
      (dbg-indent :gps (length goal-stack) "Action: ~a" (op-action op))
      (append (remove-if #'(lambda (x)
                             (member-equal x (op-del-list op)))
                         state2)
              (op-add-list op)))))

(defun appropriate-p (goal op)
  "An op is appropriate to a goal if it is in its add-list."
  (member-equal goal (op-add-list op)))


(defun use (oplist)
  (length (setf *ops* oplist)))

(load "C:\\home\\myproj\\PAIP\\cl\\chap4\\school.lisp")
(use (mapc #'convert-op *school-ops*))
;(use *school-ops*)

(gps '(son-at-home car-needs-battery have-money have-phone-book)
     '(son-at-school))


