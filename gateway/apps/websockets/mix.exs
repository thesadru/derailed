defmodule Derailed.WebSocket.MixProject do
  use Mix.Project

  def project do
    [
      app: :websockets,
      version: "0.1.0",
      build_path: "../../_build",
      config_path: "../../config/config.exs",
      deps_path: "../../deps",
      lockfile: "../../mix.lock",
      elixir: "~> 1.15",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {Derailed.WebSocket.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:cowboy, "~> 2.10"},
      {:jsonrs, "~> 0.3.1"},
      {:ex_json_schema, "~> 0.10.1"},
      {:postgrex, "~> 0.17.2"},
      {:gen_registry, "~> 1.3.0"},
      {:payloads, in_umbrella: true},
      {:tokenrs, in_umbrella: true},
      {:utils, in_umbrella: true},
      {:sessions, in_umbrella: true}
    ]
  end
end
