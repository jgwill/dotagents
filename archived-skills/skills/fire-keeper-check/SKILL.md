# Skill: Fire Keeper Check

## Purpose
Evaluate a proposed action against permission tiers and relational gates.

## Input
- Proposed action description
- Current permission tier
- Current ceremony phase
- Optional: Wilson / OCAP metadata

## Output
- accept / hold / human-needed assessment
- Unsatisfied gates
- Check-back step results
- Suggested next move

## Usage
```
mw skill run fire-keeper-check "Deploy to production"
```
