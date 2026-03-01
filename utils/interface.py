from core.models import FootprintCandle

def clear_terminal():
    """Clears the terminal screen for a clean live-update effect."""
    # '\033c' is the ANSI escape code to clear the screen and reset the cursor
    print("\033c", end="")

def print_live_footprint(candle: FootprintCandle):
    """
    Takes the current live candle and prints a formatted dashboard to the terminal.
    """
    if not candle:
        return

    clear_terminal()
    
    # 1. Print the Header (Standard Candlestick Data)
    print("=" * 63)
    print(f" LIVE 15m CANDLE | Start Time: {candle.start_time}")
    print("=" * 63)
    print(f" Open:  {candle.open}")
    print(f" High:  {candle.high}")
    print(f" Low:   {candle.low}")
    print(f" Close: {candle.close}")
    print("-" * 63)
    print(f" Total Vol:   {candle.total_volume}")
    print(f" Total Delta: {candle.delta:+}") # The :+ forces it to show + or - sign
    print("=" * 63)
    
    # 2. Print the Footprint Levels
    print(f"{'PRICE':<12} | {'BUY VOL':<10} | {'SELL VOL':<10} | {'TOTAL VOL':<10} | {'DELTA':<10}")
    print("-" * 63)
    
    # Print the price levels sorted from highest to lowest, so we sort the keys of the levels dictionary.
    sorted_prices = sorted(candle.levels.keys(), reverse=True)
    
    for price in sorted_prices:
        level = candle.levels[price]
        
        price_str = f"{level.price:.2f}"
        buy_str = f"{level.buy_volume:.4f}"
        sell_str = f"{level.sell_volume:.4f}"
        total_str = f"{level.total_volume:.4f}"
        delta_str = f"{level.delta:+.4f}"
        
        # Highlight positive delta in green, negative in red 
        if level.delta > 0:
            delta_str = f"\033[92m{delta_str}\033[0m" # Green
        elif level.delta < 0:
            delta_str = f"\033[91m{delta_str}\033[0m" # Red
            
        print(f"{price_str:<12} | {buy_str:<10} | {sell_str:<10} | {total_str:<10} | {delta_str:<10}")
        
    print("=" * 63)
    print("Waiting for next trade...")