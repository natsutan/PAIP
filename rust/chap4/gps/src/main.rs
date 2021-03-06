
#[derive(Debug, PartialEq, Copy, Clone)]
enum Action {
    DriveSonToSchool, ShopInstallsBattery, TellShopProblem, TelephoneShop, LookUpNumber,
    AskPhoneNumber, GiveShopMoney
}

#[derive(Debug, PartialEq, Copy, Clone)]
enum Condition {
    SonAtHome, SonAtSchool, CarWorks, ShopHasMoney, HaveMoney, InCommunicationWithShop, KnowPhoneNumber,
    CarNeedsBattery, ShopKnowsProblem, HavePhoneBook
}

#[derive(Debug)]
struct Op {
    action :Action,
    precond :Vec<Condition> ,
    add_list :Vec<Condition>,
    del_list :Vec<Condition>
}

impl Clone for Op {
    fn clone(&self) -> Self {
        let mut op = Op {
            action:self.action,
            precond:vec![],
            add_list:vec![],
            del_list:vec![]
        };

        op.precond = self.precond.to_vec();
        op.add_list = self.add_list.to_vec();
        op.del_list = self.del_list.to_vec();

        op
    }
}


fn school_ops() -> Vec<Op> {
    let mut ops:Vec<Op> = vec![];
    let op0 = Op {
        action:Action::DriveSonToSchool,
        precond:vec![Condition::SonAtHome, Condition::CarWorks],
        add_list:vec![Condition::SonAtSchool],
        del_list:vec![Condition::SonAtHome]
    };

    ops.push(op0);

    let op1 = Op {
        action:Action::ShopInstallsBattery,
        precond:vec![Condition::CarNeedsBattery, Condition::ShopKnowsProblem, Condition::ShopHasMoney],
        add_list:vec![Condition::CarWorks],
        del_list:vec![]
    };
    ops.push(op1);

    let op2 = Op {
        action:Action::TellShopProblem,
        precond:vec![Condition::InCommunicationWithShop],
        add_list:vec![Condition::ShopKnowsProblem],
        del_list:vec![]
    };
    ops.push(op2);

    let op3 = Op {
        action:Action::TelephoneShop,
        precond:vec![Condition::KnowPhoneNumber],
        add_list:vec![Condition::InCommunicationWithShop],
        del_list:vec![]
    };
    ops.push(op3);

    let op4 = Op {
        action:Action::LookUpNumber,
        precond:vec![Condition::HavePhoneBook],
        add_list:vec![Condition::KnowPhoneNumber],
        del_list:vec![]
    };
    ops.push(op4);

    let op5 = Op {
        action:Action::AskPhoneNumber,
        precond:vec![Condition::InCommunicationWithShop],
        add_list:vec![Condition::KnowPhoneNumber],
        del_list:vec![]
    };
    ops.push(op5);

    let op6 = Op {
        action:Action::GiveShopMoney,
        precond:vec![Condition::HaveMoney],
        add_list:vec![Condition::ShopHasMoney],
        del_list:vec![Condition::HaveMoney]
    };
    ops.push(op6);

    ops
}

fn appropriate(goal:&Condition, op:&Op) -> bool {
    op.add_list.contains(&goal)
}


#[warn(unused_variables)]
fn apply_op(state:&mut Vec<Condition>, _goal:&Condition, the_op:&Op, ops:&Vec<Op>) -> bool {

    for goal in &the_op.precond {
        if !archive(state, &goal, &ops) {
            return false
        }
    }
    println!("Executing:{:?}", &the_op.action);
    //update state
    //dellistにあるステートを削除
    for del_state in &the_op.del_list {
        state.retain(|st| *st != *del_state);
    }

    //addlistにあるステートを追加
    for add_state in &the_op.add_list {
        if !state.contains(add_state) {
            state.push(add_state.clone());
        }
    }
    return true
}

fn archive(state:&mut Vec<Condition>, goal:&Condition, ops:&Vec<Op>) -> bool {
    if state.contains(&goal) {
        return true;
    }
    // appropriateを使って、使えるOPを取り出す。
   let mut appropriate_ops :Vec<Op> = vec![];
    for op in ops {
        if appropriate(goal, op) {
            appropriate_ops.push(op.clone());
        }
    }

    for the_op in appropriate_ops {
        if apply_op(state, goal, &the_op, ops) {
            return true;
        }
    }

    false
}


fn gps(state:&mut Vec<Condition>, goals:Vec<Condition>, ops:Vec<Op>) -> bool {

    for goal in &goals {
        if !archive(state, &goal, &ops) {
            return false
        }
    }
    true
}


fn main() {

    let ops = school_ops();
    let mut state:Vec<Condition> = vec![Condition::SonAtHome, Condition::CarNeedsBattery, Condition::HaveMoney, Condition::HavePhoneBook];
    //let mut state:Vec<Condition> = vec![Condition::SonAtHome, Condition::CarWorks];
    //let mut state:Vec<Condition> = vec![Condition::SonAtHome, Condition::CarNeedsBattery, Condition::ShopKnowsProblem, Condition::ShopHasMoney];

    let goal :Vec<Condition> = vec![Condition::SonAtSchool];


    let result = gps(&mut state, goal, ops);

    println!("{:?}", result);
    println!("{:?}", state);
}

