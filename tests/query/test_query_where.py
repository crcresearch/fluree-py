# from fluree_py.query.where.operation import (
#     BindClause,
#     FilterClause,
#     OptionalClause,
#     UnionClause,
# )
# from fluree_py.query.where.variable import Var


# def test_query_where_operation_union():
#     s = Var("s")
#     assert str(s) == "?s"

#     email = Var("email")
#     assert str(email) == "?email"

#     union = UnionClause(
#         [{"@id": s, "schema:email": email}, {"@id": s, "ex:email": email}]
#     )
#     assert union.json() == [
#         "union",
#         {"@id": "?s", "schema:email": "?email"},
#         {"@id": "?s", "ex:email": "?email"},
#     ]


# def test_query_where_operation_filter():
#     age = Var("age")
#     condition = age > 45
#     assert condition.to_expr() == "(> ?age 45)"

#     condition = age < 50
#     assert condition.to_expr() == "(< ?age 50)"

#     filter = FilterClause([age > 45, age < 50])
#     assert filter.to_expr() == ["filter", "(> ?age 45)", "(< ?age 50)"]


# def test_query_where_operation_bind():
#     canVote = Var("canVote")
#     assert str(canVote) == "?canVote"

#     age = Var("age")
#     assert str(age) == "?age"

#     condition = age >= 18
#     assert condition.to_expr() == "(>= ?age 18)"

#     bind = BindClause(canVote, condition)
#     assert bind.to_expr() == ["bind", "?canVote", "(>= ?age 18)"]


# def test_query_where_operation_optional():
#     s = Var("s")
#     assert str(s) == "?s"

#     bestFriend = Var("bestFriend")
#     assert str(bestFriend) == "?bestFriend"

#     optional = OptionalClause([{"@id": s, "bestFriend": bestFriend}])
#     assert optional.to_expr() == ["optional", {"@id": "?s", "bestFriend": "?friend"}]
