(load "C:\\home\\myproj\\PAIP\\cl\\common\\paip.lisp")

(defvar *state* nil
  "the current state: a list of condtions")

(defvar *ops* nil
  "A list of available operators.")

(defstruct op
  "An operation"
  (action nil)
  (preconds nil)
  (add-list nil)
  (del-list nil))

(defun GPS (*state* goal *ops*)
  "General Problem Solver: archive all goals using *ops*"
  (if (every #'achieve goals) 'solved))

(defun achieve (goal)
  "A goal is achieved if it already holds, or if there is an appropriate op for it that applicable"
  (or (member goal *state*)
	(some #'apply-op (find-all goal *ops* :test #'appropriate-p))))

(defun appropriate-p (goal op)
  "An op is appropriate to a goal if it is in its add list"
  (member goal (op-add-list op)))

(defun apply-op (op)
  "Print a message and updat *state* is op is applicable. "
  (when (every #'achieve (op-preconds op))
    (print (list 'executing (op-action op)))
    (setf *state* (set-difference *state* (op-del-list op)))
    (setf *state* (union *state* (op-add-list op)))
    t))


