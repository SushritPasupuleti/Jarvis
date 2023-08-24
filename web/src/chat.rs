use gloo_console::log;
use gloo_timers::future::TimeoutFuture;
use leptos::*;

use crate::api;

async fn load_data(value: i32) -> i32 {
    // fake a one-second delay
    TimeoutFuture::new(1_000).await;
    value * 10
}

#[component]
pub fn Chat(cx: Scope) -> impl IntoView {
    let (value, set_value) = create_signal(cx, 0);
    let (count, set_count) = create_signal(cx, 0);
    let (question, set_question) = create_signal(cx, String::from(""));
    let (answer, set_answer) = create_signal(cx, String::from(""));

    let input_ref = create_node_ref::<leptos::html::Input>(cx);

    let answer_question = create_action(cx, move |question: &String| {
        let question = question.clone();
        let input = input_ref.get().expect("input to exist");

        log!("Input: {}", input.value());

        set_question.update(|question| *question = input.value());

        async move {
            let ans = api::get_answer(input.value()).await.unwrap();
            log!("Answer: {}", ans.clone());

            set_answer.update(|answer| *answer = ans.clone());

            ans
        }
    });

    view! {cx,
        <div class="w-full">
            <p
                class="text-gray-900 dark:text-gray-100 text-2md font-semibold mt-4"
            >
            {"Feel free to ask me anything!"}
            </p>
            <br />
            <input type="text"
                node_ref=input_ref
                height="100px"
                placeholder="Type your question here"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
            // <p
            //     class="text-gray-900 dark:text-gray-100"
            // >
            //     {"Question: "}
            //     {question}
            //     {count}
            // </p>
            <br />
            <p
                class="text-gray-900 dark:text-gray-100 text-2md font-semibold mt-4"
            >
                {"Answer: "}
                {answer}
            </p>
            <br />
            <hr 
                class="border-1 border-gray-500"
            />
            <br />
            <button on:click=move |_| {
                let question = question.get();

                log!("Question: {}", question.clone());
                answer_question.dispatch(question);
            }
            // disabled=input_ref.get().expect("input to exist").value().is_empty()
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
            >
                "Ask"
            </button>
            <br />
        </div>
    }
}
