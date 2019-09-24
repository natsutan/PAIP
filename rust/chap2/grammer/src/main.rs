//https://github.com/norvig/paip-lisp/blob/master/docs/chapter2.md#23-a-rule-based-solution
use rand::Rng;

#[macro_use]
extern crate lazy_static;
extern crate gensym;

fn random_elm_idx(i:usize) -> usize {
    let mut rng =  rand::thread_rng();
    rng.gen_range(0, i as u32) as usize
}

macro_rules! _simple_rule {
    ($gensym:ident, $e1: ident, $e2:tt, $e3: expr) => {
        lazy_static! {
            static ref $gensym:Vec<&'static str> = {
                let mut table:Vec<&'static str> = Vec::new();
                for s in $e3.split(' ') {
                    table.push(s);
                }
                table
            };
        }

        fn $e1()-> Vec<&'static str>  {
            vec![$gensym[random_elm_idx($gensym.len())]]
        }
    }
}

macro_rules! simple_rule {
    ($e1: ident, $e11:tt, $e2: expr) => {
        gensym::gensym! {
          _simple_rule!{ $e1, $e11, $e2}
        }
    };
}

macro_rules! composite_rule {
    ($e1: ident, $e2:tt, $e3: expr, $e4: expr) => {
        fn $e1() -> Vec<&'static str> {
            let mut n:Vec<&str> = Vec::new();
            for s in $e3() {
                n.push(s);
            }
            for s in $e4() {
                n.push(s);
            }
            n
        }
    };
}


/*
(defparameter *simple-grammer*
  '((sentence -> (noun-phrase verb-phrase))
    (noun-phrase -> (Article Noun))
    (verb-phrase -> (Verb noun-phrase))
    (Article -> the a)
    (Noun -> man ball woman table)
    (Verb -> hit took saw liked))
  "A grammar for a trivial subset of English")
*/

composite_rule!(noun_phrase, ->, article, noun);
composite_rule!(verb_phrase, ->, verb, noun_phrase);
composite_rule!(sentence,    ->, noun_phrase, verb_phrase);
simple_rule!(article, ->, "a the");
simple_rule!(noun,    ->, "man ball woman table");
simple_rule!(verb,    ->, "hit took saw liked");


fn conv_str(v:Vec<&'static str>) -> String {
    let mut cs:String = "".to_string();
    for s in v {
        cs = cs + s + " ";
    }
    cs + "."
}

fn main() {
    for _ in 0..10  {
        println!("{}", conv_str(sentence()));
    }
}
