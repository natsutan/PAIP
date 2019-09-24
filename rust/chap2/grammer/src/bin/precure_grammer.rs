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

composite_rule!(sentence,   ->, shubu, jutubu);
composite_rule!(shubu,      ->, precure, joshi);
composite_rule!(jutubu,     ->, syusyokubu, jutugo);
composite_rule!(precure,    ->, pre, cure);
composite_rule!(syusyokubu, ->, obj, joshi2);

simple_rule!(joshi,  ->, "は が");
simple_rule!(joshi2, ->, "が を と");
simple_rule!(jutugo, ->, "好き 戦う 会う 食べる");
simple_rule!(pre,    ->, "キュア キュア キュア シャイニー");
simple_rule!(cure,   ->, "ブラック ホワイト ルミナス マリン エール ミルキー");
simple_rule!(obj,    ->, "ザケンナー たこやき キリヤくん カッパード");


fn conv_str(v:Vec<&'static str>) -> String {
    let mut cs:String = "".to_string();
    for s in v {
        cs = cs + s + " ";
    }
    cs + "。"
}

fn main() {
    for _ in 0..10  {
        println!("{}", conv_str(sentence()));
    }
}
