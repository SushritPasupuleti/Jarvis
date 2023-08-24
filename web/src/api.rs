use reqwasm::http;
use gloo_console::log;

use crate::types::QuestionResult;

pub async fn get_answer(question: String) -> Result<String, reqwasm::Error> {

    log!("Answering Question: {}", question.clone());

    let url = format!("http://localhost:8000/chat/{}", question);
    let response = http::Request::get(&url).send().await?;
    let answer: QuestionResult = response.json().await?;

    Ok(answer.answer)
}
