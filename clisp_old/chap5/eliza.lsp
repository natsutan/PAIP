(load "c:/home/Dropbox/clisp/PAIP/chap6/tools.lsp")

(defparameter *eliza-rules*
  '((((?* ?x) hello (?* ?y))
     (How do you do. Please state your proglem.))
    (((?* ?x) I want (?* ?y))
     (What would it mean if you got it ?y)
     (Why do you want ?y)
     (Suppose you got ?y soon))
    ))


(defconstant fail nil "Indicates pat-match faiture")
(defconstant no-binding '((t.t)) "Indicates pat-match success, with novariables")

(defun rule-pattern (rule) (first rule))
(defun rule-responses (rule) (rest rule))

(defun eliza ()
  (loop
   (print 'YUKI.N>)
   (Write (flatten (use-eliza-rules (read))) :pretty t)))

(defun use-eliza-rules (input)
  (some #'(lambda (rule)
            (let ((result (pat-match (rule-pattern rule) input)))
              (if (not (eq result fail))
                (sublis (switch-viewpoint result)
                        (random-elt (rule-responses rule))))))
        *eliza-rules*))

(defun switch-viewpoint (words)
  (sublis '((I . you) (you . I) (me . you) (am . are))
          words))

(defun flatten (the-list)
  (mappend #'mklist the-list))

(defun mklist (x)
  (if (listp x)
    x
    (list x)))

(defun mappend (fn the-list)
        (apply #'append (mapcar fn the-list)))

(defun random-elt (choices)
  (elt choices (random (length choices))))

(defun get-binding (var bindings)
  "Find a (vairable . value) pair in a binding list"
  (assoc var bindings))

(defun binding-val (binding)
  "Get the value part of a single binding"
  (cdr binding))

(defun lookup (var bindings)
  "Get the value aprt (for var) from a binding list"
  (binding-val (get-binding var bindings)))

(defun extend-bindings (var val bindings)
  "Add a (var. value) pair to a binidng list"
  (cons (cons var val)
        (if (eq bindings no-binding)
          nil
          bindings)))


(defun variable-p (x)
  (and (symbolp x) (equal (char (symbol-name x) 0) #\?)))

(defun segment-pattern-p (pattern)
  (and (consp pattern)
       (starts-with (first pattern) '?*)))


(defun starts-with (list x)
    "Is x a list whose first element is x?"
    (and (consp list) (eql (first list) x)))

(defun pat-match (pattern input &optional (bindings no-binding))
  (cond ((eq bindings fail) fail)
        ((variable-p pattern)
         (match-variable pattern input bindings))
        ((eql pattern input) bindings)
        ((segment-pattern-p pattern)
         (segment-match pattern input bindings))
        ((and (consp pattern) (consp input))
         
         (pat-match (rest pattern) (rest input)
                    (pat-match (first pattern) (first input)
                               bindings)))
        (t fail)))

(defun match-variable (var input bindings)
  (let ((binding (get-binding var bindings)))
    (cond ((not binding) (extend-bindings var input bindings
                                          ))
          ((equal input (binding-val binding)) bindings)
          (t fail))))

(defun segment-match (pattern input bindings &optional (start 0))
  (let ((var (second (first pattern)))
        (pat (rest pattern)))
    (if (null pat)
      (match-variable var input bindings)
      (let ((pos (position (first pat) input :start start :test #'equal)))
        (if (null pos)
          fail
          (let ((b2 (pat-match
                     pat
                     (subseq input pos)
                     (match-variable var (subseq input 0 pos) bindings))))
            (if (eq b2 fail)
              (segment-match pattern input bindings (+ pos 1))
              b2)))))))


(defun eliza-a ()
  (interactive-interpreter 'eliza_a>
                           #'(lambda (x) (flatten (use-eliza-rules x)))))


(defun eliza-b ()
  (interactive-interpreter 'eliza_b>
                           (compose #'flatten #'use-eliza-rules)))

;;(eliza)
;;(eliza-a)
