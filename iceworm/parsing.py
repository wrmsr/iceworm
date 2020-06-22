from omnibus import antlr
from omnibus import check
from omnibus._vendor import antlr4

from . import nodes as no
from ._antlr.SnowflakeSqlLexer import SnowflakeSqlLexer
from ._antlr.SnowflakeSqlParser import SnowflakeSqlParser
from ._antlr.SnowflakeSqlVisitor import SnowflakeSqlVisitor
from .quoting import unquote


class _ParseVisitor(SnowflakeSqlVisitor):

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is not None:
            check.none(nextResult)
            return aggregate
        else:
            check.none(aggregate)
            return nextResult

    def visitAliasedRelation(self, ctx: SnowflakeSqlParser.AliasedRelationContext):
        relation = self.visit(ctx.relation())
        alias = self.visit(ctx.identifier())
        return no.AliasedRelation(relation, alias)

    def visitAllSelectItem(self, ctx: SnowflakeSqlParser.AllSelectItemContext):
        return no.AllSelectItem()

    def visitArithValueExpression(self, ctx: SnowflakeSqlParser.ArithValueExpressionContext):
        left, right = [self.visit(e) for e in ctx.valueExpression()]
        op = no.BINARY_OP_MAP[ctx.op.getText().lower()]
        return no.BinaryExpr(left, op, right)

    def visitBaseSelect(self, ctx: SnowflakeSqlParser.BaseSelectContext):
        items = [self.visit(i) for i in ctx.selectItem()]
        relations = [self.visit(r) for r in ctx.relation()]
        set_quantifier = no.SET_QUANTIFIER_MAP[ctx.setQuantifier().getText().lower()] \
            if ctx.setQuantifier() is not None else None
        where = self.visit(ctx.where) if ctx.where is not None else None
        group_by = self.visit(ctx.groupBy()) if ctx.groupBy() else None
        order_by = [self.visit(s) for s in ctx.sortItem()] if ctx.sortItem() is not None else None
        return no.Select(
            items,
            relations,
            where,
            set_quantifier=set_quantifier,
            group_by=group_by,
            order_by=order_by,
        )

    def visitBinaryBooleanExpression(self, ctx: SnowflakeSqlParser.BinaryBooleanExpressionContext):
        left, right = [self.visit(e) for e in ctx.booleanExpression()]
        op = no.BINARY_OP_MAP[ctx.op.text.lower()]
        return no.BinaryExpr(left, op, right)

    def visitCaseItem(self, ctx: SnowflakeSqlParser.CaseItemContext):
        when, then = [self.visit(e) for e in ctx.expression()]
        return no.CaseItem(when, then)

    def visitCasePrimaryExpression(self, ctx: SnowflakeSqlParser.CasePrimaryExpressionContext):
        items = [self.visit(i) for i in ctx.caseItem()]
        default = self.visit(ctx.expression()) if ctx.expression() is not None else None
        return no.Case(items, default)

    def visitCastBooleanExpression(self, ctx: SnowflakeSqlParser.CastBooleanExpressionContext):
        value = self.visit(ctx.booleanExpression())
        type = self.visit(ctx.identifier())
        return no.Cast(value, type)

    def visitCmpPredicate(self, ctx: SnowflakeSqlParser.CmpPredicateContext):
        left = self.visit(ctx.value)
        op = no.BINARY_OP_MAP[ctx.cmpOp().getText().lower()]
        right = self.visit(ctx.valueExpression())
        return no.BinaryExpr(left, op, right)

    def visitCte(self, ctx: SnowflakeSqlParser.CteContext):
        name = self.visit(ctx.identifier())
        select = self.visit(ctx.select())
        return no.Cte(name, select)

    def visitCteSelect(self, ctx: SnowflakeSqlParser.CteSelectContext):
        ctes = [self.visit(c) for c in ctx.cte()]
        select = self.visit(ctx.unionSelect())
        return no.CteSelect(ctes, select) if ctes else select

    def visitExpressionSelectItem(self, ctx: SnowflakeSqlParser.ExpressionSelectItemContext):
        value = self.visit(ctx.expression())
        label = self.visit(ctx.identifier()) if ctx.identifier() is not None else None
        return no.ExprSelectItem(value, label)

    def visitFunctionCallPrimaryExpression(self, ctx:SnowflakeSqlParser.FunctionCallPrimaryExpressionContext):
        name = self.visit(ctx.identifier())
        args = [self.visit(a) for a in ctx.expression()]
        return no.FunctionCall(name, args)

    def visitGroupBy(self, ctx: SnowflakeSqlParser.GroupByContext):
        items = [self.visit(e) for e in ctx.expression()]
        return no.GroupBy(items)

    def visitIntegerNumber(self, ctx: SnowflakeSqlParser.IntegerNumberContext):
        return no.Integer(int(ctx.INTEGER_VALUE().getText()))

    def visitJoinRelation(self, ctx: SnowflakeSqlParser.JoinRelationContext):
        left = self.visit(ctx.left)
        ty = no.JOIN_TYPE_MAP[' '.join(c.getText().lower() for c in ctx.joinType().children)] \
            if ctx.joinType() is not None else no.JoinType.DEFAULT
        right = self.visit(ctx.right)
        condition = self.visit(ctx.cond) if ctx.cond is not None else None
        return no.Join(left, ty, right, condition)

    def visitNull(self, ctx: SnowflakeSqlParser.NullContext):
        return no.Null()

    def visitParenRelation(self, ctx: SnowflakeSqlParser.ParenRelationContext):
        return self.visit(ctx.relation())

    def visitPredicatedBooleanExpression(self, ctx: SnowflakeSqlParser.PredicatedBooleanExpressionContext):
        return self.visit(ctx.predicate()) if ctx.predicate() is not None else self.visit(ctx.valueExpression())

    def visitQualifiedName(self, ctx: SnowflakeSqlParser.QualifiedNameContext):
        parts = [self.visit(i) for i in ctx.identifier()]
        return no.QualifiedName(parts)

    def visitQuotedIdentifier(self, ctx: SnowflakeSqlParser.QuotedIdentifierContext):
        name = unquote(ctx.QUOTED_IDENTIFIER().getText(), '"')
        return no.Identifier(name)

    def visitSelectPrimaryExpression(self, ctx: SnowflakeSqlParser.SelectPrimaryExpressionContext):
        select = self.visit(ctx.select())
        return no.SelectExpr(select)

    def visitSelectRelation(self, ctx: SnowflakeSqlParser.SelectRelationContext):
        select = self.visit(ctx.select())
        return no.SelectRelation(select)

    def visitSortItem(self, ctx: SnowflakeSqlParser.SortItemContext):
        value = self.visit(ctx.expression())
        direction = no.DIRECTION_MAP[ctx.direction.text.lower()] if ctx.direction is not None else None
        return no.SortItem(value, direction)

    def visitString(self, ctx: SnowflakeSqlParser.StringContext):
        value = unquote(ctx.STRING().getText(), "'")
        return no.String(value)

    def visitTableRelation(self, ctx: SnowflakeSqlParser.TableRelationContext):
        return no.Table(self.visit(ctx.qualifiedName()))

    def visitUnaryValueExpression(self, ctx: SnowflakeSqlParser.UnaryValueExpressionContext):
        op = no.UNARY_OP_MAP[ctx.op.getText().lower()]
        value = self.visit(ctx.valueExpression())
        return no.UnaryExpr(op, value)

    def visitUnaryBooleanExpression(self, ctx: SnowflakeSqlParser.UnaryBooleanExpressionContext):
        op = no.UNARY_OP_MAP[ctx.op.text.lower()]
        value = self.visit(ctx.booleanExpression())
        return no.UnaryExpr(op, value)

    def visitUnionItem(self, ctx: SnowflakeSqlParser.UnionItemContext):
        right = self.visit(ctx.baseSelect())
        set_quantifier = no.SET_QUANTIFIER_MAP[ctx.setQuantifier().getText().lower()] \
            if ctx.setQuantifier() is not None else None
        return no.UnionItem(right, set_quantifier)

    def visitUnionSelect(self, ctx: SnowflakeSqlParser.UnionSelectContext):
        left = self.visit(ctx.baseSelect())
        items = [self.visit(i) for i in ctx.unionItem()]
        return no.UnionSelect(left, items) if items else left

    def visitUnquotedIdentifier(self, ctx: SnowflakeSqlParser.UnquotedIdentifierContext):
        return no.Identifier(ctx.getText())


def parse_statement(buf: str) -> no.Node:
    lexer = SnowflakeSqlLexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = SnowflakeSqlParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    node = visitor.visit(parser.singleStatement())
    return check.isinstance(node, no.Node)
