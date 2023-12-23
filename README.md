# Derailed

Welcome! This is Derailed, a project aiming for a more versatile, easy-to-use, and customizable Discord and Slack like experience.

At the moment, all you need to run Derailed is Node.js and Python.

## Deploying Derailed

### Docker

Two official versions of Derailed are available in this repository using Docker.
One version primarily for development of the API and Gateway services, and another for
a production deployment. We also provide a `docker-compose` system to easily deploy Derailed for its
first few months.

Derailed's production Docker versions utilize NGINX (API) and Envoy (Gateway "WebSocket" portion.)
The production version of the Gateway may not currently scale beyond a single instance/system,
and please do not attempt to as it would cause severe issues. I will work on this once we have to scale that much.

### API

To run the API, install Python (ideally `3.11`,) along with PDM.

After that, simply just run `pdm install` and run with gunicorn for production,
or `pdm run dev` to run a development version. (Gunicorn only works on UNIX systems.)

### Gateway

For now:

Just do the same steps as with the API, but instead in the `gateway` directory.

*In the future:*

In able to deploy the Gateway Services, you need to firstly install Elixir `1.15`, alongside Erlang `26` (the newest version of `26` ideally.)
