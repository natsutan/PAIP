
(defun sentence () (append (noun-pharse) (verb-pharse)))
(defun noun-pharse () (append (Article) (adj*) (Noun) (pp*)))
(defun verb-pharse () (append (Verb) (noun-pharse)))
(defun Article () (one-of '(the a )))
(defun Noun ()    (one-of '(man ball woman table)))
(defun Verb ()    (one-of '(hit took saw liked)))

(defun one-of (set) (list (random-elt set)))
(defun random-elt (choices)
  (elt choices (random (length choices))))


(defun adj* ()
  (if (= (random 2) 0)
      nil
      (append (adj) (adj*))))

(defun pp* ()
  (if (random-elt '(t nil))
      (append (pp) (pp*))
      nil))

(defun pp () (append (prep) (noun-pharse)))
(defun adj () (one-of '(big little bule green adiabatic)))
(defun prep () (one-of '(to in by with on)))

              
