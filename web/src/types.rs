use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
pub struct QuestionResult {
    pub question: String,
    pub answer: String,
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
pub struct Question {
    pub question: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Message {
    pub message: String,
    pub sender: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Chat {
    pub messages: Vec<Message>,
}
