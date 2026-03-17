```
- Data always accessed from the candle cache
- Atom cant talk to other atom, only to candle
- Save every atom data to candle.cache (Not the signal result)
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

<br>

## `Check` 

| Atom & Class Name | Input (`__init__`) | Output | Desc |
| :--- | :--- | :--- | :--- |
| `CheckCandleColor` | `target_color` ("GREEN", "RED", "DOJI")| `bool` | `True` if actual color == target color. |
