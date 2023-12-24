import { FormEvent } from "react"
import JSON from "json-bigint"

export default () => {
    let errors: string[] = []
    var currentlyInvoking = false

    async function onInvoke(event: FormEvent) {
        event.preventDefault()

        if (currentlyInvoking) {
            return
        }

        currentlyInvoking = true

        // @ts-ignore
        const data = new FormData(event.target)

        const response = await fetch(
            import.meta.env.VITE_API_URL + "/register",
            {
                mode: "cors",
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    invite_code: data.get("invite_code"),
                    email: data.get("email"),
                    password: data.get("password"),
                    username: data.get("username")
                })
            }
        )

        if (response.status !== 201) {
            const respData = await response.json()
            console.error(respData)
            errors.push(respData.message)
        }

        currentlyInvoking = false
    }

    return (
        <div className="flex bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 min-h-screen text-white font-primary">
            <form onSubmit={onInvoke} className="bg-gradient-to-bl from-gray-700 via-gray-900 to-black flex flex-col justify-center text-center gap-7 m-auto rounded-3xl p-20">
                <section>
                    <h1 className="font-light text-3xl">
                        It's time for something new.<br/>Something innovative.<br/>Something Derailed.
                    </h1>
                    <i className="text-[#007aff] font-extralight">
                        <a href="/login">
                            Trying to login instead?
                        </a>
                    </i>
                    </section>
                <section>
                    <input id="invite_code" name="invite_code" className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="text" size={30} placeholder="Invite Code" maxLength={100} required />
                </section>
                <section>
                    <input id="username" name="username" className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="text" size={30} placeholder="Username" minLength={3} maxLength={32} required autoComplete="username" />
                </section>
                <section>
                    <input id="email" name="email" className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="email" size={30} placeholder="Email" minLength={5} maxLength={128} required autoComplete="email" />
                </section>
                <section>
                    <input id="password" name="password" className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="password" size={30} placeholder="Password" minLength={8} maxLength={128} required autoComplete="current-password" />
                </section>
                <button type="submit" className="text-xl placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 rounded-2xl py-2 hover:scale-110 transition duration-700 ease-in-out">
                    Let's start
                </button>
                <ul className="text-red-600 font-bold">
                    {errors.map(
                        (v, idx, _arr) => {
                            return (<li>
                                <p key={idx}>
                                    {v}
                                </p>
                            </li>)
                        }
                    )}
                </ul>
            </form>
        </div>
    )
}