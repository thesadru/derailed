import { getState } from "../lib/state";
import { observer } from "mobx-react-lite"
import { Navigate } from "@tanstack/react-router";
import Sidebar from "../components/Sidebar";
import Channel from "../components/Channel";

export default observer(() => {
    if (!localStorage.getItem("token")) {
        return <Navigate to="/login" />
    }

    const state = getState()

    return (
        <main>
            {!state.loading ? (
                    <div className="bg-[#ffc0cb] flex">
                        <Sidebar channelId={BigInt(1)} />
                        <Channel channelId={BigInt(1)} />
                    </div>
            ) : (
                <div>
                    Loading...
                </div>
            )}
        </main>
    )
})