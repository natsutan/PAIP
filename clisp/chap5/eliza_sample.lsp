

(pat-match '((?* ?x) a b  (?* ?x)) '(1 2 a b a b 1 2 a b))
(pat-match '((?* ?x) a  (?* ?x)) '(1 a b a 1 a b))
(pat-match '((?* ?p) need (?* ?x)) '(Mr Hulot and I need a vacation))
(pat-match '((?* ?x) is a (?* ?y)) '(what he is a fool))
(pat-match '(?X) '(a))
(pat-match '(I need a ?X) '(I need a vacation))
(pat-match '(a ?X) '(a vacation))
(pat-match '(I need a ?X) '(I really need a vacation))
(pat-match '(This is easy) '(This is easy))
(pat-match '(?x is ?x) '((2 + 2) is 4))
(pat-match '(?x is ?x) '((2 + 2) is (2 + 2)))
(pat-match '(?p need . ?x) '(i need a long vacation))
; sublis memo
;(sublis '((?X . vacation))
;        '(what would it mean to you if you got a ?X ?))

