import { DerailedWebSocket } from "./gateway"
import { HTTPClient } from "./http"

export class Client {
    public http: HTTPClient
    public gateway: DerailedWebSocket

    private token: string

    constructor(token: string) {
        this.token = token
        this.http = new HTTPClient(token)
        this.gateway = new DerailedWebSocket(token)
    }
}