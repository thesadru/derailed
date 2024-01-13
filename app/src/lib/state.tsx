import { HTTPClient, DerailedWebSocket, User, Relationship, Channel, Settings } from "derailed.js";
import {makeAutoObservable} from "mobx"

interface Ready {
    user: User,
    relationships: Relationship[],
    channels: Channel[],
    settings: Settings
}

class Cache {
    public relationships: Relationship[] = []
    public channels: Channel[] = []
    public user: User | null = null
    public settings: Settings | null = null
}

export class State {
    public http: HTTPClient
    public ws: DerailedWebSocket
    public cache: Cache = new Cache()

    constructor(token: string) {
        makeAutoObservable(this)

        this.http = new HTTPClient(token)
        this.ws = new DerailedWebSocket(token)
        this.ws.emitter.on("READY", this.onReady, this)
        this.ws.connect()
    }

    // event-related functions
    onReady(data: Ready) {
        this.cache.user = data.user
        this.cache.settings = data.settings
        this.cache.channels = data.channels
        this.cache.relationships = data.relationships
    }
}


export function getState(): State {
    var state: State = (window as any)["state"]

    if (state === undefined) {
        state = new State(localStorage.getItem("token")!);
        (window as any)["state"] = state
    }

    return state
}
