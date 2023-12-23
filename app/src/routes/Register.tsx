export default () => {
    return (
        <div className="flex bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 min-h-screen text-white font-primary">
            <form className="bg-gradient-to-bl from-gray-700 via-gray-900 to-black flex flex-col justify-center text-center gap-7 m-auto rounded-3xl p-20">
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
                    <input className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="text" size={30} placeholder="Invite Code" required />
                </section>
                <section>
                    <input className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="text" size={30} placeholder="Username" minLength={3} maxLength={32} required />
                </section>
                <section>
                    <input className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="email" size={30} placeholder="Email" minLength={5} maxLength={128} required />
                </section>
                <section>
                    <input className="outline-none placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 outline-1 font-light outline rounded-lg p-2 text-lg" type="password" size={30} placeholder="Password" minLength={8} maxLength={128} required />
                </section>
                <button className="text-xl placeholder-gray-900 text-gray-900 bg-gradient-to-bl bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200 rounded-2xl py-2 hover:scale-110 transition duration-700 ease-in-out">
                    I'm ready.
                </button>
            </form>
        </div>
    )
}