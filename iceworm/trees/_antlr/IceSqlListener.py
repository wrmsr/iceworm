# flake8: noqa
# Generated from IceSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .IceSqlParser import IceSqlParser
else:
    from IceSqlParser import IceSqlParser

# This class defines a complete listener for a parse tree produced by IceSqlParser.
class IceSqlListener(ParseTreeListener):

    # Enter a parse tree produced by IceSqlParser#singleStatement.
    def enterSingleStatement(self, ctx:IceSqlParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by IceSqlParser#singleStatement.
    def exitSingleStatement(self, ctx:IceSqlParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by IceSqlParser#statement.
    def enterStatement(self, ctx:IceSqlParser.StatementContext):
        pass

    # Exit a parse tree produced by IceSqlParser#statement.
    def exitStatement(self, ctx:IceSqlParser.StatementContext):
        pass


    # Enter a parse tree produced by IceSqlParser#createTable.
    def enterCreateTable(self, ctx:IceSqlParser.CreateTableContext):
        pass

    # Exit a parse tree produced by IceSqlParser#createTable.
    def exitCreateTable(self, ctx:IceSqlParser.CreateTableContext):
        pass


    # Enter a parse tree produced by IceSqlParser#colSpec.
    def enterColSpec(self, ctx:IceSqlParser.ColSpecContext):
        pass

    # Exit a parse tree produced by IceSqlParser#colSpec.
    def exitColSpec(self, ctx:IceSqlParser.ColSpecContext):
        pass


    # Enter a parse tree produced by IceSqlParser#insert.
    def enterInsert(self, ctx:IceSqlParser.InsertContext):
        pass

    # Exit a parse tree produced by IceSqlParser#insert.
    def exitInsert(self, ctx:IceSqlParser.InsertContext):
        pass


    # Enter a parse tree produced by IceSqlParser#delete.
    def enterDelete(self, ctx:IceSqlParser.DeleteContext):
        pass

    # Exit a parse tree produced by IceSqlParser#delete.
    def exitDelete(self, ctx:IceSqlParser.DeleteContext):
        pass


    # Enter a parse tree produced by IceSqlParser#select.
    def enterSelect(self, ctx:IceSqlParser.SelectContext):
        pass

    # Exit a parse tree produced by IceSqlParser#select.
    def exitSelect(self, ctx:IceSqlParser.SelectContext):
        pass


    # Enter a parse tree produced by IceSqlParser#cteSelect.
    def enterCteSelect(self, ctx:IceSqlParser.CteSelectContext):
        pass

    # Exit a parse tree produced by IceSqlParser#cteSelect.
    def exitCteSelect(self, ctx:IceSqlParser.CteSelectContext):
        pass


    # Enter a parse tree produced by IceSqlParser#cte.
    def enterCte(self, ctx:IceSqlParser.CteContext):
        pass

    # Exit a parse tree produced by IceSqlParser#cte.
    def exitCte(self, ctx:IceSqlParser.CteContext):
        pass


    # Enter a parse tree produced by IceSqlParser#setSelect.
    def enterSetSelect(self, ctx:IceSqlParser.SetSelectContext):
        pass

    # Exit a parse tree produced by IceSqlParser#setSelect.
    def exitSetSelect(self, ctx:IceSqlParser.SetSelectContext):
        pass


    # Enter a parse tree produced by IceSqlParser#setSelectItem.
    def enterSetSelectItem(self, ctx:IceSqlParser.SetSelectItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#setSelectItem.
    def exitSetSelectItem(self, ctx:IceSqlParser.SetSelectItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#setSelectKind.
    def enterSetSelectKind(self, ctx:IceSqlParser.SetSelectKindContext):
        pass

    # Exit a parse tree produced by IceSqlParser#setSelectKind.
    def exitSetSelectKind(self, ctx:IceSqlParser.SetSelectKindContext):
        pass


    # Enter a parse tree produced by IceSqlParser#parenSelect.
    def enterParenSelect(self, ctx:IceSqlParser.ParenSelectContext):
        pass

    # Exit a parse tree produced by IceSqlParser#parenSelect.
    def exitParenSelect(self, ctx:IceSqlParser.ParenSelectContext):
        pass


    # Enter a parse tree produced by IceSqlParser#primarySelect.
    def enterPrimarySelect(self, ctx:IceSqlParser.PrimarySelectContext):
        pass

    # Exit a parse tree produced by IceSqlParser#primarySelect.
    def exitPrimarySelect(self, ctx:IceSqlParser.PrimarySelectContext):
        pass


    # Enter a parse tree produced by IceSqlParser#topN.
    def enterTopN(self, ctx:IceSqlParser.TopNContext):
        pass

    # Exit a parse tree produced by IceSqlParser#topN.
    def exitTopN(self, ctx:IceSqlParser.TopNContext):
        pass


    # Enter a parse tree produced by IceSqlParser#allSelectItem.
    def enterAllSelectItem(self, ctx:IceSqlParser.AllSelectItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#allSelectItem.
    def exitAllSelectItem(self, ctx:IceSqlParser.AllSelectItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#identifierAllSelectItem.
    def enterIdentifierAllSelectItem(self, ctx:IceSqlParser.IdentifierAllSelectItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#identifierAllSelectItem.
    def exitIdentifierAllSelectItem(self, ctx:IceSqlParser.IdentifierAllSelectItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#expressionSelectItem.
    def enterExpressionSelectItem(self, ctx:IceSqlParser.ExpressionSelectItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#expressionSelectItem.
    def exitExpressionSelectItem(self, ctx:IceSqlParser.ExpressionSelectItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#expression.
    def enterExpression(self, ctx:IceSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#expression.
    def exitExpression(self, ctx:IceSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#binaryBooleanExpression.
    def enterBinaryBooleanExpression(self, ctx:IceSqlParser.BinaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#binaryBooleanExpression.
    def exitBinaryBooleanExpression(self, ctx:IceSqlParser.BinaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#predicatedBooleanExpression.
    def enterPredicatedBooleanExpression(self, ctx:IceSqlParser.PredicatedBooleanExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#predicatedBooleanExpression.
    def exitPredicatedBooleanExpression(self, ctx:IceSqlParser.PredicatedBooleanExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unaryBooleanExpression.
    def enterUnaryBooleanExpression(self, ctx:IceSqlParser.UnaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unaryBooleanExpression.
    def exitUnaryBooleanExpression(self, ctx:IceSqlParser.UnaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#cmpPredicate.
    def enterCmpPredicate(self, ctx:IceSqlParser.CmpPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#cmpPredicate.
    def exitCmpPredicate(self, ctx:IceSqlParser.CmpPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#isNullPredicate.
    def enterIsNullPredicate(self, ctx:IceSqlParser.IsNullPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#isNullPredicate.
    def exitIsNullPredicate(self, ctx:IceSqlParser.IsNullPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#betweenPredicate.
    def enterBetweenPredicate(self, ctx:IceSqlParser.BetweenPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#betweenPredicate.
    def exitBetweenPredicate(self, ctx:IceSqlParser.BetweenPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#inListPredicate.
    def enterInListPredicate(self, ctx:IceSqlParser.InListPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#inListPredicate.
    def exitInListPredicate(self, ctx:IceSqlParser.InListPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#inSelectPredicate.
    def enterInSelectPredicate(self, ctx:IceSqlParser.InSelectPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#inSelectPredicate.
    def exitInSelectPredicate(self, ctx:IceSqlParser.InSelectPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#inJinjaPredicate.
    def enterInJinjaPredicate(self, ctx:IceSqlParser.InJinjaPredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#inJinjaPredicate.
    def exitInJinjaPredicate(self, ctx:IceSqlParser.InJinjaPredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#likePredicate.
    def enterLikePredicate(self, ctx:IceSqlParser.LikePredicateContext):
        pass

    # Exit a parse tree produced by IceSqlParser#likePredicate.
    def exitLikePredicate(self, ctx:IceSqlParser.LikePredicateContext):
        pass


    # Enter a parse tree produced by IceSqlParser#primaryValueExpression.
    def enterPrimaryValueExpression(self, ctx:IceSqlParser.PrimaryValueExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#primaryValueExpression.
    def exitPrimaryValueExpression(self, ctx:IceSqlParser.PrimaryValueExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unaryValueExpression.
    def enterUnaryValueExpression(self, ctx:IceSqlParser.UnaryValueExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unaryValueExpression.
    def exitUnaryValueExpression(self, ctx:IceSqlParser.UnaryValueExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#traversalValueExpression.
    def enterTraversalValueExpression(self, ctx:IceSqlParser.TraversalValueExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#traversalValueExpression.
    def exitTraversalValueExpression(self, ctx:IceSqlParser.TraversalValueExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#castValueExpression.
    def enterCastValueExpression(self, ctx:IceSqlParser.CastValueExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#castValueExpression.
    def exitCastValueExpression(self, ctx:IceSqlParser.CastValueExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#arithValueExpression.
    def enterArithValueExpression(self, ctx:IceSqlParser.ArithValueExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#arithValueExpression.
    def exitArithValueExpression(self, ctx:IceSqlParser.ArithValueExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#traversalKey.
    def enterTraversalKey(self, ctx:IceSqlParser.TraversalKeyContext):
        pass

    # Exit a parse tree produced by IceSqlParser#traversalKey.
    def exitTraversalKey(self, ctx:IceSqlParser.TraversalKeyContext):
        pass


    # Enter a parse tree produced by IceSqlParser#functionCallExpression.
    def enterFunctionCallExpression(self, ctx:IceSqlParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#functionCallExpression.
    def exitFunctionCallExpression(self, ctx:IceSqlParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#caseExpression.
    def enterCaseExpression(self, ctx:IceSqlParser.CaseExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#caseExpression.
    def exitCaseExpression(self, ctx:IceSqlParser.CaseExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#intervalExpression.
    def enterIntervalExpression(self, ctx:IceSqlParser.IntervalExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#intervalExpression.
    def exitIntervalExpression(self, ctx:IceSqlParser.IntervalExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#selectExpression.
    def enterSelectExpression(self, ctx:IceSqlParser.SelectExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#selectExpression.
    def exitSelectExpression(self, ctx:IceSqlParser.SelectExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#parenExpression.
    def enterParenExpression(self, ctx:IceSqlParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#parenExpression.
    def exitParenExpression(self, ctx:IceSqlParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#castCallExpression.
    def enterCastCallExpression(self, ctx:IceSqlParser.CastCallExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#castCallExpression.
    def exitCastCallExpression(self, ctx:IceSqlParser.CastCallExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#dateExpression.
    def enterDateExpression(self, ctx:IceSqlParser.DateExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#dateExpression.
    def exitDateExpression(self, ctx:IceSqlParser.DateExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#extractExpression.
    def enterExtractExpression(self, ctx:IceSqlParser.ExtractExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#extractExpression.
    def exitExtractExpression(self, ctx:IceSqlParser.ExtractExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#jinjaExpression.
    def enterJinjaExpression(self, ctx:IceSqlParser.JinjaExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#jinjaExpression.
    def exitJinjaExpression(self, ctx:IceSqlParser.JinjaExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#simplePrimaryExpression.
    def enterSimplePrimaryExpression(self, ctx:IceSqlParser.SimplePrimaryExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#simplePrimaryExpression.
    def exitSimplePrimaryExpression(self, ctx:IceSqlParser.SimplePrimaryExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#simpleExpression.
    def enterSimpleExpression(self, ctx:IceSqlParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by IceSqlParser#simpleExpression.
    def exitSimpleExpression(self, ctx:IceSqlParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by IceSqlParser#typeSpec.
    def enterTypeSpec(self, ctx:IceSqlParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by IceSqlParser#typeSpec.
    def exitTypeSpec(self, ctx:IceSqlParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by IceSqlParser#expressionFunctionCall.
    def enterExpressionFunctionCall(self, ctx:IceSqlParser.ExpressionFunctionCallContext):
        pass

    # Exit a parse tree produced by IceSqlParser#expressionFunctionCall.
    def exitExpressionFunctionCall(self, ctx:IceSqlParser.ExpressionFunctionCallContext):
        pass


    # Enter a parse tree produced by IceSqlParser#kwargFunctionCall.
    def enterKwargFunctionCall(self, ctx:IceSqlParser.KwargFunctionCallContext):
        pass

    # Exit a parse tree produced by IceSqlParser#kwargFunctionCall.
    def exitKwargFunctionCall(self, ctx:IceSqlParser.KwargFunctionCallContext):
        pass


    # Enter a parse tree produced by IceSqlParser#nullsFunctionCall.
    def enterNullsFunctionCall(self, ctx:IceSqlParser.NullsFunctionCallContext):
        pass

    # Exit a parse tree produced by IceSqlParser#nullsFunctionCall.
    def exitNullsFunctionCall(self, ctx:IceSqlParser.NullsFunctionCallContext):
        pass


    # Enter a parse tree produced by IceSqlParser#starFunctionCall.
    def enterStarFunctionCall(self, ctx:IceSqlParser.StarFunctionCallContext):
        pass

    # Exit a parse tree produced by IceSqlParser#starFunctionCall.
    def exitStarFunctionCall(self, ctx:IceSqlParser.StarFunctionCallContext):
        pass


    # Enter a parse tree produced by IceSqlParser#kwarg.
    def enterKwarg(self, ctx:IceSqlParser.KwargContext):
        pass

    # Exit a parse tree produced by IceSqlParser#kwarg.
    def exitKwarg(self, ctx:IceSqlParser.KwargContext):
        pass


    # Enter a parse tree produced by IceSqlParser#caseItem.
    def enterCaseItem(self, ctx:IceSqlParser.CaseItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#caseItem.
    def exitCaseItem(self, ctx:IceSqlParser.CaseItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#over.
    def enterOver(self, ctx:IceSqlParser.OverContext):
        pass

    # Exit a parse tree produced by IceSqlParser#over.
    def exitOver(self, ctx:IceSqlParser.OverContext):
        pass


    # Enter a parse tree produced by IceSqlParser#numFrameBound.
    def enterNumFrameBound(self, ctx:IceSqlParser.NumFrameBoundContext):
        pass

    # Exit a parse tree produced by IceSqlParser#numFrameBound.
    def exitNumFrameBound(self, ctx:IceSqlParser.NumFrameBoundContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unboundedFrameBound.
    def enterUnboundedFrameBound(self, ctx:IceSqlParser.UnboundedFrameBoundContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unboundedFrameBound.
    def exitUnboundedFrameBound(self, ctx:IceSqlParser.UnboundedFrameBoundContext):
        pass


    # Enter a parse tree produced by IceSqlParser#currentRowFrameBound.
    def enterCurrentRowFrameBound(self, ctx:IceSqlParser.CurrentRowFrameBoundContext):
        pass

    # Exit a parse tree produced by IceSqlParser#currentRowFrameBound.
    def exitCurrentRowFrameBound(self, ctx:IceSqlParser.CurrentRowFrameBoundContext):
        pass


    # Enter a parse tree produced by IceSqlParser#singleFrame.
    def enterSingleFrame(self, ctx:IceSqlParser.SingleFrameContext):
        pass

    # Exit a parse tree produced by IceSqlParser#singleFrame.
    def exitSingleFrame(self, ctx:IceSqlParser.SingleFrameContext):
        pass


    # Enter a parse tree produced by IceSqlParser#doubleFrame.
    def enterDoubleFrame(self, ctx:IceSqlParser.DoubleFrameContext):
        pass

    # Exit a parse tree produced by IceSqlParser#doubleFrame.
    def exitDoubleFrame(self, ctx:IceSqlParser.DoubleFrameContext):
        pass


    # Enter a parse tree produced by IceSqlParser#sortItem.
    def enterSortItem(self, ctx:IceSqlParser.SortItemContext):
        pass

    # Exit a parse tree produced by IceSqlParser#sortItem.
    def exitSortItem(self, ctx:IceSqlParser.SortItemContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unpivotRelation.
    def enterUnpivotRelation(self, ctx:IceSqlParser.UnpivotRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unpivotRelation.
    def exitUnpivotRelation(self, ctx:IceSqlParser.UnpivotRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#functionCallRelation.
    def enterFunctionCallRelation(self, ctx:IceSqlParser.FunctionCallRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#functionCallRelation.
    def exitFunctionCallRelation(self, ctx:IceSqlParser.FunctionCallRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#jinjaRelation.
    def enterJinjaRelation(self, ctx:IceSqlParser.JinjaRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#jinjaRelation.
    def exitJinjaRelation(self, ctx:IceSqlParser.JinjaRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#aliasedRelation.
    def enterAliasedRelation(self, ctx:IceSqlParser.AliasedRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#aliasedRelation.
    def exitAliasedRelation(self, ctx:IceSqlParser.AliasedRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#lateralRelation.
    def enterLateralRelation(self, ctx:IceSqlParser.LateralRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#lateralRelation.
    def exitLateralRelation(self, ctx:IceSqlParser.LateralRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#joinRelation.
    def enterJoinRelation(self, ctx:IceSqlParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#joinRelation.
    def exitJoinRelation(self, ctx:IceSqlParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#pivotRelation.
    def enterPivotRelation(self, ctx:IceSqlParser.PivotRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#pivotRelation.
    def exitPivotRelation(self, ctx:IceSqlParser.PivotRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#selectRelation.
    def enterSelectRelation(self, ctx:IceSqlParser.SelectRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#selectRelation.
    def exitSelectRelation(self, ctx:IceSqlParser.SelectRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#tableRelation.
    def enterTableRelation(self, ctx:IceSqlParser.TableRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#tableRelation.
    def exitTableRelation(self, ctx:IceSqlParser.TableRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#parenRelation.
    def enterParenRelation(self, ctx:IceSqlParser.ParenRelationContext):
        pass

    # Exit a parse tree produced by IceSqlParser#parenRelation.
    def exitParenRelation(self, ctx:IceSqlParser.ParenRelationContext):
        pass


    # Enter a parse tree produced by IceSqlParser#flatGrouping.
    def enterFlatGrouping(self, ctx:IceSqlParser.FlatGroupingContext):
        pass

    # Exit a parse tree produced by IceSqlParser#flatGrouping.
    def exitFlatGrouping(self, ctx:IceSqlParser.FlatGroupingContext):
        pass


    # Enter a parse tree produced by IceSqlParser#setsGrouping.
    def enterSetsGrouping(self, ctx:IceSqlParser.SetsGroupingContext):
        pass

    # Exit a parse tree produced by IceSqlParser#setsGrouping.
    def exitSetsGrouping(self, ctx:IceSqlParser.SetsGroupingContext):
        pass


    # Enter a parse tree produced by IceSqlParser#groupingSet.
    def enterGroupingSet(self, ctx:IceSqlParser.GroupingSetContext):
        pass

    # Exit a parse tree produced by IceSqlParser#groupingSet.
    def exitGroupingSet(self, ctx:IceSqlParser.GroupingSetContext):
        pass


    # Enter a parse tree produced by IceSqlParser#qualifiedName.
    def enterQualifiedName(self, ctx:IceSqlParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by IceSqlParser#qualifiedName.
    def exitQualifiedName(self, ctx:IceSqlParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by IceSqlParser#identifierList.
    def enterIdentifierList(self, ctx:IceSqlParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by IceSqlParser#identifierList.
    def exitIdentifierList(self, ctx:IceSqlParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by IceSqlParser#identifier.
    def enterIdentifier(self, ctx:IceSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by IceSqlParser#identifier.
    def exitIdentifier(self, ctx:IceSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by IceSqlParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:IceSqlParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by IceSqlParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:IceSqlParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by IceSqlParser#var.
    def enterVar(self, ctx:IceSqlParser.VarContext):
        pass

    # Exit a parse tree produced by IceSqlParser#var.
    def exitVar(self, ctx:IceSqlParser.VarContext):
        pass


    # Enter a parse tree produced by IceSqlParser#param.
    def enterParam(self, ctx:IceSqlParser.ParamContext):
        pass

    # Exit a parse tree produced by IceSqlParser#param.
    def exitParam(self, ctx:IceSqlParser.ParamContext):
        pass


    # Enter a parse tree produced by IceSqlParser#integerNumber.
    def enterIntegerNumber(self, ctx:IceSqlParser.IntegerNumberContext):
        pass

    # Exit a parse tree produced by IceSqlParser#integerNumber.
    def exitIntegerNumber(self, ctx:IceSqlParser.IntegerNumberContext):
        pass


    # Enter a parse tree produced by IceSqlParser#decimalNumber.
    def enterDecimalNumber(self, ctx:IceSqlParser.DecimalNumberContext):
        pass

    # Exit a parse tree produced by IceSqlParser#decimalNumber.
    def exitDecimalNumber(self, ctx:IceSqlParser.DecimalNumberContext):
        pass


    # Enter a parse tree produced by IceSqlParser#floatNumber.
    def enterFloatNumber(self, ctx:IceSqlParser.FloatNumberContext):
        pass

    # Exit a parse tree produced by IceSqlParser#floatNumber.
    def exitFloatNumber(self, ctx:IceSqlParser.FloatNumberContext):
        pass


    # Enter a parse tree produced by IceSqlParser#integer.
    def enterInteger(self, ctx:IceSqlParser.IntegerContext):
        pass

    # Exit a parse tree produced by IceSqlParser#integer.
    def exitInteger(self, ctx:IceSqlParser.IntegerContext):
        pass


    # Enter a parse tree produced by IceSqlParser#string.
    def enterString(self, ctx:IceSqlParser.StringContext):
        pass

    # Exit a parse tree produced by IceSqlParser#string.
    def exitString(self, ctx:IceSqlParser.StringContext):
        pass


    # Enter a parse tree produced by IceSqlParser#null.
    def enterNull(self, ctx:IceSqlParser.NullContext):
        pass

    # Exit a parse tree produced by IceSqlParser#null.
    def exitNull(self, ctx:IceSqlParser.NullContext):
        pass


    # Enter a parse tree produced by IceSqlParser#true.
    def enterTrue(self, ctx:IceSqlParser.TrueContext):
        pass

    # Exit a parse tree produced by IceSqlParser#true.
    def exitTrue(self, ctx:IceSqlParser.TrueContext):
        pass


    # Enter a parse tree produced by IceSqlParser#false.
    def enterFalse(self, ctx:IceSqlParser.FalseContext):
        pass

    # Exit a parse tree produced by IceSqlParser#false.
    def exitFalse(self, ctx:IceSqlParser.FalseContext):
        pass


    # Enter a parse tree produced by IceSqlParser#setQuantifier.
    def enterSetQuantifier(self, ctx:IceSqlParser.SetQuantifierContext):
        pass

    # Exit a parse tree produced by IceSqlParser#setQuantifier.
    def exitSetQuantifier(self, ctx:IceSqlParser.SetQuantifierContext):
        pass


    # Enter a parse tree produced by IceSqlParser#joinType.
    def enterJoinType(self, ctx:IceSqlParser.JoinTypeContext):
        pass

    # Exit a parse tree produced by IceSqlParser#joinType.
    def exitJoinType(self, ctx:IceSqlParser.JoinTypeContext):
        pass


    # Enter a parse tree produced by IceSqlParser#cmpOp.
    def enterCmpOp(self, ctx:IceSqlParser.CmpOpContext):
        pass

    # Exit a parse tree produced by IceSqlParser#cmpOp.
    def exitCmpOp(self, ctx:IceSqlParser.CmpOpContext):
        pass


    # Enter a parse tree produced by IceSqlParser#arithOp.
    def enterArithOp(self, ctx:IceSqlParser.ArithOpContext):
        pass

    # Exit a parse tree produced by IceSqlParser#arithOp.
    def exitArithOp(self, ctx:IceSqlParser.ArithOpContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unaryOp.
    def enterUnaryOp(self, ctx:IceSqlParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unaryOp.
    def exitUnaryOp(self, ctx:IceSqlParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by IceSqlParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:IceSqlParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by IceSqlParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:IceSqlParser.UnquotedIdentifierContext):
        pass



del IceSqlParser
