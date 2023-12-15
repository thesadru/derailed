defmodule WebsocketsTest do
  use ExUnit.Case
  doctest Websockets

  test "greets the world" do
    assert Derailed.WebSocket.hello() == :world
  end
end
