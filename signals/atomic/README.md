```
- Data always accessed from the candle cache
- Atom cant talk to other atom, only to candle
- Save every atom data(if theres any) and result to candle.cache 
- Every atom that has parameter must be named with the param in the name like `CalculatePoc_{param}`
```


# Atom Naming Format

| Atom & Class Name              | Meaning                                  | Need init input ? |
|--------------------------------|------------------------------------------|-------------|
| `Calculate{Value}{Modifier}`   | Calculated value (usually a Decimal)       | Optional    |
| `Is{Condition}{Modifier}`      | Boolean condition (True or False)        | No          |
| `Check{Condition}{Modifier}`   | Boolean condition (True or False)        | Yes         |

<br>
<br>

# List of Atom Definitions

## `Calculate` 

| Atom & Class Name | Input (`__init__`) | Cached | Type | Desc |
| :--- | :--- | :--- | :--- | :--- |
| `CalculatePoc` | None | `poc_price` | `Decimal` | Finds the highest volume price node. |
| `CalculatePocGaussian` | None | `poc_price_gaussian` | `Decimal` | Finds the highest volume price node after applying a Gaussian convolution. |
| `CalculateValueArea` | `cal_poc` (CalculatePoc() or CalculatePocGaussian()), `value_area_pct` (str '0.70' for 70%) | `value_area_high`, `value_area_low` | `Decimal` | Calculates the Value Area High and Low based on the specified percentage of total volume. |

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
| `CheckPocLocation` | `target_wick` ("UPPER", "LOWER", "BODY"), `cal_poc` (CalculatePoc() or CalculatePocGaussian()) | `bool` | `True` if POC is in the target wick. |
| `CheckTrappedValueArea` | `target_wick` ("UPPER", "LOWER"), `cal_va` (CalculateValueArea()) | `bool` | `True` if value area is in the target wick.|
