(defparameter *simple-grammer*
  '((sentence -> (noun-phrase verb-phrase))
    (noun-phrase -> (Article Noun))
    (verb-phrase -> (Verb noun-phrase))
    (Article -> the a)
    (Noun -> man ball woman table)
    (Verb -> hit took saw liked))
  "A grammar for a trivial subset of English")

(defvar *grammer* *simple-grammer*
  "The grammar used by generate. Initially, this is *simple-grammer*, but we can switch to other grammers.")

(defun mapend (fn the-list)
  "apply fn to each element of list and append the result"
  (apply #'append (mapcar fn the-list)))


(defun rule-lhs (rule)
  "The left-hand side of a rule"
  (first rule))

(defun rule-rhs (rule)
  "the right-hand side of a rule"
  (rest (rest rule)))

(defun rewrites (category)
  "Return a list of the possible rewrites for this category"
  (rule-rhs (assoc category *grammer*)))


(defun generate (phrase)
  "Generate a random sentence or phrase"
  (cond ((listp phrase)
         (mapend #'generate phrase))
        ((rewrites phrase)
         (generate (random-elt (rewrites phrase))))
        (t (list phrase))))
