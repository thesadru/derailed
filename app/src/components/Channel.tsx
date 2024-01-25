import { getState } from "../lib/state";
import { observer } from "mobx-react-lite"
import Message from "./Message";

interface ChannelProps {
    channelId: BigInt
}

export default observer((props: ChannelProps) => {
    const state = getState()

    return (
        <div className="bg-[#e8a7b2] w-full m-4 rounded-lg">
            <ul className="flex h-full flex-col-reverse overflow-y-scroll scroll-smooth snap-mandatory snap-y">
                <Message message={{id: BigInt(1), channel_id: BigInt(1), author: state.cache.user!, content: "I like poosay", timestamp: "2024-01-25T12:48:15+0000", edited_timestamp: null, referenced_message_id: null}} />
            </ul>
        </div>
    )
})