export default () => {
    return (
        <div className="flex bg-cheesy-black min-h-screen text-white font-primary">
            <form className="shadow-2xl shadow-silver-gray bg-cheesy-black flex flex-col justify-center text-center gap-6 m-auto rounded-3xl p-20">
                <section className="hover:blur-lg transition duration-1000">
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
                    <input className="outline-none bg-pepperoni-black outline-1 font-light outline rounded-lg p-2 text-lg text-white" size={30} placeholder="Email" minLength={5} maxLength={128} required />
                </section>
                <section>
                    <input className="outline-none bg-pepperoni-black outline-1 font-light outline rounded-lg p-2 text-lg text-white" size={30} placeholder="Password" minLength={8} maxLength={128} required />
                </section>
                <button className="text-lg bg-pepperoni-black rounded-2xl py-2">
                    I'm ready.
                </button>
            </form>
        </div>
    )
}