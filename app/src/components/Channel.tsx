import { getState } from "../lib/state";
import { observer } from "mobx-react-lite"


export default observer(() => {
    const state = getState()

    return (
        <div className="bg-pepperoni-black w-full m-3.5 rounded-lg">
        </div>
    )
})