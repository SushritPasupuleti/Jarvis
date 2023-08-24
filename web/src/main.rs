mod api;
mod chat;
mod types;
// use api::get_answer;
// use gloo_net::http::Request;
// use yew::prelude::*;
// use log::info;
use gloo_console::log;
use leptos::*;
// use wasm_bindgen::JsValue;
use chat::Chat;

fn main() {
    mount_to_body(|cx| {
        view! { cx,
            <div
                class="bg-white dark:bg-slate-800 p-10"
                style="min-height: 100vh"
                >
                <div
                    class="bg-gray-200 dark:bg-slate-700 flex flex-col items-center justify-center py-10 px-10 rounded-lg shadow-xl ring-1 ring-slate-900/5 border border-gray-700"
                >
                    <h1
                        class="text-gray-900 dark:text-white text-2xl font-semibold"
                    >
                        { "J.A.R.V.I.S" }
                    </h1>
                    <br />
                    <Chat />
                    </div>
                </div>
        }
    })
}

// #[function_component]
// fn App() -> Html {
//     let counter = use_state(|| 0);
//
//     let question = types::Question {
//         question: "What is the meaning of life?".to_string(),
//     };
//
//     // let question_result = types::QuestionResult {
//     //     question: "What is the meaning of life?".to_string(),
//     //     answer: "42".to_string(),
//     // };
//
//     let question_result = use_state(String::new);
//
//     let message = types::Message {
//         message: "Hello, world!".to_string(),
//         sender: "J.A.R.V.I.S".to_string(),
//     };
//
//     let chat = types::Chat {
//         messages: vec![message],
//     };
//
//     let onclick = Callback::from(move |event: MouseEvent| {
//     // let onclick =  {
//     let question_res = question_result.clone();
//     // let onclick = {
//         // event.prevent_default();
//         log!("Question: {}", question.question.clone());
//         // let counter = counter.clone();
//
//         let question: String = question.question.clone();
//
//         let url = format!("http://localhost:8000/chat/{}", question);
//
//         log!("URL: {}", url.clone());
//
//
//         wasm_bindgen_futures::spawn_local(async move {
//             let res: types::QuestionResult = Request::get(&url)
//                 .send()
//                 .await
//                 .unwrap()
//                 .json()
//                 .await
//                 .unwrap();
//
//             log!("Response: {:?}", res.clone().answer);
//
//             let answer = res.clone().answer.to_string();
//
//             question_res.set(answer);
//
//             // question_result = res.json().await.unwrap();
//             // println!("Response: {:?}", res);
//
//             // assert_eq!(res.status(), 200);
//         }) // api::get_answer("question".to_string());
//
//         // move |_| {
//         //     let value = *counter + 1;
//         //     counter.set(value);
//         // }
//     });
//
//     html! {
//         <div
//             class={classes!("bg-white", "dark:bg-slate-800", "p-10")}
//             style="min-height: 100vh"
//         >
//             <div
//                 class={classes!("bg-gray-200", "dark:bg-slate-700", "flex", "flex-col", "items-center", "justify-center", "py-20", "px-10", "rounded-lg", "shadow-xl", "ring-1", "ring-slate-900/5", "border", "border-gray-700", )}
//             >
//                 <h1
//                     class={classes!("text-gray-900", "dark:text-white", "text-2xl", "font-semibold")}
//                 >
//                     { "J.A.R.V.I.S" }
//                 </h1>
//                     <br/>
//                     <p
//                         class={classes!("text-gray-900", "dark:text-white", "text-2md", "font-semibold")}
//                     >
//                         { "Welcome to the chat!
//     Type a message and press Enter to send." }
//                     </p>
//                     <br/>
//                 <button
//                     class={classes!("bg-blue-500", "hover:bg-blue-700", "text-white", "font-bold", "py-2", "px-4", "rounded-full")}
//                     onclick={onclick}
//                     //{onclick}
//                 >
//                     { "Send Message" }
//                 </button>
//                 <br/>
//                 <p
//                     class={classes!("text-gray-900", "dark:text-white", "text-2xl", "font-semibold")}
//                 >
//                     { *counter }
//                 </p>
//                 <br/>
//                 <p
//                     class={classes!("text-gray-900", "dark:text-white", "text-2xl", "font-semibold")}
//                 >
//                     {"Answer:"}
//                     { question_result.to_string() }
//                 </p>
//             </div>
//         </div>
//     }
// }
//
// fn main() {
//     yew::Renderer::<App>::new().render();
// }
