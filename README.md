# Autotrader Bot

<!--
    Trading is not easy. I have haven no solid background trading (forex, stocks, and equity) and its related terms and gimmicks (quotes, indicators, signals account activity) in order to trade effectively.

    Trading is complex, and it's even more complex building a software for it.

    I'm learning while building this software.

    This should be fun, interesting and frustrating all at the same time!

    "We move!"
-->
------------------------------------------------------------------------

## SOFTWARE OBJECTIVES

_program should be able to do the following:_
-------------------------------------------------------------------------
- Stream real-time QUOTES: get realtime stock price information

- place ENTER & EXIT POSITIONS(Buy & Sell): Buy and sell instrument, may create a new order

- Manage account data (ORDERS, POSITIONS & ACTIVITY): prevent entering same positions and manage decision making. Account data is critical

- Calculate different TECHNICAL INDICATORS: Determines enter & exit positions, knows market conditions using technical patterns. Set up mechanism for calculating indicators

## SOLUTION BREAKDOWN

_In terms of OOP programming_
------------------------------

- Robot: 
    + Handles the interaction with stock API.
    + Makes reqest related to API
    + Represents the HIGHEST LEVEL OF HIERARCHY
    
- Stock frame (Name will change):
    + Stores all PRICE DATA
    + Add INDICATORS
    + Handles APPENDING, ORGANIZING and DELETING of data
    
- Portfolio (Mimicks account activities):
    + Represents trading portfolio of MULTIPLE POSITIONS
    + Calculates common portfolio metrics used to answer general questions on trade positions

- Trade:
    + A trade which REPRESENT AN ORDER to be placed
    + MODIFIES DIFFERENT ASPECT of an order

- INDICATORS:
    + Technial indicators to be used during training trade signal indicator
    + SPECIFIES BUY/SELL CRITERIA, and any METHODLODY used for calculations


