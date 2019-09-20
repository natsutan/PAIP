(defun lisp ()
  (interactive-interpreter '> #'eval))

(defun interactive-interpreter (prompt transformer)
  (loop
   (handler-case
       (progn 
         (print prompt)
         (print (funcall transformer (read))))
     (error (condition)
       (format t "~&;; Error ~a ignored, back to top level." condition)))))
         
     


(defun compose (f g)
  #'(lambda (x) (funcall f (funcall g x))))

                         

  
