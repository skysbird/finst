-module(user_func).
-author('skysbird@gmail.com').
-export([add_user/1,remove_user/1,modify_user/1,get_user/1]).
-include("account.hrl").



record_to_proplist(#account{} = Rec) ->
  lists:zipwith(fun(X,Y)->
                {list_to_binary(atom_to_list(X)),Y}
                end
        ,record_info(fields, account),tl(tuple_to_list(Rec))).

add_user(User)->
    Save = fun()->
            mnesia:write(User)
        end,
    mnesia:transaction(Save),
    ok.

remove_user(User)->
    Save = fun()->
            mnesia:delete({account,User#account.username})
     end,
    mnesia:transaction(Save),
    ok.

modify_user(User1)->
    F = fun() ->  
        User = #account{username = User1#account.username, email='_',passwd='_'},  
        io:format("to search ~p",[User]),
        case mnesia:select(account, [{User, [], ['$_']}]) of
            [Result]->
                Result2 = Result#account{email= User1#account.email},
                io:format("~p",[Result2]),
                mnesia:write(Result2);
            _->
                io:format("not found"),
                ok
        end
      end,  
    {atomic,_Result1} = mnesia:transaction(F),
    ok.

get_user(Username)->
    F = fun() ->  
        User = #account{username = Username, email='_',passwd='_'},  
        mnesia:select(account, [{User, [], ['$_']}])  
      end,  
    {atomic,Result} = mnesia:transaction(F),
    case Result of
        [Result1] ->
            io:format("~p",[Result1]),
            RP = {struct,record_to_proplist(Result1)},
            RP;
        _->
            {error,"no data"}
    end.

