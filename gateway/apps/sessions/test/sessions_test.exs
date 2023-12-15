defmodule SessionsTest do
  use ExUnit.Case
  doctest Sessions

  test "greets the world" do
    assert Derailed.Session.hello() == :world
  end
end
