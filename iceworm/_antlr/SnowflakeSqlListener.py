# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete listener for a parse tree produced by SnowflakeSqlParser.
class SnowflakeSqlListener(ParseTreeListener):

    # Enter a parse tree produced by SnowflakeSqlParser#singleStatement.
    def enterSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#singleStatement.
    def exitSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#statement.
    def enterStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#statement.
    def exitStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#select.
    def enterSelect(self, ctx:SnowflakeSqlParser.SelectContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#select.
    def exitSelect(self, ctx:SnowflakeSqlParser.SelectContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cteSelect.
    def enterCteSelect(self, ctx:SnowflakeSqlParser.CteSelectContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cteSelect.
    def exitCteSelect(self, ctx:SnowflakeSqlParser.CteSelectContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cte.
    def enterCte(self, ctx:SnowflakeSqlParser.CteContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cte.
    def exitCte(self, ctx:SnowflakeSqlParser.CteContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unionSelect.
    def enterUnionSelect(self, ctx:SnowflakeSqlParser.UnionSelectContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unionSelect.
    def exitUnionSelect(self, ctx:SnowflakeSqlParser.UnionSelectContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unionItem.
    def enterUnionItem(self, ctx:SnowflakeSqlParser.UnionItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unionItem.
    def exitUnionItem(self, ctx:SnowflakeSqlParser.UnionItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#primarySelect.
    def enterPrimarySelect(self, ctx:SnowflakeSqlParser.PrimarySelectContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#primarySelect.
    def exitPrimarySelect(self, ctx:SnowflakeSqlParser.PrimarySelectContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#topN.
    def enterTopN(self, ctx:SnowflakeSqlParser.TopNContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#topN.
    def exitTopN(self, ctx:SnowflakeSqlParser.TopNContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def enterAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def exitAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#identifierAllSelectItem.
    def enterIdentifierAllSelectItem(self, ctx:SnowflakeSqlParser.IdentifierAllSelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#identifierAllSelectItem.
    def exitIdentifierAllSelectItem(self, ctx:SnowflakeSqlParser.IdentifierAllSelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def enterExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def exitExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expression.
    def enterExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expression.
    def exitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def enterBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def exitBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#predicatedBooleanExpression.
    def enterPredicatedBooleanExpression(self, ctx:SnowflakeSqlParser.PredicatedBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#predicatedBooleanExpression.
    def exitPredicatedBooleanExpression(self, ctx:SnowflakeSqlParser.PredicatedBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def enterUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def exitUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cmpPredicate.
    def enterCmpPredicate(self, ctx:SnowflakeSqlParser.CmpPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cmpPredicate.
    def exitCmpPredicate(self, ctx:SnowflakeSqlParser.CmpPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#isNullPredicate.
    def enterIsNullPredicate(self, ctx:SnowflakeSqlParser.IsNullPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#isNullPredicate.
    def exitIsNullPredicate(self, ctx:SnowflakeSqlParser.IsNullPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#betweenPredicate.
    def enterBetweenPredicate(self, ctx:SnowflakeSqlParser.BetweenPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#betweenPredicate.
    def exitBetweenPredicate(self, ctx:SnowflakeSqlParser.BetweenPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#inListPredicate.
    def enterInListPredicate(self, ctx:SnowflakeSqlParser.InListPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#inListPredicate.
    def exitInListPredicate(self, ctx:SnowflakeSqlParser.InListPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#inSelectPredicate.
    def enterInSelectPredicate(self, ctx:SnowflakeSqlParser.InSelectPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#inSelectPredicate.
    def exitInSelectPredicate(self, ctx:SnowflakeSqlParser.InSelectPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#inJinjaPredicate.
    def enterInJinjaPredicate(self, ctx:SnowflakeSqlParser.InJinjaPredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#inJinjaPredicate.
    def exitInJinjaPredicate(self, ctx:SnowflakeSqlParser.InJinjaPredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#likePredicate.
    def enterLikePredicate(self, ctx:SnowflakeSqlParser.LikePredicateContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#likePredicate.
    def exitLikePredicate(self, ctx:SnowflakeSqlParser.LikePredicateContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#primaryValueExpression.
    def enterPrimaryValueExpression(self, ctx:SnowflakeSqlParser.PrimaryValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#primaryValueExpression.
    def exitPrimaryValueExpression(self, ctx:SnowflakeSqlParser.PrimaryValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unaryValueExpression.
    def enterUnaryValueExpression(self, ctx:SnowflakeSqlParser.UnaryValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unaryValueExpression.
    def exitUnaryValueExpression(self, ctx:SnowflakeSqlParser.UnaryValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#castValueExpression.
    def enterCastValueExpression(self, ctx:SnowflakeSqlParser.CastValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#castValueExpression.
    def exitCastValueExpression(self, ctx:SnowflakeSqlParser.CastValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#brackeetValueExpression.
    def enterBrackeetValueExpression(self, ctx:SnowflakeSqlParser.BrackeetValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#brackeetValueExpression.
    def exitBrackeetValueExpression(self, ctx:SnowflakeSqlParser.BrackeetValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#arithValueExpression.
    def enterArithValueExpression(self, ctx:SnowflakeSqlParser.ArithValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#arithValueExpression.
    def exitArithValueExpression(self, ctx:SnowflakeSqlParser.ArithValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#colonValueExpression.
    def enterColonValueExpression(self, ctx:SnowflakeSqlParser.ColonValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#colonValueExpression.
    def exitColonValueExpression(self, ctx:SnowflakeSqlParser.ColonValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#functionCallExpression.
    def enterFunctionCallExpression(self, ctx:SnowflakeSqlParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#functionCallExpression.
    def exitFunctionCallExpression(self, ctx:SnowflakeSqlParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#lastValueExpression.
    def enterLastValueExpression(self, ctx:SnowflakeSqlParser.LastValueExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#lastValueExpression.
    def exitLastValueExpression(self, ctx:SnowflakeSqlParser.LastValueExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#caseExpression.
    def enterCaseExpression(self, ctx:SnowflakeSqlParser.CaseExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#caseExpression.
    def exitCaseExpression(self, ctx:SnowflakeSqlParser.CaseExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#intervalExpression.
    def enterIntervalExpression(self, ctx:SnowflakeSqlParser.IntervalExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#intervalExpression.
    def exitIntervalExpression(self, ctx:SnowflakeSqlParser.IntervalExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#selectExpression.
    def enterSelectExpression(self, ctx:SnowflakeSqlParser.SelectExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#selectExpression.
    def exitSelectExpression(self, ctx:SnowflakeSqlParser.SelectExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#parenExpression.
    def enterParenExpression(self, ctx:SnowflakeSqlParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#parenExpression.
    def exitParenExpression(self, ctx:SnowflakeSqlParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#castCallExpression.
    def enterCastCallExpression(self, ctx:SnowflakeSqlParser.CastCallExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#castCallExpression.
    def exitCastCallExpression(self, ctx:SnowflakeSqlParser.CastCallExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#dateExpression.
    def enterDateExpression(self, ctx:SnowflakeSqlParser.DateExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#dateExpression.
    def exitDateExpression(self, ctx:SnowflakeSqlParser.DateExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#extractExpreession.
    def enterExtractExpreession(self, ctx:SnowflakeSqlParser.ExtractExpreessionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#extractExpreession.
    def exitExtractExpreession(self, ctx:SnowflakeSqlParser.ExtractExpreessionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#jinjaExpression.
    def enterJinjaExpression(self, ctx:SnowflakeSqlParser.JinjaExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#jinjaExpression.
    def exitJinjaExpression(self, ctx:SnowflakeSqlParser.JinjaExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#simplePrimaryExpression.
    def enterSimplePrimaryExpression(self, ctx:SnowflakeSqlParser.SimplePrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#simplePrimaryExpression.
    def exitSimplePrimaryExpression(self, ctx:SnowflakeSqlParser.SimplePrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#simpleExpression.
    def enterSimpleExpression(self, ctx:SnowflakeSqlParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#simpleExpression.
    def exitSimpleExpression(self, ctx:SnowflakeSqlParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#typeSpec.
    def enterTypeSpec(self, ctx:SnowflakeSqlParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#typeSpec.
    def exitTypeSpec(self, ctx:SnowflakeSqlParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expressionFunctionCall.
    def enterExpressionFunctionCall(self, ctx:SnowflakeSqlParser.ExpressionFunctionCallContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expressionFunctionCall.
    def exitExpressionFunctionCall(self, ctx:SnowflakeSqlParser.ExpressionFunctionCallContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#kwargFunctionCall.
    def enterKwargFunctionCall(self, ctx:SnowflakeSqlParser.KwargFunctionCallContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#kwargFunctionCall.
    def exitKwargFunctionCall(self, ctx:SnowflakeSqlParser.KwargFunctionCallContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#starFunctionCall.
    def enterStarFunctionCall(self, ctx:SnowflakeSqlParser.StarFunctionCallContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#starFunctionCall.
    def exitStarFunctionCall(self, ctx:SnowflakeSqlParser.StarFunctionCallContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#kwarg.
    def enterKwarg(self, ctx:SnowflakeSqlParser.KwargContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#kwarg.
    def exitKwarg(self, ctx:SnowflakeSqlParser.KwargContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#caseItem.
    def enterCaseItem(self, ctx:SnowflakeSqlParser.CaseItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#caseItem.
    def exitCaseItem(self, ctx:SnowflakeSqlParser.CaseItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#over.
    def enterOver(self, ctx:SnowflakeSqlParser.OverContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#over.
    def exitOver(self, ctx:SnowflakeSqlParser.OverContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cumulativeFrameMin.
    def enterCumulativeFrameMin(self, ctx:SnowflakeSqlParser.CumulativeFrameMinContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cumulativeFrameMin.
    def exitCumulativeFrameMin(self, ctx:SnowflakeSqlParser.CumulativeFrameMinContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cumulativeFrameMax.
    def enterCumulativeFrameMax(self, ctx:SnowflakeSqlParser.CumulativeFrameMaxContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cumulativeFrameMax.
    def exitCumulativeFrameMax(self, ctx:SnowflakeSqlParser.CumulativeFrameMaxContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#slidingFrameMin.
    def enterSlidingFrameMin(self, ctx:SnowflakeSqlParser.SlidingFrameMinContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#slidingFrameMin.
    def exitSlidingFrameMin(self, ctx:SnowflakeSqlParser.SlidingFrameMinContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#slidingFrameMax.
    def enterSlidingFrameMax(self, ctx:SnowflakeSqlParser.SlidingFrameMaxContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#slidingFrameMax.
    def exitSlidingFrameMax(self, ctx:SnowflakeSqlParser.SlidingFrameMaxContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unboundedFrame.
    def enterUnboundedFrame(self, ctx:SnowflakeSqlParser.UnboundedFrameContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unboundedFrame.
    def exitUnboundedFrame(self, ctx:SnowflakeSqlParser.UnboundedFrameContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cumulativeFrame.
    def enterCumulativeFrame(self, ctx:SnowflakeSqlParser.CumulativeFrameContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cumulativeFrame.
    def exitCumulativeFrame(self, ctx:SnowflakeSqlParser.CumulativeFrameContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#slidingFrame.
    def enterSlidingFrame(self, ctx:SnowflakeSqlParser.SlidingFrameContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#slidingFrame.
    def exitSlidingFrame(self, ctx:SnowflakeSqlParser.SlidingFrameContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#sortItem.
    def enterSortItem(self, ctx:SnowflakeSqlParser.SortItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#sortItem.
    def exitSortItem(self, ctx:SnowflakeSqlParser.SortItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unpivotRelation.
    def enterUnpivotRelation(self, ctx:SnowflakeSqlParser.UnpivotRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unpivotRelation.
    def exitUnpivotRelation(self, ctx:SnowflakeSqlParser.UnpivotRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#functionCallRelation.
    def enterFunctionCallRelation(self, ctx:SnowflakeSqlParser.FunctionCallRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#functionCallRelation.
    def exitFunctionCallRelation(self, ctx:SnowflakeSqlParser.FunctionCallRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#jinjaRelation.
    def enterJinjaRelation(self, ctx:SnowflakeSqlParser.JinjaRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#jinjaRelation.
    def exitJinjaRelation(self, ctx:SnowflakeSqlParser.JinjaRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#aliasedRelation.
    def enterAliasedRelation(self, ctx:SnowflakeSqlParser.AliasedRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#aliasedRelation.
    def exitAliasedRelation(self, ctx:SnowflakeSqlParser.AliasedRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#lateralRelation.
    def enterLateralRelation(self, ctx:SnowflakeSqlParser.LateralRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#lateralRelation.
    def exitLateralRelation(self, ctx:SnowflakeSqlParser.LateralRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#joinRelation.
    def enterJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#joinRelation.
    def exitJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#pivotRelation.
    def enterPivotRelation(self, ctx:SnowflakeSqlParser.PivotRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#pivotRelation.
    def exitPivotRelation(self, ctx:SnowflakeSqlParser.PivotRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#selectRelation.
    def enterSelectRelation(self, ctx:SnowflakeSqlParser.SelectRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#selectRelation.
    def exitSelectRelation(self, ctx:SnowflakeSqlParser.SelectRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#tableRelation.
    def enterTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#tableRelation.
    def exitTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#parenRelation.
    def enterParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#parenRelation.
    def exitParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#groupBy.
    def enterGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#groupBy.
    def exitGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#qualifiedName.
    def enterQualifiedName(self, ctx:SnowflakeSqlParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#qualifiedName.
    def exitQualifiedName(self, ctx:SnowflakeSqlParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#identifierList.
    def enterIdentifierList(self, ctx:SnowflakeSqlParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#identifierList.
    def exitIdentifierList(self, ctx:SnowflakeSqlParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#identifier.
    def enterIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#identifier.
    def exitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#integerNumber.
    def enterIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def exitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#decimalNumber.
    def enterDecimalNumber(self, ctx:SnowflakeSqlParser.DecimalNumberContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#decimalNumber.
    def exitDecimalNumber(self, ctx:SnowflakeSqlParser.DecimalNumberContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#floatNumber.
    def enterFloatNumber(self, ctx:SnowflakeSqlParser.FloatNumberContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#floatNumber.
    def exitFloatNumber(self, ctx:SnowflakeSqlParser.FloatNumberContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#string.
    def enterString(self, ctx:SnowflakeSqlParser.StringContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#string.
    def exitString(self, ctx:SnowflakeSqlParser.StringContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#null.
    def enterNull(self, ctx:SnowflakeSqlParser.NullContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#null.
    def exitNull(self, ctx:SnowflakeSqlParser.NullContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#true.
    def enterTrue(self, ctx:SnowflakeSqlParser.TrueContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#true.
    def exitTrue(self, ctx:SnowflakeSqlParser.TrueContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#false.
    def enterFalse(self, ctx:SnowflakeSqlParser.FalseContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#false.
    def exitFalse(self, ctx:SnowflakeSqlParser.FalseContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#setQuantifier.
    def enterSetQuantifier(self, ctx:SnowflakeSqlParser.SetQuantifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#setQuantifier.
    def exitSetQuantifier(self, ctx:SnowflakeSqlParser.SetQuantifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#joinType.
    def enterJoinType(self, ctx:SnowflakeSqlParser.JoinTypeContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#joinType.
    def exitJoinType(self, ctx:SnowflakeSqlParser.JoinTypeContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#cmpOp.
    def enterCmpOp(self, ctx:SnowflakeSqlParser.CmpOpContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#cmpOp.
    def exitCmpOp(self, ctx:SnowflakeSqlParser.CmpOpContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#arithOp.
    def enterArithOp(self, ctx:SnowflakeSqlParser.ArithOpContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#arithOp.
    def exitArithOp(self, ctx:SnowflakeSqlParser.ArithOpContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unaryOp.
    def enterUnaryOp(self, ctx:SnowflakeSqlParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unaryOp.
    def exitUnaryOp(self, ctx:SnowflakeSqlParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        pass



del SnowflakeSqlParser
