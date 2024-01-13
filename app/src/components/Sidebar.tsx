import { getState } from "../lib/state";
import { observer } from "mobx-react-lite"
import { Link } from "@tanstack/react-router";
import { Icon } from "@iconify/react"
import Channel from "../routes/Channel";


export default observer(() => {
    const state = getState()
    state.cache.channels.push({
        id: new BigInt(1),

    })
    return (
        <ul className="bg-pink-400">
            {state.cache.channels.map((channel, _idx, _arr) => {
                return (
                    <li className="flex flex-col gap-2 justify-center">
                        <Link to="/channels/@me">
                            <Icon icon="material-symbols:home-app-logo" />
                        </Link>
                        <Link params={{channelId: channel.id.toString()}} to={`/channels/$channelId`}>
                            <div className="flex">
                                <Icon icon="material-symbols:tag-rounded" />
                                <h5>{channel.name}</h5>
                            </div>
                        </Link>
                    </li>
                )
            })}
        </ul>
    )
})