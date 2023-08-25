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
