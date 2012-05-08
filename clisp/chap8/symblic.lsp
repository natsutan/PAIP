
(defun infix->prefix (exp)
  "Tranlate  an infix expression into prefix notation."
  (cond ((atom exp) exp)
        ((= (length exp) 1) (infix->prefix (first exp)))
        ((rule-based-translator exp *infix-prefix-rules*
                                :rule-if #'rule-pattern :rule-then #'rule-response
                                :action #'(lambda (bindings response)
                                            (sublis (mapcar
                                                     #'(lambda (pair)
                                                         (cons (first pair)
                                                               (infix->prefix (rest pair))))
                                                     bindings)
                                                    response))))
        ((symbolp (first exp))
         (list (first exp) (infix->prefix (res exp))))
        (t (error "Illegal exp"))))


; (variable-p 'x) => (X Y Z M N O P Q R S T U V W)
; (variable-p 'a) => NIL
(defun variable-p (exp)
  "Variabless are the symbols M through Z."
  (member exp '(x y z m n o p q r s t u v w)))

(pat-match-abbrev 'x+ '(?+ x))


