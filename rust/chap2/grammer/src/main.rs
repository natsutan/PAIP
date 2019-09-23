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

fn article() -> &'static str {
    ARTICLE_TABLE[random_elm_idx(ARTICLE_TABLE.len())]
}

fn noun() -> &'static str {
    let idx = random_elm_idx(NOUN_TABLE.len());
    NOUN_TABLE[idx]
}

fn verb() -> &'static str {
    let idx = random_elm_idx(VERB_TABLE.len());
    VERB_TABLE[idx]
}


fn main() {
    let gen_art = article();
    let gen_noun = noun();
    let gen_verb = verb();

    println!("{} {} {} ", gen_art, gen_noun, gen_verb);
}
