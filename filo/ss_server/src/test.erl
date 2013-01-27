-module(test).
-export([start/0]).
-include("account.hrl").
start()->
    mnesia:create_schema([node()]),
    application:start(mnesia),
    mnesia:create_table(account,[{disc_copies,[node()]},
                                 {attributes,
                                        record_info(fields,account)}]).

