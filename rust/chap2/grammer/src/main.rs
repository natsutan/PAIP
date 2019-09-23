use rand::Rng;


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

static ARTICLE_TABLE:[&str; 2] = ["a", "the"];
static NOUN_TABLE:[&str; 4] = ["man", "ball", "woman", "table"];
static VERB_TABLE:[&str; 4] = ["hit", "took", "saw", "liked"];

fn random_elm_idx(i:usize) -> usize {
    let mut rng =  rand::thread_rng();
    rng.gen_range(0, i as u32) as usize
}

macro_rules! simple_rule {
    ($e1: ident, $e2: expr) => {
        fn $e1() -> &'static str {
            $e2[random_elm_idx($e2.len())]
        }
    };
}

simple_rule!(article, ARTICLE_TABLE);
simple_rule!(noun, NOUN_TABLE);
simple_rule!(verb, VERB_TABLE);

S
fn noun_phrase() -> Vec<&'static str> {
    let art = article();
    let no = noun();
    vec![art, no]
}

fn conv_str(v:Vec<&'static str>) -> String {



    "".to_string()
}

fn main() {
    let gen_art = article();
    let gen_noun = noun();
    let gen_verb = verb();

    println!("{} {} {} ", gen_art, gen_noun, gen_verb);

    let gen_noun_pharse = noun_phrase();
    println!("{}", gen_noun_pharse);

}
