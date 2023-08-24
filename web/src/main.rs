use yew::prelude::*;

#[function_component]
fn App() -> Html {
    let counter = use_state(|| 0);
    let onclick = {
        let counter = counter.clone();
        move |_| {
            let value = *counter + 1;
            counter.set(value);
        }
    };

    html! {
        <div
            class={classes!("bg-white", "dark:bg-slate-800", "p-10")}
            style="min-height: 100vh"
        >
            <div
                class={classes!("bg-gray-200", "dark:bg-slate-700", "flex", "flex-col", "items-center", "justify-center", "py-20", "px-10", "rounded-lg", "shadow-xl", "ring-1", "ring-slate-900/5", "border", "border-gray-700", )}
            >
                <h1
                    class={classes!("text-gray-900", "dark:text-white", "text-2xl", "font-semibold")}
                >
                    { "J.A.R.V.I.S" }
                </h1>
                    <br/>
                    <p
                        class={classes!("text-gray-900", "dark:text-white", "text-2md", "font-semibold")}
                    >
                        { "Welcome to the chat!
    Type a message and press Enter to send." }
                    </p>
                    <br/>
                <button
                    class={classes!("bg-blue-500", "hover:bg-blue-700", "text-white", "font-bold", "py-2", "px-4", "rounded-full")}
                    {onclick}
                >
                    { "+1" }
                </button>
                <br/>
                <p
                    class={classes!("text-gray-900", "dark:text-white", "text-2xl", "font-semibold")}
                >
                    { *counter }
                </p>
            </div>
        </div>
    }
}

fn main() {
    yew::Renderer::<App>::new().render();
}
