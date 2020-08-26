# flake8: noqa
# Generated from IceSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .IceSqlParser import IceSqlParser
else:
    from IceSqlParser import IceSqlParser

# This class defines a complete generic visitor for a parse tree produced by IceSqlParser.

class IceSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IceSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:IceSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#statement.
    def visitStatement(self, ctx:IceSqlParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#createTable.
    def visitCreateTable(self, ctx:IceSqlParser.CreateTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#colSpec.
    def visitColSpec(self, ctx:IceSqlParser.ColSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#insert.
    def visitInsert(self, ctx:IceSqlParser.InsertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#delete.
    def visitDelete(self, ctx:IceSqlParser.DeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#select.
    def visitSelect(self, ctx:IceSqlParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#cteSelect.
    def visitCteSelect(self, ctx:IceSqlParser.CteSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#cte.
    def visitCte(self, ctx:IceSqlParser.CteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#setSelect.
    def visitSetSelect(self, ctx:IceSqlParser.SetSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#setSelectItem.
    def visitSetSelectItem(self, ctx:IceSqlParser.SetSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#setSelectKind.
    def visitSetSelectKind(self, ctx:IceSqlParser.SetSelectKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#parenSelect.
    def visitParenSelect(self, ctx:IceSqlParser.ParenSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#primarySelect.
    def visitPrimarySelect(self, ctx:IceSqlParser.PrimarySelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#topN.
    def visitTopN(self, ctx:IceSqlParser.TopNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#allSelectItem.
    def visitAllSelectItem(self, ctx:IceSqlParser.AllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#identifierAllSelectItem.
    def visitIdentifierAllSelectItem(self, ctx:IceSqlParser.IdentifierAllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#expressionSelectItem.
    def visitExpressionSelectItem(self, ctx:IceSqlParser.ExpressionSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#expression.
    def visitExpression(self, ctx:IceSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#binaryBooleanExpression.
    def visitBinaryBooleanExpression(self, ctx:IceSqlParser.BinaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#predicatedBooleanExpression.
    def visitPredicatedBooleanExpression(self, ctx:IceSqlParser.PredicatedBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unaryBooleanExpression.
    def visitUnaryBooleanExpression(self, ctx:IceSqlParser.UnaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#cmpPredicate.
    def visitCmpPredicate(self, ctx:IceSqlParser.CmpPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#isNullPredicate.
    def visitIsNullPredicate(self, ctx:IceSqlParser.IsNullPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#betweenPredicate.
    def visitBetweenPredicate(self, ctx:IceSqlParser.BetweenPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#inListPredicate.
    def visitInListPredicate(self, ctx:IceSqlParser.InListPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#inSelectPredicate.
    def visitInSelectPredicate(self, ctx:IceSqlParser.InSelectPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#inJinjaPredicate.
    def visitInJinjaPredicate(self, ctx:IceSqlParser.InJinjaPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#likePredicate.
    def visitLikePredicate(self, ctx:IceSqlParser.LikePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#primaryValueExpression.
    def visitPrimaryValueExpression(self, ctx:IceSqlParser.PrimaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unaryValueExpression.
    def visitUnaryValueExpression(self, ctx:IceSqlParser.UnaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#traversalValueExpression.
    def visitTraversalValueExpression(self, ctx:IceSqlParser.TraversalValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#castValueExpression.
    def visitCastValueExpression(self, ctx:IceSqlParser.CastValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#arithValueExpression.
    def visitArithValueExpression(self, ctx:IceSqlParser.ArithValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#traversalKey.
    def visitTraversalKey(self, ctx:IceSqlParser.TraversalKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#functionCallExpression.
    def visitFunctionCallExpression(self, ctx:IceSqlParser.FunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#caseExpression.
    def visitCaseExpression(self, ctx:IceSqlParser.CaseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#intervalExpression.
    def visitIntervalExpression(self, ctx:IceSqlParser.IntervalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#selectExpression.
    def visitSelectExpression(self, ctx:IceSqlParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#parenExpression.
    def visitParenExpression(self, ctx:IceSqlParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#castCallExpression.
    def visitCastCallExpression(self, ctx:IceSqlParser.CastCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#dateExpression.
    def visitDateExpression(self, ctx:IceSqlParser.DateExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#extractExpression.
    def visitExtractExpression(self, ctx:IceSqlParser.ExtractExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#jinjaExpression.
    def visitJinjaExpression(self, ctx:IceSqlParser.JinjaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#simplePrimaryExpression.
    def visitSimplePrimaryExpression(self, ctx:IceSqlParser.SimplePrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#simpleExpression.
    def visitSimpleExpression(self, ctx:IceSqlParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#typeSpec.
    def visitTypeSpec(self, ctx:IceSqlParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#expressionFunctionCall.
    def visitExpressionFunctionCall(self, ctx:IceSqlParser.ExpressionFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#kwargFunctionCall.
    def visitKwargFunctionCall(self, ctx:IceSqlParser.KwargFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#nullsFunctionCall.
    def visitNullsFunctionCall(self, ctx:IceSqlParser.NullsFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#starFunctionCall.
    def visitStarFunctionCall(self, ctx:IceSqlParser.StarFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#kwarg.
    def visitKwarg(self, ctx:IceSqlParser.KwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#caseItem.
    def visitCaseItem(self, ctx:IceSqlParser.CaseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#over.
    def visitOver(self, ctx:IceSqlParser.OverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#numFrameBound.
    def visitNumFrameBound(self, ctx:IceSqlParser.NumFrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unboundedFrameBound.
    def visitUnboundedFrameBound(self, ctx:IceSqlParser.UnboundedFrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#currentRowFrameBound.
    def visitCurrentRowFrameBound(self, ctx:IceSqlParser.CurrentRowFrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#singleFrame.
    def visitSingleFrame(self, ctx:IceSqlParser.SingleFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#doubleFrame.
    def visitDoubleFrame(self, ctx:IceSqlParser.DoubleFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#sortItem.
    def visitSortItem(self, ctx:IceSqlParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unpivotRelation.
    def visitUnpivotRelation(self, ctx:IceSqlParser.UnpivotRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#functionCallRelation.
    def visitFunctionCallRelation(self, ctx:IceSqlParser.FunctionCallRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#jinjaRelation.
    def visitJinjaRelation(self, ctx:IceSqlParser.JinjaRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#aliasedRelation.
    def visitAliasedRelation(self, ctx:IceSqlParser.AliasedRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#lateralRelation.
    def visitLateralRelation(self, ctx:IceSqlParser.LateralRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:IceSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#pivotRelation.
    def visitPivotRelation(self, ctx:IceSqlParser.PivotRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#selectRelation.
    def visitSelectRelation(self, ctx:IceSqlParser.SelectRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#tableRelation.
    def visitTableRelation(self, ctx:IceSqlParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#parenRelation.
    def visitParenRelation(self, ctx:IceSqlParser.ParenRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#flatGrouping.
    def visitFlatGrouping(self, ctx:IceSqlParser.FlatGroupingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#setsGrouping.
    def visitSetsGrouping(self, ctx:IceSqlParser.SetsGroupingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#groupingSet.
    def visitGroupingSet(self, ctx:IceSqlParser.GroupingSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#qualifiedName.
    def visitQualifiedName(self, ctx:IceSqlParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#identifierList.
    def visitIdentifierList(self, ctx:IceSqlParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#identifier.
    def visitIdentifier(self, ctx:IceSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#quotedIdentifier.
    def visitQuotedIdentifier(self, ctx:IceSqlParser.QuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#integerNumber.
    def visitIntegerNumber(self, ctx:IceSqlParser.IntegerNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#decimalNumber.
    def visitDecimalNumber(self, ctx:IceSqlParser.DecimalNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#floatNumber.
    def visitFloatNumber(self, ctx:IceSqlParser.FloatNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#integer.
    def visitInteger(self, ctx:IceSqlParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#string.
    def visitString(self, ctx:IceSqlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#null.
    def visitNull(self, ctx:IceSqlParser.NullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#true.
    def visitTrue(self, ctx:IceSqlParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#false.
    def visitFalse(self, ctx:IceSqlParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#setQuantifier.
    def visitSetQuantifier(self, ctx:IceSqlParser.SetQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#joinType.
    def visitJoinType(self, ctx:IceSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#cmpOp.
    def visitCmpOp(self, ctx:IceSqlParser.CmpOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#arithOp.
    def visitArithOp(self, ctx:IceSqlParser.ArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unaryOp.
    def visitUnaryOp(self, ctx:IceSqlParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IceSqlParser#unquotedIdentifier.
    def visitUnquotedIdentifier(self, ctx:IceSqlParser.UnquotedIdentifierContext):
        return self.visitChildren(ctx)



del IceSqlParser
