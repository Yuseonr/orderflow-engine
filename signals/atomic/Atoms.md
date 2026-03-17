```
- Data always accessed from the candle cache
- Atom cant talk to other atom, only to candle
- Save every atom data(if theres any) and result to candle.cache 
- Every atom that has parameter must be named with the param in the name like `CalculatePoc_{param}`
```


# Atom Naming Format

| Atom & Class Name              | Meaning                                  | Need init input ? |
|--------------------------------|------------------------------------------|-------------|
| `Calculate{Value}{Modifier}`   | Calculated value (usually a float)       | Optional    |
| `Is{Condition}{Modifier}`      | Boolean condition (True or False)        | No          |
| `Check{Condition}{Modifier}`   | Boolean condition (True or False)        | Yes         |

<br>
<br>

# List of Atom Definitions

## `Calculate` 

| Atom & Class Name | Input (`__init__`) | Cached | Type | Desc |
| :--- | :--- | :--- | :--- | :--- |
| `CalculatePoc` | None | `poc_price` | `float` | Finds the highest volume price node. |

<br>

## `Is` 

| Atom & Class Name | Required Metric in Cache | Output | Desc |
| :--- | :--- | :--- | :--- |
| `IsNewYorkSession` | None | `bool` | `True` if candle is in New York session. |

<br>

## `Check` 

| Atom & Class Name | Input (`__init__`) | Output | Desc |
| :--- | :--- | :--- | :--- |
| `CheckCandleColor` | `target_color` ("GREEN", "RED", "DOJI")| `bool` | `True` if actual color == target color. |
| `CheckPocLocation` | `target_wick` ("UPPER", "LOWER", "BODY"), `cal_poc` (CalculatePoc() or CalculatePocProminance()) | `bool` | `True` if POC is in the target wick. |
