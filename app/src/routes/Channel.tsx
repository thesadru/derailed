import { getState } from "../lib/state";
import { observer } from "mobx-react-lite"
import { Navigate } from "@tanstack/react-router";
import Sidebar from "../components/Sidebar";

export default observer(() => {
    if (!localStorage.getItem("token")) {
        return <Navigate to="/login" />
    }

    const state = getState()

    return (
        <main>
            <Sidebar />
        </main>
    )
})