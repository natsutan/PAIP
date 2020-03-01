
#[derive(Debug, PartialEq)]
enum Action {
    DriveSonToSchool, ShopInstallsBattery, TellShopProblem, TelephoneShop, LookUpNumber,
    AskPhoneNumber, GiveShopMoney
}

#[derive(Debug, PartialEq)]
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



fn main() {

    let ops = school_ops();


    println!("{:?}", ops);
}
