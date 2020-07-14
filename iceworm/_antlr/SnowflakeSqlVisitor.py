# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete generic visitor for a parse tree produced by SnowflakeSqlParser.

class SnowflakeSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SnowflakeSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#statement.
    def visitStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#select.
    def visitSelect(self, ctx:SnowflakeSqlParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cteSelect.
    def visitCteSelect(self, ctx:SnowflakeSqlParser.CteSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cte.
    def visitCte(self, ctx:SnowflakeSqlParser.CteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unionSelect.
    def visitUnionSelect(self, ctx:SnowflakeSqlParser.UnionSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unionItem.
    def visitUnionItem(self, ctx:SnowflakeSqlParser.UnionItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#primarySelect.
    def visitPrimarySelect(self, ctx:SnowflakeSqlParser.PrimarySelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#topN.
    def visitTopN(self, ctx:SnowflakeSqlParser.TopNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def visitAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#identifierAllSelectItem.
    def visitIdentifierAllSelectItem(self, ctx:SnowflakeSqlParser.IdentifierAllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def visitExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expression.
    def visitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def visitBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#predicatedBooleanExpression.
    def visitPredicatedBooleanExpression(self, ctx:SnowflakeSqlParser.PredicatedBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def visitUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cmpPredicate.
    def visitCmpPredicate(self, ctx:SnowflakeSqlParser.CmpPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#isNullPredicate.
    def visitIsNullPredicate(self, ctx:SnowflakeSqlParser.IsNullPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#inListPredicate.
    def visitInListPredicate(self, ctx:SnowflakeSqlParser.InListPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#inSelectPredicate.
    def visitInSelectPredicate(self, ctx:SnowflakeSqlParser.InSelectPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#inJinjaPredicate.
    def visitInJinjaPredicate(self, ctx:SnowflakeSqlParser.InJinjaPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#likePredicate.
    def visitLikePredicate(self, ctx:SnowflakeSqlParser.LikePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#ilikePredicate.
    def visitIlikePredicate(self, ctx:SnowflakeSqlParser.IlikePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#primaryValueExpression.
    def visitPrimaryValueExpression(self, ctx:SnowflakeSqlParser.PrimaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryValueExpression.
    def visitUnaryValueExpression(self, ctx:SnowflakeSqlParser.UnaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#castValueExpression.
    def visitCastValueExpression(self, ctx:SnowflakeSqlParser.CastValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#arithValueExpression.
    def visitArithValueExpression(self, ctx:SnowflakeSqlParser.ArithValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#functionCallExpression.
    def visitFunctionCallExpression(self, ctx:SnowflakeSqlParser.FunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#caseExpression.
    def visitCaseExpression(self, ctx:SnowflakeSqlParser.CaseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#intervalExpression.
    def visitIntervalExpression(self, ctx:SnowflakeSqlParser.IntervalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#selectExpression.
    def visitSelectExpression(self, ctx:SnowflakeSqlParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#parenExpression.
    def visitParenExpression(self, ctx:SnowflakeSqlParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#castCallExpression.
    def visitCastCallExpression(self, ctx:SnowflakeSqlParser.CastCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#jinjaExpression.
    def visitJinjaExpression(self, ctx:SnowflakeSqlParser.JinjaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#simplePrimaryExpression.
    def visitSimplePrimaryExpression(self, ctx:SnowflakeSqlParser.SimplePrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#simpleExpression.
    def visitSimpleExpression(self, ctx:SnowflakeSqlParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#typeSpec.
    def visitTypeSpec(self, ctx:SnowflakeSqlParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expressionFunctionCall.
    def visitExpressionFunctionCall(self, ctx:SnowflakeSqlParser.ExpressionFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#kwargFunctionCall.
    def visitKwargFunctionCall(self, ctx:SnowflakeSqlParser.KwargFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#starFunctionCall.
    def visitStarFunctionCall(self, ctx:SnowflakeSqlParser.StarFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#kwarg.
    def visitKwarg(self, ctx:SnowflakeSqlParser.KwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#caseItem.
    def visitCaseItem(self, ctx:SnowflakeSqlParser.CaseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#over.
    def visitOver(self, ctx:SnowflakeSqlParser.OverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cumulativeFrameMin.
    def visitCumulativeFrameMin(self, ctx:SnowflakeSqlParser.CumulativeFrameMinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cumulativeFrameMax.
    def visitCumulativeFrameMax(self, ctx:SnowflakeSqlParser.CumulativeFrameMaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#slidingFrameMin.
    def visitSlidingFrameMin(self, ctx:SnowflakeSqlParser.SlidingFrameMinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#slidingFrameMax.
    def visitSlidingFrameMax(self, ctx:SnowflakeSqlParser.SlidingFrameMaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unboundedFrame.
    def visitUnboundedFrame(self, ctx:SnowflakeSqlParser.UnboundedFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cumulativeFrame.
    def visitCumulativeFrame(self, ctx:SnowflakeSqlParser.CumulativeFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#slidingFrame.
    def visitSlidingFrame(self, ctx:SnowflakeSqlParser.SlidingFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#sortItem.
    def visitSortItem(self, ctx:SnowflakeSqlParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unpivotRelation.
    def visitUnpivotRelation(self, ctx:SnowflakeSqlParser.UnpivotRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#functionCallRelation.
    def visitFunctionCallRelation(self, ctx:SnowflakeSqlParser.FunctionCallRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#jinjaRelation.
    def visitJinjaRelation(self, ctx:SnowflakeSqlParser.JinjaRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#aliasedRelation.
    def visitAliasedRelation(self, ctx:SnowflakeSqlParser.AliasedRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#lateralRelation.
    def visitLateralRelation(self, ctx:SnowflakeSqlParser.LateralRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#pivotRelation.
    def visitPivotRelation(self, ctx:SnowflakeSqlParser.PivotRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#selectRelation.
    def visitSelectRelation(self, ctx:SnowflakeSqlParser.SelectRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#tableRelation.
    def visitTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#parenRelation.
    def visitParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#groupBy.
    def visitGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#qualifiedName.
    def visitQualifiedName(self, ctx:SnowflakeSqlParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#identifierList.
    def visitIdentifierList(self, ctx:SnowflakeSqlParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#identifier.
    def visitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def visitQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def visitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#decimalNumber.
    def visitDecimalNumber(self, ctx:SnowflakeSqlParser.DecimalNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#floatNumber.
    def visitFloatNumber(self, ctx:SnowflakeSqlParser.FloatNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#string.
    def visitString(self, ctx:SnowflakeSqlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#null.
    def visitNull(self, ctx:SnowflakeSqlParser.NullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#true.
    def visitTrue(self, ctx:SnowflakeSqlParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#false.
    def visitFalse(self, ctx:SnowflakeSqlParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#setQuantifier.
    def visitSetQuantifier(self, ctx:SnowflakeSqlParser.SetQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#joinType.
    def visitJoinType(self, ctx:SnowflakeSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cmpOp.
    def visitCmpOp(self, ctx:SnowflakeSqlParser.CmpOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#arithOp.
    def visitArithOp(self, ctx:SnowflakeSqlParser.ArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryOp.
    def visitUnaryOp(self, ctx:SnowflakeSqlParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def visitUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        return self.visitChildren(ctx)



del SnowflakeSqlParser
